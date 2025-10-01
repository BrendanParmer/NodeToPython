if "bpy" in locals():
    import importlib
    importlib.reload(panel)
    importlib.reload(materials)
    importlib.reload(shader_node_groups)
else:
    from . import panel
    from . import materials
    from . import shader_node_groups

import bpy

modules : list = [
    panel,
    materials,
    shader_node_groups
]