import bpy
from bpy.types import Menu

from .operator import NTPGeoNodesOperator

class NTPGeoNodesMenu(Menu):
    bl_idname = "NODE_MT_ntp_geo_nodes"
    bl_label = "Select Geo Nodes"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'

        geo_node_groups = [node_tree for node_tree in bpy.data.node_groups 
                           if node_tree.bl_idname == 'GeometryNodeTree']

        for node_tree in bpy.data.node_groups:
            if node_tree.bl_idname == 'GeometryNodeTree':
                op = layout.operator(NTPGeoNodesOperator.bl_idname, 
                                     text=node_tree.name)
                op.geo_nodes_group_name = node_tree.name