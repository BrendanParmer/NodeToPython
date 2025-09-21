import bpy

from . import panel

class Slot(bpy.types.PropertyGroup):
    """
    TODO: There's a bug where the filtering doesn't update when renaming a
    slotted object. For now, we'll need to just remove and re-add the slot
    to the UI list.
    """
    name: bpy.props.StringProperty(
        name="Node Tree Name",
        default=""
    )

    def poll_node_tree(self, node_tree: bpy.types.NodeTree) -> bool:
        scene = bpy.context.scene

        for slot in scene.compositor_node_group_slots:
            if slot is not self and slot.node_tree == node_tree:
              return False
        return node_tree.bl_idname == 'CompositorNodeTree'
    
    def update_node_tree(self, context):
        if self.node_tree:
            self.name = self.node_tree.name
        else:
            self.name = "Compositor Node Group"

    node_tree: bpy.props.PointerProperty(
        name="Node Tree",
        type=bpy.types.NodeTree,
        poll=poll_node_tree,
        update=update_node_tree
    )

def register_props():
    bpy.types.Scene.compositor_node_group_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.compositor_node_group_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.compositor_node_group_slots
    del bpy.types.Scene.compositor_node_group_slots_index

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_compositor_node_group_slot_add"
    bl_label = "Add Compositor Node Group Slot"
    bl_description = "Add Compositor Node Group Slot"

    def execute(self, context):
        slots = context.scene.compositor_node_group_slots
        slot = slots.add()
        context.scene.compositor_node_group_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_compositor_node_group_slot_remove"
    bl_label = "Remove Compositor Node Group Slot"
    bl_description = "Remove Compositor Node Group Slot"

    def execute(self, context):
        slots = context.scene.compositor_node_group_slots
        idx = context.scene.compositor_node_group_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.compositor_node_group_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
        return {'FINISHED'}
        
class CNG_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "node_tree", bpy.data, "node_groups", text="")

class CNG_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_compositor_node_group_panel"
    bl_label = "Node Groups"
    bl_parent_id = panel.NTPCompositorPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = ("List of compositor node group objects to replicate.\n"
                      "These are typically subgroups within a larger scene tree")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "CNG_UIList", "", 
            context.scene, "compositor_node_group_slots", 
            context.scene, "compositor_node_group_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    CNG_UIList,
    CNG_Panel
]