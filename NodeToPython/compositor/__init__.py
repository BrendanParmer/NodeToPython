if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(ui)
else:
    from . import operator
    from . import ui

import bpy

modules = [
    operator
]
modules += ui.modules