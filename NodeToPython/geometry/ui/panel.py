import bpy

class NTPGeoNodesPanel(bpy.types.Panel):
    bl_label = "Geometry Nodes to Python"
    bl_idname = "NODE_PT_ntp_geonodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout

classes: list[type] = [
    NTPGeoNodesPanel
]