import bpy

from . import panel

def register_props():
    bpy.types.Scene.material_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.material_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.material_slots
    del bpy.types.Scene.material_slots_index
    
class Slot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Material Name",
        default=""
    )

    def poll_material(self, material: bpy.types.Material) -> bool:
        for slot in bpy.context.scene.material_slots:
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

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_material_slot_add"
    bl_label = "Add Material Slot"
    bl_description = "Add Material Slot"

    def execute(self, context):
        slots = context.scene.material_slots
        slot = slots.add()
        context.scene.material_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_material_slot_remove"
    bl_label = "Remove Material Slot"
    bl_description = "Remove Material Slot"

    def execute(self, context):
        slots = context.scene.material_slots
        idx = context.scene.material_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.material_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
            return {'FINISHED'}
        
class Material_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "material", bpy.data, "materials", text="")

class Material_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_material_panel"
    bl_label = "Materials"
    bl_parent_id = panel.NTPShaderPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.Material objects to replicate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "Material_UIList", "", 
            context.scene, "material_slots", 
            context.scene, "material_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    Material_UIList,
    Material_Panel
]