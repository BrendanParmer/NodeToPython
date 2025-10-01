import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_world_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.ntp_world_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_world_slots
    del bpy.types.Scene.ntp_world_slots_index
    
class Slot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="World Name",
        default=""
    )

    def poll_world(self, world: bpy.types.World) -> bool:
        for slot in bpy.context.scene.ntp_world_slots:
            if slot is not self and slot.world == world:
                return False
        return world.use_nodes

    def update_world(self, context):
        if self.world:
            self.name = self.world.name
        else:
            self.name = "World"

    world: bpy.props.PointerProperty(
        name="World",
        type=bpy.types.World,
        poll=poll_world,
        update=update_world
    )

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_world_slot_add"
    bl_label = "Add World Slot"
    bl_description = "Add World Slot"

    def execute(self, context):
        slots = context.scene.ntp_world_slots
        slot = slots.add()
        context.scene.ntp_world_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_world_slot_remove"
    bl_label = "Remove World Slot"
    bl_description = "Remove World Slot"

    def execute(self, context):
        slots = context.scene.ntp_world_slots
        idx = context.scene.ntp_world_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_world_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
            return {'FINISHED'}
        
class World_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "world", bpy.data, "worlds", text="")

class World_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_world_panel"
    bl_label = "Worlds"
    bl_parent_id = panel.NTPShaderPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.World objects to replicate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "World_UIList", "", 
            context.scene, "ntp_world_slots", 
            context.scene, "ntp_world_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    World_UIList,
    World_Panel
]