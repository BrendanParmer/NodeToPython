if "bpy" in locals():
    import importlib
    importlib.reload(node_tree)
    importlib.reload(operator)
    importlib.reload(ui)
else:
    from . import node_tree
    from . import operator
    from . import ui

import bpy

modules = [
    node_tree,
    operator
]
modules += ui.modules