bl_info = {
    "name": "Node to Python", 
    "description": "Convert Blender node groups to a Python add-on!",
    "author": "Brendan Parmer",
    "version": (3, 5, 1),
    "blender": (3, 0, 0),
    "location": "Node", 
    "category": "Node",
}

if "bpy" in locals():
    import importlib
    importlib.reload(compositor)
    importlib.reload(geometry)
    importlib.reload(shader)
    importlib.reload(options)
else:
    from . import compositor
    from . import geometry
    from . import shader
    from . import options

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


classes: list[type] = [
    NodeToPythonMenu,
    #options
    options.NTPOptions,
    options.NTPOptionsPanel,
    #geometry
    geometry.operator.NTPGeoNodesOperator,
    geometry.ui.NTPGeoNodesMenu,
    geometry.ui.NTPGeoNodesPanel,
    #material
    shader.operator.NTPShaderOperator,
    shader.ui.NTPShaderMenu,
    shader.ui.NTPShaderPanel,
]
classes += compositor.classes

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    scene = bpy.types.Scene
    scene.ntp_options = bpy.props.PointerProperty(type=options.NTPOptions)
    compositor.register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ntp_options
    compositor.unregister_props()

if __name__ == "__main__":
    register()