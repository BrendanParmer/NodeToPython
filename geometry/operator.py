import bpy
from bpy.types import GeometryNode, GeometryNodeTree
from bpy.types import Node

if bpy.app.version >= (3, 6, 0):
    from bpy.types import GeometryNodeSimulationInput
    from bpy.types import GeometryNodeSimulationOutput
if bpy.app.version >= (4, 0, 0):
    from bpy.types import GeometryNodeRepeatInput
    from bpy.types import GeometryNodeRepeatOutput

from io import StringIO

from ..ntp_operator import NTP_Operator
from ..utils import *
from .node_tree import NTP_GeoNodeTree
from .node_settings import geo_node_settings

class NTPGeoNodesOperator(NTP_Operator):
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
        super().__init__()
        self._settings = geo_node_settings

    if bpy.app.version >= (3, 6, 0):
        def _process_zone_output_node(self, node: GeometryNode, inner: str,
                                    node_var: str) -> None:
            is_sim = False
            if node.bl_idname == 'GeometryNodeSimulationOutput':
                items = "state_items"
                is_sim = True
            elif node.bl_idname == 'GeometryNodeRepeatOutput':
                items = "repeat_items"
            else:
                self.report({'WARNING'}, f"{node.bl_idname} is not recognized "
                                         f" as avalid zone output")

            self._write(f"{inner}# Remove generated {items}\n")
            self._write(f"{inner}for item in {node_var}.{items}:\n")
            self._write(f"{inner}\t{node_var}.{items}.remove(item)\n")

            for i, item in enumerate(getattr(node, items)):
                socket_type = enum_to_py_str(item.socket_type)
                name = str_to_py_str(item.name)
                self._write(f"{inner}# Create item {name}\n")
                self._write(f"{inner}{node_var}.{items}.new"
                            f"({socket_type}, {name})\n")
                if is_sim:
                    item_var = f"{node_var}.{items}[{i}]"
                    attr_domain = enum_to_py_str(item.attribute_domain)
                    self._write((f"{inner}{item_var}.attribute_domain = "
                                f"{attr_domain}\n"))

    def _process_node(self, node: Node, ntp_node_tree: NTP_GeoNodeTree,
                      inner: str, level: int) -> None:
        #create node
        node_var: str = self._create_node(node, inner, ntp_node_tree.var)
        self._set_settings_defaults(node, inner, node_var)
        if node.bl_idname == 'GeometryNodeGroup':
            self._process_group_node_tree(node, node_var, level, inner)

        elif node.bl_idname == 'NodeGroupInput' and not ntp_node_tree.inputs_set:
            self._group_io_settings(node, inner, "input", ntp_node_tree)
            ntp_node_tree.inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not ntp_node_tree.outputs_set:
            self._group_io_settings(node, inner, "output", ntp_node_tree)
            ntp_node_tree.outputs_set = True

        elif node.bl_idname == 'GeometryNodeSimulationInput':
            ntp_node_tree.sim_inputs.append(node)

        elif node.bl_idname == 'GeometryNodeSimulationOutput':
            self._process_zone_output_node(node, inner, node_var)

        elif node.bl_idname == 'GeometryNodeRepeatInput':
            ntp_node_tree.repeat_inputs.append(node)
        
        elif node.bl_idname == 'GeometryNodeRepeatOutput':
            self._process_zone_output_node(node, inner, node_var)
        
        self._hide_hidden_sockets(node, inner, node_var)

        if node.bl_idname not in {'GeometryNodeSimulationInput', 'GeometryNodeRepeatInput'}:
            self._set_socket_defaults(node, node_var, inner)

    if bpy.app.version >= (3, 6, 0):
        def _process_zones(self, zone_inputs: list[GeometryNode], 
                            inner: str) -> None:
            """
            Recreates a zone
            zone_inputs (list[GeometryNodeSimulationInput]): list of 
                simulation input nodes
            inner (str): identation string
            """
            for zone_input in zone_inputs:
                zone_output = zone_input.paired_output

                zone_input_var = self._node_vars[zone_input]
                zone_output_var = self._node_vars[zone_output]

                self._write(f"{inner}#Process zone input {zone_input.name}\n")
                self._write((f"{inner}{zone_input_var}.pair_with_output"
                            f"({zone_output_var})\n"))

                #must set defaults after paired with output
                self._set_socket_defaults(zone_input, zone_input_var, inner)
                self._set_socket_defaults(zone_output, zone_output_var, inner)
            self._write("\n")

    def _process_node_tree(self, node_tree: GeometryNodeTree, 
                               level: int) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (GeometryNodeTree): geometry node tree to be recreated
        level (int): number of tabs to use for each line, used with
            node groups within node groups and script/add-on differences
        """
        
        nt_var = self._create_var(node_tree.name)    
        outer, inner = make_indents(level) #TODO: put in NTP_NodeTree class?
        # Eventually these should go away anyways, and level of indentation depends just on the mode

        #initialize node group
        self._write(f"{outer}#initialize {nt_var} node group\n")
        self._write(f"{outer}def {nt_var}_node_group():\n")
        self._write((f"{inner}{nt_var} = bpy.data.node_groups.new("
                     f"type = \'GeometryNodeTree\', "
                     f"name = {str_to_py_str(node_tree.name)})\n"))
        self._write("\n")

        if bpy.app.version >= (4, 0, 0):
            is_mod = node_tree.is_modifier
            is_tool = node_tree.is_tool
            if is_mod:
                self._write(f"{inner}{nt_var}.is_modifier = True\n")
            if is_tool:
                self._write(f"{inner}{nt_var}.is_tool = True\n")

                tool_flags =  ["is_mode_edit", 
                               "is_mode_sculpt",
                               "is_type_curve",
                               "is_type_mesh",
                               "is_type_point_cloud"]
            
                for flag in tool_flags:
                    self._write(f"{inner}{nt_var}.{flag} = "
                                f"{getattr(node_tree, flag)}\n")
            self._write("\n")
    
        #initialize nodes
        self._write(f"{inner}#initialize {nt_var} nodes\n")

        ntp_nt = NTP_GeoNodeTree(node_tree, nt_var)

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt, inner, level)

        if bpy.app.version >= (3, 6, 0):
            self._process_zones(ntp_nt.sim_inputs, inner)
        if bpy.app.version >= (4, 0, 0):
            self._process_zones(ntp_nt.repeat_inputs, inner)

        #set look of nodes
        self._set_parents(node_tree, inner)
        self._set_locations(node_tree, inner)
        self._set_dimensions(node_tree,  inner)

        #create connections
        self._init_links(node_tree, inner, nt_var)
        
        self._write(f"{inner}return {nt_var}\n")

        #create node group
        self._write(f"\n{outer}{nt_var} = {nt_var}_node_group()\n\n")
        return self._used_vars


    def _apply_modifier(self, nt: GeometryNodeTree, nt_var: str):
        #get object
        self._write(f"\t\tname = bpy.context.object.name\n")
        self._write(f"\t\tobj = bpy.data.objects[name]\n")

        #set modifier to the one we just created
        mod_name = str_to_py_str(nt.name)
        self._write((f"\t\tmod = obj.modifiers.new(name = {mod_name}, "
                     f"type = 'NODES')\n"))
        self._write(f"\t\tmod.node_group = {nt_var}\n")


    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            self._setup_addon_directories(context, nt_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            self._create_header(nt.name)
            self._class_name = clean_string(nt.name, lower = False)
            self._init_operator(nt_var, nt.name)
            self._write("\tdef execute(self, context):\n")
        else:
            self._file = StringIO("")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0
        self._process_node_tree(nt, level)

        if self.mode == 'ADDON':
            self._apply_modifier(nt, nt_var)
            self._write("\t\treturn {'FINISHED'}\n\n")
            self._create_menu_func()
            self._create_register_func()
            self._create_unregister_func()
            self._create_main_func()
        else:
            context.window_manager.clipboard = self._file.getvalue()
        self._file.close()

        if self.mode == 'ADDON':
            self._zip_addon()

        self._report_finished("geometry node group")

        return {'FINISHED'}