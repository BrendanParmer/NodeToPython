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
        def _process_zone_output_node(self, node: GeometryNode) -> None:
            is_sim = False
            if node.bl_idname == 'GeometryNodeSimulationOutput':
                items = "state_items"
                is_sim = True
            elif node.bl_idname == 'GeometryNodeRepeatOutput':
                items = "repeat_items"
            else:
                self.report({'WARNING'}, f"NodeToPython: {node.bl_idname} is "
                                         f"not recognized as a valid zone output")

            node_var = self._node_vars[node]

            self._write(f"# Remove generated {items}")
            self._write(f"for item in {node_var}.{items}:")
            self._write(f"\t{node_var}.{items}.remove(item)")

            for i, item in enumerate(getattr(node, items)):
                socket_type = enum_to_py_str(item.socket_type)
                name = str_to_py_str(item.name)
                self._write(f"# Create item {name}")
                self._write(f"{node_var}.{items}.new"
                            f"({socket_type}, {name})")
                if is_sim:
                    item_var = f"{node_var}.{items}[{i}]"
                    ad = enum_to_py_str(item.attribute_domain)
                    self._write(f"{item_var}.attribute_domain = {ad}")

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

        if node.bl_idname == 'GeometryNodeGroup':
            self._process_group_node_tree(node)

        elif node.bl_idname == 'GeometryNodeSimulationInput':
            ntp_nt.sim_inputs.append(node)

        elif node.bl_idname == 'GeometryNodeSimulationOutput':
            self._process_zone_output_node(node)

        elif node.bl_idname == 'GeometryNodeRepeatInput':
            ntp_nt.repeat_inputs.append(node)
        
        elif node.bl_idname == 'GeometryNodeRepeatOutput':
            self._process_zone_output_node(node)
        
        self._hide_hidden_sockets(node)

        if node.bl_idname not in {'GeometryNodeSimulationInput', 'GeometryNodeRepeatInput'}:
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
            self._write("")

    if bpy.app.version >= (4, 0, 0):
        def _set_geo_tree_properties(self, node_tree: GeometryNodeTree) -> None:
            is_mod = node_tree.is_modifier
            is_tool = node_tree.is_tool

            nt_var = self._node_tree_vars[node_tree]

            if is_mod:
                self._write(f"{nt_var}.is_modifier = True")
            if is_tool:
                self._write(f"{nt_var}.is_tool = True")

                tool_flags =  ["is_mode_edit", 
                               "is_mode_sculpt",
                               "is_type_curve",
                               "is_type_mesh",
                               "is_type_point_cloud"]
            
                for flag in tool_flags:
                    self._write(f"{nt_var}.{flag} = {getattr(node_tree, flag)}")
            self._write("")

    def _process_node_tree(self, node_tree: GeometryNodeTree) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (GeometryNodeTree): geometry node tree to be recreated
        """
        
        nt_var = self._create_var(node_tree.name)
        self._node_tree_vars[node_tree] = nt_var

        #initialize node group
        self._write(f"#initialize {nt_var} node group", self._outer)
        self._write(f"def {nt_var}_node_group():", self._outer)
        self._write(f"{nt_var} = bpy.data.node_groups.new("
                    f"type = \'GeometryNodeTree\', "
                    f"name = {str_to_py_str(node_tree.name)})\n")

        if bpy.app.version >= (4, 0, 0):
            self._set_geo_tree_properties(node_tree)
    
        #initialize nodes
        self._write(f"#initialize {nt_var} nodes")

        ntp_nt = NTP_GeoNodeTree(node_tree, nt_var)

        if bpy.app.version >= (4, 0, 0):
            self._tree_interface_settings(ntp_nt)

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt)

        if bpy.app.version >= (3, 6, 0):
            self._process_zones(ntp_nt.sim_inputs)
        if bpy.app.version >= (4, 0, 0):
            self._process_zones(ntp_nt.repeat_inputs)

        #set look of nodes
        self._set_parents(node_tree)
        self._set_locations(node_tree)
        self._set_dimensions(node_tree)

        #create connections
        self._init_links(node_tree)
        
        self._write(f"return {nt_var}\n")

        #create node group
        self._write(f"{nt_var} = {nt_var}_node_group()\n", self._outer)


    def _apply_modifier(self, nt: GeometryNodeTree, nt_var: str):
        #get object
        self._write(f"name = bpy.context.object.name", self._outer)
        self._write(f"obj = bpy.data.objects[name]", self._outer)

        #set modifier to the one we just created
        mod_name = str_to_py_str(nt.name)
        self._write(f"mod = obj.modifiers.new(name = {mod_name}, "
                    f"type = 'NODES')", self._outer)
        self._write(f"mod.node_group = {nt_var}", self._outer)


    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            self._outer = "\t\t"
            self._inner = "\t\t\t"

            self._setup_addon_directories(context, nt_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            self._create_header(nt.name)
            self._class_name = clean_string(nt.name, lower = False)
            self._init_operator(nt_var, nt.name)
            self._write("def execute(self, context):", "\t")
        else:
            self._file = StringIO("")

        node_trees_to_process = self._topological_sort(nt)

        for node_tree in node_trees_to_process:  
            self._process_node_tree(node_tree)

        if self.mode == 'ADDON':
            self._apply_modifier(nt, nt_var)
            self._write("return {'FINISHED'}\n", self._outer)
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