import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_light_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.ntp_light_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_light_slots
    del bpy.types.Scene.ntp_light_slots_index
    
class Slot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Light Name",
        default=""
    )

    def poll_light(self, light: bpy.types.Light) -> bool:
        for slot in bpy.context.scene.ntp_light_slots:
            if slot is not self and slot.light == light:
                return False
        return light.use_nodes

    def update_light(self, context):
        if self.light:
            self.name = self.light.name
        else:
            self.name = "Light"

    light: bpy.props.PointerProperty(
        name="Light",
        type=bpy.types.Light,
        poll=poll_light,
        update=update_light
    )

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_light_slot_add"
    bl_label = "Add Light Slot"
    bl_description = "Add Light Slot"

    def execute(self, context):
        slots = context.scene.ntp_light_slots
        slot = slots.add()
        context.scene.ntp_light_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_light_slot_remove"
    bl_label = "Remove Light Slot"
    bl_description = "Remove Light Slot"

    def execute(self, context):
        slots = context.scene.ntp_light_slots
        idx = context.scene.ntp_light_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_light_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
            return {'FINISHED'}
        
class Light_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "light", bpy.data, "lights", text="")

class Light_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_light_panel"
    bl_label = "Lights"
    bl_parent_id = panel.NTPShaderPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.Light objects to replicate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "Light_UIList", "", 
            context.scene, "ntp_light_slots", 
            context.scene, "ntp_light_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    Light_UIList,
    Light_Panel
]