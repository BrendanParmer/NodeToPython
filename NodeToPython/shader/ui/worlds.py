import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_world_slots = bpy.props.CollectionProperty(
        type=NTP_PG_WorldSlot
    )
    bpy.types.Scene.ntp_world_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_world_slots
    del bpy.types.Scene.ntp_world_slots_index
    
class NTP_PG_WorldSlot(bpy.types.PropertyGroup):
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

class NTP_OT_AddWorldSlot(bpy.types.Operator):
    bl_idname = "ntp.add_world_slot"
    bl_label = "Add World Slot"
    bl_description = "Add World Slot"

    def execute(self, context):
        slots = context.scene.ntp_world_slots
        slot = slots.add()
        context.scene.ntp_world_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class NTP_OT_RemoveWorldSlot(bpy.types.Operator):
    bl_idname = "ntp.remove_world_slot"
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
        
class NTP_UL_World(bpy.types.UIList):
    bl_idname = "NTP_UL_world"

    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "world", bpy.data, "worlds", text="")

class NTP_PT_World(bpy.types.Panel):
    bl_idname = "NTP_PT_world"
    bl_label = "Worlds"
    bl_parent_id = panel.NTP_PT_Shader.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.World objects to replicate"
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
            NTP_UL_World.bl_idname, "", 
            context.scene, "ntp_world_slots", 
            context.scene, "ntp_world_slots_index"
        )

        col = row.column(align=True)
        col.operator(NTP_OT_AddWorldSlot.bl_idname, icon="ADD", text="")
        col.operator(NTP_OT_RemoveWorldSlot.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    NTP_PG_WorldSlot,
    NTP_OT_AddWorldSlot,
    NTP_OT_RemoveWorldSlot,
    NTP_UL_World,
    NTP_PT_World
]