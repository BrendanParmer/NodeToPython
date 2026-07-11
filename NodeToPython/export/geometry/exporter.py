import bpy

from ..node_group_gatherer import NodeGroupType
from ..node_tree_exporter import NodeTreeExporter, NODE_TREE_NAMES
from ..ntp_operator import NTP_OT_Export, NodeTreeInfo
from ..utils import *

from .node_tree import NTP_GeoNodeTree, NTP_NodeTree

GEO_OP_RESERVED_NAMES = {
}

class GeometryNodesExporter(NodeTreeExporter):
    bl_idname = "ntp.geometry_nodes"
    bl_label = "Geometry Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(
        self,
        ntp_operator: NTP_OT_Export,
        node_tree_info: NodeTreeInfo
    ):
        if not node_tree_info._group_type.is_geometry():
            ntp_operator.report(
                {'ERROR'},
                f"Cannot initialize GeometryNodesExporter with group type "
                f"{node_tree_info._group_type}"
            )
        NodeTreeExporter.__init__(self, ntp_operator, node_tree_info)
        for name in GEO_OP_RESERVED_NAMES:
            self._used_vars[name] = 0

    def _set_node_tree_properties(self, node_tree: bpy.types.NodeTree) -> None:
        NodeTreeExporter._set_node_tree_properties(self, node_tree)
        self._set_geo_tree_properties(node_tree)

    def _set_geo_tree_properties(self, node_tree: bpy.types.GeometryNodeTree) -> None:
        is_mod = node_tree.is_modifier
        is_tool = node_tree.is_tool
        nt_var = self._node_tree_vars[node_tree]
        if is_mod:
            self._write(f"{nt_var}.is_modifier = True")
            
        if is_tool:
            self._write(f"{nt_var}.is_tool = True")
            tool_flags =  [
                "is_mode_object",
                "is_mode_edit", 
                "is_mode_sculpt",
                "is_type_curve",
                "is_type_mesh",
                "is_type_point_cloud"
            ]
        
            for flag in tool_flags:
                if hasattr(node_tree, flag) is True:
                    self._write(f"{nt_var}.{flag} = {getattr(node_tree, flag)}")

        if node_tree.use_wait_for_click:
            self._write(f"{nt_var}.use_wait_for_click = True")
                
        if bpy.app.version >= (5, 0, 0):
            if node_tree.show_modifier_manage_panel:
                self._write(f"{nt_var}.show_modifier_manage_panel = True")
        self._write("", 0)

    # NodeTreeExporter interface
    def _create_obj(self) -> None:
        pass

    def _initialize_ntp_node_tree(
        self, 
        node_tree: bpy.types.NodeTree,
        nt_var: str
    ) -> NTP_NodeTree:
        return NTP_GeoNodeTree(node_tree, nt_var)
    
    # NodeTreeExporter interface
    def _initialize_node_tree(
        self, 
        ntp_node_tree: NTP_NodeTree
    ) -> None:
        nt_name = ntp_node_tree._node_tree.name
        self._node_tree_info._func = self._operator._create_var(
            f"{ntp_node_tree._var}_node_group"
        )
        #initialize node group
        self._write(f"def {self._node_tree_info._func}("
                    f"{NODE_TREE_NAMES}: dict[typing.Callable, str]):", 
                    self._operator._outer_indent_level)
        self._write(f'"""Initialize {nt_name} node group"""')
        self._write(f"{ntp_node_tree._var} = bpy.data.node_groups.new("
                    f"type=\'GeometryNodeTree\', "
                    f"name={str_to_py_str(nt_name)})\n")