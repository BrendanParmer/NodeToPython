from bpy.types import NodeTree

class NTP_NodeTree:
    def __init__(self, node_tree: NodeTree, var: str):
        # Blender node tree object being copied
        self.node_tree: NodeTree = node_tree

        # The variable named for the regenerated node tree
        self.var: str = var

        # Keep track of if we need to set the default values for the node
        # tree inputs and outputs
        self.inputs_set: bool = False
        self.outputs_set: bool = False