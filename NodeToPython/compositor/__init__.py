if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(ui)
else:
    from . import operator
    from . import ui

import bpy

classes: list[type] = []
classes += operator.classes
classes += ui.classes

def register_props():
    ui.register_props()

def unregister_props():
    ui.unregister_props()