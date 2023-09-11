import bpy
from bpy.types import Panel

class NTPGeoNodesPanel(Panel):
    bl_label = "Geometry Nodes to Python"
    bl_idname = "NODE_PT_geo_nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        
        # Disables menu when len of geometry nodes is 0
        geo_node_groups = [node_tree for node_tree in bpy.data.node_groups 
                            if node_tree.bl_idname == 'GeometryNodeTree']
        geo_node_groups_exist = len(geo_node_groups) > 0
        row.enabled = geo_node_groups_exist

        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_ntp_geo_nodes", text="Geometry Nodes")