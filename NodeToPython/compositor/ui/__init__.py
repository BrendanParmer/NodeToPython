if "bpy" in locals():
    import importlib
    importlib.reload(panel)
    importlib.reload(scenes)
    importlib.reload(compositor_node_groups)

else:
    from . import panel
    from . import scenes
    from . import compositor_node_groups

import bpy

classes: list[type] = []
classes += panel.classes
classes += scenes.classes
classes += compositor_node_groups.classes

def register_props():
    scenes.register_props()
    compositor_node_groups.register_props()

def unregister_props():
    scenes.unregister_props()
    compositor_node_groups.unregister_props()