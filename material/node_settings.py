from ..utils import ST, NTPNodeSetting

shader_node_settings : dict[str, list[NTPNodeSetting]] = {
    # INPUT
    'ShaderNodeAmbientOcclusion' : [
        NTPNodeSetting("inside",     ST.BOOL),
        NTPNodeSetting("only_local", ST.BOOL),
        NTPNodeSetting("samples",    ST.INT)
    ],

    'ShaderNodeAttribute' : [
        NTPNodeSetting("attribute_name", ST.STRING), #TODO: separate attribute type?
        NTPNodeSetting("attribute_type", ST.ENUM)
    ],

    'ShaderNodeBevel' : [
        NTPNodeSetting("samples", ST.INT)
    ],

    'ShaderNodeCameraData' : [],

    'ShaderNodeVertexColor' : [
        NTPNodeSetting("layer_name", ST.STRING) #TODO: separate color attribute type?
    ],

    'ShaderNodeHairInfo'     : [],
    'ShaderNodeFresnel'      : [],
    'ShaderNodeNewGeometry'  : [],
    'ShaderNodeLayerWeight'  : [],
    'ShaderNodeLightPath'    : [],
    'ShaderNodeObjectInfo'   : [],
    'ShaderNodeParticleInfo' : [],
    'ShaderNodePointInfo'    : [],
    'ShaderNodeRGB'          : [],

    'ShaderNodeTangent' : [
        NTPNodeSetting("axis",           ST.ENUM),
        NTPNodeSetting("direction_type", ST.ENUM),
        NTPNodeSetting("uv_map",         ST.STRING) #TODO: special UV Map type?
    ],

    'ShaderNodeTexCoord' : [
        NTPNodeSetting("from_instancer", ST.BOOL),
        NTPNodeSetting("object",         ST.OBJECT)
    ],

    'ShaderNodeUVAlongStroke' : [
        NTPNodeSetting("use_tips", ST.BOOL)
    ],

    'ShaderNodeUVMap' : [
        NTPNodeSetting("from_instancer", ST.BOOL), 
        NTPNodeSetting("uv_map",         ST.STRING)
    ], #TODO: see ShaderNodeTangent

    'ShaderNodeValue'      : [],
    'ShaderNodeVolumeInfo' : [],

    'ShaderNodeWireframe' : [
        NTPNodeSetting("use_pixel_size", ST.BOOL)
    ],


    # OUTPUT
    'ShaderNodeOutputAOV' : [
        NTPNodeSetting("name", ST.STRING)
    ],

    'ShaderNodeOutputLight' : [
        NTPNodeSetting("is_active_output", ST.BOOL),
        NTPNodeSetting("target",           ST.ENUM)
    ],

    'ShaderNodeOutputLineStyle' : [
        NTPNodeSetting("blend_type",       ST.ENUM),
        NTPNodeSetting("is_active_output", ST.BOOL),
        NTPNodeSetting("target",           ST.ENUM),
        NTPNodeSetting("use_alpha",        ST.BOOL),
        NTPNodeSetting("use_clamp",        ST.BOOL)
    ],

    'ShaderNodeOutputMaterial' : [
        NTPNodeSetting("is_active_output", ST.BOOL),
        NTPNodeSetting("target",           ST.ENUM)
    ],

    'ShaderNodeOutputWorld' : [
        NTPNodeSetting("is_active_output", ST.BOOL),
        NTPNodeSetting("target",           ST.ENUM)
    ],


    # SHADER
    'ShaderNodeAddShader' : [],

    'ShaderNodeBsdfAnisotropic' : [
        NTPNodeSetting("distribution", ST.ENUM)
    ],

    'ShaderNodeBackground'  : [],
    'ShaderNodeBsdfDiffuse' : [],
    'ShaderNodeEmission'    : [],

    'ShaderNodeBsdfGlass' : [
        NTPNodeSetting("distribution", ST.ENUM)
    ],

    'ShaderNodeBsdfGlossy' : [
        NTPNodeSetting("distribution", ST.ENUM)
    ],

    'ShaderNodeBsdfHair' : [
        NTPNodeSetting("component", ST.ENUM)
    ],

    'ShaderNodeHoldout'   : [],
    'ShaderNodeMixShader' : [],

    'ShaderNodeBsdfPrincipled' : [
        NTPNodeSetting("distribution",      ST.ENUM),
        NTPNodeSetting("subsurface_method", ST.ENUM)
    ],

    'ShaderNodeBsdfHairPrincipled' : [
        NTPNodeSetting("model",           ST.ENUM),
        NTPNodeSetting("parametrization", ST.ENUM)
    ],

    'ShaderNodeVolumePrincipled' : [],

    'ShaderNodeBsdfRefraction' : [
        NTPNodeSetting("distribution", ST.ENUM)
    ],

    'ShaderNodeBsdfSheen' : [
        NTPNodeSetting("distribution", ST.ENUM, min_version = (4, 0, 0))
    ],

    'ShaderNodeEeveeSpecular' : [],

    'ShaderNodeSubsurfaceScattering' : [
        NTPNodeSetting("falloff", ST.ENUM)
    ],

    'ShaderNodeBsdfToon' : [
        NTPNodeSetting("component", ST.ENUM)
    ],

    'ShaderNodeBsdfTranslucent'  : [],
    'ShaderNodeBsdfTransparent'  : [],
    'ShaderNodeBsdfVelvet'       : [],
    'ShaderNodeVolumeAbsorption' : [],
    'ShaderNodeVolumeScatter'    : [],


    # TEXTURE
    'ShaderNodeTexBrick' : [
        NTPNodeSetting("offset",           ST.FLOAT), 
        NTPNodeSetting("offset_frequency", ST.INT),
        NTPNodeSetting("squash",           ST.FLOAT),
        NTPNodeSetting("squash_frequency", ST.INT)
    ],

    'ShaderNodeTexChecker' : [],

    'ShaderNodeTexEnvironment'  : [
        NTPNodeSetting("image",         ST.IMAGE),
        NTPNodeSetting("image_user",    ST.IMAGE_USER),
        NTPNodeSetting("interpolation", ST.ENUM),
        NTPNodeSetting("projection",    ST.ENUM)
    ],

    'ShaderNodeTexGradient' : [
        NTPNodeSetting("gradient_type", ST.ENUM)
    ],

    'ShaderNodeTexIES' : [
        NTPNodeSetting("filepath", ST.STRING), #TODO
        NTPNodeSetting("ies",      ST.TEXT),
        NTPNodeSetting("mode",     ST.ENUM)
    ],

    'ShaderNodeTexImage' : [
        NTPNodeSetting("extension",        ST.ENUM),
        NTPNodeSetting("image",            ST.IMAGE),
        NTPNodeSetting("image_user",       ST.IMAGE_USER),
        NTPNodeSetting("interpolation",    ST.ENUM),
        NTPNodeSetting("projection",       ST.ENUM),
        NTPNodeSetting("projection_blend", ST.FLOAT)
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

    'ShaderNodeTexPointDensity' : [
        NTPNodeSetting("interpolation",         ST.ENUM),
        NTPNodeSetting("object",                ST.OBJECT),
        NTPNodeSetting("particle_color_source", ST.ENUM),
        NTPNodeSetting("particle_system",       ST.PARTICLE_SYSTEM),
        NTPNodeSetting("point_source",          ST.ENUM),
        NTPNodeSetting("radius",                ST.FLOAT),
        NTPNodeSetting("resolution",            ST.INT),
        NTPNodeSetting("space",                 ST.ENUM),
        NTPNodeSetting("vertex_attribute_name", ST.STRING), #TODO
        NTPNodeSetting("vertex_color_source",   ST.ENUM)
    ],

    'ShaderNodeTexSky' : [
        NTPNodeSetting("air_density",   ST.FLOAT),
        NTPNodeSetting("altitude",      ST.FLOAT),
        NTPNodeSetting("dust_density",  ST.FLOAT),
        NTPNodeSetting("ground_albedo", ST.FLOAT),
        NTPNodeSetting("ozone_density", ST.FLOAT),
        NTPNodeSetting("sky_type",      ST.ENUM),
        NTPNodeSetting("sun_direction", ST.VEC3),
        NTPNodeSetting("sun_disc",      ST.BOOL),
        NTPNodeSetting("sun_elevation", ST.FLOAT),
        NTPNodeSetting("sun_intensity", ST.FLOAT),
        NTPNodeSetting("sun_rotation",  ST.FLOAT),
        NTPNodeSetting("sun_size",      ST.FLOAT),
        NTPNodeSetting("turbidity",     ST.FLOAT)
    ],

    'ShaderNodeTexVoronoi' : [
        NTPNodeSetting("distance",           ST.ENUM),
        NTPNodeSetting("feature",            ST.ENUM),
        NTPNodeSetting("normalize",          ST.BOOL, min_version = (4, 0, 0)),
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


    # COLOR
    'ShaderNodeBrightContrast' : [],
    'ShaderNodeGamma'          : [],
    'ShaderNodeHueSaturation'  : [],
    'ShaderNodeInvert'         : [],
    'ShaderNodeLightFalloff'   : [],

    'ShaderNodeMix' : [
        NTPNodeSetting("blend_type",   ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("clamp_factor", ST.BOOL, min_version = (3, 4, 0)),
        NTPNodeSetting("clamp_result", ST.BOOL, min_version = (3, 4, 0)),
        NTPNodeSetting("data_type",    ST.ENUM, min_version = (3, 4, 0)),
        NTPNodeSetting("factor_mode",  ST.ENUM, min_version = (3, 4, 0))
    ],

    'ShaderNodeMixRGB' : [
        NTPNodeSetting("blend_type", ST.ENUM),
        NTPNodeSetting("use_alpha",  ST.BOOL),
        NTPNodeSetting("use_clamp",  ST.BOOL)
    ],

    'ShaderNodeRGBCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],


    # VECTOR
    'ShaderNodeBump' : [
        NTPNodeSetting("invert", ST.BOOL)
    ],

    'ShaderNodeDisplacement' : [
        NTPNodeSetting("space", ST.ENUM)
    ],

    'ShaderNodeMapping' : [
        NTPNodeSetting("vector_type", ST.ENUM)
    ],

    'ShaderNodeNormal' : [],

    'ShaderNodeNormalMap' : [
        NTPNodeSetting("space",  ST.ENUM),
        NTPNodeSetting("uv_map", ST.STRING) #TODO
    ],

    'ShaderNodeVectorCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'ShaderNodeVectorDisplacement' : [
        NTPNodeSetting("space", ST.ENUM)
    ],

    'ShaderNodeVectorRotate' : [
        NTPNodeSetting("invert",        ST.BOOL),
        NTPNodeSetting("rotation_type", ST.ENUM)
    ],

    'ShaderNodeVectorTransform' : [
        NTPNodeSetting("convert_from", ST.ENUM),
        NTPNodeSetting("convert_to",   ST.ENUM),
        NTPNodeSetting("vector_type",  ST.ENUM)
    ],
    

    # CONVERTER
    'ShaderNodeBlackbody' : [],

    'ShaderNodeClamp' : [
        NTPNodeSetting("clamp_type", ST.ENUM)
    ],

    'ShaderNodeValToRGB' : [
        NTPNodeSetting("color_ramp", ST.COLOR_RAMP)
    ],

    'ShaderNodeCombineColor' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'ShaderNodeCombineXYZ' : [],

    'ShaderNodeFloatCurve' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
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

    'ShaderNodeRGBToBW' : [],

    'ShaderNodeSeparateColor' : [
        NTPNodeSetting("mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'ShaderNodeSeparateXYZ' : [],
    'ShaderNodeShaderToRGB' : [],

    'ShaderNodeVectorMath' : [
        NTPNodeSetting("operation", ST.ENUM)
    ],

    'ShaderNodeWavelength' : [],


    # SCRIPT
    'ShaderNodeScript' : [
        NTPNodeSetting("bytecode",        ST.STRING), #TODO: test all that
        NTPNodeSetting("bytecode_hash",   ST.STRING),
        NTPNodeSetting("filepath",        ST.STRING),
        NTPNodeSetting("mode",            ST.ENUM),
        NTPNodeSetting("script",          ST.TEXT),
        NTPNodeSetting("use_auto_update", ST.BOOL)
    ],

    # MISC
    'ShaderNodeGroup' : [
        NTPNodeSetting('node_tree', ST.NODE_TREE)
    ],

    'NodeFrame' : [
        NTPNodeSetting("label_size", ST.INT),
        NTPNodeSetting("shrink", ST.BOOL),
        NTPNodeSetting("text", ST.TEXT)
    ],

    'NodeGroupInput' : [],

    'NodeGroupOutput' : [
        NTPNodeSetting("is_active_output", ST.BOOL)
    ],

    'NodeReroute' : []
}
