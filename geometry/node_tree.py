from bpy.types import GeometryNodeTree, GeometryNodeSimulationInput

from ..ntp_node_tree import NTP_NodeTree

class NTP_GeoNodeTree(NTP_NodeTree):
    def __init__(self, node_tree: GeometryNodeTree, var: str):
        super().__init__(node_tree, var)
        self.sim_inputs: list[GeometryNodeSimulationInput] = []
