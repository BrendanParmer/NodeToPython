from ..utils import ST

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
    'GeometryNodeTool3DCursor'   : [],

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
    'GeometryNodeToolSelection'       : [],

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
    'GeometryNodeSetID'            : [],
    'GeometryNodeSetPosition'      : [],
    'GeometryNodeToolSetSelection' : [],

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
    'GeometryNodeToolFaceSet'              : [],
    'GeometryNodeMeshFaceSetBoundaries'    : [],
    'GeometryNodeInputMeshFaceIsPlanar'    : [],
    'GeometryNodeInputShadeSmooth'         : [],
    'GeometryNodeInputEdgeSmooth'          : [],
    'GeometryNodeInputMeshIsland'          : [],
    'GeometryNodeInputShortestEdgePaths'   : [],
    'GeometryNodeInputMeshVertexNeighbors' : [],

    # Mesh > Sample
    'GeometryNodeSampleNearestSurface' : [("data_type", ST.ENUM)],

    'GeometryNodeSampleUVSurface'      : [("data_type", ST.ENUM)],

    # Mesh > Write
    'GeometryNodeToolSetFaceSet' : [],
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
    'GeometryNodePointsToCurves'           : [],
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

    'GeometryNodeRepeatInput'  : [],
    'GeometryNodeRepeatOutput' : [],

    'GeometryNodeSwitch' : [("input_type", ST.ENUM)],
    
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
    'FunctionNodeAlignEulerToVector'    : [("axis",       ST.ENUM),
                                           ("pivot_axis", ST.ENUM)],

    'FunctionNodeAxisAngleToRotation'   : [],
    'FunctionNodeEulerToRotation'       : [],
    'FunctionNodeInvertRotation'        : [],
                                        
    'FunctionNodeRotateEuler'           : [("space", ST.ENUM),
                                           ("type",  ST.ENUM)],

    'FunctionNodeRotateVector'          : [],
    'FunctionNodeRotationToAxisAngle'   : [],
    'FunctionNodeRotationToEuler'       : [],
    'FunctionNodeRotationToQuaternion'  : [],
    'FunctionNodeQuaternionToRotation'  : [],

    # MISC
    'NodeFrame'       : [("label_size", ST.INT),
                         ("shrink", ST.BOOL),
                         ("text", ST.TEXT)],

    'NodeGroupInput'  : [],

    'NodeGroupOutput' : [("is_active_output", ST.BOOL)],

    'NodeReroute'     : []

}