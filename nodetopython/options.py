import bpy

class NTPOptions(bpy.types.PropertyGroup):
    """
    Property group used during conversion of node group to python
    """
    # General properties
    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full add-on")
        ]
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

    #Script properties
    include_imports : bpy.props.BoolProperty(
        name = "Include imports",
        description="Generate necessary import statements",
        default = True
    )
    
    # Addon properties
    dir_path : bpy.props.StringProperty(
        name = "Save Location",
        subtype='DIR_PATH',
        description="Save location if generating an add-on",
        default = "//"
    )
    name_override : bpy.props.StringProperty(
        name = "Name Override",
        description="Name used for the add-on's, default is node group name",
        default = ""
    )
    description : bpy.props.StringProperty(
        name = "Description",
        description="Description used for the add-on",
        default=""
    )
    author_name : bpy.props.StringProperty(
        name = "Author",
        description = "Name used for the author/maintainer of the add-on",
        default = "Node To Python"
    )
    version: bpy.props.IntVectorProperty(
        name = "Version",
        description="Version of the add-on",
        default = (1, 0, 0)
    )
    location: bpy.props.StringProperty(
        name = "Location",
        description="Location of the addon",
        default="Node"
    )
    menu_id: bpy.props.StringProperty(
        name = "Menu ID",
        description = "Python ID of the menu you'd like to register the add-on "
                      "to. You can find this by enabling Python tooltips "
                      "(Preferences > Interface > Python tooltips) and "
                      "hovering over the desired menu",
        default="NODE_MT_add"
    )
    license: bpy.props.EnumProperty(
        name="License",
        items = [
            ('SPDX:GPL-2.0-or-later', "GNU General Public License v2.0 or later", ""),
            ('SPDX:GPL-3.0-or-later', "GNU General Public License v3.0 or later", ""),
            ('SPDX:LGPL-2.1-or-later', "GNU Lesser General Public License v2.1 or later", ""),
            ('SPDX:LGPL-3.0-or-later', "GNU Lesser General Public License v3.0 or later", ""),
            ('SPDX:BSD-1-Clause', "BSD 1-Clause \"Simplified\" License", ""),
            ('SPDX:BSD-2-Clause', "BSD 2-Clause \"Simplified\" License", ""),
            ('SPDX:BSD-3-Clause', "BSD 3-Clause \"New\" or \"Revised\" License", ""),
            ('SPDX:BSL-1.0', "Boost Software License 1.0", ""),
            ('SPDX:MIT', "MIT License", ""),
            ('SPDX:MIT-0', "MIT No Attribution", ""),
            ('SPDX:MPL-2.0', "Mozilla Public License 2.0", ""),
            ('SPDX:Pixar', "Pixar License", ""),
            ('SPDX:Zlib', "Zlib License", ""),
            ('OTHER', "Other", "")
        ],
        default = 'OTHER'
    )
    category: bpy.props.EnumProperty(
        name = "Category",
        items = [
            ('Custom',          "Custom",           "Use an unofficial category"),
            ('3D View',         "3D View",          ""),
            ('Add Curve',       "Add Curve",        ""),
            ('Add Mesh',        "Add Mesh",         ""),
            ('Animation',       "Animation",        ""),
            ('Bake',            "Bake",             ""),
            ('Compositing',     "Compositing",      ""),
            ('Development',     "Development",      ""),
            ('Game Engine',     "Game Engine",      ""),
            ('Geometry Nodes',  "Geometry Nodes",   ""),
            ("Grease Pencil",   "Grease Pencil",    ""),
            ('Import-Export',   "Import-Export",    ""),
            ('Lighting',        "Lighting",         ""),
            ('Material',        "Material",         ""),
            ('Mesh',            "Mesh",             ""),
            ('Modeling',        "Modeling",         ""),
            ('Node',            "Node",             ""),
            ('Object',          "Object",           ""),
            ('Paint',           "Paint",            ""),
            ('Pipeline',        "Pipeline",         ""),
            ('Physics',         "Physics",          ""),
            ('Render',          "Render",           ""),
            ('Rigging',         "Rigging",          ""),
            ('Scene',           "Scene",            ""),
            ('Sculpt',          "Sculpt",           ""),
            ('Sequencer',       "Sequencer",        ""),
            ('System',          "System",           ""),
            ('Text Editor',     "Text Editor",      ""),
            ('Tracking',        "Tracking",         ""),
            ('UV',              "UV",               ""),
            ('User Interface',  "User Interface",   ""),
        ],
        default = 'Node'
    )
    custom_category: bpy.props.StringProperty(
        name="Custom Category",
        description="Custom category",
        default = ""
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
            "mode",
            "include_group_socket_values",
            "set_dimensions"
        ]
        if bpy.app.version >= (3, 4, 0):
            option_list.append("set_unavailable_defaults")
        
        if ntp_options.mode == 'SCRIPT':
            script_options = [
                "include_imports"
            ]
            option_list += script_options
        elif ntp_options.mode == 'ADDON':
            addon_options = [
                "dir_path",
                "name_override",
                "description",
                "author_name",
                "version",
                "location",
                "menu_id",
                "license",
                "category"
            ]
            option_list += addon_options
            if ntp_options.category == 'CUSTOM':
                option_list.append("custom_category")

        for option in option_list:
            layout.prop(ntp_options, option)