if "bpy" in locals():
    import importlib
    importlib.reload(node_settings)
    importlib.reload(operator)
    importlib.reload(ui)
else:
    from . import node_settings
    from . import operator
    from . import ui

import bpy