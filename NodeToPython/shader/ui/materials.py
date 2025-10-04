import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_material_slots = bpy.props.CollectionProperty(
        type=NTP_PG_MaterialSlot
    )
    bpy.types.Scene.ntp_material_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_material_slots
    del bpy.types.Scene.ntp_material_slots_index
    
class NTP_PG_MaterialSlot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Material Name",
        default=""
    )

    def poll_material(self, material: bpy.types.Material) -> bool:
        for slot in bpy.context.scene.ntp_material_slots:
            if slot is not self and slot.material == material:
                return False
        return material.use_nodes

    def update_material(self, context):
        if self.material:
            self.name = self.material.name
        else:
            self.name = "Material"

    material: bpy.props.PointerProperty(
        name="Material",
        type=bpy.types.Material,
        poll=poll_material,
        update=update_material
    )

class NTP_OT_AddMaterialSlot(bpy.types.Operator):
    bl_idname = "ntp.add_material_slot"
    bl_label = "Add Material Slot"
    bl_description = "Add Material Slot"

    def execute(self, context):
        slots = context.scene.ntp_material_slots
        slot = slots.add()
        context.scene.ntp_material_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class NTP_OT_RemoveMaterialSlot(bpy.types.Operator):
    bl_idname = "ntp.remove_material_slot"
    bl_label = "Remove Material Slot"
    bl_description = "Remove Material Slot"

    def execute(self, context):
        slots = context.scene.ntp_material_slots
        idx = context.scene.ntp_material_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_material_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
        return {'FINISHED'}
        
class NTP_UL_Material(bpy.types.UIList):
    bl_idname = "NTP_UL_material"

    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "material", bpy.data, "materials", text="")

class NTP_PT_Material(bpy.types.Panel):
    bl_idname = "NTP_PT_material"
    bl_label = "Materials"
    bl_parent_id = panel.NTP_PT_Shader.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.Material objects to replicate"
    bl_options = {'DEFAULT_CLOSED'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            NTP_UL_Material.bl_idname, "", 
            context.scene, "ntp_material_slots", 
            context.scene, "ntp_material_slots_index"
        )

        col = row.column(align=True)
        col.operator(NTP_OT_AddMaterialSlot.bl_idname, icon="ADD", text="")
        col.operator(NTP_OT_RemoveMaterialSlot.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    NTP_PG_MaterialSlot,
    NTP_OT_AddMaterialSlot,
    NTP_OT_RemoveMaterialSlot,
    NTP_UL_Material,
    NTP_PT_Material
]