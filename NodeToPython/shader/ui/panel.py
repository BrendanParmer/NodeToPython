import bpy

class NTP_PT_Shader(bpy.types.Panel):
    bl_label = "Shader to Python"
    bl_idname = "NTP_PT_shader"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_options = {'DEFAULT_CLOSED'}
    
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
    NTP_PT_Shader
]