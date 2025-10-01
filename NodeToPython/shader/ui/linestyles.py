import bpy

from . import panel

def register_props():
    bpy.types.Scene.ntp_line_style_slots = bpy.props.CollectionProperty(
        type=Slot
    )
    bpy.types.Scene.ntp_line_style_slots_index = bpy.props.IntProperty()

def unregister_props():
    del bpy.types.Scene.ntp_line_style_slots
    del bpy.types.Scene.ntp_line_style_slots_index
    
class Slot(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Line Style Name",
        default=""
    )

    def poll_line_style(self, line_style: bpy.types.FreestyleLineStyle) -> bool:
        for slot in bpy.context.scene.ntp_line_style_slots:
            if slot is not self and slot.line_style == line_style:
                return False
        return line_style.use_nodes

    def update_line_style(self, context):
        if self.line_style:
            self.name = self.line_style.name
        else:
            self.name = "Line Style"

    line_style: bpy.props.PointerProperty(
        name="Line Style",
        type=bpy.types.FreestyleLineStyle,
        poll=poll_line_style,
        update=update_line_style
    )

class AddSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_line_style_slot_add"
    bl_label = "Add Line Style Slot"
    bl_description = "Add Line Style Slot"

    def execute(self, context):
        slots = context.scene.ntp_line_style_slots
        slot = slots.add()
        context.scene.ntp_line_style_slots_index = len(slots) - 1
        return {'FINISHED'}
    
class RemoveSlotOperator(bpy.types.Operator):
    bl_idname = "node.ntp_line_style_slot_remove"
    bl_label = "Remove Line Style Slot"
    bl_description = "Remove Line Style Slot"

    def execute(self, context):
        slots = context.scene.ntp_line_style_slots
        idx = context.scene.ntp_line_style_slots_index

        if idx >= 0 and idx < len(slots):
            slots.remove(idx)
            context.scene.ntp_line_style_slots_index = min(
                max(0, idx - 1), len(slots) - 1
            )
            return {'FINISHED'}
        
class LineStyle_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active):
        if item:
            layout.prop_search(item, "line_style", bpy.data, "linestyles", text="")

class LineStyle_Panel(bpy.types.Panel):
    bl_idname = "node.ntp_line_style_panel"
    bl_label = "Line Styles"
    bl_parent_id = panel.NTPShaderPanel.bl_idname
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"
    bl_description = "List of bpy.types.FreestyleLineStyle objects to replicate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            "LineStyle_UIList", "", 
            context.scene, "ntp_line_style_slots", 
            context.scene, "ntp_line_style_slots_index"
        )

        col = row.column(align=True)
        col.operator(AddSlotOperator.bl_idname, icon="ADD", text="")
        col.operator(RemoveSlotOperator.bl_idname, icon="REMOVE", text="")

classes: list[type] = [
    Slot,
    AddSlotOperator,
    RemoveSlotOperator,
    LineStyle_UIList,
    LineStyle_Panel
]