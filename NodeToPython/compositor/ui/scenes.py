import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_scene_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.ntp_scene_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_scene_slots
    del bpy.types.Scene.ntp_scene_slots_index

class Slot(bpy.types.PropertyGroup):
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

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_scene_slot_add"
    bl_label = "Add Scene Slot"
    bl_description = "Add Scene Slot"

    def execute(self, context):
        slots = context.scene.ntp_scene_slots
        slot = slots.add()
        context.scene.ntp_scene_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_scene_slot_remove"
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
        
class Scene_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "scene", bpy.data, "scenes", text="")

class Scene_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_scene_panel"
    bl_label = "Scenes"
    bl_parent_id = panel.NTPCompositorPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.Scene objects to replicate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "Scene_UIList", "", 
            context.scene, "ntp_scene_slots", 
            context.scene, "ntp_scene_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    Scene_UIList,
    Scene_Panel
]