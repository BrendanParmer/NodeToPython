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
    include_imports : bpy.props.BoolProperty(
        name = "Include imports",
        description="Generate necessary import statements",
        default = True
    )
    include_group_socket_values : bpy.props.BoolProperty(
        name = "Include group socket values",
        description = "Generate group socket default, min, and max values",
        default = True
    )
    set_dimensions : bpy.props.BoolProperty(
        name = "Set dimensions",
        description = "Set dimensions of generated nodes",
        default = True
    )
    if bpy.app.version >= (3, 4, 0):
        set_unavailable_defaults : bpy.props.BoolProperty(
            name = "Set unavailable defaults",
            description = "Set default values for unavailable sockets",
            default = False
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
        ntp_options = context.scene.ntp_options

        option_list = [
            "dir_path", 
            "include_imports", 
            "include_group_socket_values",
            "set_dimensions"
        ]
        if bpy.app.version >= (3, 4, 0):
            option_list.append("set_unavailable_defaults")
        for option in option_list:
            layout.prop(ntp_options, option)