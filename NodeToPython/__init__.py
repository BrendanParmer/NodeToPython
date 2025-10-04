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

# TODO: do away with this, separate out into more appropriate modules
classes: list[type] = [
    NodeToPythonMenu
]

modules = [options]
for parent_module in [compositor, geometry, shader]:
    if hasattr(parent_module, "modules"):
        modules += parent_module.modules
    else:
        raise Exception(f"Module {parent_module} does not have list of modules")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for module in modules:
        if hasattr(module, "classes"):
            for cls in getattr(module, "classes"):
                bpy.utils.register_class(cls)
        if hasattr(module, "register_props"):
            getattr(module, "register_props")()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for module in modules:
        if hasattr(module, "classes"):
            for cls in getattr(module, "classes"):
                bpy.utils.unregister_class(cls)
        if hasattr(module, "unregister_props"):
            getattr(module, "unregister_props")()

if __name__ == "__main__":
    register()