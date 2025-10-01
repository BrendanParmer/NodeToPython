if "bpy" in locals():
    import importlib
    importlib.reload(panel)
    importlib.reload(geometry_node_groups)
else:
    from . import panel
    from . import geometry_node_groups

import bpy

modules = [panel, geometry_node_groups]