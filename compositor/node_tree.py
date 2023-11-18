from bpy.types import CompositorNodeTree

from ..NTP_NodeTree import NTP_NodeTree

class NTP_CompositorNodeTree(NTP_NodeTree):
    def __init__(self, node_tree: CompositorNodeTree, var: str):
        super().__init__(node_tree, var)