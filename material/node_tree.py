from ..NTP_NodeTree import NTP_NodeTree
from bpy.types import ShaderNodeTree

class NTP_ShaderNodeTree(NTP_NodeTree):
    def __init__(self, node_tree: ShaderNodeTree, var: str):
        super().__init__(node_tree, var)