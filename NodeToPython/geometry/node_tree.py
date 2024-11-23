import bpy
from bpy.types import GeometryNodeTree, GeometryNode

if bpy.app.version >= (3, 6, 0):
    from bpy.types import GeometryNodeSimulationInput

if bpy.app.version >= (4, 0, 0):
    from bpy.types import GeometryNodeRepeatInput

if bpy.app.version >= (4, 3, 0):
    from bpy.types import GeometryNodeForeachGeometryElementInput

from ..ntp_node_tree import NTP_NodeTree

class NTP_GeoNodeTree(NTP_NodeTree):
    def __init__(self, node_tree: GeometryNodeTree, var: str):
        super().__init__(node_tree, var)
        self.zone_inputs_: dict[list[GeometryNode]] = {}
        if bpy.app.version >= (3, 6, 0):
            self.zone_inputs_["GeometryNodeSimulationInput"] = []
        if bpy.app.version >= (4, 0, 0):
            self.zone_inputs_["GeometryNodeRepeatInput"] = []
        if bpy.app.version >= (4, 3, 0):
            self.zone_inputs_["GeometryNodeForeachGeometryElementInput"] = []
