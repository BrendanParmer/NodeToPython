import bpy

class NTPOptions(bpy.types.PropertyGroup):
    """
    Property group used during conversion of node group to python
    """
    dir_path : bpy.props.StringProperty(
        name = "Save Location",
        subtype='DIR_PATH',
        description="Save location if generating an add-on",
        default = "//"
    )

class NTPOptionsPanel(bpy.types.Panel):
    bl_label = "Options"
    bl_idname = "NODE_PT_ntp_options"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    @classmethod
    def poll(cls, context):
        return True
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.prop(context.scene.ntp_options, "dir_path")