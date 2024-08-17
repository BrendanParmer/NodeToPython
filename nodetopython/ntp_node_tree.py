from bpy.types import NodeTree
import bpy

class NTP_NodeTree:
    def __init__(self, node_tree: NodeTree, var: str):
        # Blender node tree object being copied
        self.node_tree: NodeTree = node_tree

        # The variable named for the regenerated node tree
        self.var: str = var

        if bpy.app.version < (4, 0, 0):
            # Keep track of if we need to set the default values for the node
            # tree inputs and outputs
            self.inputs_set: bool = False
            self.outputs_set: bool = False