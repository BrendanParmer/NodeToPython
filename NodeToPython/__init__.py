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

def register_props():
    bpy.types.Scene.ntp_options = bpy.props.PointerProperty(
        type=options.NTPOptions
    )

def unregister_props():
    del bpy.types.Scene.ntp_options

# TODO: do away with this, separate out into more appropriate modules
classes: list[type] = [
    NodeToPythonMenu,
    #options
    options.NTPOptions,
    options.NTPOptionsPanel,
    #shader
    shader.operator.NTPShaderOperator,
    shader.ui.NTPShaderMenu,
    shader.ui.NTPShaderPanel,
]

modules = []
for parent_module in [compositor, geometry, shader]:
    if hasattr(parent_module, "modules"):
        modules += parent_module.modules
    else:
        raise Exception(f"Module {parent_module} does not have list of modules")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

    for module in modules:
        if hasattr(module, "classes"):
            for cls in getattr(module, "classes"):
                bpy.utils.register_class(cls)
        if hasattr(module, "register_props"):
            getattr(module, "register_props")()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregister_props()

    for module in modules:
        if hasattr(module, "classes"):
            for cls in getattr(module, "classes"):
                bpy.utils.unregister_class(cls)
        if hasattr(module, "unregister_props"):
            getattr(module, "unregister_props")()

if __name__ == "__main__":
    register()