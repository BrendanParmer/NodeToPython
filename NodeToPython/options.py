import bpy

def register_props():
    bpy.types.Scene.ntp_options = bpy.props.PointerProperty(
        type=NTP_PG_Options
    )

def unregister_props():
    del bpy.types.Scene.ntp_options

class NTP_PG_Options(bpy.types.PropertyGroup):
    """
    Property group used during conversion of node group to python
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # General properties
    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full add-on")
        ]
    )
    set_group_defaults : bpy.props.BoolProperty(
        name = "Set Group Defaults",
        description = "Generate group socket default, min, and max values",
        default = True
    )
    set_node_sizes : bpy.props.BoolProperty(
        name = "Set Node Sizes",
        description = "Set dimensions of generated nodes",
        default = True
    )

    indentation_type: bpy.props.EnumProperty(
        name="Indentation Type",
        description="Whitespace to use for each indentation block",
        items = [
            ('SPACES_2', "2 Spaces", ""),
            ('SPACES_4', "4 Spaces", ""),
            ('SPACES_8', "8 Spaces", ""),
            ('TABS', "Tabs", "")
        ],
        default = 'SPACES_4'
    )

    if bpy.app.version >= (3, 4, 0):
        set_unavailable_defaults : bpy.props.BoolProperty(
            name = "Set unavailable defaults",
            description = "Set default values for unavailable sockets",
            default = False
        )

    #Script properties
    include_imports : bpy.props.BoolProperty(
        name = "Include Imports",
        description="Generate necessary import statements (i.e. bpy, mathutils, etc)",
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
        name = "Author Name",
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
        description="Location property of the addon",
        default="Node"
    )
    menu_id: bpy.props.StringProperty(
        name = "Menu ID",
        description = "Python ID of the menu you'd like to register the add-on "
                      "to. You can find these by enabling Python tooltips "
                      "(Preferences > Interface > Python tooltips) and "
                      "hovering over the desired menu",
        default="NODE_MT_add"
    )
    license: bpy.props.EnumProperty(
        name="License",
        items = [
            ('SPDX:GPL-3.0-or-later', "GNU General Public License v3.0 or later", ""),
            ('OTHER', "Other", "User is responsible for including the license "
                               "and adding it to the manifest.\n"
                               "Please note that by using the Blender Python "
                               "API, your add-on must comply with the GNU GPL. "
                               "See https://www.blender.org/about/license/ for "
                               "more details")
        ],
        default = 'SPDX:GPL-3.0-or-later'
    )
    should_create_license: bpy.props.BoolProperty(
        name="Create License",
        description="Should NodeToPython include a license file for your add-on",
        default=True
    )
    category: bpy.props.EnumProperty(
        name = "Category",
        items = [
            ('Custom',         "Custom",         "Use an unofficial category"),
            ('3D View',        "3D View",        ""),
            ('Add Curve',      "Add Curve",      ""),
            ('Add Mesh',       "Add Mesh",       ""),
            ('Animation',      "Animation",      ""),
            ('Bake',           "Bake",           ""),
            ('Compositing',    "Compositing",    ""),
            ('Development',    "Development",    ""),
            ('Game Engine',    "Game Engine",    ""),
            ('Geometry Nodes', "Geometry Nodes", ""),
            ("Grease Pencil",  "Grease Pencil",  ""),
            ('Import-Export',  "Import-Export",  ""),
            ('Lighting',       "Lighting",       ""),
            ('Material',       "Material",       ""),
            ('Mesh',           "Mesh",           ""),
            ('Modeling',       "Modeling",       ""),
            ('Node',           "Node",           ""),
            ('Object',         "Object",         ""),
            ('Paint',          "Paint",          ""),
            ('Pipeline',       "Pipeline",       ""),
            ('Physics',        "Physics",        ""),
            ('Render',         "Render",         ""),
            ('Rigging',        "Rigging",        ""),
            ('Scene',          "Scene",          ""),
            ('Sculpt',         "Sculpt",         ""),
            ('Sequencer',      "Sequencer",      ""),
            ('System',         "System",         ""),
            ('Text Editor',    "Text Editor",    ""),
            ('Tracking',       "Tracking",       ""),
            ('UV',             "UV",             ""),
            ('User Interface', "User Interface", ""),
        ],
        default = 'Node'
    )
    custom_category: bpy.props.StringProperty(
        name="Custom Category",
        description="Set the custom category property for your add-on",
        default = ""
    )

class NTP_PT_Options(bpy.types.Panel):
    bl_label = "Options"
    bl_idname = "NODE_PT_ntp_options"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def poll(cls, context):
        return True
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        ntp_options = context.scene.ntp_options

        option_list = [
            "mode",
            "set_group_defaults",
            "set_node_sizes", 
            "indentation_type"
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
                "should_create_license",
                "category"
            ]
            option_list += addon_options
            if ntp_options.category == 'Custom':
                option_list.append("custom_category")

        for option in option_list:
            layout.prop(ntp_options, option)

classes = [
    NTP_PG_Options,
    NTP_PT_Options
]