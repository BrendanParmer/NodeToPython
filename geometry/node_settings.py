from ..utils import ST, NTPNodeSetting

geo_node_settings : dict[str, list[NTPNodeSetting]] = {
    # ATTRIBUTE
    'GeometryNodeAttributeStatistic' : [
        NTPNodeSetting("data_type", ST.ENUM), 
        NTPNodeSetting("domain",    ST.ENUM)
    ],

    'GeometryNodeAttributeDomainSize' : [
        NTPNodeSetting("component", ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeBlurAttribute' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 5, 0))
    ],

    'GeometryNodeCaptureAttribute' : [
        NTPNodeSetting("data_type", ST.ENUM),
        NTPNodeSetting("domain",    ST.ENUM)
    ],

    'GeometryNodeRemoveAttribute' : [],

    'GeometryNodeStoreNamedAttribute' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 2, 0)),
        NTPNodeSetting("domain",    ST.ENUM, min_version = (3, 2, 0))
    ],

    'GeometryNodeAttributeTransfer' : [
        NTPNodeSetting("data_type", ST.ENUM),
        NTPNodeSetting("domain",    ST.ENUM),
        NTPNodeSetting("mapping",   ST.ENUM)
    ],

    # INPUT
    # Input > Constant
    'FunctionNodeInputBool' : [
        NTPNodeSetting("boolean",  ST.BOOL)
    ],

    'FunctionNodeInputColor' : [
        NTPNodeSetting("color", ST.VEC4)
    ],

    'GeometryNodeInputImage' : [
        NTPNodeSetting("image", ST.IMAGE, min_version = (3, 5, 0))
    ],

    'FunctionNodeInputInt' : [
        NTPNodeSetting("integer", ST.INT)
    ],

    'GeometryNodeInputMaterial' : [
        NTPNodeSetting("material", ST.MATERIAL)
    ],

    'FunctionNodeInputString' : [
        NTPNodeSetting("string", ST.STRING)
    ],

    'ShaderNodeValue' : [],

    'FunctionNodeInputVector' : [
        NTPNodeSetting("vector", ST.VEC3)
    ],

    #Input > Group
    'NodeGroupInput' : [],
    
    # Input > Scene
    'GeometryNodeTool3DCursor' : [],

    'GeometryNodeInputActiveCamera' : [],
    
    'GeometryNodeCollectionInfo' : [
        NTPNodeSetting("transform_space", ST.ENUM)
    ],

    'GeometryNodeImageInfo' : [],
    'GeometryNodeIsViewport' : [],

    'GeometryNodeObjectInfo' : [
        NTPNodeSetting("transform_space", ST.ENUM)
    ],

    'GeometryNodeSelfObject' : [],
    'GeometryNodeInputSceneTime' : [],


    # OUTPUT
    'GeometryNodeViewer'  : [
        NTPNodeSetting("data_type", ST.ENUM),
        NTPNodeSetting("domain",    ST.ENUM, min_version = (3, 4, 0))
    ],


    # GEOMETRY
    'GeometryNodeJoinGeometry' : [],
    'GeometryNodeGeometryToInstance' : [],

    # Geometry > Read
    'GeometryNodeInputID' : [],
    'GeometryNodeInputIndex' : [],

    'GeometryNodeInputNamedAttribute' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 2, 0))
    ],

    'GeometryNodeInputNormal' : [],
    'GeometryNodeInputPosition' : [],
    'GeometryNodeInputRadius' : [],
    'GeometryNodeToolSelection' : [],

    # Geometry > Sample
    'GeometryNodeProximity' : [
        NTPNodeSetting("target_element", ST.ENUM)
    ],

    'GeometryNodeIndexOfNearest' : [],

    'GeometryNodeRaycast' : [
        NTPNodeSetting("data_type", ST.ENUM),
        NTPNodeSetting("mapping",   ST.ENUM)
    ],

    'GeometryNodeSampleIndex' : [
        NTPNodeSetting("clamp",     ST.BOOL, min_version = (3, 4, 0)),
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("domain",    ST.ENUM, min_version = (3, 4, 0))
    ],

    'GeometryNodeSampleNearest' : [
        NTPNodeSetting("domain", ST.ENUM, min_version = (3, 4, 0))
    ],

    # Geometry > Write
    'GeometryNodeSetID' : [],
    'GeometryNodeSetPosition' : [],
    'GeometryNodeToolSetSelection' : [],

    # Geometry > Operations
    'GeometryNodeBake' : [
        NTPNodeSetting("bake_items", ST.BAKE_ITEMS, min_version = (4, 1, 0))
    ],

    'GeometryNodeBoundBox' : [],
    'GeometryNodeConvexHull' : [],

    'GeometryNodeDeleteGeometry' : [
        NTPNodeSetting("domain", ST.ENUM),
        NTPNodeSetting("mode",   ST.ENUM)
    ],

    'GeometryNodeDuplicateElements' : [
        NTPNodeSetting("domain", ST.ENUM, min_version = (3, 2, 0))
    ],

    'GeometryNodeMergeByDistance' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeSortElements' : [
        NTPNodeSetting("domain", ST.ENUM, min_version = (4, 1, 0))
    ],

    'GeometryNodeTransform' : [],
    'GeometryNodeSeparateComponents' : [],

    'GeometryNodeSeparateGeometry' : [
        NTPNodeSetting("domain", ST.ENUM)
    ],


    # CURVE
    # Curve > Read
    'GeometryNodeInputCurveHandlePositions' : [],
    'GeometryNodeCurveLength' : [],
    'GeometryNodeInputTangent' : [],
    'GeometryNodeInputCurveTilt' : [],
    'GeometryNodeCurveEndpointSelection' : [],

    'GeometryNodeCurveHandleTypeSelection' : [
        NTPNodeSetting("handle_type", ST.ENUM),
        NTPNodeSetting("mode",        ST.ENUM_SET)
    ],

    'GeometryNodeInputSplineCyclic' : [],
    'GeometryNodeSplineLength' : [],
    'GeometryNodeSplineParameter' : [],
    'GeometryNodeInputSplineResolution' : [],

    # Curve > Sample
    'GeometryNodeSampleCurve' : [
        NTPNodeSetting("data_type",      ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("mode",           ST.ENUM),
        NTPNodeSetting("use_all_curves", ST.BOOL, min_version = (3, 4, 0))
    ],

    # Curve > Write
    'GeometryNodeSetCurveNormal' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 4, 0))
    ],

    'GeometryNodeSetCurveRadius' : [],
    'GeometryNodeSetCurveTilt' : [],

    'GeometryNodeSetCurveHandlePositions' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeCurveSetHandles' : [
        NTPNodeSetting("handle_type", ST.ENUM),
        NTPNodeSetting("mode",        ST.ENUM_SET)
    ],

    'GeometryNodeSetSplineCyclic' : [],
    'GeometryNodeSetSplineResolution' : [],

    'GeometryNodeCurveSplineType' : [
        NTPNodeSetting("spline_type", ST.ENUM)
    ],

    # Curve > Operations
    'GeometryNodeCurveToMesh' : [],

    'GeometryNodeCurveToPoints' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeDeformCurvesOnSurface' : [],

    'GeometryNodeFillCurve' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeFilletCurve' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeInterpolateCurves' : [],

    'GeometryNodeResampleCurve' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeReverseCurve' : [],
    'GeometryNodeSubdivideCurve' : [],

    'GeometryNodeTrimCurve' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    # Curve > Primitives
    'GeometryNodeCurveArc' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeCurvePrimitiveBezierSegment' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeCurvePrimitiveCircle' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeCurvePrimitiveLine' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeCurveSpiral' : [],
    'GeometryNodeCurveQuadraticBezier' : [],

    'GeometryNodeCurvePrimitiveQuadrilateral' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeCurveStar' : [],

    # Curve > Topology
    'GeometryNodeOffsetPointInCurve' : [],
    'GeometryNodeCurveOfPoint'       : [],
    'GeometryNodePointsOfCurve'      : [],


    # INSTANCES
    'GeometryNodeInstanceOnPoints' : [],
    'GeometryNodeInstancesToPoints' : [],

    'GeometryNodeRealizeInstances' : [
        NTPNodeSetting("legacy_behavior", ST.BOOL, min_version = (3, 1, 0), 
                                                   max_version = (4, 0, 0))
    ],

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
    'GeometryNodeSampleNearestSurface' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 4, 0))
    ],

    'GeometryNodeSampleUVSurface' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 4, 0))
    ],

    # Mesh > Write
    'GeometryNodeToolSetFaceSet' : [],

    'GeometryNodeSetShadeSmooth' : [
        NTPNodeSetting("domain", ST.ENUM, min_version = (4, 0, 0))
    ],

    # Mesh > Operations
    'GeometryNodeDualMesh'             : [],
    'GeometryNodeEdgePathsToCurves'    : [],
    'GeometryNodeEdgePathsToSelection' : [],

    'GeometryNodeExtrudeMesh' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeFlipFaces' : [],

    'GeometryNodeMeshBoolean' : [
        NTPNodeSetting("operation", ST.ENUM)
    ],

    'GeometryNodeMeshToCurve' : [],

    'GeometryNodeMeshToPoints' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'GeometryNodeMeshToVolume' : [
        NTPNodeSetting("resolution_mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'GeometryNodeScaleElements' : [
        NTPNodeSetting("domain",     ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("scale_mode", ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeSplitEdges'    : [],
    'GeometryNodeSubdivideMesh' : [],

    'GeometryNodeSubdivisionSurface' : [
        NTPNodeSetting("boundary_smooth", ST.ENUM),
        NTPNodeSetting("uv_smooth",       ST.ENUM)
    ],

    'GeometryNodeTriangulate' : [
        NTPNodeSetting("ngon_method", ST.ENUM),
        NTPNodeSetting("quad_method", ST.ENUM)
    ],

    # Mesh > Primitives
    'GeometryNodeMeshCone' : [
        NTPNodeSetting("fill_type", ST.ENUM)
    ],

    'GeometryNodeMeshCube' : [],

    'GeometryNodeMeshCylinder' : [
        NTPNodeSetting("fill_type", ST.ENUM)
    ],

    'GeometryNodeMeshGrid'      : [],
    'GeometryNodeMeshIcoSphere' : [],

    'GeometryNodeMeshCircle' : [
        NTPNodeSetting("fill_type", ST.ENUM)
    ],

    'GeometryNodeMeshLine' : [
        NTPNodeSetting("count_mode", ST.ENUM),
        NTPNodeSetting("mode",       ST.ENUM)
    ],

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

    'GeometryNodeUVUnwrap': [
        NTPNodeSetting("method", ST.ENUM, min_version = (3, 3, 0))
    ],


    # POINT
    'GeometryNodeDistributePointsInVolume' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 4, 0))
    ],

    'GeometryNodeDistributePointsOnFaces' : [
        NTPNodeSetting("distribute_method", ST.ENUM),
        NTPNodeSetting("use_legacy_normal", ST.BOOL, min_version = (3, 5, 0))
    ],

    'GeometryNodePoints'           : [],
    'GeometryNodePointsToCurves'   : [],
    'GeometryNodePointsToVertices' : [],

    'GeometryNodePointsToVolume' : [
        NTPNodeSetting("resolution_mode", ST.ENUM)
    ],

    'GeometryNodeSetPointRadius' : [],


    # VOLUME
    'GeometryNodeVolumeCube'   : [],
    'GeometryNodeVolumeToMesh' : [
        NTPNodeSetting("resolution_mode", ST.ENUM)
    ],

    
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
    'ShaderNodeTexBrick' : [
        NTPNodeSetting("offset",           ST.FLOAT),
        NTPNodeSetting("offset_frequency", ST.INT),
        NTPNodeSetting("squash",           ST.FLOAT), 
        NTPNodeSetting("squash_frequency", ST.INT)
    ],

    'ShaderNodeTexChecker' : [],

    'ShaderNodeTexGradient' : [
        NTPNodeSetting("gradient_type", ST.ENUM)
    ],

    'GeometryNodeImageTexture' : [
        NTPNodeSetting("extension",     ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("interpolation", ST.ENUM, min_version = (3, 1, 0))
    ],

    'ShaderNodeTexMagic' : [
        NTPNodeSetting("turbulence_depth", ST.INT)
    ],

    'ShaderNodeTexMusgrave' : [
        NTPNodeSetting("musgrave_dimensions", ST.ENUM, max_version = (4, 1, 0)),
        NTPNodeSetting("musgrave_type",       ST.ENUM, max_version = (4, 1, 0))
    ],

    'ShaderNodeTexNoise' : [
        NTPNodeSetting("noise_dimensions", ST.ENUM),
        NTPNodeSetting("noise_type",       ST.ENUM, min_version=(4, 1, 0)),
        NTPNodeSetting("normalize",        ST.BOOL, min_version=(4, 0, 0)),
    ],

    'ShaderNodeTexVoronoi' : [
        NTPNodeSetting("distance",           ST.ENUM),
        NTPNodeSetting("feature",            ST.ENUM),
        NTPNodeSetting("voronoi_dimensions", ST.ENUM)
    ],

    'ShaderNodeTexWave' : [
        NTPNodeSetting("bands_direction", ST.ENUM),
        NTPNodeSetting("rings_direction", ST.ENUM),
        NTPNodeSetting("wave_profile",    ST.ENUM),
        NTPNodeSetting("wave_type",       ST.ENUM)
    ],

    'ShaderNodeTexWhiteNoise' : [
        NTPNodeSetting("noise_dimensions", ST.ENUM)
    ],


    # UTILITIES
    'GeometryNodeIndexSwitch' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (4, 1, 0)),
        NTPNodeSetting("index_switch_items", ST.INDEX_SWITCH_ITEMS, min_version = (4, 1, 0))
    ],

    'GeometryNodeMenuSwitch' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (4, 1, 0)),
        NTPNodeSetting("enum_definition", ST.ENUM_DEFINITION, min_version = (4, 1, 0))
    ],

    'ShaderNodeMix' : [
        NTPNodeSetting("blend_type",   ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("clamp_factor", ST.BOOL, min_version = (3, 4, 0)),
        NTPNodeSetting("clamp_result", ST.BOOL, min_version = (3, 4, 0)),
        NTPNodeSetting("data_type",    ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("factor_mode",  ST.ENUM, min_version = (3, 4, 0))
    ],

    'FunctionNodeRandomValue' : [
        NTPNodeSetting("data_type", ST.ENUM)
    ],

    'GeometryNodeRepeatInput' : [],

    'GeometryNodeRepeatOutput' : [
        NTPNodeSetting("inspection_index", ST.INT, min_version = (4, 0, 0))
    ],

    'GeometryNodeSwitch' : [
        NTPNodeSetting("input_type", ST.ENUM)
    ],
    
    # Utilities > Color
    'ShaderNodeValToRGB' : [
        NTPNodeSetting("color_ramp", ST.COLOR_RAMP)
    ],

    'ShaderNodeRGBCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'FunctionNodeCombineColor' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'ShaderNodeMixRGB' : [
        NTPNodeSetting("blend_type", ST.ENUM),
        NTPNodeSetting("use_alpha",  ST.BOOL),
        NTPNodeSetting("use_clamp",  ST.BOOL)
    ], #legacy

    'FunctionNodeSeparateColor' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 3, 0))
    ],
    
    # Utilities > Text
    'GeometryNodeStringJoin'    : [],
    'FunctionNodeReplaceString' : [],
    'FunctionNodeSliceString'   : [],
    'FunctionNodeStringLength'  : [],

    'GeometryNodeStringToCurves' : [
        NTPNodeSetting("align_x",    ST.ENUM),
        NTPNodeSetting("align_y",    ST.ENUM),
        NTPNodeSetting("font",       ST.FONT),
        NTPNodeSetting("overflow",   ST.ENUM),
        NTPNodeSetting("pivot_mode", ST.ENUM, min_version = (3, 1, 0))
    ],

    'FunctionNodeValueToString'          : [],
    'FunctionNodeInputSpecialCharacters' : [],

    # Utilities > Vector
    'ShaderNodeVectorCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'ShaderNodeVectorMath' : [
        NTPNodeSetting("operation", ST.ENUM)
    ],

    'ShaderNodeVectorRotate' : [
        NTPNodeSetting("invert",        ST.BOOL),
        NTPNodeSetting("rotation_type", ST.ENUM)
    ],

    'ShaderNodeCombineXYZ'  : [],
    'ShaderNodeSeparateXYZ' : [],

    # Utilities > Field
    'GeometryNodeAccumulateField' : [
        NTPNodeSetting("data_type", ST.ENUM),
        NTPNodeSetting("domain",    ST.ENUM)
    ],

    'GeometryNodeFieldAtIndex' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("domain",    ST.ENUM, min_version = (3, 1, 0))
    ],

    'GeometryNodeFieldOnDomain' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 3, 0)),
        NTPNodeSetting("domain",    ST.ENUM, min_version = (3, 3, 0))
    ],

    # Utilities > Math
    'FunctionNodeBooleanMath' : [
        NTPNodeSetting("operation", ST.ENUM)
    ],

    'ShaderNodeClamp' : [
        NTPNodeSetting("clamp_type", ST.ENUM)
    ],

    'FunctionNodeCompare' : [
        NTPNodeSetting("data_type", ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("mode",      ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("operation", ST.ENUM, min_version = (3, 1, 0))
    ],

    'FunctionNodeCompareFloats' : [
        NTPNodeSetting("operation", ST.ENUM, max_version = (3, 2, 0))
    ],

    'ShaderNodeFloatCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'FunctionNodeFloatToInt' : [
        NTPNodeSetting("rounding_mode", ST.ENUM)
    ],

    'ShaderNodeMapRange' : [
        NTPNodeSetting("clamp",              ST.BOOL),
        NTPNodeSetting("data_type",          ST.ENUM, min_version = (3, 1, 0)),
        NTPNodeSetting("interpolation_type", ST.ENUM)
    ],

    'ShaderNodeMath' : [
        NTPNodeSetting("operation", ST.ENUM),
        NTPNodeSetting("use_clamp", ST.BOOL)
    ],

    # Utilities > Rotation
    'FunctionNodeAlignEulerToVector' : [
        NTPNodeSetting("axis",       ST.ENUM),
        NTPNodeSetting("pivot_axis", ST.ENUM)
    ],

    'FunctionNodeAxisAngleToRotation' : [],
    'FunctionNodeEulerToRotation'     : [],
    'FunctionNodeInvertRotation'      : [],

    'FunctionNodeRotateRotation' : [
        NTPNodeSetting("rotation_space", ST.ENUM, min_version = (4, 1, 0))
    ],

    'FunctionNodeRotateEuler' : [
        NTPNodeSetting("rotation_type", ST.ENUM, min_version = (4, 1, 0)),
        NTPNodeSetting("space", ST.ENUM),
        NTPNodeSetting("type",  ST.ENUM, max_version = (4, 1, 0))
    ],

    'FunctionNodeRotateVector'          : [],
    'FunctionNodeRotationToAxisAngle'   : [],
    'FunctionNodeRotationToEuler'       : [],
    'FunctionNodeRotationToQuaternion'  : [],
    'FunctionNodeQuaternionToRotation'  : [],

    # MISC
    'GeometryNodeGroup' : [
        NTPNodeSetting("node_tree", ST.NODE_TREE)
    ],

    'NodeFrame' : [
        NTPNodeSetting("label_size", ST.INT),
        NTPNodeSetting("shrink", ST.BOOL),
        NTPNodeSetting("text", ST.TEXT)
    ],

    'NodeGroupInput'  : [],

    'NodeGroupOutput' : [
        NTPNodeSetting("is_active_output", ST.BOOL)
    ],

    'NodeReroute'     : []

}