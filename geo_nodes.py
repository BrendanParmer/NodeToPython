import bpy
import os

from .utils import *
from io import StringIO

geo_node_settings : dict[str, list[(str, ST)]] = {
    # ATTRIBUTE
    'GeometryNodeAttributeStatistic'  : [("data_type", ST.ENUM), 
                                         ("domain",    ST.ENUM)],

    'GeometryNodeAttributeDomainSize' : [("component", ST.ENUM)],

    'GeometryNodeBlurAttribute'       : [("data_type", ST.ENUM)],

    'GeometryNodeCaptureAttribute'    : [("data_type", ST.ENUM),
                                         ("domain",    ST.ENUM)],

    'GeometryNodeRemoveAttribute'     : [],

    'GeometryNodeStoreNamedAttribute' : [("data_type", ST.ENUM),
                                         ("domain",    ST.ENUM)],

    'GeometryNodeAttributeTransfer'   : [("data_type", ST.ENUM),
                                         ("domain",    ST.ENUM),
                                         ("mapping",   ST.ENUM)],

    # INPUT
    # Input > Constant
    'FunctionNodeInputBool'     : [("boolean",  ST.BOOL)],

    'FunctionNodeInputColor'    : [("color", ST.VEC4)],

    'GeometryNodeInputImage'    : [("image", ST.IMAGE)],

    'FunctionNodeInputInt'      : [("integer", ST.INT)],

    'GeometryNodeInputMaterial' : [("material", ST.MATERIAL)],

    'FunctionNodeInputString'   : [("string", ST.STRING)],

    'ShaderNodeValue'           : [],

    'FunctionNodeInputVector'   : [("vector", ST.VEC3)],

    #Input > Group
    'NodeGroupInput' : [],
    
    # Input > Scene
    'GeometryNodeCollectionInfo' : [("transform_space", ST.ENUM)],

    'GeometryNodeImageInfo'      : [],

    'GeometryNodeIsViewport'     : [],

    'GeometryNodeObjectInfo'     : [("transform_space", ST.ENUM)],

    'GeometryNodeSelfObject'     : [],

    'GeometryNodeInputSceneTime' : [],


    # OUTPUT
    'GeometryNodeViewer'         : [("data_type", ST.ENUM),

                                    ("domain",    ST.ENUM)],


    # GEOMETRY
    'GeometryNodeJoinGeometry'       : [],

    'GeometryNodeGeometryToInstance' : [],

    # Geometry > Read
    'GeometryNodeInputID'             : [],

    'GeometryNodeInputIndex'          : [],

    'GeometryNodeInputNamedAttribute' : [("data_type", ST.ENUM)],

    'GeometryNodeInputNormal'         : [],

    'GeometryNodeInputPosition'       : [],

    'GeometryNodeInputRadius'         : [],

    # Geometry > Sample
    'GeometryNodeProximity'      : [("target_element", ST.ENUM)],

    'GeometryNodeIndexOfNearest' : [],

    'GeometryNodeRaycast'        : [("data_type", ST.ENUM),
                                    ("mapping",   ST.ENUM)],

    'GeometryNodeSampleIndex'    : [("clamp",     ST.BOOL),
                                    ("data_type", ST.ENUM),
                                    ("domain",    ST.ENUM)],

    'GeometryNodeSampleNearest'  : [("domain", ST.ENUM)],

    # Geometry > Write
    'GeometryNodeSetID'       : [],

    'GeometryNodeSetPosition' : [],

    # Geometry > Operations
    'GeometryNodeBoundBox'           : [],

    'GeometryNodeConvexHull'         : [],

    'GeometryNodeDeleteGeometry'     : [("domain", ST.ENUM),
                                        ("mode",   ST.ENUM)],

    'GeometryNodeDuplicateElements'  : [("domain", ST.ENUM)],

    'GeometryNodeMergeByDistance'    : [("mode",   ST.ENUM)],

    'GeometryNodeTransform'          : [],

    'GeometryNodeSeparateComponents' : [],

    'GeometryNodeSeparateGeometry'   : [("domain", ST.ENUM)],


    # CURVE
    # Curve > Read
    'GeometryNodeInputCurveHandlePositions' : [],

    'GeometryNodeCurveLength'               : [],

    'GeometryNodeInputTangent'              : [],

    'GeometryNodeInputCurveTilt'            : [],

    'GeometryNodeCurveEndpointSelection'    : [],

    'GeometryNodeCurveHandleTypeSelection'  : [("handle_type", ST.ENUM),
                                               ("mode",        ST.ENUM_SET)],

    'GeometryNodeInputSplineCyclic'         : [],

    'GeometryNodeSplineLength'              : [],

    'GeometryNodeSplineParameter'           : [],

    'GeometryNodeInputSplineResolution'     : [],

    # Curve > Sample
    'GeometryNodeSampleCurve' : [("data_type",      ST.ENUM),
                                 ("mode",           ST.ENUM),
                                 ("use_all_curves", ST.BOOL)],

    # Curve > Write
    'GeometryNodeSetCurveNormal'          : [("mode", ST.ENUM)],

    'GeometryNodeSetCurveRadius'          : [],

    'GeometryNodeSetCurveTilt'            : [],

    'GeometryNodeSetCurveHandlePositions' : [("mode", ST.ENUM)],

    'GeometryNodeCurveSetHandles'         : [("handle_type", ST.ENUM),
                                             ("mode",        ST.ENUM_SET)],

    'GeometryNodeSetSplineCyclic'         : [],

    'GeometryNodeSetSplineResolution'     : [],

    'GeometryNodeCurveSplineType'         : [("spline_type", ST.ENUM)],

    # Curve > Operations
    'GeometryNodeCurveToMesh'           : [],

    'GeometryNodeCurveToPoints'         : [("mode", ST.ENUM)],

    'GeometryNodeDeformCurvesOnSurface' : [],

    'GeometryNodeFillCurve'             : [("mode", ST.ENUM)],

    'GeometryNodeFilletCurve'           : [("mode", ST.ENUM)],

    'GeometryNodeInterpolateCurves'     : [],

    'GeometryNodeResampleCurve'         : [("mode", ST.ENUM)],

    'GeometryNodeReverseCurve'          : [],

    'GeometryNodeSubdivideCurve'        : [],

    'GeometryNodeTrimCurve'             : [("mode", ST.ENUM)],

    # Curve > Primitives
    'GeometryNodeCurveArc'                    : [("mode", ST.ENUM)],

    'GeometryNodeCurvePrimitiveBezierSegment' : [("mode", ST.ENUM)],

    'GeometryNodeCurvePrimitiveCircle'        : [("mode", ST.ENUM)],

    'GeometryNodeCurvePrimitiveLine'          : [("mode", ST.ENUM)],

    'GeometryNodeCurveSpiral'                 : [],

    'GeometryNodeCurveQuadraticBezier'        : [],

    'GeometryNodeCurvePrimitiveQuadrilateral' : [("mode", ST.ENUM)],

    'GeometryNodeCurveStar'                   : [],

    # Curve > Topology
    'GeometryNodeOffsetPointInCurve' : [],

    'GeometryNodeCurveOfPoint'       : [],

    'GeometryNodePointsOfCurve'      : [],


    # INSTANCES
    'GeometryNodeInstanceOnPoints'      : [],

    'GeometryNodeInstancesToPoints'     : [],

    'GeometryNodeRealizeInstances'      : [("legacy_behavior", ST.BOOL)],

    'GeometryNodeRotateInstances'       : [],

    'GeometryNodeScaleInstances'        : [],

    'GeometryNodeTranslateInstances'    : [],

    'GeometryNodeInputInstanceRotation' : [],

    'GeometryNodeInputInstanceScale'    : [],


    # MESH
    # Mesh > Read
    'GeometryNodeInputMeshEdgeAngle'       : [],

    'GeometryNodeInputMeshEdgeNeighbors'   : [],
    
    'GeometryNodeInputMeshEdgeVertices'    : [],

    'GeometryNodeEdgesToFaceGroups'        : [],

    'GeometryNodeInputMeshFaceArea'        : [],

    'GeometryNodeInputMeshFaceNeighbors'   : [],

    'GeometryNodeMeshFaceSetBoundaries'    : [],

    'GeometryNodeInputMeshFaceIsPlanar'    : [],

    'GeometryNodeInputShadeSmooth'         : [],

    'GeometryNodeInputMeshIsland'          : [],

    'GeometryNodeInputShortestEdgePaths'   : [],

    'GeometryNodeInputMeshVertexNeighbors' : [],

    # Mesh > Sample
    'GeometryNodeSampleNearestSurface' : [("data_type", ST.ENUM)],

    'GeometryNodeSampleUVSurface'      : [("data_type", ST.ENUM)],

    # Mesh > Write
    'GeometryNodeSetShadeSmooth' : [],

    # Mesh > Operations
    'GeometryNodeDualMesh'             : [],

    'GeometryNodeEdgePathsToCurves'    : [],

    'GeometryNodeEdgePathsToSelection' : [],

    'GeometryNodeExtrudeMesh'          : [("mode", ST.ENUM)],

    'GeometryNodeFlipFaces'            : [],

    'GeometryNodeMeshBoolean'          : [("operation", ST.ENUM)],

    'GeometryNodeMeshToCurve'          : [],

    'GeometryNodeMeshToPoints'         : [("mode", ST.ENUM)],

    'GeometryNodeMeshToVolume'         : [("resolution_mode", ST.ENUM)],

    'GeometryNodeScaleElements'        : [("domain",     ST.ENUM),
                                          ("scale_mode", ST.ENUM)],

    'GeometryNodeSplitEdges'           : [],

    'GeometryNodeSubdivideMesh'        : [],

    'GeometryNodeSubdivisionSurface'   : [("boundary_smooth", ST.ENUM),
                                          ("uv_smooth",       ST.ENUM)],

    'GeometryNodeTriangulate'          : [("ngon_method", ST.ENUM),
                                          ("quad_method", ST.ENUM)],

    # Mesh > Primitives
    'GeometryNodeMeshCone'      : [("fill_type", ST.ENUM)],

    'GeometryNodeMeshCube'      : [],

    'GeometryNodeMeshCylinder'  : [("fill_type", ST.ENUM)],

    'GeometryNodeMeshGrid'      : [],

    'GeometryNodeMeshIcoSphere' : [],

    'GeometryNodeMeshCircle'    : [("fill_type", ST.ENUM)],

    'GeometryNodeMeshLine'      : [("count_mode", ST.ENUM),
                                   ("mode",       ST.ENUM)],

    'GeometryNodeMeshUVSphere'  : [],

    # Mesh > Topology
    'GeometryNodeCornersOfFace'      : [],

    'GeometryNodeCornersOfVertex'    : [],

    'GeometryNodeEdgesOfCorner'      : [],

    'GeometryNodeEdgesOfVertex'      : [],

    'GeometryNodeFaceOfCorner'       : [],

    'GeometryNodeOffsetCornerInFace' : [],

    'GeometryNodeVertexOfCorner'     : [],

    # Mesh > UV
    'GeometryNodeUVPackIslands' : [],

    'GeometryNodeUVUnwrap'      : [("method", ST.ENUM)],


    # POINT
    'GeometryNodeDistributePointsInVolume' : [("mode", ST.ENUM)],

    'GeometryNodeDistributePointsOnFaces'  : [("distribute_method", ST.ENUM),
                                              ("use_legacy_normal", ST.BOOL)],

    'GeometryNodePoints'                   : [],

    'GeometryNodePointsToVertices'         : [],

    'GeometryNodePointsToVolume'           : [("resolution_mode", ST.ENUM)],

    'GeometryNodeSetPointRadius'           : [],


    # VOLUME
    'GeometryNodeVolumeCube'   : [],

    'GeometryNodeVolumeToMesh' : [("resolution_mode", ST.ENUM)],

    
    # SIMULATION
    'GeometryNodeSimulationInput'  : [],

    'GeometryNodeSimulationOutput' : [],


    # MATERIAL
    'GeometryNodeReplaceMaterial'    : [],

    'GeometryNodeInputMaterialIndex' : [],

    'GeometryNodeMaterialSelection'  : [],

    'GeometryNodeSetMaterial'        : [],

    'GeometryNodeSetMaterialIndex'   : [],


    # TEXTURE
    'ShaderNodeTexBrick'       : [("offset",           ST.FLOAT),
                                  ("offset_frequency", ST.INT),
                                  ("squash",           ST.FLOAT), 
                                  ("squash_frequency", ST.INT)],

    'ShaderNodeTexChecker'     : [],

    'ShaderNodeTexGradient'    : [("gradient_type", ST.ENUM)],

    'GeometryNodeImageTexture' : [("extension",     ST.ENUM),
                                  ("interpolation", ST.ENUM)],

    'ShaderNodeTexMagic'       : [("turbulence_depth", ST.INT)],

    'ShaderNodeTexMusgrave'    : [("musgrave_dimensions", ST.ENUM),
                                  ("musgrave_type",       ST.ENUM)],

    'ShaderNodeTexNoise'       : [("noise_dimensions", ST.ENUM)],

    'ShaderNodeTexVoronoi'     : [("distance",           ST.ENUM),
                                  ("feature",            ST.ENUM),
                                  ("voronoi_dimensions", ST.ENUM)],

    'ShaderNodeTexWave'        : [("bands_direction", ST.ENUM),
                                  ("rings_direction", ST.ENUM),
                                  ("wave_profile",    ST.ENUM),
                                  ("wave_type",       ST.ENUM)],

    'ShaderNodeTexWhiteNoise'  : [("noise_dimensions", ST.ENUM)],


    # UTILITIES
    'ShaderNodeMix'           : [("blend_type",   ST.ENUM),
                                 ("clamp_factor", ST.BOOL),
                                 ("clamp_result", ST.BOOL),
                                 ("data_type",    ST.ENUM),
                                 ("factor_mode",  ST.ENUM)],

    'FunctionNodeRandomValue' : [("data_type", ST.ENUM)],

    'GeometryNodeSwitch'      : [("input_type", ST.ENUM)],
    
    # Utilities > Color
    'ShaderNodeValToRGB'        : [("color_ramp", ST.COLOR_RAMP)],

    'ShaderNodeRGBCurve'        : [("mapping", ST.CURVE_MAPPING)],

    'FunctionNodeCombineColor'  : [("mode", ST.ENUM)],

    'ShaderNodeMixRGB'          : [("blend_type", ST.ENUM),
                                   ("use_alpha",  ST.BOOL),
                                   ("use_clamp",  ST.BOOL)], #legacy

    'FunctionNodeSeparateColor' : [("mode", ST.ENUM)],
    
    # Utilities > Text
    'GeometryNodeStringJoin'             : [],

    'FunctionNodeReplaceString'          : [],

    'FunctionNodeSliceString'            : [],

    'FunctionNodeStringLength'           : [],

    'GeometryNodeStringToCurves'         : [("align_x",    ST.ENUM),
                                            ("align_y",    ST.ENUM),
                                            ("font",       ST.FONT),
                                            ("overflow",   ST.ENUM),
                                            ("pivot_mode", ST.ENUM)],

    'FunctionNodeValueToString'          : [],

    'FunctionNodeInputSpecialCharacters' : [],

    # Utilities > Vector
    'ShaderNodeVectorCurve'  : [("mapping", ST.CURVE_MAPPING)],

    'ShaderNodeVectorMath'   : [("operation", ST.ENUM)],

    'ShaderNodeVectorRotate' : [("invert",        ST.BOOL),
                                ("rotation_type", ST.ENUM)],

    'ShaderNodeCombineXYZ'   : [],

    'ShaderNodeSeparateXYZ'  : [],

    # Utilities > Field
    'GeometryNodeAccumulateField' : [("data_type", ST.ENUM),
                                     ("domain",    ST.ENUM)],

    'GeometryNodeFieldAtIndex'    : [("data_type", ST.ENUM),
                                     ("domain",    ST.ENUM)],

    'GeometryNodeFieldOnDomain'   : [("data_type", ST.ENUM),
                                     ("domain",    ST.ENUM)],

    # Utilities > Math
    'FunctionNodeBooleanMath' : [("operation", ST.ENUM)],

    'ShaderNodeClamp'         : [("clamp_type", ST.ENUM)],

    'FunctionNodeCompare'     : [("data_type", ST.ENUM),
                                 ("mode",      ST.ENUM),
                                 ("operation", ST.ENUM)],

    'ShaderNodeFloatCurve'    : [("mapping", ST.CURVE_MAPPING)],

    'FunctionNodeFloatToInt'  : [("rounding_mode", ST.ENUM)],

    'ShaderNodeMapRange'      : [("clamp",              ST.BOOL),
                                 ("data_type",          ST.ENUM),
                                 ("interpolation_type", ST.ENUM)],

    'ShaderNodeMath'          : [("operation", ST.ENUM),
                                 ("use_clamp", ST.BOOL)],

    # Utilities > Rotation
    'FunctionNodeAlignEulerToVector' : [("axis",       ST.ENUM),
                                        ("pivot_axis", ST.ENUM)],
                                        
    'FunctionNodeRotateEuler'        : [("space", ST.ENUM),
                                        ("type",  ST.ENUM)]
}

