import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_scene_slots = bpy.props.CollectionProperty(
        type=NTP_PG_SceneSlot
    )
    bpy.types.Scene.ntp_scene_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_scene_slots
    del bpy.types.Scene.ntp_scene_slots_index

class NTP_PG_SceneSlot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Scene Name",
        default=""
    )

    def poll_scene(self, scene: bpy.types.Scene) -> bool:
        for slot in bpy.context.scene.ntp_scene_slots:
            if slot is not self and slot.scene == scene:
                return False
        return scene.use_nodes

    def update_scene(self, context):
        if self.scene:
            self.name = self.scene.name
        else:
            self.name = "Scene"

    scene: bpy.props.PointerProperty(
        name="Scene",
        type=bpy.types.Scene,
        poll=poll_scene,
        update=update_scene
    )

class NTP_OT_AddSceneSlot(bpy.types.Operator):
    bl_idname = "ntp.add_scene_slot"
    bl_label = "Add Scene Slot"
    bl_description = "Add Scene Slot"

    def execute(self, context):
        slots = context.scene.ntp_scene_slots
        slot = slots.add()
        context.scene.ntp_scene_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class NTP_OT_RemoveSceneSlot(bpy.types.Operator):
    bl_idname = "ntp.remove_scene_slot"
    bl_label = "Remove Scene Slot"
    bl_description = "Remove Scene Slot"

    def execute(self, context):
        slots = context.scene.ntp_scene_slots
        idx = context.scene.ntp_scene_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_scene_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
        return {'FINISHED'}
        
class NTP_UL_Scene(bpy.types.UIList):
    bl_idname = "NTP_UL_scene"

    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "scene", bpy.data, "scenes", text="")

class NTP_PT_Scene(bpy.types.Panel):
    bl_idname = "NTP_PT_scene"
    bl_label = "Scenes"
    bl_parent_id = panel.NTP_PT_Compositor.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.Scene objects to replicate"
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
            NTP_UL_Scene.bl_idname, "", 
            context.scene, "ntp_scene_slots", 
            context.scene, "ntp_scene_slots_index"
        )

        col = row.column(align=True)
        col.operator(NTP_OT_AddSceneSlot.bl_idname, icon="ADD", text="")
        col.operator(NTP_OT_RemoveSceneSlot.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    NTP_PG_SceneSlot,
    NTP_OT_AddSceneSlot,
    NTP_OT_RemoveSceneSlot,
    NTP_UL_Scene,
    NTP_PT_Scene
]