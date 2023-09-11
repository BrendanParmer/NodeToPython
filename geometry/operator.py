import bpy
from bpy.types import Context
from bpy.types import GeometryNodeGroup
from bpy.types import GeometryNodeSimulationInput
from bpy.types import GeometryNodeSimulationOutput
from bpy.types import GeometryNodeTree
from bpy.types import Node
from bpy.types import Operator

import os

from ..utils import *
from .node_tree import NTP_GeoNodeTree
from .node_settings import geo_node_settings
from io import StringIO

class NTPGeoNodesOperator(Operator):
    bl_idname = "node.ntp_geo_nodes"
    bl_label = "Geo Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON',  "Addon", "Create a full addon")
        ]
    )

    geo_nodes_group_name: bpy.props.StringProperty(name="Node Group")
    
    def __init__(self):
        # File/string the add-on/script is generated into
        self._file: TextIO = None

        # Path to the directory of the zip file
        self._zip_dir: str = None

        # Path to the directory for the generated addon
        self._addon_dir: str = None

        # Set to keep track of already created node trees
        self._node_trees: set[GeometryNodeTree] = set()

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}
    
    def _setup_addon_directories(self, context: Context, nt_var: str):
        #find base directory to save new addon
        dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
        if not dir or dir == "":
            self.report({'ERROR'}, 
                        ("NodeToPython: Save your blend file before using "
                         "NodeToPython!")) #TODO: Still valid??
            return {'CANCELLED'}

        self._zip_dir = os.path.join(dir, nt_var)
        self._addon_dir = os.path.join(self._zip_dir, nt_var)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)

    def _process_geo_node_group_node(self, node: GeometryNodeGroup, 
                                     level: int, inner: str, node_var: str
                                    ) -> None:
        nt = node.node_tree
        if nt is not None:
            if nt not in self._node_trees:
                self._process_geo_node_tree(nt, level + 1)
            self._file.write((f"{inner}{node_var}.node_tree = "
                                      f"bpy.data.node_groups"
                                      f"[{str_to_py_str(nt.name)}]\n"))
    
    def _process_sim_output_node(self, node: GeometryNodeSimulationOutput,
                                 inner: str, node_var: str) -> None:
        self._file.write(f"{inner}# Remove generated sim state items\n")
        self._file.write(f"{inner}for item in {node_var}.state_items:\n")
        self._file.write(f"{inner}\t{node_var}.state_items.remove(item)\n")

        for i, si in enumerate(node.state_items):
            socket_type = enum_to_py_str(si.socket_type)
            name = str_to_py_str(si.name)
            self._file.write(f"{inner}#create SSI {name}\n")
            self._file.write((f"{inner}{node_var}.state_items.new"
                              f"({socket_type}, {name})\n"))
            si_var = f"{node_var}.state_items[{i}]"
            attr_domain = enum_to_py_str(si.attribute_domain)
            self._file.write((f"{inner}{si_var}.attribute_domain "
                              f"= {attr_domain}\n"))

    def _set_socket_defaults(self, node: Node, inner: str,
                             node_var: str) -> None:
        if self.mode == 'ADDON':
            set_input_defaults(node, self._file, inner, node_var, self._addon_dir)
        else:
            set_input_defaults(node, self._file, inner, node_var)
        set_output_defaults(node, self._file, inner, node_var)

    def _process_node(self, node: Node, ntp_node_tree: NTP_GeoNodeTree,
                      inner: str, level: int) -> None:
        #create node
        node_var: str = create_node(node, self._file, inner, ntp_node_tree.var_name, 
                                    self._node_vars, self._used_vars)
        set_settings_defaults(node, geo_node_settings, self._file, 
                                self._addon_dir, inner, node_var)
        if node.bl_idname == 'GeometryNodeGroup':
            self._process_geo_node_group_node(node, level, inner, node_var)

        elif node.bl_idname == 'NodeGroupInput' and not ntp_node_tree.inputs_set:
            group_io_settings(node, self._file, inner, "input", ntp_node_tree.var_name, 
                              ntp_node_tree.node_tree) #TODO: convert to using NTP_NodeTrees
            ntp_node_tree.inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not ntp_node_tree.outputs_set:
            group_io_settings(node, self._file, inner, "output", 
                              ntp_node_tree.var_name, ntp_node_tree.node_tree)
            ntp_node_tree.outputs_set = True

        elif node.bl_idname == 'GeometryNodeSimulationInput':
            ntp_node_tree.sim_inputs.append(node)

        elif node.bl_idname == 'GeometryNodeSimulationOutput':
            self._process_sim_output_node(node, inner, node_var)
        
        hide_hidden_sockets(node, self._file, inner, node_var)

        if node.bl_idname != 'GeometryNodeSimulationInput':
            self._set_socket_defaults(node, inner, node_var)

    def _process_sim_zones(self, sim_inputs: list[GeometryNodeSimulationInput], 
                           inner: str) -> None:
        """
        Recreate simulation zones
        sim_inputs (list[GeometryNodeSimulationInput]): list of 
            simulation input nodes
        inner (str): identation string
        """
        for sim_input in sim_inputs:
            sim_output = sim_input.paired_output

            sim_input_var = self._node_vars[sim_input]
            sim_output_var = self._node_vars[sim_output]
            self._file.write((f"{inner}{sim_input_var}.pair_with_output"
                              f"({sim_output_var})\n"))

            #must set defaults after paired with output
            self._set_socket_defaults(sim_input, inner, sim_input_var)
            self._set_socket_defaults(sim_output, inner, sim_output_var)

    def _process_geo_node_tree(self, node_tree: GeometryNodeTree, 
                               level: int) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (GeometryNodeTree): geometry node tree to be recreated
        level (int): number of tabs to use for each line, used with
            node groups within node groups and script/add-on differences
        """
        
        nt_var = create_var(node_tree.name, self._used_vars)    
        outer, inner = make_indents(level) #TODO: put in NTP_NodeTree class?

        #initialize node group
        self._file.write(f"{outer}#initialize {nt_var} node group\n")
        self._file.write(f"{outer}def {nt_var}_node_group():\n")
        self._file.write((f"{inner}{nt_var} = bpy.data.node_groups.new("
                          f"type = \'GeometryNodeTree\', "
                          f"name = {str_to_py_str(node_tree.name)})\n"))
        self._file.write("\n")

        #initialize nodes
        self._file.write(f"{inner}#initialize {nt_var} nodes\n")

        ntp_nt = NTP_GeoNodeTree(node_tree, nt_var)
        for node in node_tree.nodes:
            self._process_node(node, ntp_nt, inner, level)

        self._process_sim_zones(ntp_nt.sim_inputs, inner)
        
        #set look of nodes
        set_parents(node_tree, self._file, inner, self._node_vars)
        set_locations(node_tree, self._file, inner, self._node_vars)
        set_dimensions(node_tree, self._file, inner, self._node_vars)

        #create connections
        init_links(node_tree, self._file, inner, nt_var, self._node_vars)
        
        self._file.write(f"{inner}return {nt_var}\n")

        #create node group
        self._file.write(f"\n{outer}{nt_var} = {nt_var}_node_group()\n\n")
        return self._used_vars

    def _apply_modifier(self, nt: GeometryNodeTree, nt_var: str):
        #get object
        self._file.write(f"\t\tname = bpy.context.object.name\n")
        self._file.write(f"\t\tobj = bpy.data.objects[name]\n")

        #set modifier to the one we just created
        mod_name = str_to_py_str(nt.name)
        self._file.write((f"\t\tmod = obj.modifiers.new(name = {mod_name}, "
                    f"type = 'NODES')\n"))
        self._file.write(f"\t\tmod.node_group = {nt_var}\n")

    def _report_finished(self):
        #alert user that NTP is finished
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = dir
        self.report({'INFO'}, 
                    f"NodeToPython: Saved geometry nodes group to {location}")

    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            self._setup_addon_directories(context, nt_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            create_header(self._file, nt.name)
            class_name = clean_string(nt.name.replace(" ", "").replace('.', ""), 
                                      lower = False) #TODO: should probably be standardized name to class name util method
            init_operator(self._file, class_name, nt_var, nt.name)
            self._file.write("\tdef execute(self, context):\n")
        else:
            self._file = StringIO("")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0
        self._process_geo_node_tree(nt, level)

        if self.mode == 'ADDON':
            self._apply_modifier(nt, nt_var)
            self._file.write("\t\treturn {'FINISHED'}\n\n")
            create_menu_func(self._file, class_name)
            create_register_func(self._file, class_name)
            create_unregister_func(self._file, class_name)
            create_main_func(self._file)
        else:
            context.window_manager.clipboard = self._file.getvalue()
        self._file.close()

        if self.mode == 'ADDON':
            zip_addon(self._zip_dir)

        self._report_finished()

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")
