if "bpy" in locals():
    import importlib
    importlib.reload(panel)
    importlib.reload(materials)
    importlib.reload(shader_node_groups)
    importlib.reload(worlds)
    importlib.reload(line_styles)
    importlib.reload(lights)
else:
    from . import panel
    from . import materials
    from . import shader_node_groups
    from . import worlds
    from . import line_styles
    from . import lights

import bpy

modules : list = [
    panel,
    materials,
    shader_node_groups,
    worlds,
    line_styles,
    lights
]