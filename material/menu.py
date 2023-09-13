import bpy
from bpy.types import Menu
from .operator import NTPMaterialOperator

class NTPMaterialMenu(Menu):
    bl_idname = "NODE_MT_ntp_material"
    bl_label = "Select Material"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for mat in bpy.data.materials:
            if mat.node_tree:
                op = layout.operator(NTPMaterialOperator.bl_idname, 
                                     text=mat.name)
                op.material_name = mat.name