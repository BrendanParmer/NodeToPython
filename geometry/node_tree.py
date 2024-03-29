import bpy
from bpy.types import GeometryNodeTree

if bpy.app.version >= (3, 6, 0):
    from bpy.types import GeometryNodeSimulationInput

if bpy.app.version > (4, 0, 0):
    from bpy.types import GeometryNodeRepeatInput

from ..ntp_node_tree import NTP_NodeTree

class NTP_GeoNodeTree(NTP_NodeTree):
    def __init__(self, node_tree: GeometryNodeTree, var: str):
        super().__init__(node_tree, var)
        if bpy.app.version >= (3, 6, 0):
            self.sim_inputs: list[GeometryNodeSimulationInput] = []
        if bpy.app.version >= (4, 0, 0):
            self.repeat_inputs: list[GeometryNodeRepeatInput] = []
