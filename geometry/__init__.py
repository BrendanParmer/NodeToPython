if "bpy" in locals():
    import importlib
    importlib.reload(menu)
    importlib.reload(node_settings)
    importlib.reload(node_tree)
    importlib.reload(operator)
    importlib.reload(panel)
else:
    from . import menu
    from . import node_settings
    from . import node_tree
    from . import operator
    from . import panel

import bpy