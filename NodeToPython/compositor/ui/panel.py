import bpy
from bpy.types import Panel
from bpy.types import Menu
from ..operator import NTPCompositorOperator

class NTPCompositorPanel(Panel):
    bl_label = "Compositor to Python"
    bl_idname = "NODE_PT_ntp_compositor"
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
    NTPCompositorPanel
]