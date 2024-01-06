from ..utils import ST 

compositor_node_settings : dict[str, list[(str, ST)]] = {
    # INPUT
    'CompositorNodeBokehImage' : [("angle",        ST.FLOAT),
                                  ("catadioptric", ST.FLOAT),
                                  ("flaps",        ST.INT),
                                  ("rounding",     ST.FLOAT),
                                  ("shift",        ST.FLOAT)],

    'CompositorNodeImage'      : [("frame_duration",            ST.INT),
                                  ("frame_offset",              ST.INT),
                                  ("frame_start",               ST.INT),
                                  ("image",                     ST.IMAGE),
                                  ("layer",                     ST.ENUM),
                                  ("use_auto_refresh",          ST.BOOL),
                                  ("use_cyclic",                ST.BOOL),
                                  ("use_straight_alpha_output", ST.BOOL),
                                  ("view",                      ST.ENUM)],

    'CompositorNodeMask'       : [("mask",                ST.MASK),
                                  ("motion_blur_samples", ST.INT),
                                  ("motion_blur_shutter", ST.FLOAT),
                                  ("size_source",         ST.ENUM),
                                  ("size_x",              ST.INT),
                                  ("size_y",              ST.INT),
                                  ("use_feather",         ST.BOOL),
                                  ("use_motion_blur",     ST.BOOL)],

    'CompositorNodeMovieClip'  : [("clip", ST.MOVIE_CLIP)],

    'CompositorNodeTexture'    : [("node_output", ST.INT), #TODO: ??
                                  ("texture",     ST.TEXTURE)],

    # Input > Constant

    'CompositorNodeRGB'        : [],
    'CompositorNodeValue'      : [],

    # Input > Scene

    'CompositorNodeRLayers'    : [("layer", ST.ENUM),
                                  ("scene", ST.SCENE)],

    'CompositorNodeSceneTime'  : [],

    'CompositorNodeTime'       : [("curve",       ST.CURVE_MAPPING),
                                  ("frame_end",   ST.INT),
                                  ("frame_start", ST.INT)],


    # OUTPUT
    'CompositorNodeComposite'   : [("use_alpha",          ST.BOOL)],

    'CompositorNodeOutputFile'  : [("active_input_index", ST.INT), #TODO: probably not right at all

                                   ("base_path",   ST.STRING),
                                   ("file_slots",  ST.FILE_SLOTS),
                                   ("format",      ST.IMAGE_FORMAT_SETTINGS),
                                   ("layer_slots", ST.LAYER_SLOTS)],

    'CompositorNodeViewer'      : [("center_x",   ST.FLOAT),
                                   ("center_y",   ST.FLOAT),
                                   ("tile_order", ST.ENUM),
                                   ("use_alpha",  ST.BOOL)],

    'CompositorNodeSplitViewer' : [("axis",   ST.ENUM),
                                   ("factor", ST.INT)],


    # COLOR
    'CompositorNodeAlphaOver'       : [("premul",          ST.FLOAT),
                                       ("use_premultiply", ST.BOOL)],

    'CompositorNodeBrightContrast'  : [("use_premultiply", ST.BOOL)],

    'CompositorNodeColorBalance'    : [("correction_method", ST.ENUM),
                                       ("gain",              ST.COLOR),
                                       ("gamma",             ST.COLOR),
                                       ("lift",              ST.COLOR),
                                       ("offset",            ST.COLOR),
                                       ("offset_basis",      ST.FLOAT),
                                       ("power",             ST.COLOR),
                                       ("slope",             ST.COLOR)],

    'CompositorNodeColorCorrection' : [("red",   ST.BOOL),
                                       ("green", ST.BOOL),
                                       ("blue",  ST.BOOL),
                                       #master
                                       ("master_saturation", ST.FLOAT),
                                       ("master_contrast",   ST.FLOAT),
                                       ("master_gamma",      ST.FLOAT),
                                       ("master_gain",       ST.FLOAT),
                                       ("master_lift",       ST.FLOAT),
                                       #highlights
                                       ("highlights_saturation", ST.FLOAT),
                                       ("highlights_contrast",   ST.FLOAT),
                                       ("highlights_gamma",      ST.FLOAT),
                                       ("highlights_gain",       ST.FLOAT),
                                       ("highlights_lift",       ST.FLOAT),
                                       #midtones
                                       ("midtones_saturation", ST.FLOAT),
                                       ("midtones_contrast",   ST.FLOAT),
                                       ("midtones_gamma",      ST.FLOAT),
                                       ("midtones_gain",       ST.FLOAT),
                                       ("midtones_lift",       ST.FLOAT),
                                       #shadows
                                       ("shadows_saturation", ST.FLOAT),
                                       ("shadows_contrast",   ST.FLOAT),
                                       ("shadows_gamma",      ST.FLOAT),
                                       ("shadows_gain",       ST.FLOAT),
                                       ("shadows_lift",       ST.FLOAT),
                                       #midtones location
                                       ("midtones_start", ST.FLOAT),
                                       ("midtones_end",   ST.FLOAT)],

    'CompositorNodeExposure'        : [],

    'CompositorNodeGamma'           : [],

    'CompositorNodeHueCorrect'      : [("mapping", ST.CURVE_MAPPING)],

    'CompositorNodeHueSat'          : [],

    'CompositorNodeInvert'          : [("invert_alpha", ST.BOOL),
                                       ("invert_rgb",   ST.BOOL)],

    'CompositorNodeMixRGB'          : [("blend_type", ST.ENUM),
                                       ("use_alpha", ST.BOOL),
                                       ("use_clamp", ST.BOOL)], #TODO: what is update() method for?

    'CompositorNodePosterize'       : [],

    'CompositorNodeCurveRGB'        : [("mapping", ST.CURVE_MAPPING)],

    'CompositorNodeTonemap'         : [("adaptation",   ST.FLOAT),
                                       ("contrast",     ST.FLOAT),
                                       ("correction",   ST.FLOAT),
                                       ("gamma",        ST.FLOAT),
                                       ("intensity",    ST.FLOAT),
                                       ("key",          ST.FLOAT),
                                       ("offset",       ST.FLOAT),
                                       ("tonemap_type", ST.ENUM)],

    'CompositorNodeZcombine'        : [("use_alpha",       ST.BOOL),
                                       ("use_antialias_z", ST.BOOL)],


    # CONVERTER
    'CompositorNodePremulKey'         : [("mapping", ST.ENUM)],

    'CompositorNodeValToRGB'          : [("color_ramp", ST.COLOR_RAMP)], 

    'CompositorNodeConvertColorSpace' : [("from_color_space", ST.ENUM),
                                         ("to_color_space",   ST.ENUM)],

    'CompositorNodeCombineColor'      : [("mode",     ST.ENUM),
                                         ("ycc_mode", ST.ENUM)],

    'CompositorNodeCombineXYZ'        : [],

    'CompositorNodeIDMask'            : [("index",            ST.INT),
                                         ("use_antialiasing", ST.BOOL)],

    'CompositorNodeMath'              : [("operation", ST.ENUM),
                                         ("use_clamp", ST.BOOL)],

    'CompositorNodeRGBToBW'           : [],

    'CompositorNodeSeparateColor'     : [("mode",     ST.ENUM),
                                         ("ycc_mode", ST.ENUM)],

    'CompositorNodeSeparateXYZ'       : [],

    'CompositorNodeSetAlpha'          : [("mode", ST.ENUM)],

    'CompositorNodeSwitchView'        : [],


    # FILTER
    'CompositorNodeAntiAliasing'  : [("contrast_limit",  ST.FLOAT),
                                     ("corner_rounding", ST.FLOAT),
                                     ("threshold",       ST.FLOAT)],

    'CompositorNodeBilateralblur' : [("iterations",  ST.INT),
                                     ("sigma_color", ST.FLOAT),
                                     ("sigma_space", ST.FLOAT)],

    'CompositorNodeBlur'          : [("aspect_correction",    ST.ENUM),
                                     ("factor",               ST.FLOAT),
                                     ("factor_x",             ST.FLOAT),
                                     ("factor_y",             ST.FLOAT),
                                     ("filter_type",          ST.ENUM),
                                     ("size_x",               ST.INT),
                                     ("size_y",               ST.INT),
                                     ("use_bokeh",            ST.BOOL),
                                     ("use_extended_bounds",  ST.BOOL),
                                     ("use_gamma_correction", ST.BOOL),
                                     ("use_relative",         ST.BOOL),
                                     ("use_variable_size",    ST.BOOL)],

    'CompositorNodeBokehBlur'     : [("blur_max",            ST.FLOAT),
                                     ("use_extended_bounds", ST.BOOL), 
                                     ("use_variable_size",   ST.BOOL)],

    'CompositorNodeDefocus'       : [("angle",                ST.FLOAT),
                                     ("blur_max",             ST.FLOAT),
                                     ("bokeh",                ST.ENUM),
                                     ("f_stop",               ST.FLOAT),
                                     ("scene",                ST.SCENE),
                                     ("threshold",            ST.FLOAT),
                                     ("use_gamma_correction", ST.BOOL),
                                     ("use_preview",          ST.BOOL),
                                     ("use_zbuffer",          ST.BOOL),
                                     ("z_scale",              ST.FLOAT)],

    'CompositorNodeDespeckle'     : [("threshold",          ST.FLOAT),
                                     ("threshold_neighbor", ST.FLOAT)],

    'CompositorNodeDilateErode'   : [("distance", ST.INT),
                                     ("edge",     ST.FLOAT),
                                     ("falloff",  ST.ENUM),
                                     ("mode",     ST.ENUM)],

    'CompositorNodeDBlur'         : [("angle",      ST.FLOAT),
                                     ("center_x",   ST.FLOAT),
                                     ("center_y",   ST.FLOAT),
                                     ("distance",   ST.FLOAT),
                                     ("iterations", ST.INT),
                                     ("spin",       ST.FLOAT),
                                     ("zoom",       ST.FLOAT)],

    'CompositorNodeFilter'        : [("filter_type", ST.ENUM)],

    'CompositorNodeGlare'         : [("angle_offset",     ST.FLOAT),
                                     ("color_modulation", ST.FLOAT),
                                     ("fade",             ST.FLOAT),
                                     ("glare_type",       ST.ENUM),
                                     ("iterations",       ST.INT),
                                     ("mix",              ST.FLOAT),
                                     ("quality",          ST.ENUM),
                                     ("size",             ST.INT),
                                     ("streaks",          ST.INT),
                                     ("threshold",        ST.FLOAT),
                                     ("use_rotate_45",    ST.BOOL)],

    'CompositorNodeInpaint'       : [("distance", ST.INT)],

    'CompositorNodePixelate'      : [],

    'CompositorNodeSunBeams'      : [("ray_length", ST.FLOAT),
                                     ("source",     ST.VEC2)],

    'CompositorNodeVecBlur'       : [("factor",     ST.FLOAT),
                                     ("samples",    ST.INT),
                                     ("speed_max",  ST.INT),
                                     ("speed_min",  ST.INT),
                                     ("use_curved", ST.BOOL)],


    # VECTOR
    'CompositorNodeMapRange'  : [("use_clamp", ST.BOOL)],

    'CompositorNodeMapValue'  : [("max",     ST.VEC1),
                                 ("min",     ST.VEC1),
                                 ("offset",  ST.VEC1),
                                 ("size",    ST.VEC1),
                                 ("use_max", ST.BOOL),
                                 ("use_min", ST.BOOL)],

    'CompositorNodeNormal'    : [],

    'CompositorNodeNormalize' : [],

    'CompositorNodeCurveVec'  : [("mapping", ST.CURVE_MAPPING)],


    # MATTE
    'CompositorNodeBoxMask'        : [("height",    ST.FLOAT),
                                      ("mask_type", ST.ENUM),
                                      ("rotation",  ST.FLOAT),
                                      ("width",     ST.FLOAT),
                                      ("x",         ST.FLOAT),
                                      ("y",         ST.FLOAT)],

    'CompositorNodeChannelMatte'   : [("color_space",   ST.ENUM),
                                      ("limit_channel", ST.ENUM),
                                      ("limit_max",     ST.FLOAT),
                                      ("limit_method",  ST.ENUM),
                                      ("limit_min",     ST.FLOAT),
                                      ("matte_channel", ST.ENUM)],

    'CompositorNodeChromaMatte'    : [("gain",          ST.FLOAT),
                                      ("lift",          ST.FLOAT),
                                      ("shadow_adjust", ST.FLOAT),
                                      ("threshold",     ST.FLOAT),
                                      ("tolerance",     ST.FLOAT)],

    'CompositorNodeColorMatte'     : [("color_hue",        ST.FLOAT),
                                      ("color_saturation", ST.FLOAT),
                                      ("color_value",      ST.FLOAT)],

    'CompositorNodeColorSpill'     : [("channel",       ST.ENUM),
                                      ("limit_channel", ST.ENUM),
                                      ("limit_method",  ST.ENUM),
                                      ("ratio",         ST.FLOAT),
                                      ("unspill_blue",  ST.FLOAT),
                                      ("unspill_green", ST.FLOAT),
                                      ("unspill_red",   ST.FLOAT),
                                      ("use_unspill",   ST.BOOL)],

    'CompositorNodeCryptomatteV2'  : [("add",              ST.COLOR),
                                      ("entries",          ST.CRYPTOMATTE_ENTRIES),
                                      ("frame_duration",   ST.INT),
                                      ("frame_offset",     ST.INT),
                                      ("frame_start",      ST.INT),
                                      #("has_layers",       ST.BOOL), #TODO: readonly?
                                      #("has_views",        ST.BOOL), #TODO: readonly?
                                      ("image",            ST.IMAGE),
                                      ("layer",            ST.ENUM),
                                      ("layer_name",       ST.ENUM),
                                      ("matte_id",         ST.STRING),
                                      ("remove",           ST.COLOR),
                                      ("scene",            ST.SCENE),
                                      ("source",           ST.ENUM),
                                      ("use_auto_refresh", ST.BOOL),
                                      ("use_cyclic",       ST.BOOL),
                                      ("view",             ST.ENUM)],

    'CompositorNodeCryptomatte'    : [("add",      ST.COLOR), #TODO: may need special handling
                                      ("matte_id", ST.STRING),
                                      ("remove",   ST.COLOR)],

    'CompositorNodeDiffMatte'      : [("falloff",   ST.FLOAT),
                                      ("tolerance", ST.FLOAT)],

    'CompositorNodeDistanceMatte'  : [("channel",   ST.ENUM),
                                      ("falloff",   ST.FLOAT),
                                      ("tolerance", ST.FLOAT)],

    'CompositorNodeDoubleEdgeMask' : [("edge_mode",  ST.ENUM),
                                      ("inner_mode", ST.ENUM)],

    'CompositorNodeEllipseMask'    : [("height",    ST.FLOAT),
                                      ("mask_type", ST.ENUM),
                                      ("rotation",  ST.FLOAT),
                                      ("width",     ST.FLOAT),
                                      ("x",         ST.FLOAT),
                                      ("y",         ST.FLOAT)],

    'CompositorNodeKeying'         : [("blur_post",             ST.INT),
                                      ("blur_pre",              ST.INT),
                                      ("clip_black",            ST.FLOAT),
                                      ("clip_white",            ST.FLOAT),
                                      ("despill_balance",       ST.FLOAT),
                                      ("despill_factor",        ST.FLOAT),
                                      ("dilate_distance",       ST.INT),
                                      ("edge_kernel_radius",    ST.INT),
                                      ("edge_kernel_tolerance", ST.FLOAT),
                                      ("feather_distance",      ST.INT),
                                      ("feather_falloff",       ST.ENUM),
                                      ("screen_balance",        ST.FLOAT)],

    'CompositorNodeKeyingScreen'   : [("clip",           ST.MOVIE_CLIP),
                                      ("tracing_object", ST.STRING)],

    'CompositorNodeLumaMatte'      : [("limit_max", ST.FLOAT),
                                      ("limit_min", ST.FLOAT)],


    # DISTORT
    'CompositorNodeCornerPin'        : [],

    'CompositorNodeCrop'             : [("max_x",         ST.INT),
                                        ("max_y",         ST.INT),
                                        ("min_x",         ST.INT),
                                        ("min_y",         ST.INT),
                                        ("rel_max_x",     ST.FLOAT),
                                        ("rel_max_y",     ST.FLOAT),
                                        ("rel_min_x",     ST.FLOAT),
                                        ("rel_min_y",     ST.FLOAT),
                                        ("relative",      ST.BOOL),
                                        ("use_crop_size", ST.BOOL)],

    'CompositorNodeDisplace'         : [],

    'CompositorNodeFlip'             : [("axis", ST.ENUM)],

    'CompositorNodeLensdist'         : [("use_fit",       ST.BOOL),
                                        ("use_jitter",    ST.BOOL),
                                        ("use_projector", ST.BOOL)],

    'CompositorNodeMapUV'            : [("alpha", ST.INT)],

    'CompositorNodeMovieDistortion'  : [("clip",            ST.MOVIE_CLIP),
                                        ("distortion_type", ST.ENUM)],

    'CompositorNodePlaneTrackDeform' : [("clip",                ST.MOVIE_CLIP),
                                        ("motion_blur_samples", ST.INT),
                                        ("motion_blur_shutter", ST.FLOAT),
                                        ("plane_track_name",    ST.STRING),
                                        ("tracking_object",     ST.STRING),
                                        ("use_motion_blur",     ST.BOOL)],

    'CompositorNodeRotate'           : [("filter_type",  ST.ENUM)],

    'CompositorNodeScale'            : [("frame_method", ST.ENUM),
                                        ("offset_x",     ST.FLOAT),
                                        ("offset_y",     ST.FLOAT),
                                        ("space",        ST.ENUM)],

    'CompositorNodeStabilize'        : [("clip",        ST.MOVIE_CLIP),
                                        ("filter_type", ST.ENUM),
                                        ("invert",      ST.BOOL)],

    'CompositorNodeTransform'        : [("filter_type", ST.ENUM)],

    'CompositorNodeTranslate'        : [("use_relative", ST.BOOL),
                                        ("wrap_axis",    ST.ENUM)],

    # TRACKING
    'CompositorNodeTrackPos'   : [("clip",            ST.MOVIE_CLIP),
                                  ("frame_relative",  ST.INT),
                                  ("position",        ST.ENUM),
                                  ("track_name",      ST.STRING), #TODO: probably not right
                                  ("tracking_object", ST.STRING)], 

    # UTILITIES
    'CompositorNodeLevels'      : [("channel", ST.ENUM)],

    # LAYOUT
    'CompositorNodeSwitch' : [("check", ST.BOOL)],


    # MISC
    'NodeFrame'       : [("label_size", ST.INT),
                         ("shrink", ST.BOOL),
                         ("text", ST.TEXT)],

    'NodeGroupInput'  : [],

    'NodeGroupOutput' : [("is_active_output", ST.BOOL)],

    'NodeReroute'     : []
}
