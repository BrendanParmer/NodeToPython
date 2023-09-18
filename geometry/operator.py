import bpy
from bpy.types import Context
from bpy.types import GeometryNodeGroup
from bpy.types import GeometryNodeSimulationInput
from bpy.types import GeometryNodeSimulationOutput
from bpy.types import GeometryNodeTree
from bpy.types import Node

import os
from io import StringIO

from ..NTP_Operator import NTP_Operator
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

    def _process_node(self, node: Node, ntp_node_tree: NTP_GeoNodeTree,
                      inner: str, level: int) -> None:
        #create node
        node_var: str = create_node(node, self._file, inner, ntp_node_tree.var, 
                                    self._node_vars, self._used_vars)
        set_settings_defaults(node, self._settings, self._file, 
                                self._addon_dir, inner, node_var)
        if node.bl_idname == 'GeometryNodeGroup':
            self._process_group_node_tree(node, node_var, level, inner)

        elif node.bl_idname == 'NodeGroupInput' and not ntp_node_tree.inputs_set:
            group_io_settings(node, self._file, inner, "input", ntp_node_tree.var, 
                              ntp_node_tree.node_tree) #TODO: convert to using NTP_NodeTrees
            ntp_node_tree.inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not ntp_node_tree.outputs_set:
            group_io_settings(node, self._file, inner, "output", 
                              ntp_node_tree.var, ntp_node_tree.node_tree)
            ntp_node_tree.outputs_set = True

        elif node.bl_idname == 'GeometryNodeSimulationInput':
            ntp_node_tree.sim_inputs.append(node)

        elif node.bl_idname == 'GeometryNodeSimulationOutput':
            self._process_sim_output_node(node, inner, node_var)
        
        hide_hidden_sockets(node, self._file, inner, node_var)

        if node.bl_idname != 'GeometryNodeSimulationInput':
            self._set_socket_defaults(node, node_var, inner)


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
            self._set_socket_defaults(sim_input, sim_input_var, inner)
            self._set_socket_defaults(sim_output, sim_output_var, inner)


    def _process_node_tree(self, node_tree: GeometryNodeTree, 
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
        # Eventually these should go away anyways, and level of indentation depends just on the mode

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


    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            self._setup_addon_directories(context, nt_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            create_header(self._file, nt.name)
            class_name = clean_string(nt.name, lower = False)
            init_operator(self._file, class_name, nt_var, nt.name)
            self._file.write("\tdef execute(self, context):\n")
        else:
            self._file = StringIO("")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0
        self._process_node_tree(nt, level)

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

        self._report_finished("geometry node group")

        return {'FINISHED'}