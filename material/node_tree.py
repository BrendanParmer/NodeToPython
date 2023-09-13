from bpy.types import ShaderNodeTree

class NTP_ShaderNodeTree: #TODO: these should derive from a single base class
    def __init__(self, node_tree: ShaderNodeTree, var_name: str):
        self.node_tree: ShaderNodeTree = node_tree 
        self.var_name: str = var_name

        self.inputs_set: bool = False
        self.outputs_set: bool = False