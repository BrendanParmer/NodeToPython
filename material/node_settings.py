from ..utils import ST

shader_node_settings : dict[str, list[(str, ST)]] = {
    # INPUT
    'ShaderNodeAmbientOcclusion' : [("inside",     ST.BOOL),
                                    ("only_local", ST.BOOL),
                                    ("samples",    ST.INT)],

    'ShaderNodeAttribute'        : [("attribute_name", ST.STRING), #TODO: separate attribute type?
                                    ("attribute_type", ST.ENUM)],

    'ShaderNodeBevel'            : [("samples", ST.INT)],

    'ShaderNodeCameraData'       : [],

    'ShaderNodeVertexColor'      : [("layer_name", ST.STRING)], #TODO: separate color attribute type?

    'ShaderNodeHairInfo'         : [],

    'ShaderNodeFresnel'          : [],

    'ShaderNodeNewGeometry'      : [],

    'ShaderNodeLayerWeight'      : [],

    'ShaderNodeLightPath'        : [],

    'ShaderNodeObjectInfo'       : [],

    'ShaderNodeParticleInfo'     : [],

    'ShaderNodePointInfo'        : [],

    'ShaderNodeRGB'              : [],

    'ShaderNodeTangent'          : [("axis",           ST.ENUM),
                                    ("direction_type", ST.ENUM),
                                    ("uv_map",         ST.STRING)], #TODO: special UV Map type?

    'ShaderNodeTexCoord'         : [("from_instancer", ST.BOOL),
                                    ("object",         ST.OBJECT)],

    'ShaderNodeUVAlongStroke'     : [("use_tips", ST.BOOL)],

    'ShaderNodeUVMap'            : [("from_instancer", ST.BOOL), 
                                    ("uv_map",         ST.STRING)], #TODO: see ShaderNodeTangent

    'ShaderNodeValue'            : [],

    'ShaderNodeVolumeInfo'       : [],

    'ShaderNodeWireframe'        : [("use_pixel_size", ST.BOOL)],


    # OUTPUT
    'ShaderNodeOutputAOV'       : [("name", ST.STRING)],

    'ShaderNodeOutputLight'     : [("is_active_output", ST.BOOL),
                                   ("target",           ST.ENUM)],

    'ShaderNodeOutputLineStyle' : [("blend_type",       ST.ENUM),
                                   ("is_active_output", ST.BOOL),
                                   ("target",           ST.ENUM),
                                   ("use_alpha",        ST.BOOL),
                                   ("use_clamp",        ST.BOOL)],

    'ShaderNodeOutputMaterial'  : [("is_active_output", ST.BOOL),
                                   ("target",           ST.ENUM)],

    'ShaderNodeOutputWorld'     : [("is_active_output", ST.BOOL),
                                   ("target",           ST.ENUM)],


    # SHADER
    'ShaderNodeAddShader'            : [],

    'ShaderNodeBsdfAnisotropic'      : [("distribution", ST.ENUM)],

    'ShaderNodeBackground'           : [],

    'ShaderNodeBsdfDiffuse'          : [],

    'ShaderNodeEmission'             : [],

    'ShaderNodeBsdfGlass'            : [("distribution", ST.ENUM)],

    'ShaderNodeBsdfGlossy'           : [("distribution", ST.ENUM)],

    'ShaderNodeBsdfHair'             : [("component", ST.ENUM)],

    'ShaderNodeHoldout'              : [],

    'ShaderNodeMixShader'            : [],

    'ShaderNodeBsdfPrincipled'       : [("distribution",      ST.ENUM),
                                        ("subsurface_method", ST.ENUM)],

    'ShaderNodeBsdfHairPrincipled'   : [("parametrization", ST.ENUM)],

    'ShaderNodeVolumePrincipled'     : [],

    'ShaderNodeBsdfRefraction'       : [("distribution", ST.ENUM)],

    'ShaderNodeEeveeSpecular'        : [],

    'ShaderNodeSubsurfaceScattering' : [("falloff", ST.ENUM)],

    'ShaderNodeBsdfToon'             : [("component", ST.ENUM)],

    'ShaderNodeBsdfTranslucent'      : [],

    'ShaderNodeBsdfTransparent'      : [],

    'ShaderNodeBsdfVelvet'           : [],

    'ShaderNodeVolumeAbsorption'     : [],

    'ShaderNodeVolumeScatter'        : [],


    # TEXTURE
    'ShaderNodeTexBrick'        : [("offset",           ST.FLOAT), 
                                   ("offset_frequency", ST.INT),
                                   ("squash",           ST.FLOAT),
                                   ("squash_frequency", ST.INT)],

    'ShaderNodeTexChecker'      : [],

    'ShaderNodeTexEnvironment'  : [("image",         ST.IMAGE),
                                   ("image_user",    ST.IMAGE_USER),
                                   ("interpolation", ST.ENUM),
                                   ("projection",    ST.ENUM)],

    'ShaderNodeTexGradient'     : [("gradient_type", ST.ENUM)],

    'ShaderNodeTexIES'          : [("filepath", ST.STRING), #TODO
                                   ("ies",      ST.TEXT),
                                   ("mode",     ST.ENUM)],

    'ShaderNodeTexImage'        : [("extension",        ST.ENUM),
                                   ("image",            ST.IMAGE),
                                   ("image_user",       ST.IMAGE_USER),
                                   ("interpolation",    ST.ENUM),
                                   ("projection",       ST.ENUM),
                                   ("projection_blend", ST.FLOAT)],

    'ShaderNodeTexMagic'        : [("turbulence_depth", ST.INT)],

    'ShaderNodeTexMusgrave'     : [("musgrave_dimensions", ST.ENUM),
                                   ("musgrave_type",       ST.ENUM)],

    'ShaderNodeTexNoise'        : [("noise_dimensions", ST.ENUM)],

    'ShaderNodeTexPointDensity' : [("interpolation",         ST.ENUM),
                                   ("object",                ST.OBJECT),
                                   ("particle_color_source", ST.ENUM),
                                   ("particle_system",       ST.PARTICLE_SYSTEM),
                                   ("point_source",          ST.ENUM),
                                   ("radius",                ST.FLOAT),
                                   ("resolution",            ST.INT),
                                   ("space",                 ST.ENUM),
                                   ("vertex_attribute_name", ST.STRING), #TODO
                                   ("vertex_color_source",   ST.ENUM)],

    'ShaderNodeTexSky'          : [("air_density",   ST.FLOAT),
                                   ("altitude",      ST.FLOAT),
                                   ("dust_density",  ST.FLOAT),
                                   ("ground_albedo", ST.FLOAT),
                                   ("ozone_density", ST.FLOAT),
                                   ("sky_type",      ST.ENUM),
                                   ("sun_direction", ST.VEC3),
                                   ("sun_disc",      ST.BOOL),
                                   ("sun_elevation", ST.FLOAT),
                                   ("sun_intensity", ST.FLOAT),
                                   ("sun_rotation",  ST.FLOAT),
                                   ("sun_size",      ST.FLOAT),
                                   ("turbidity",     ST.FLOAT)],

    'ShaderNodeTexVoronoi'      : [("distance",           ST.ENUM),
                                   ("feature",            ST.ENUM),
                                   ("voronoi_dimensions", ST.ENUM)],

    'ShaderNodeTexWave'         : [("bands_direction", ST.ENUM),
                                   ("rings_direction", ST.ENUM),
                                   ("wave_profile",    ST.ENUM),
                                   ("wave_type",       ST.ENUM)],

    'ShaderNodeTexWhiteNoise'   : [("noise_dimensions", ST.ENUM)],


    # COLOR
    'ShaderNodeBrightContrast' : [],

    'ShaderNodeGamma'          : [],

    'ShaderNodeHueSaturation'  : [],

    'ShaderNodeInvert'         : [],

    'ShaderNodeLightFalloff'   : [],

    'ShaderNodeMix'            : [("blend_type",   ST.ENUM),
                                  ("clamp_factor", ST.BOOL),
                                  ("clamp_result", ST.BOOL),
                                  ("data_type",    ST.ENUM),
                                  ("factor_mode",  ST.ENUM)],

    'ShaderNodeRGBCurve'       : [("mapping", ST.CURVE_MAPPING)],


    # VECTOR
    'ShaderNodeBump'               : [("invert", ST.BOOL)],

    'ShaderNodeDisplacement'       : [("space", ST.ENUM)],

    'ShaderNodeMapping'            : [("vector_type", ST.ENUM)],

    'ShaderNodeNormal'             : [],

    'ShaderNodeNormalMap'          : [("space",  ST.ENUM),
                                      ("uv_map", ST.STRING)], #TODO

    'ShaderNodeVectorCurve'        : [("mapping", ST.CURVE_MAPPING)],

    'ShaderNodeVectorDisplacement' : [("space", ST.ENUM)],

    'ShaderNodeVectorRotate'       : [("invert",        ST.BOOL),
                                      ("rotation_type", ST.ENUM)],

    'ShaderNodeVectorTransform'    : [("convert_from", ST.ENUM),
                                      ("convert_to",   ST.ENUM),
                                      ("vector_type",  ST.ENUM)],
    

    # CONVERTER
    'ShaderNodeBlackbody'     : [],

    'ShaderNodeClamp'         : [("clamp_type", ST.ENUM)],

    'ShaderNodeValToRGB'      : [("color_ramp", ST.COLOR_RAMP)],

    'ShaderNodeCombineColor'  : [("mode", ST.ENUM)],

    'ShaderNodeCombineXYZ'    : [],

    'ShaderNodeFloatCurve'    : [("mapping", ST.CURVE_MAPPING)],

    'ShaderNodeMapRange'      : [("clamp",              ST.BOOL),
                                 ("data_type",          ST.ENUM),
                                 ("interpolation_type", ST.ENUM)],

    'ShaderNodeMath'          : [("operation", ST.ENUM), 
                                 ("use_clamp", ST.BOOL)],

    'ShaderNodeRGBToBW'       : [],

    'ShaderNodeSeparateColor' : [("mode", ST.ENUM)],

    'ShaderNodeSeparateXYZ'   : [],

    'ShaderNodeShaderToRGB'   : [],

    'ShaderNodeVectorMath'    : [("operation", ST.ENUM)],

    'ShaderNodeWavelength'    : [],


    # SCRIPT
    'ShaderNodeScript' : [("bytecode",        ST.STRING), #TODO: test all that
                          ("bytecode_hash",   ST.STRING),
                          ("filepath",        ST.STRING),
                          ("mode",            ST.ENUM),
                          ("script",          ST.TEXT),
                          ("use_auto_update", ST.BOOL)],

    # MISC
    'NodeFrame' : [],
    'NodeGroupInput' : [],
    'NodeGroupOutput' : [],
    'NodeReroute' : []
}
