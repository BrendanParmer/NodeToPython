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

modules : list = [
    panel,
    scenes,
    compositor_node_groups
]