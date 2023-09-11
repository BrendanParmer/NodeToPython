from bpy.types import GeometryNodeTree, GeometryNodeSimulationInput

class NTP_GeoNodeTree:
    def __init__(self, node_tree: GeometryNodeTree, var_name: str):
        self.node_tree: GeometryNodeTree = node_tree 
        self.var_name: str = var_name

        self.inputs_set: bool = False
        self.outputs_set: bool = False
        self.sim_inputs: list[GeometryNodeSimulationInput] = []