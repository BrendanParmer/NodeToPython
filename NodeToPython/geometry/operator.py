import bpy
from bpy.types import GeometryNode, GeometryNodeTree
from bpy.types import Node

from io import StringIO

from ..ntp_operator import NTP_Operator
from ..utils import *
from .node_tree import NTP_GeoNodeTree
from ..node_settings import node_settings

OBJECT_NAME = "name"
OBJECT = "obj"
MODIFIER = "mod"
GEO_OP_RESERVED_NAMES = {OBJECT_NAME, 
                         OBJECT,
                         MODIFIER}

class NTPGeoNodesOperator(NTP_Operator):
    bl_idname = "node.ntp_geo_nodes"
    bl_label = "Geo Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}

    geo_nodes_group_name: bpy.props.StringProperty(name="Node Group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._node_infos = node_settings
        for name in GEO_OP_RESERVED_NAMES:
            self._used_vars[name] = 0

    def _process_node(self, node: Node, ntp_nt: NTP_GeoNodeTree) -> None:
        """
        Create node and set settings, defaults, and cosmetics

        Parameters:
        node (Node): node to process
        ntp_nt (NTP_NodeTree): the node tree that node belongs to
        """
        node_var: str = self._create_node(node, ntp_nt.var)
        self._set_settings_defaults(node)

        if bpy.app.version < (4, 0, 0):
            if node.bl_idname == 'NodeGroupInput' and not ntp_nt.inputs_set:
                self._group_io_settings(node, "input", ntp_nt)
                ntp_nt.inputs_set = True

            elif node.bl_idname == 'NodeGroupOutput' and not ntp_nt.outputs_set:
                self._group_io_settings(node, "output", ntp_nt)
                ntp_nt.outputs_set = True

        if node.bl_idname in ntp_nt.zone_inputs:
            ntp_nt.zone_inputs[node.bl_idname].append(node)
        
        self._hide_hidden_sockets(node)

        if node.bl_idname not in ntp_nt.zone_inputs:
            self._set_socket_defaults(node)

    if bpy.app.version >= (3, 6, 0):
        def _process_zones(self, zone_inputs: list[GeometryNode]) -> None:
            """
            Recreates a zone
            zone_inputs (list[GeometryNodeSimulationInput]): list of 
                simulation input nodes
            """
            for zone_input in zone_inputs:
                zone_output = zone_input.paired_output

                zone_input_var = self._node_vars[zone_input]
                zone_output_var = self._node_vars[zone_output]

                self._write(f"#Process zone input {zone_input.name}")
                self._write(f"{zone_input_var}.pair_with_output"
                            f"({zone_output_var})")

                #must set defaults after paired with output
                self._set_socket_defaults(zone_input)
                self._set_socket_defaults(zone_output)
            self._write("", 0)

    if bpy.app.version >= (4, 0, 0):
        def _set_geo_tree_properties(self, node_tree: GeometryNodeTree) -> None:
            is_mod = node_tree.is_modifier
            is_tool = node_tree.is_tool

            nt_var = self._node_tree_vars[node_tree]

            if is_mod:
                self._write(f"{nt_var}.is_modifier = True")
            if is_tool:
                self._write(f"{nt_var}.is_tool = True")

                tool_flags =  ["is_mode_object",
                               "is_mode_edit", 
                               "is_mode_sculpt",
                               "is_type_curve",
                               "is_type_mesh",
                               "is_type_point_cloud"]
            
                for flag in tool_flags:
                    if hasattr(node_tree, flag) is True:
                        self._write(f"{nt_var}.{flag} = {getattr(node_tree, flag)}")
            self._write("", 0)

    def _process_node_tree(self, node_tree: GeometryNodeTree) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (GeometryNodeTree): geometry node tree to be recreated
        """
        
        nt_var = self._create_var(node_tree.name)
        self._node_tree_vars[node_tree] = nt_var

        #initialize node group
        self._write(f"def {nt_var}_node_group():", self._outer_indent_level)
        self._write(f'"""Initialize {nt_var} node group"""')
        self._write(f"{nt_var} = bpy.data.node_groups.new("
                    f"type = \'GeometryNodeTree\', "
                    f"name = {str_to_py_str(node_tree.name)})\n")

        self._set_node_tree_properties(node_tree)
        if bpy.app.version >= (4, 0, 0):
            self._set_geo_tree_properties(node_tree)
    
        ntp_nt = NTP_GeoNodeTree(node_tree, nt_var)

        if bpy.app.version >= (4, 0, 0):
            self._tree_interface_settings(ntp_nt)

        #initialize nodes
        self._write(f"#initialize {nt_var} nodes")
        for node in node_tree.nodes:
            self._process_node(node, ntp_nt)

        for zone_list in ntp_nt.zone_inputs.values():
            self._process_zones(zone_list)

        #set look of nodes
        self._set_parents(node_tree)
        self._set_locations(node_tree)
        self._set_dimensions(node_tree)

        #create connections
        self._init_links(node_tree)
        
        self._write(f"return {nt_var}\n")

        #create node group
        self._write(f"{nt_var} = {nt_var}_node_group()\n", self._outer_indent_level)


    def _apply_modifier(self, nt: GeometryNodeTree, nt_var: str):
        #get object
        self._write(f"{OBJECT_NAME} = bpy.context.object.name", self._outer_indent_level)
        self._write(f"{OBJECT} = bpy.data.objects[{OBJECT_NAME}]", self._outer_indent_level)

        #set modifier to the one we just created
        mod_name = str_to_py_str(nt.name)
        self._write(f"{MODIFIER} = obj.modifiers.new(name = {mod_name}, "
                    f"type = 'NODES')", self._outer_indent_level)
        self._write(f"{MODIFIER}.node_group = {nt_var}", self._outer_indent_level)


    def execute(self, context):
        if not self._setup_options(context.scene.ntp_options):
            return {'CANCELLED'}

        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self._mode == 'ADDON':
            self._outer_indent_level = 2
            self._inner_indent_level = 3

            if not self._setup_addon_directories(context, nt_var):
                return {'CANCELLED'}

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            self._create_header(nt.name)
            self._class_name = clean_string(nt.name, lower = False)
            self._init_operator(nt_var, nt.name)
            self._write("def execute(self, context):", 1)
        else:
            self._file = StringIO("")
            if self._include_imports:
                self._file.write("import bpy\nimport mathutils\n\n\n")


        node_trees_to_process = self._topological_sort(nt)

        for node_tree in node_trees_to_process:  
            self._process_node_tree(node_tree)

        if self._mode == 'ADDON':
            self._apply_modifier(nt, nt_var)
            self._write("return {'FINISHED'}\n", self._outer_indent_level)
            self._create_menu_func()
            self._create_register_func()
            self._create_unregister_func()
            self._create_main_func()
            self._create_license()
            if bpy.app.version >= (4, 2, 0):
                self._create_manifest()
        else:
            context.window_manager.clipboard = self._file.getvalue()
        self._file.close()

        if self._mode == 'ADDON':
            self._zip_addon()

        self._report_finished("geometry node group")

        return {'FINISHED'}