class NTP_GeoNodeTree:
    def __init__(self, node_tree: bpy.types.GeometryNodeTree, var_name: str):
        self.node_tree: bpy.types.GeometryNodeTree = node_tree 
        self.var_name: str = var_name

        self.inputs_set: bool = False
        self.outputs_set: bool = False
        self.sim_inputs: list[bpy.types.GeometryNodeSimulationInput] = []

class NTP_GeoNode:
    def __init__(self, node: bpy.types.GeometryNode, var_name: str):
        self.node = node
        self.var_name = var_name

class NTPGeoNodesOperator(bpy.types.Operator):
    bl_idname = "node.ntp_geo_nodes"
    bl_label = "Geo Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON',  "Addon", "Create a full addon")
        ]
    )

    geo_nodes_group_name: bpy.props.StringProperty(name="Node Group")
    
    def __init__(self):
        # File/string the add-on/script is generated into
        self._file: TextIO = None

        # Path to the directory of the zip file
        self._zip_dir: str = None

        # Path to the directory for the generated addon
        self._addon_dir: str = None

        # Set to keep track of already created node trees
        self._node_trees: set[bpy.types.NodeTree] = set()

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[bpy.types.Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}
    
    def _setup_addon_directories(self, context: bpy.types.Context, nt_var: str):
        #find base directory to save new addon
        dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
        if not dir or dir == "":
            self.report({'ERROR'}, 
                        ("NodeToPython: Save your blend file before using "
                         "NodeToPython!")) #TODO: Still valid??
            return {'CANCELLED'}

        self._zip_dir = os.path.join(dir, nt_var)
        self._addon_dir = os.path.join(self._zip_dir, nt_var)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)

    def _process_geo_node_group_node(self, node: bpy.types.GeometryNodeGroup, 
                                     level: int, inner: str, node_var: str
                                    ) -> None:
        nt = node.node_tree
        if nt is not None:
            if nt not in self._node_trees:
                self._process_geo_node_tree(nt, level + 1)
            self._file.write((f"{inner}{node_var}.node_tree = "
                                      f"bpy.data.node_groups"
                                      f"[{str_to_py_str(nt.name)}]\n"))
    
    def _process_sim_output_node(self, node: bpy.types.GeometryNodeSimulationOutput,
                                 inner: str, node_var: str) -> None:
        self._file.write(f"{inner}# Remove generated sim state items\n")
        self._file.write(f"{inner}for item in {node_var}.state_items:\n")
        self._file.write(f"{inner}\t{node_var}.state_items.remove(item)\n")

        for i, si in enumerate(node.state_items):
            socket_type = enum_to_py_str(si.socket_type)
            name = str_to_py_str(si.name)
            self._file.write(f"{inner}#create SSI {name}\n")
            self._file.write((f"{inner}{node_var}.state_items.new"
                              f"({socket_type}, {name})\n"))
            si_var = f"{node_var}.state_items[{i}]"
            attr_domain = enum_to_py_str(si.attribute_domain)
            self._file.write((f"{inner}{si_var}.attribute_domain "
                              f"= {attr_domain}\n"))

    def _set_socket_defaults(self, node: bpy.types.GeometryNode, inner: str,
                             node_var: str) -> None:
        if self.mode == 'ADDON':
            set_input_defaults(node, self._file, inner, node_var, self._addon_dir)
        else:
            set_input_defaults(node, self._file, inner, node_var)
        set_output_defaults(node, self._file, inner, node_var)

    def _process_node(self, node: bpy.types.GeometryNode,
                      ntp_node_tree: NTP_GeoNodeTree,
                      inner: str, level: int) -> None:
        #create node
        node_var: str = create_node(node, self._file, inner, ntp_node_tree.var_name, 
                                    self._node_vars, self._used_vars)
        set_settings_defaults(node, geo_node_settings, self._file, 
                                self._addon_dir, inner, node_var)
        if node.bl_idname == 'GeometryNodeGroup':
            self._process_geo_node_group_node(node, level, inner, node_var)

        elif node.bl_idname == 'NodeGroupInput' and not ntp_node_tree.inputs_set:
            group_io_settings(node, self._file, inner, "input", ntp_node_tree.var_name, 
                              ntp_node_tree.node_tree) #TODO: convert to using NTP_NodeTrees
            ntp_node_tree.inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not ntp_node_tree.outputs_set:
            group_io_settings(node, self._file, inner, "output", 
                              ntp_node_tree.var_name, ntp_node_tree.node_tree)
            ntp_node_tree.outputs_set = True

        elif node.bl_idname == 'GeometryNodeSimulationInput':
            ntp_node_tree.sim_inputs.append(node)

        elif node.bl_idname == 'GeometryNodeSimulationOutput':
            self._process_sim_output_node(node, inner, node_var)
        
        hide_hidden_sockets(node, self._file, inner, node_var)

        if node.bl_idname != 'GeometryNodeSimulationInput':
            self._set_socket_defaults(node, inner, node_var)

    def _process_sim_zones(self, sim_inputs: list[bpy.types.GeometryNodeSimulationInput], 
                           inner: str) -> None:
        """
        Recreate simulation zones
        sim_inputs (list[bpy.types.GeometryNodeSimulationInput]): list of 
            simulation input nodes
        inner (str): identation string
        """
        for sim_input in sim_inputs:
            sim_output = sim_input.paired_output

            sim_input_var = self._node_vars[sim_input]
            sim_output_var = self._node_vars[sim_output]
            self._file.write((f"{inner}{sim_input_var}.pair_with_output"
                              f"({sim_output_var})\n"))

            #must set defaults after paired with output
            self._set_socket_defaults(sim_input, inner, sim_input_var)
            self._set_socket_defaults(sim_output, inner, sim_output_var)

    def _process_geo_node_tree(self, node_tree: bpy.types.GeometryNodeTree, 
                               level: int) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (bpy.types.NodeTree): geometry node tree to be recreated
        level (int): number of tabs to use for each line, used with
            node groups within node groups and script/add-on differences
        """
        
        nt_var = create_var(node_tree.name, self._used_vars)    
        outer, inner = make_indents(level) #TODO: put in NTP_NodeTree class?

        #initialize node group
        self._file.write(f"{outer}#initialize {nt_var} node group\n")
        self._file.write(f"{outer}def {nt_var}_node_group():\n")
        self._file.write((f"{inner}{nt_var} = bpy.data.node_groups.new("
                          f"type = \'GeometryNodeTree\', "
                          f"name = {str_to_py_str(node_tree.name)})\n"))
        self._file.write("\n")

        #initialize nodes
        self._file.write(f"{inner}#initialize {nt_var} nodes\n")

        ntp_nt = NTP_GeoNodeTree(node_tree, nt_var)
        for node in node_tree.nodes:
            self._process_node(node, ntp_nt, inner, level)

        self._process_sim_zones(ntp_nt.sim_inputs, inner)
        
        #set look of nodes
        set_parents(node_tree, self._file, inner, self._node_vars)
        set_locations(node_tree, self._file, inner, self._node_vars)
        set_dimensions(node_tree, self._file, inner, self._node_vars)

        #create connections
        init_links(node_tree, self._file, inner, nt_var, self._node_vars)
        
        self._file.write(f"{inner}return {nt_var}\n")

        #create node group
        self._file.write(f"\n{outer}{nt_var} = {nt_var}_node_group()\n\n")
        return self._used_vars

    def _apply_modifier(self, nt: bpy.types.GeometryNodeTree, nt_var: str):
        #get object
        self._file.write(f"\t\tname = bpy.context.object.name\n")
        self._file.write(f"\t\tobj = bpy.data.objects[name]\n")

        #set modifier to the one we just created
        mod_name = str_to_py_str(nt.name)
        self._file.write((f"\t\tmod = obj.modifiers.new(name = {mod_name}, "
                    f"type = 'NODES')\n"))
        self._file.write(f"\t\tmod.node_group = {nt_var}\n")

    def _report_finished(self):
        #alert user that NTP is finished
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = dir
        self.report({'INFO'}, 
                    f"NodeToPython: Saved geometry nodes group to {location}")

    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            self._setup_addon_directories(context, nt_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")
            
            create_header(self._file, nt.name)
            class_name = clean_string(nt.name.replace(" ", "").replace('.', ""), 
                                      lower = False) #TODO: should probably be standardized name to class name util method
            init_operator(self._file, class_name, nt_var, nt.name)
            self._file.write("\tdef execute(self, context):\n")
        else:
            self._file = StringIO("")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0
        self._process_geo_node_tree(nt, level)

        if self.mode == 'ADDON':
            self._apply_modifier(nt, nt_var)
            self._file.write("\t\treturn {'FINISHED'}\n\n")
            create_menu_func(self._file, class_name)
            create_register_func(self._file, class_name)
            create_unregister_func(self._file, class_name)
            create_main_func(self._file)
        else:
            context.window_manager.clipboard = self._file.getvalue()
        self._file.close()

        if self.mode == 'ADDON':
            zip_addon(self._zip_dir)

        self._report_finished()

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")
    
class NTPGeoNodesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_geo_nodes"
    bl_label = "Select Geo Nodes"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'

        geo_node_groups = [node for node in bpy.data.node_groups 
                           if node.type == 'GEOMETRY']

        for geo_ng in geo_node_groups:
            op = layout.operator(NTPGeoNodesOperator.bl_idname, text=geo_ng.name)
            op.geo_nodes_group_name = geo_ng.name
            
class NTPGeoNodesPanel(bpy.types.Panel):
    bl_label = "Geometry Nodes to Python"
    bl_idname = "NODE_PT_geo_nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        
        # Disables menu when len of geometry nodes is 0
        geo_node_groups = [node 
                            for node in bpy.data.node_groups 
                            if node.type == 'GEOMETRY']
        geo_node_groups_exist = len(geo_node_groups) > 0
        row.enabled = geo_node_groups_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_ntp_geo_nodes", text="Geometry Nodes")