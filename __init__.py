bl_info = {
    "name": "Node to Python", 
    "description": "Convert Blender node groups to a Python add-on!",
    "author": "Brendan Parmer",
    "version": (2, 2, 0),
    "blender": (3, 0, 0),
    "location": "Node", 
    "category": "Node",
}

if "bpy" in locals():
    import importlib
    importlib.reload(materials)
    importlib.reload(geo_nodes)
else:
    from . import materials
    from . import geo_nodes

import bpy

class NodeToPythonMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_node_to_python"
    bl_label = "Node To Python"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'


class NTPOptions(bpy.types.PropertyGroup):
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

classes = [NodeToPythonMenu,
            NTPOptions,
            geo_nodes.GeoNodesToPython,
            geo_nodes.SelectGeoNodesMenu,
            geo_nodes.GeoNodesToPythonPanel,
            materials.MaterialToPython,
            materials.SelectMaterialMenu,
            materials.MaterialToPythonPanel,
            NTPOptionsPanel
            ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    scene = bpy.types.Scene
    scene.ntp_options = bpy.props.PointerProperty(type=NTPOptions)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ntp_options

if __name__ == "__main__":
    register()