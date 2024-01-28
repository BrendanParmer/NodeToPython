from ..utils import ST, NTPNodeSetting

compositor_node_settings : dict[str, list[NTPNodeSetting]] = {
    # INPUT
    'CompositorNodeBokehImage' : [
        NTPNodeSetting("angle",        ST.FLOAT),
        NTPNodeSetting("catadioptric", ST.FLOAT),
        NTPNodeSetting("flaps",        ST.INT),
        NTPNodeSetting("rounding",     ST.FLOAT),
        NTPNodeSetting("shift",        ST.FLOAT)
    ],

    'CompositorNodeImage' : [
        NTPNodeSetting("frame_duration",            ST.INT),
        NTPNodeSetting("frame_offset",              ST.INT),
        NTPNodeSetting("frame_start",               ST.INT),
        NTPNodeSetting("image",                     ST.IMAGE),
        NTPNodeSetting("layer",                     ST.ENUM),
        NTPNodeSetting("use_auto_refresh",          ST.BOOL),
        NTPNodeSetting("use_cyclic",                ST.BOOL),
        NTPNodeSetting("use_straight_alpha_output", ST.BOOL),
        NTPNodeSetting("view",                      ST.ENUM)
    ],

    'CompositorNodeMask' : [
        NTPNodeSetting("mask",                ST.MASK),
        NTPNodeSetting("motion_blur_samples", ST.INT),
        NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
        NTPNodeSetting("size_source",         ST.ENUM),
        NTPNodeSetting("size_x",              ST.INT),
        NTPNodeSetting("size_y",              ST.INT),
        NTPNodeSetting("use_feather",         ST.BOOL),
        NTPNodeSetting("use_motion_blur",     ST.BOOL)
    ],

    'CompositorNodeMovieClip' : [
        NTPNodeSetting("clip", ST.MOVIE_CLIP)
    ],

    'CompositorNodeTexture' : [
        NTPNodeSetting("node_output", ST.INT), #TODO: ??
        NTPNodeSetting("texture",     ST.TEXTURE)
    ],

    # Input > Constant
    'CompositorNodeRGB' : [],
    'CompositorNodeValue' : [],

    # Input > Scene
    'CompositorNodeRLayers' : [
        NTPNodeSetting("layer", ST.ENUM),
        NTPNodeSetting("scene", ST.SCENE)
    ],

    'CompositorNodeSceneTime' : [],

    'CompositorNodeTime' : [
        NTPNodeSetting("curve",       ST.CURVE_MAPPING),
        NTPNodeSetting("frame_end",   ST.INT),
        NTPNodeSetting("frame_start", ST.INT)
    ],


    # OUTPUT
    'CompositorNodeComposite' : [
        NTPNodeSetting("use_alpha", ST.BOOL)
    ],

    'CompositorNodeOutputFile'  : [
        NTPNodeSetting("active_input_index", ST.INT), #TODO: probably not right at all
        NTPNodeSetting("base_path",          ST.STRING),
        NTPNodeSetting("file_slots",         ST.FILE_SLOTS),
        NTPNodeSetting("format",             ST.IMAGE_FORMAT_SETTINGS),
        NTPNodeSetting("layer_slots",        ST.LAYER_SLOTS)
    ],

    'CompositorNodeViewer' : [
        NTPNodeSetting("center_x",   ST.FLOAT),
        NTPNodeSetting("center_y",   ST.FLOAT),
        NTPNodeSetting("tile_order", ST.ENUM),
        NTPNodeSetting("use_alpha",  ST.BOOL)
    ],    
    
    'CompositorNodeSplitViewer' : [
        NTPNodeSetting("axis",   ST.ENUM),
        NTPNodeSetting("factor", ST.INT)
    ],


    # COLOR
    'CompositorNodePremulKey' : [
        NTPNodeSetting("mapping", ST.ENUM)
    ],

    'CompositorNodeValToRGB' : [
        NTPNodeSetting("color_ramp", ST.COLOR_RAMP)
    ],

    'CompositorNodeConvertColorSpace' : [
        NTPNodeSetting("from_color_space", ST.ENUM, min_version=(3, 1, 0)),
        NTPNodeSetting("to_color_space",   ST.ENUM, min_version=(3, 1, 0))
    ],

    'CompositorNodeSetAlpha' : [
        NTPNodeSetting("mode", ST.ENUM)
    ],

    'CompositorNodeInvert' : [
        NTPNodeSetting("invert_alpha", ST.BOOL),
        NTPNodeSetting("invert_rgb",   ST.BOOL)
    ],

    'CompositorNodeRGBToBW' : [],

    # Color > Adjust
    'CompositorNodeBrightContrast' : [
        NTPNodeSetting("use_premultiply", ST.BOOL)
    ],

    'CompositorNodeColorBalance' : [
        NTPNodeSetting("correction_method", ST.ENUM),
        NTPNodeSetting("gain",              ST.COLOR),
        NTPNodeSetting("gamma",             ST.COLOR),
        NTPNodeSetting("lift",              ST.COLOR),
        NTPNodeSetting("offset",            ST.COLOR),
        NTPNodeSetting("offset_basis",      ST.FLOAT),
        NTPNodeSetting("power",             ST.COLOR),
        NTPNodeSetting("slope",             ST.COLOR)
    ],

    'CompositorNodeColorCorrection' : [
        NTPNodeSetting("red",   ST.BOOL),
        NTPNodeSetting("green", ST.BOOL),
        NTPNodeSetting("blue",  ST.BOOL),
        #master
        NTPNodeSetting("master_saturation", ST.FLOAT),
        NTPNodeSetting("master_contrast",   ST.FLOAT),
        NTPNodeSetting("master_gamma",      ST.FLOAT),
        NTPNodeSetting("master_gain",       ST.FLOAT),
        NTPNodeSetting("master_lift",       ST.FLOAT),
        #highlights
        NTPNodeSetting("highlights_saturation", ST.FLOAT),
        NTPNodeSetting("highlights_contrast",   ST.FLOAT),
        NTPNodeSetting("highlights_gamma",      ST.FLOAT),
        NTPNodeSetting("highlights_gain",       ST.FLOAT),
        NTPNodeSetting("highlights_lift",       ST.FLOAT),
        #midtones
        NTPNodeSetting("midtones_saturation", ST.FLOAT),
        NTPNodeSetting("midtones_contrast",   ST.FLOAT),
        NTPNodeSetting("midtones_gamma",      ST.FLOAT),
        NTPNodeSetting("midtones_gain",       ST.FLOAT),
        NTPNodeSetting("midtones_lift",       ST.FLOAT),
        #shadows
        NTPNodeSetting("shadows_saturation", ST.FLOAT),
        NTPNodeSetting("shadows_contrast",   ST.FLOAT),
        NTPNodeSetting("shadows_gamma",      ST.FLOAT),
        NTPNodeSetting("shadows_gain",       ST.FLOAT),
        NTPNodeSetting("shadows_lift",       ST.FLOAT),
        #midtones location
        NTPNodeSetting("midtones_start", ST.FLOAT),
        NTPNodeSetting("midtones_end",   ST.FLOAT)
    ],

    'CompositorNodeExposure' : [],
    'CompositorNodeGamma' : [],

    'CompositorNodeHueCorrect' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'CompositorNodeHueSat' : [],

    'CompositorNodeCurveRGB' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],

    'CompositorNodeTonemap' : [
        NTPNodeSetting("adaptation",   ST.FLOAT),
        NTPNodeSetting("contrast",     ST.FLOAT),
        NTPNodeSetting("correction",   ST.FLOAT),
        NTPNodeSetting("gamma",        ST.FLOAT),
        NTPNodeSetting("intensity",    ST.FLOAT),
        NTPNodeSetting("key",          ST.FLOAT),
        NTPNodeSetting("offset",       ST.FLOAT),
        NTPNodeSetting("tonemap_type", ST.ENUM)
    ],

    
    # Color > Mix
    'CompositorNodeAlphaOver' : [
        NTPNodeSetting("premul",          ST.FLOAT),
        NTPNodeSetting("use_premultiply", ST.BOOL)
    ],

    'CompositorNodeCombineColor' : [
        NTPNodeSetting("mode",     ST.ENUM, min_version = (3, 3, 0)),
        NTPNodeSetting("ycc_mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'CompositorNodeSeparateColor' : [
        NTPNodeSetting("mode",     ST.ENUM, min_version = (3, 3, 0)),
        NTPNodeSetting("ycc_mode", ST.ENUM, min_version = (3, 3, 0))
    ],

    'CompositorNodeMixRGB' : [
        NTPNodeSetting("blend_type", ST.ENUM),
        NTPNodeSetting("use_alpha",  ST.BOOL),
        NTPNodeSetting("use_clamp",  ST.BOOL)
    ],

    'CompositorNodeZcombine' : [
        NTPNodeSetting("use_alpha",       ST.BOOL),
        NTPNodeSetting("use_antialias_z", ST.BOOL)
    ],


    # FILTER
    'CompositorNodeAntiAliasing' : [
        NTPNodeSetting("contrast_limit",  ST.FLOAT),
        NTPNodeSetting("corner_rounding", ST.FLOAT),
        NTPNodeSetting("threshold",       ST.FLOAT)
    ],
    
    'CompositorNodeDenoise' : [
        NTPNodeSetting("prefilter", ST.ENUM),
        NTPNodeSetting("use_hdr",   ST.BOOL)
    ],

    'CompositorNodeDespeckle' : [
        NTPNodeSetting("threshold",          ST.FLOAT),
        NTPNodeSetting("threshold_neighbor", ST.FLOAT)
    ],

    'CompositorNodeDilateErode' : [
        NTPNodeSetting("distance", ST.INT),
        NTPNodeSetting("edge",     ST.FLOAT),
        NTPNodeSetting("falloff",  ST.ENUM),
        NTPNodeSetting("mode",     ST.ENUM)
    ],

    'CompositorNodeInpaint' : [
        NTPNodeSetting("distance", ST.INT)
    ],

    'CompositorNodeFilter' : [
        NTPNodeSetting("filter_type", ST.ENUM)
    ],

    'CompositorNodeGlare' : [
        NTPNodeSetting("angle_offset",     ST.FLOAT),
        NTPNodeSetting("color_modulation", ST.FLOAT),
        NTPNodeSetting("fade",             ST.FLOAT),
        NTPNodeSetting("glare_type",       ST.ENUM),
        NTPNodeSetting("iterations",       ST.INT),
        NTPNodeSetting("mix",              ST.FLOAT),
        NTPNodeSetting("quality",          ST.ENUM),
        NTPNodeSetting("size",             ST.INT),
        NTPNodeSetting("streaks",          ST.INT),
        NTPNodeSetting("threshold",        ST.FLOAT),
        NTPNodeSetting("use_rotate_45",    ST.BOOL)
    ],
    
    'CompositorNodeKuwahara' : [
        NTPNodeSetting("eccentricity", ST.FLOAT, min_version = (4, 0, 0)),
        NTPNodeSetting("sharpness",    ST.FLOAT, min_version = (4, 0, 0)),
        NTPNodeSetting("size",         ST.INT,   min_version = (4, 0, 0)),
        NTPNodeSetting("uniformity",   ST.INT,   min_version = (4, 0, 0)),
        NTPNodeSetting("variation",    ST.ENUM,  min_version = (4, 0, 0))
    ],

    'CompositorNodePixelate' : [],
    'CompositorNodePosterize' : [],

    'CompositorNodeSunBeams' : [
        NTPNodeSetting("ray_length", ST.FLOAT),
        NTPNodeSetting("source",     ST.VEC2)
    ],

    # Filter > Blur
    'CompositorNodeBilateralblur' : [
        NTPNodeSetting("iterations",  ST.INT),
        NTPNodeSetting("sigma_color", ST.FLOAT),
        NTPNodeSetting("sigma_space", ST.FLOAT)
    ],

    'CompositorNodeBlur' : [
        NTPNodeSetting("aspect_correction",    ST.ENUM),
        NTPNodeSetting("factor",               ST.FLOAT),
        NTPNodeSetting("factor_x",             ST.FLOAT),
        NTPNodeSetting("factor_y",             ST.FLOAT),
        NTPNodeSetting("filter_type",          ST.ENUM),
        NTPNodeSetting("size_x",               ST.INT),
        NTPNodeSetting("size_y",               ST.INT),
        NTPNodeSetting("use_bokeh",            ST.BOOL),
        NTPNodeSetting("use_extended_bounds",  ST.BOOL),
        NTPNodeSetting("use_gamma_correction", ST.BOOL),
        NTPNodeSetting("use_relative",         ST.BOOL),
        NTPNodeSetting("use_variable_size",    ST.BOOL)
    ],

    'CompositorNodeBokehBlur' : [
        NTPNodeSetting("blur_max",            ST.FLOAT),
        NTPNodeSetting("use_extended_bounds", ST.BOOL), 
        NTPNodeSetting("use_variable_size",   ST.BOOL)
    ],

    'CompositorNodeDefocus' : [
        NTPNodeSetting("angle",                ST.FLOAT),
        NTPNodeSetting("blur_max",             ST.FLOAT),
        NTPNodeSetting("bokeh",                ST.ENUM),
        NTPNodeSetting("f_stop",               ST.FLOAT),
        NTPNodeSetting("scene",                ST.SCENE),
        NTPNodeSetting("threshold",            ST.FLOAT),
        NTPNodeSetting("use_gamma_correction", ST.BOOL),
        NTPNodeSetting("use_preview",          ST.BOOL),
        NTPNodeSetting("use_zbuffer",          ST.BOOL),
        NTPNodeSetting("z_scale",              ST.FLOAT)
    ],

    'CompositorNodeDBlur' : [
        NTPNodeSetting("angle",      ST.FLOAT),
        NTPNodeSetting("center_x",   ST.FLOAT),
        NTPNodeSetting("center_y",   ST.FLOAT),
        NTPNodeSetting("distance",   ST.FLOAT),
        NTPNodeSetting("iterations", ST.INT),
        NTPNodeSetting("spin",       ST.FLOAT),
        NTPNodeSetting("use_wrap",   ST.BOOL, max_version = (3, 4, 0)),
        NTPNodeSetting("zoom",       ST.FLOAT)
    ],
    
    'CompositorNodeVecBlur' : [
        NTPNodeSetting("factor",     ST.FLOAT),
        NTPNodeSetting("samples",    ST.INT),
        NTPNodeSetting("speed_max",  ST.INT),
        NTPNodeSetting("speed_min",  ST.INT),
        NTPNodeSetting("use_curved", ST.BOOL)
    ],

    
    # KEYING
    'CompositorNodeChannelMatte' : [
        NTPNodeSetting("color_space",   ST.ENUM),
        NTPNodeSetting("limit_channel", ST.ENUM),
        NTPNodeSetting("limit_max",     ST.FLOAT),
        NTPNodeSetting("limit_method",  ST.ENUM),
        NTPNodeSetting("limit_min",     ST.FLOAT),
        NTPNodeSetting("matte_channel", ST.ENUM)
    ],

    'CompositorNodeChromaMatte' : [
        NTPNodeSetting("gain",          ST.FLOAT),
        NTPNodeSetting("lift",          ST.FLOAT),
        NTPNodeSetting("shadow_adjust", ST.FLOAT),
        NTPNodeSetting("threshold",     ST.FLOAT),
        NTPNodeSetting("tolerance",     ST.FLOAT)
    ],

    'CompositorNodeColorMatte' : [
        NTPNodeSetting("color_hue",        ST.FLOAT),
        NTPNodeSetting("color_saturation", ST.FLOAT),
        NTPNodeSetting("color_value",      ST.FLOAT)
    ],

    'CompositorNodeColorSpill' : [
        NTPNodeSetting("channel",       ST.ENUM),
        NTPNodeSetting("limit_channel", ST.ENUM),
        NTPNodeSetting("limit_method",  ST.ENUM),
        NTPNodeSetting("ratio",         ST.FLOAT),
        NTPNodeSetting("unspill_blue",  ST.FLOAT),
        NTPNodeSetting("unspill_green", ST.FLOAT),
        NTPNodeSetting("unspill_red",   ST.FLOAT),
        NTPNodeSetting("use_unspill",   ST.BOOL)
    ],

    'CompositorNodeDiffMatte' : [
        NTPNodeSetting("falloff",   ST.FLOAT),
        NTPNodeSetting("tolerance", ST.FLOAT)
    ],

    'CompositorNodeDistanceMatte' : [
        NTPNodeSetting("channel",   ST.ENUM),
        NTPNodeSetting("falloff",   ST.FLOAT),
        NTPNodeSetting("tolerance", ST.FLOAT)
    ],

    'CompositorNodeKeying' : [
        NTPNodeSetting("blur_post",             ST.INT),
        NTPNodeSetting("blur_pre",              ST.INT),
        NTPNodeSetting("clip_black",            ST.FLOAT),
        NTPNodeSetting("clip_white",            ST.FLOAT),
        NTPNodeSetting("despill_balance",       ST.FLOAT),
        NTPNodeSetting("despill_factor",        ST.FLOAT),
        NTPNodeSetting("dilate_distance",       ST.INT),
        NTPNodeSetting("edge_kernel_radius",    ST.INT),
        NTPNodeSetting("edge_kernel_tolerance", ST.FLOAT),
        NTPNodeSetting("feather_distance",      ST.INT),
        NTPNodeSetting("feather_falloff",       ST.ENUM),
        NTPNodeSetting("screen_balance",        ST.FLOAT)
    ],

    'CompositorNodeKeyingScreen' : [
        NTPNodeSetting("clip",            ST.MOVIE_CLIP),
        NTPNodeSetting("tracking_object", ST.STRING)
    ],

    'CompositorNodeLumaMatte' : [
        NTPNodeSetting("limit_max", ST.FLOAT),
        NTPNodeSetting("limit_min", ST.FLOAT)
    ],


    # MASK
    'CompositorNodeCryptomatteV2' : [
        NTPNodeSetting("add",              ST.COLOR),
        NTPNodeSetting("entries",          ST.CRYPTOMATTE_ENTRIES),
        NTPNodeSetting("frame_duration",   ST.INT),
        NTPNodeSetting("frame_offset",     ST.INT),
        NTPNodeSetting("frame_start",      ST.INT),
        NTPNodeSetting("image",            ST.IMAGE),
        NTPNodeSetting("layer",            ST.ENUM),
        NTPNodeSetting("layer_name",       ST.ENUM),
        NTPNodeSetting("matte_id",         ST.STRING),
        NTPNodeSetting("remove",           ST.COLOR),
        NTPNodeSetting("scene",            ST.SCENE),
        NTPNodeSetting("source",           ST.ENUM),
        NTPNodeSetting("use_auto_refresh", ST.BOOL),
        NTPNodeSetting("use_cyclic",       ST.BOOL),
        NTPNodeSetting("view",             ST.ENUM)
    ],

    'CompositorNodeCryptomatte' : [
        NTPNodeSetting("add",      ST.COLOR), #TODO: may need special handling
        NTPNodeSetting("matte_id", ST.STRING),
        NTPNodeSetting("remove",   ST.COLOR)
    ],

    'CompositorNodeBoxMask' : [
        NTPNodeSetting("height",    ST.FLOAT),
        NTPNodeSetting("mask_type", ST.ENUM),
        NTPNodeSetting("rotation",  ST.FLOAT),
        NTPNodeSetting("width",     ST.FLOAT),
        NTPNodeSetting("x",         ST.FLOAT),
        NTPNodeSetting("y",         ST.FLOAT)
    ],

    'CompositorNodeEllipseMask' : [
        NTPNodeSetting("height",    ST.FLOAT),
        NTPNodeSetting("mask_type", ST.ENUM),
        NTPNodeSetting("rotation",  ST.FLOAT),
        NTPNodeSetting("width",     ST.FLOAT),
        NTPNodeSetting("x",         ST.FLOAT),
        NTPNodeSetting("y",         ST.FLOAT)
    ],

    'CompositorNodeDoubleEdgeMask' : [
        NTPNodeSetting("edge_mode",  ST.ENUM),
        NTPNodeSetting("inner_mode", ST.ENUM)
    ],

    'CompositorNodeIDMask' : [
        NTPNodeSetting("index",            ST.INT),
        NTPNodeSetting("use_antialiasing", ST.BOOL)
    ],


    # TRACKING
    'CompositorNodePlaneTrackDeform' : [
        NTPNodeSetting("clip",                ST.MOVIE_CLIP),
        NTPNodeSetting("motion_blur_samples", ST.INT),
        NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
        NTPNodeSetting("plane_track_name",    ST.STRING),
        NTPNodeSetting("tracking_object",     ST.STRING),
        NTPNodeSetting("use_motion_blur",     ST.BOOL)
    ],

    'CompositorNodeStabilize' : [
        NTPNodeSetting("clip",        ST.MOVIE_CLIP),
        NTPNodeSetting("filter_type", ST.ENUM),
        NTPNodeSetting("invert",      ST.BOOL)
    ],

    'CompositorNodeTrackPos' : [
        NTPNodeSetting("clip",            ST.MOVIE_CLIP),
        NTPNodeSetting("frame_relative",  ST.INT),
        NTPNodeSetting("position",        ST.ENUM),
        NTPNodeSetting("track_name",      ST.STRING), #TODO: probably not right
        NTPNodeSetting("tracking_object", ST.STRING)
    ],


    # TRANSFORM
    'CompositorNodeRotate' : [
        NTPNodeSetting("filter_type",  ST.ENUM)
    ],

    'CompositorNodeScale' : [
        NTPNodeSetting("frame_method", ST.ENUM),
        NTPNodeSetting("offset_x",     ST.FLOAT),
        NTPNodeSetting("offset_y",     ST.FLOAT),
        NTPNodeSetting("space",        ST.ENUM)
    ],

    'CompositorNodeTransform' : [
        NTPNodeSetting("filter_type", ST.ENUM)
    ],

    'CompositorNodeTranslate' : [
        NTPNodeSetting("use_relative", ST.BOOL),
        NTPNodeSetting("wrap_axis",    ST.ENUM)
    ],

    'CompositorNodeCornerPin' : [],

    'CompositorNodeCrop' : [
        NTPNodeSetting("max_x",         ST.INT),
        NTPNodeSetting("max_y",         ST.INT),
        NTPNodeSetting("min_x",         ST.INT),
        NTPNodeSetting("min_y",         ST.INT),
        NTPNodeSetting("rel_max_x",     ST.FLOAT),
        NTPNodeSetting("rel_max_y",     ST.FLOAT),
        NTPNodeSetting("rel_min_x",     ST.FLOAT),
        NTPNodeSetting("rel_min_y",     ST.FLOAT),
        NTPNodeSetting("relative",      ST.BOOL),
        NTPNodeSetting("use_crop_size", ST.BOOL)
    ],

    'CompositorNodeDisplace' : [],

    'CompositorNodeFlip' : [
        NTPNodeSetting("axis", ST.ENUM)
    ],

    'CompositorNodeMapUV' : [
        NTPNodeSetting("alpha", ST.INT)
    ],

    'CompositorNodeLensdist' : [
        NTPNodeSetting("use_fit",       ST.BOOL),
        NTPNodeSetting("use_jitter",    ST.BOOL),
        NTPNodeSetting("use_projector", ST.BOOL)
    ],

    'CompositorNodeMovieDistortion' : [
        NTPNodeSetting("clip",            ST.MOVIE_CLIP),
        NTPNodeSetting("distortion_type", ST.ENUM)
    ],


    # UTILITIES
    'CompositorNodeMapRange' : [
        NTPNodeSetting("use_clamp", ST.BOOL)
    ],

    'CompositorNodeMapValue' : [
        NTPNodeSetting("max",     ST.VEC1),
        NTPNodeSetting("min",     ST.VEC1),
        NTPNodeSetting("offset",  ST.VEC1),
        NTPNodeSetting("size",    ST.VEC1),
        NTPNodeSetting("use_max", ST.BOOL),
        NTPNodeSetting("use_min", ST.BOOL)
    ],

    'CompositorNodeMath' : [
        NTPNodeSetting("operation", ST.ENUM),
        NTPNodeSetting("use_clamp", ST.BOOL)
    ],

    'CompositorNodeLevels' : [
        NTPNodeSetting("channel", ST.ENUM)
    ],
    
    'CompositorNodeNormalize' : [],


    'CompositorNodeSwitch' : [
        NTPNodeSetting("check", ST.BOOL)
    ],

    'CompositorNodeSwitchView' : [],


    # VECTOR
    'CompositorNodeCombineXYZ'  : [],
    'CompositorNodeSeparateXYZ' : [],
    'CompositorNodeNormal'      : [],

    'CompositorNodeCurveVec' : [
        NTPNodeSetting("mapping", ST.CURVE_MAPPING)
    ],


    # MISC
    'CompositorNodeGroup' : [
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
