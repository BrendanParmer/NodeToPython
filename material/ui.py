import bpy
from bpy.types import Panel
from bpy.types import Menu
from .operator import NTPMaterialOperator

class NTPMaterialPanel(Panel):
    bl_label = "Material to Python"
    bl_idname = "NODE_PT_mat_to_python"
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
        row = layout.row()
        
        # Disables menu when there are no materials
        materials = [mat for mat in bpy.data.materials if mat.node_tree]
        materials_exist = len(materials) > 0
        row.enabled = materials_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_ntp_material", text="Materials")

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