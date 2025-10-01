import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_geometry_node_group_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.ntp_geometry_node_group_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_geometry_node_group_slots
    del bpy.types.Scene.ntp_geometry_node_group_slots_index
    
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

        for slot in scene.ntp_geometry_node_group_slots:
            if slot is not self and slot.node_tree == node_tree:
              return False
        return node_tree.bl_idname == 'GeometryNodeTree'
    
    def update_node_tree(self, context):
        if self.node_tree:
            self.name = self.node_tree.name
        else:
            self.name = "Geometry Node Group"

    node_tree: bpy.props.PointerProperty(
        name="Node Tree",
        type=bpy.types.NodeTree,
        poll=poll_node_tree,
        update=update_node_tree
    )

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_geometry_node_group_slot_add"
    bl_label = "Add Geometry Node Group Slot"
    bl_description = "Add Geometry Node Group Slot"

    def execute(self, context):
        slots = context.scene.ntp_geometry_node_group_slots
        slot = slots.add()
        context.scene.ntp_geometry_node_group_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_geometry_node_group_slot_remove"
    bl_label = "Remove Geometry Node Group Slot"
    bl_description = "Remove Geometry Node Group Slot"

    def execute(self, context):
        slots = context.scene.ntp_geometry_node_group_slots
        idx = context.scene.ntp_geometry_node_group_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_geometry_node_group_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
        return {'FINISHED'}
        
class GNG_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "node_tree", bpy.data, "node_groups", text="")

class GNG_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_geometry_node_group_panel"
    bl_label = "Node Groups"
    bl_parent_id = panel.NTPGeoNodesPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = ("List of geometry node group objects to replicate")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "GNG_UIList", "", 
            context.scene, "ntp_geometry_node_group_slots", 
            context.scene, "ntp_geometry_node_group_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    GNG_UIList,
    GNG_Panel
]