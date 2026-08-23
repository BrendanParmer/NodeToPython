if "bpy" in locals():
    import importlib
    importlib.reload(license_templates)
    importlib.reload(node_group_gatherer)
    importlib.reload(node_settings)
    importlib.reload(node_tree_exporter)
    importlib.reload(ntp_operator)
    importlib.reload(ntp_options)
    importlib.reload(utils)
else:
    from . import license_templates
    from . import node_group_gatherer
    from . import node_settings
    from . import node_tree_exporter
    from . import ntp_operator
    from . import ntp_options
    from . import utils

import bpy

modules = [
    ntp_options,
    ntp_operator
]