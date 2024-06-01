from .utils import ST, NTPNodeSetting

node_settings : dict[str, list[NTPNodeSetting]] = {
	'CompositorNodeAlphaOver' : [
		NTPNodeSetting("premul", ST.FLOAT),
		NTPNodeSetting("use_premultiply", ST.BOOL),
	],

	'CompositorNodeAntiAliasing' : [
		NTPNodeSetting("contrast_limit", ST.FLOAT),
		NTPNodeSetting("corner_rounding", ST.FLOAT),
		NTPNodeSetting("threshold", ST.FLOAT),
	],

	'CompositorNodeBilateralblur' : [
		NTPNodeSetting("iterations", ST.INT),
		NTPNodeSetting("sigma_color", ST.FLOAT),
		NTPNodeSetting("sigma_space", ST.FLOAT),
	],

	'CompositorNodeBlur' : [
		NTPNodeSetting("aspect_correction", ST.ENUM),
		NTPNodeSetting("factor", ST.FLOAT),
		NTPNodeSetting("factor_x", ST.FLOAT),
		NTPNodeSetting("factor_y", ST.FLOAT),
		NTPNodeSetting("filter_type", ST.ENUM),
		NTPNodeSetting("size_x", ST.INT),
		NTPNodeSetting("size_y", ST.INT),
		NTPNodeSetting("use_bokeh", ST.BOOL),
		NTPNodeSetting("use_extended_bounds", ST.BOOL),
		NTPNodeSetting("use_gamma_correction", ST.BOOL),
		NTPNodeSetting("use_relative", ST.BOOL),
		NTPNodeSetting("use_variable_size", ST.BOOL),
	],

	'CompositorNodeBokehBlur' : [
		NTPNodeSetting("blur_max", ST.FLOAT),
		NTPNodeSetting("use_extended_bounds", ST.BOOL),
		NTPNodeSetting("use_variable_size", ST.BOOL),
	],

	'CompositorNodeBokehImage' : [
		NTPNodeSetting("angle", ST.FLOAT),
		NTPNodeSetting("catadioptric", ST.FLOAT),
		NTPNodeSetting("flaps", ST.INT),
		NTPNodeSetting("rounding", ST.FLOAT),
		NTPNodeSetting("shift", ST.FLOAT),
	],

	'CompositorNodeBoxMask' : [
		NTPNodeSetting("height", ST.FLOAT),
		NTPNodeSetting("mask_type", ST.ENUM),
		NTPNodeSetting("rotation", ST.FLOAT),
		NTPNodeSetting("width", ST.FLOAT),
		NTPNodeSetting("x", ST.FLOAT),
		NTPNodeSetting("y", ST.FLOAT),
	],

	'CompositorNodeBrightContrast' : [
		NTPNodeSetting("use_premultiply", ST.BOOL),
	],

	'CompositorNodeChannelMatte' : [
		NTPNodeSetting("color_space", ST.ENUM),
		NTPNodeSetting("limit_channel", ST.ENUM),
		NTPNodeSetting("limit_max", ST.FLOAT),
		NTPNodeSetting("limit_method", ST.ENUM),
		NTPNodeSetting("limit_min", ST.FLOAT),
		NTPNodeSetting("matte_channel", ST.ENUM),
	],

	'CompositorNodeChromaMatte' : [
		NTPNodeSetting("gain", ST.FLOAT),
		NTPNodeSetting("lift", ST.FLOAT),
		NTPNodeSetting("shadow_adjust", ST.FLOAT),
		NTPNodeSetting("threshold", ST.FLOAT),
		NTPNodeSetting("tolerance", ST.FLOAT),
	],

	'CompositorNodeColorBalance' : [
		NTPNodeSetting("correction_method", ST.ENUM),
		NTPNodeSetting("gain", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("gain", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("gamma", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("gamma", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("lift", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("lift", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("offset", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("offset", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("offset_basis", ST.FLOAT),
		NTPNodeSetting("power", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("power", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("slope", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("slope", ST.VEC3, max_version=(3, 5, 0)),
	],

	'CompositorNodeColorCorrection' : [
		NTPNodeSetting("blue", ST.BOOL),
		NTPNodeSetting("green", ST.BOOL),
		NTPNodeSetting("highlights_contrast", ST.FLOAT),
		NTPNodeSetting("highlights_gain", ST.FLOAT),
		NTPNodeSetting("highlights_gamma", ST.FLOAT),
		NTPNodeSetting("highlights_lift", ST.FLOAT),
		NTPNodeSetting("highlights_saturation", ST.FLOAT),
		NTPNodeSetting("master_contrast", ST.FLOAT),
		NTPNodeSetting("master_gain", ST.FLOAT),
		NTPNodeSetting("master_gamma", ST.FLOAT),
		NTPNodeSetting("master_lift", ST.FLOAT),
		NTPNodeSetting("master_saturation", ST.FLOAT),
		NTPNodeSetting("midtones_contrast", ST.FLOAT),
		NTPNodeSetting("midtones_end", ST.FLOAT),
		NTPNodeSetting("midtones_gain", ST.FLOAT),
		NTPNodeSetting("midtones_gamma", ST.FLOAT),
		NTPNodeSetting("midtones_lift", ST.FLOAT),
		NTPNodeSetting("midtones_saturation", ST.FLOAT),
		NTPNodeSetting("midtones_start", ST.FLOAT),
		NTPNodeSetting("red", ST.BOOL),
		NTPNodeSetting("shadows_contrast", ST.FLOAT),
		NTPNodeSetting("shadows_gain", ST.FLOAT),
		NTPNodeSetting("shadows_gamma", ST.FLOAT),
		NTPNodeSetting("shadows_lift", ST.FLOAT),
		NTPNodeSetting("shadows_saturation", ST.FLOAT),
	],

	'CompositorNodeColorMatte' : [
		NTPNodeSetting("color_hue", ST.FLOAT),
		NTPNodeSetting("color_saturation", ST.FLOAT),
		NTPNodeSetting("color_value", ST.FLOAT),
	],

	'CompositorNodeColorSpill' : [
		NTPNodeSetting("channel", ST.ENUM),
		NTPNodeSetting("limit_channel", ST.ENUM),
		NTPNodeSetting("limit_method", ST.ENUM),
		NTPNodeSetting("ratio", ST.FLOAT),
		NTPNodeSetting("unspill_blue", ST.FLOAT),
		NTPNodeSetting("unspill_green", ST.FLOAT),
		NTPNodeSetting("unspill_red", ST.FLOAT),
		NTPNodeSetting("use_unspill", ST.BOOL),
	],

	'CompositorNodeCombHSVA' : [],

	'CompositorNodeCombRGBA' : [],

	'CompositorNodeCombYCCA' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'CompositorNodeCombYUVA' : [],

	'CompositorNodeCombineColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
		NTPNodeSetting("ycc_mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'CompositorNodeCombineXYZ' : [],

	'CompositorNodeComposite' : [
		NTPNodeSetting("use_alpha", ST.BOOL),
	],

	'CompositorNodeConvertColorSpace' : [
		NTPNodeSetting("from_color_space", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("to_color_space", ST.ENUM, min_version=(3, 1, 0)),
	],

	'CompositorNodeCornerPin' : [],

	'CompositorNodeCrop' : [
		NTPNodeSetting("max_x", ST.INT),
		NTPNodeSetting("max_y", ST.INT),
		NTPNodeSetting("min_x", ST.INT),
		NTPNodeSetting("min_y", ST.INT),
		NTPNodeSetting("rel_max_x", ST.FLOAT),
		NTPNodeSetting("rel_max_y", ST.FLOAT),
		NTPNodeSetting("rel_min_x", ST.FLOAT),
		NTPNodeSetting("rel_min_y", ST.FLOAT),
		NTPNodeSetting("relative", ST.BOOL),
		NTPNodeSetting("use_crop_size", ST.BOOL),
	],

	'CompositorNodeCryptomatte' : [
		NTPNodeSetting("add", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("add", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("matte_id", ST.STRING),
		NTPNodeSetting("remove", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("remove", ST.VEC3, max_version=(3, 5, 0)),
	],

	'CompositorNodeCryptomatteV2' : [
		NTPNodeSetting("add", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("add", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("entries", ST.CRYPTOMATTE_ENTRIES),
		NTPNodeSetting("frame_duration", ST.INT),
		NTPNodeSetting("frame_offset", ST.INT),
		NTPNodeSetting("frame_start", ST.INT),
		NTPNodeSetting("image", ST.IMAGE),
		NTPNodeSetting("layer", ST.ENUM),
		NTPNodeSetting("layer_name", ST.ENUM),
		NTPNodeSetting("matte_id", ST.STRING),
		NTPNodeSetting("remove", ST.COLOR, min_version=(3, 5, 0)),
		NTPNodeSetting("remove", ST.VEC3, max_version=(3, 5, 0)),
		NTPNodeSetting("scene", ST.SCENE),
		NTPNodeSetting("source", ST.ENUM),
		NTPNodeSetting("use_auto_refresh", ST.BOOL),
		NTPNodeSetting("use_cyclic", ST.BOOL),
		NTPNodeSetting("view", ST.ENUM),
	],

	'CompositorNodeCurveRGB' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'CompositorNodeCurveVec' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'CompositorNodeCustomGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'CompositorNodeDBlur' : [
		NTPNodeSetting("angle", ST.FLOAT),
		NTPNodeSetting("center_x", ST.FLOAT),
		NTPNodeSetting("center_y", ST.FLOAT),
		NTPNodeSetting("distance", ST.FLOAT),
		NTPNodeSetting("iterations", ST.INT),
		NTPNodeSetting("spin", ST.FLOAT),
		NTPNodeSetting("use_wrap", ST.BOOL, max_version=(3, 5, 0)),
		NTPNodeSetting("zoom", ST.FLOAT),
	],

	'CompositorNodeDefocus' : [
		NTPNodeSetting("angle", ST.FLOAT),
		NTPNodeSetting("blur_max", ST.FLOAT),
		NTPNodeSetting("bokeh", ST.ENUM),
		NTPNodeSetting("f_stop", ST.FLOAT),
		NTPNodeSetting("scene", ST.SCENE),
		NTPNodeSetting("threshold", ST.FLOAT),
		NTPNodeSetting("use_gamma_correction", ST.BOOL),
		NTPNodeSetting("use_preview", ST.BOOL),
		NTPNodeSetting("use_zbuffer", ST.BOOL),
		NTPNodeSetting("z_scale", ST.FLOAT),
	],

	'CompositorNodeDenoise' : [
		NTPNodeSetting("prefilter", ST.ENUM),
		NTPNodeSetting("use_hdr", ST.BOOL),
	],

	'CompositorNodeDespeckle' : [
		NTPNodeSetting("threshold", ST.FLOAT),
		NTPNodeSetting("threshold_neighbor", ST.FLOAT),
	],

	'CompositorNodeDiffMatte' : [
		NTPNodeSetting("falloff", ST.FLOAT),
		NTPNodeSetting("tolerance", ST.FLOAT),
	],

	'CompositorNodeDilateErode' : [
		NTPNodeSetting("distance", ST.INT),
		NTPNodeSetting("edge", ST.FLOAT),
		NTPNodeSetting("falloff", ST.ENUM),
		NTPNodeSetting("mode", ST.ENUM),
	],

	'CompositorNodeDisplace' : [],

	'CompositorNodeDistanceMatte' : [
		NTPNodeSetting("channel", ST.ENUM),
		NTPNodeSetting("falloff", ST.FLOAT),
		NTPNodeSetting("tolerance", ST.FLOAT),
	],

	'CompositorNodeDoubleEdgeMask' : [
		NTPNodeSetting("edge_mode", ST.ENUM),
		NTPNodeSetting("inner_mode", ST.ENUM),
	],

	'CompositorNodeEllipseMask' : [
		NTPNodeSetting("height", ST.FLOAT),
		NTPNodeSetting("mask_type", ST.ENUM),
		NTPNodeSetting("rotation", ST.FLOAT),
		NTPNodeSetting("width", ST.FLOAT),
		NTPNodeSetting("x", ST.FLOAT),
		NTPNodeSetting("y", ST.FLOAT),
	],

	'CompositorNodeExposure' : [],

	'CompositorNodeFilter' : [
		NTPNodeSetting("filter_type", ST.ENUM),
	],

	'CompositorNodeFlip' : [
		NTPNodeSetting("axis", ST.ENUM),
	],

	'CompositorNodeGamma' : [],

	'CompositorNodeGlare' : [
		NTPNodeSetting("angle_offset", ST.FLOAT),
		NTPNodeSetting("color_modulation", ST.FLOAT),
		NTPNodeSetting("fade", ST.FLOAT),
		NTPNodeSetting("glare_type", ST.ENUM),
		NTPNodeSetting("iterations", ST.INT),
		NTPNodeSetting("mix", ST.FLOAT),
		NTPNodeSetting("quality", ST.ENUM),
		NTPNodeSetting("size", ST.INT),
		NTPNodeSetting("streaks", ST.INT),
		NTPNodeSetting("threshold", ST.FLOAT),
		NTPNodeSetting("use_rotate_45", ST.BOOL),
	],

	'CompositorNodeGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'CompositorNodeHueCorrect' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'CompositorNodeHueSat' : [],

	'CompositorNodeIDMask' : [
		NTPNodeSetting("index", ST.INT),
		NTPNodeSetting("use_antialiasing", ST.BOOL),
	],

	'CompositorNodeImage' : [
		NTPNodeSetting("frame_duration", ST.INT),
		NTPNodeSetting("frame_offset", ST.INT),
		NTPNodeSetting("frame_start", ST.INT),
		NTPNodeSetting("image", ST.IMAGE),
		NTPNodeSetting("layer", ST.ENUM),
		NTPNodeSetting("use_auto_refresh", ST.BOOL),
		NTPNodeSetting("use_cyclic", ST.BOOL),
		NTPNodeSetting("use_straight_alpha_output", ST.BOOL),
		NTPNodeSetting("view", ST.ENUM),
	],

	'CompositorNodeInpaint' : [
		NTPNodeSetting("distance", ST.INT),
	],

	'CompositorNodeInvert' : [
		NTPNodeSetting("invert_alpha", ST.BOOL),
		NTPNodeSetting("invert_rgb", ST.BOOL),
	],

	'CompositorNodeKeying' : [
		NTPNodeSetting("blur_post", ST.INT),
		NTPNodeSetting("blur_pre", ST.INT),
		NTPNodeSetting("clip_black", ST.FLOAT),
		NTPNodeSetting("clip_white", ST.FLOAT),
		NTPNodeSetting("despill_balance", ST.FLOAT),
		NTPNodeSetting("despill_factor", ST.FLOAT),
		NTPNodeSetting("dilate_distance", ST.INT),
		NTPNodeSetting("edge_kernel_radius", ST.INT),
		NTPNodeSetting("edge_kernel_tolerance", ST.FLOAT),
		NTPNodeSetting("feather_distance", ST.INT),
		NTPNodeSetting("feather_falloff", ST.ENUM),
		NTPNodeSetting("screen_balance", ST.FLOAT),
	],

	'CompositorNodeKeyingScreen' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
		NTPNodeSetting("smoothness", ST.FLOAT, min_version=(4, 1, 0)),
		NTPNodeSetting("tracking_object", ST.STRING),
	],

	'CompositorNodeKuwahara' : [
		NTPNodeSetting("eccentricity", ST.FLOAT, min_version=(4, 0, 0)),
		NTPNodeSetting("sharpness", ST.FLOAT, min_version=(4, 0, 0)),
		NTPNodeSetting("size", ST.INT, min_version=(4, 0, 0), max_version=(4, 1, 0)),
		NTPNodeSetting("uniformity", ST.INT, min_version=(4, 0, 0)),
		NTPNodeSetting("use_high_precision", ST.BOOL, min_version=(4, 1, 0)),
		NTPNodeSetting("variation", ST.ENUM, min_version=(4, 0, 0)),
	],

	'CompositorNodeLensdist' : [
		NTPNodeSetting("use_fit", ST.BOOL),
		NTPNodeSetting("use_jitter", ST.BOOL),
		NTPNodeSetting("use_projector", ST.BOOL),
	],

	'CompositorNodeLevels' : [
		NTPNodeSetting("channel", ST.ENUM),
	],

	'CompositorNodeLumaMatte' : [
		NTPNodeSetting("limit_max", ST.FLOAT),
		NTPNodeSetting("limit_min", ST.FLOAT),
	],

	'CompositorNodeMapRange' : [
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'CompositorNodeMapUV' : [
		NTPNodeSetting("alpha", ST.INT),
		NTPNodeSetting("filter_type", ST.ENUM, min_version=(4, 1, 0)),
	],

	'CompositorNodeMapValue' : [
		NTPNodeSetting("max", ST.VEC1),
		NTPNodeSetting("min", ST.VEC1),
		NTPNodeSetting("offset", ST.VEC1),
		NTPNodeSetting("size", ST.VEC1),
		NTPNodeSetting("use_max", ST.BOOL),
		NTPNodeSetting("use_min", ST.BOOL),
	],

	'CompositorNodeMask' : [
		NTPNodeSetting("mask", ST.MASK),
		NTPNodeSetting("motion_blur_samples", ST.INT),
		NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
		NTPNodeSetting("size_source", ST.ENUM),
		NTPNodeSetting("size_x", ST.INT),
		NTPNodeSetting("size_y", ST.INT),
		NTPNodeSetting("use_feather", ST.BOOL),
		NTPNodeSetting("use_motion_blur", ST.BOOL),
	],

	'CompositorNodeMath' : [
		NTPNodeSetting("operation", ST.ENUM),
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'CompositorNodeMixRGB' : [
		NTPNodeSetting("blend_type", ST.ENUM),
		NTPNodeSetting("use_alpha", ST.BOOL),
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'CompositorNodeMovieClip' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
	],

	'CompositorNodeMovieDistortion' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
		NTPNodeSetting("distortion_type", ST.ENUM),
	],

	'CompositorNodeNormal' : [],

	'CompositorNodeNormalize' : [],

	'CompositorNodeOutputFile' : [
		NTPNodeSetting("active_input_index", ST.INT),
		NTPNodeSetting("base_path", ST.STRING),
		NTPNodeSetting("file_slots", ST.FILE_SLOTS),
		NTPNodeSetting("format", ST.IMAGE_FORMAT_SETTINGS),
		NTPNodeSetting("layer_slots", ST.LAYER_SLOTS),
	],

	'CompositorNodePixelate' : [
		NTPNodeSetting("pixel_size", ST.INT, min_version=(4, 1, 0)),
	],

	'CompositorNodePlaneTrackDeform' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
		NTPNodeSetting("motion_blur_samples", ST.INT),
		NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
		NTPNodeSetting("plane_track_name", ST.STRING),
		NTPNodeSetting("tracking_object", ST.STRING),
		NTPNodeSetting("use_motion_blur", ST.BOOL),
	],

	'CompositorNodePosterize' : [],

	'CompositorNodePremulKey' : [
		NTPNodeSetting("mapping", ST.ENUM),
	],

	'CompositorNodeRGB' : [],

	'CompositorNodeRGBToBW' : [],

	'CompositorNodeRLayers' : [
		NTPNodeSetting("layer", ST.ENUM),
		NTPNodeSetting("scene", ST.SCENE),
	],

	'CompositorNodeRotate' : [
		NTPNodeSetting("filter_type", ST.ENUM),
	],

	'CompositorNodeScale' : [
		NTPNodeSetting("frame_method", ST.ENUM),
		NTPNodeSetting("offset_x", ST.FLOAT),
		NTPNodeSetting("offset_y", ST.FLOAT),
		NTPNodeSetting("space", ST.ENUM),
	],

	'CompositorNodeSceneTime' : [],

	'CompositorNodeSepHSVA' : [],

	'CompositorNodeSepRGBA' : [],

	'CompositorNodeSepYCCA' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'CompositorNodeSepYUVA' : [],

	'CompositorNodeSeparateColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
		NTPNodeSetting("ycc_mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'CompositorNodeSeparateXYZ' : [],

	'CompositorNodeSetAlpha' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'CompositorNodeSplit' : [
		NTPNodeSetting("axis", ST.ENUM, min_version=(4, 1, 0)),
		NTPNodeSetting("factor", ST.INT, min_version=(4, 1, 0)),
	],

	'CompositorNodeSplitViewer' : [
		NTPNodeSetting("axis", ST.ENUM, max_version=(4, 1, 0)),
		NTPNodeSetting("factor", ST.INT, max_version=(4, 1, 0)),
	],

	'CompositorNodeStabilize' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
		NTPNodeSetting("filter_type", ST.ENUM),
		NTPNodeSetting("invert", ST.BOOL),
	],

	'CompositorNodeSunBeams' : [
		NTPNodeSetting("ray_length", ST.FLOAT),
		NTPNodeSetting("source", ST.VEC2),
	],

	'CompositorNodeSwitch' : [
		NTPNodeSetting("check", ST.BOOL),
	],

	'CompositorNodeSwitchView' : [],

	'CompositorNodeTexture' : [
		NTPNodeSetting("node_output", ST.INT),
		NTPNodeSetting("texture", ST.TEXTURE),
	],

	'CompositorNodeTime' : [
		NTPNodeSetting("curve", ST.CURVE_MAPPING),
		NTPNodeSetting("frame_end", ST.INT),
		NTPNodeSetting("frame_start", ST.INT),
	],

	'CompositorNodeTonemap' : [
		NTPNodeSetting("adaptation", ST.FLOAT),
		NTPNodeSetting("contrast", ST.FLOAT),
		NTPNodeSetting("correction", ST.FLOAT),
		NTPNodeSetting("gamma", ST.FLOAT),
		NTPNodeSetting("intensity", ST.FLOAT),
		NTPNodeSetting("key", ST.FLOAT),
		NTPNodeSetting("offset", ST.FLOAT),
		NTPNodeSetting("tonemap_type", ST.ENUM),
	],

	'CompositorNodeTrackPos' : [
		NTPNodeSetting("clip", ST.MOVIE_CLIP),
		NTPNodeSetting("frame_relative", ST.INT),
		NTPNodeSetting("position", ST.ENUM),
		NTPNodeSetting("track_name", ST.STRING),
		NTPNodeSetting("tracking_object", ST.STRING),
	],

	'CompositorNodeTransform' : [
		NTPNodeSetting("filter_type", ST.ENUM),
	],

	'CompositorNodeTranslate' : [
		NTPNodeSetting("use_relative", ST.BOOL),
		NTPNodeSetting("wrap_axis", ST.ENUM),
	],

	'CompositorNodeValToRGB' : [
		NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
	],

	'CompositorNodeValue' : [],

	'CompositorNodeVecBlur' : [
		NTPNodeSetting("factor", ST.FLOAT),
		NTPNodeSetting("samples", ST.INT),
		NTPNodeSetting("speed_max", ST.INT),
		NTPNodeSetting("speed_min", ST.INT),
		NTPNodeSetting("use_curved", ST.BOOL),
	],

	'CompositorNodeViewer' : [
		NTPNodeSetting("center_x", ST.FLOAT),
		NTPNodeSetting("center_y", ST.FLOAT),
		NTPNodeSetting("tile_order", ST.ENUM),
		NTPNodeSetting("use_alpha", ST.BOOL),
	],

	'CompositorNodeZcombine' : [
		NTPNodeSetting("use_alpha", ST.BOOL),
		NTPNodeSetting("use_antialias_z", ST.BOOL),
	],

	'FunctionNodeAlignEulerToVector' : [
		NTPNodeSetting("axis", ST.ENUM),
		NTPNodeSetting("pivot_axis", ST.ENUM),
	],

	'FunctionNodeAxisAngleToRotation' : [],

	'FunctionNodeBooleanMath' : [
		NTPNodeSetting("operation", ST.ENUM),
	],

	'FunctionNodeCombineColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'FunctionNodeCompare' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("operation", ST.ENUM, min_version=(3, 1, 0)),
	],

	'FunctionNodeCompareFloats' : [
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 1, 0)),
	],

	'FunctionNodeEulerToRotation' : [],

	'FunctionNodeFloatToInt' : [
		NTPNodeSetting("rounding_mode", ST.ENUM),
	],

	'FunctionNodeInputBool' : [
		NTPNodeSetting("boolean", ST.BOOL),
	],

	'FunctionNodeInputColor' : [
		NTPNodeSetting("color", ST.VEC4),
	],

	'FunctionNodeInputInt' : [
		NTPNodeSetting("integer", ST.INT),
	],

	'FunctionNodeInputSpecialCharacters' : [],

	'FunctionNodeInputString' : [
		NTPNodeSetting("string", ST.STRING),
	],

	'FunctionNodeInputVector' : [
		NTPNodeSetting("vector", ST.VEC3),
	],

	'FunctionNodeInvertRotation' : [],

	'FunctionNodeLegacyRandomFloat' : [],

	'FunctionNodeQuaternionToRotation' : [],

	'FunctionNodeRandomValue' : [
		NTPNodeSetting("data_type", ST.ENUM),
	],

	'FunctionNodeReplaceString' : [],

	'FunctionNodeRotateEuler' : [
		NTPNodeSetting("rotation_type", ST.ENUM, min_version=(4, 1, 0)),
		NTPNodeSetting("space", ST.ENUM),
		NTPNodeSetting("type", ST.ENUM, max_version=(4, 1, 0)),
	],

	'FunctionNodeRotateRotation' : [
		NTPNodeSetting("rotation_space", ST.ENUM, min_version=(4, 1, 0)),
	],

	'FunctionNodeRotateVector' : [],

	'FunctionNodeRotationToAxisAngle' : [],

	'FunctionNodeRotationToEuler' : [],

	'FunctionNodeRotationToQuaternion' : [],

	'FunctionNodeSeparateColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'FunctionNodeSliceString' : [],

	'FunctionNodeStringLength' : [],

	'FunctionNodeValueToString' : [],

	'GeometryNodeAccumulateField' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeAttributeDomainSize' : [
		NTPNodeSetting("component", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeAttributeRemove' : [],

	'GeometryNodeAttributeStatistic' : [
		NTPNodeSetting("data_type", ST.ENUM),
		NTPNodeSetting("domain", ST.ENUM),
	],

	'GeometryNodeAttributeTransfer' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 4, 0)),
		NTPNodeSetting("domain", ST.ENUM, max_version=(3, 4, 0)),
		NTPNodeSetting("mapping", ST.ENUM, max_version=(3, 4, 0)),
	],

	'GeometryNodeBake' : [
		NTPNodeSetting("active_index", ST.INT, min_version=(4, 1, 0)),
		NTPNodeSetting("bake_items", ST.BAKE_ITEMS, min_version=(4, 1, 0)),
	],

	'GeometryNodeBlurAttribute' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 5, 0)),
	],

	'GeometryNodeBoundBox' : [],

	'GeometryNodeCaptureAttribute' : [
		NTPNodeSetting("data_type", ST.ENUM),
		NTPNodeSetting("domain", ST.ENUM),
	],

	'GeometryNodeCollectionInfo' : [
		NTPNodeSetting("transform_space", ST.ENUM),
	],

	'GeometryNodeConvexHull' : [],

	'GeometryNodeCornersOfEdge' : [],

	'GeometryNodeCornersOfFace' : [],

	'GeometryNodeCornersOfVertex' : [],

	'GeometryNodeCurveArc' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeCurveEndpointSelection' : [],

	'GeometryNodeCurveHandleTypeSelection' : [
		NTPNodeSetting("handle_type", ST.ENUM),
		NTPNodeSetting("mode", ST.ENUM_SET),
	],

	'GeometryNodeCurveLength' : [],

	'GeometryNodeCurveOfPoint' : [],

	'GeometryNodeCurveParameter' : [],

	'GeometryNodeCurvePrimitiveBezierSegment' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeCurvePrimitiveCircle' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeCurvePrimitiveLine' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeCurvePrimitiveQuadrilateral' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeCurveQuadraticBezier' : [],

	'GeometryNodeCurveSetHandles' : [
		NTPNodeSetting("handle_type", ST.ENUM),
		NTPNodeSetting("mode", ST.ENUM_SET),
	],

	'GeometryNodeCurveSpiral' : [],

	'GeometryNodeCurveSplineType' : [
		NTPNodeSetting("spline_type", ST.ENUM),
	],

	'GeometryNodeCurveStar' : [],

	'GeometryNodeCurveToMesh' : [],

	'GeometryNodeCurveToPoints' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeCustomGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'GeometryNodeDeformCurvesOnSurface' : [],

	'GeometryNodeDeleteGeometry' : [
		NTPNodeSetting("domain", ST.ENUM),
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeDistributePointsInVolume' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeDistributePointsOnFaces' : [
		NTPNodeSetting("distribute_method", ST.ENUM),
		NTPNodeSetting("use_legacy_normal", ST.BOOL, min_version=(3, 5, 0)),
	],

	'GeometryNodeDualMesh' : [],

	'GeometryNodeDuplicateElements' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 2, 0)),
	],

	'GeometryNodeEdgePathsToCurves' : [],

	'GeometryNodeEdgePathsToSelection' : [],

	'GeometryNodeEdgesOfCorner' : [],

	'GeometryNodeEdgesOfVertex' : [],

	'GeometryNodeEdgesToFaceGroups' : [],

	'GeometryNodeExtrudeMesh' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeFaceOfCorner' : [],

	'GeometryNodeFieldAtIndex' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeFieldOnDomain' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 3, 0)),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 3, 0)),
	],

	'GeometryNodeFillCurve' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeFilletCurve' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeFlipFaces' : [],

	'GeometryNodeGeometryToInstance' : [],

	'GeometryNodeGetNamedGrid' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(4, 1, 0)),
	],

	'GeometryNodeGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'GeometryNodeImageInfo' : [],

	'GeometryNodeImageTexture' : [
		NTPNodeSetting("extension", ST.ENUM),
		NTPNodeSetting("interpolation", ST.ENUM),
	],

	'GeometryNodeIndexOfNearest' : [],

	'GeometryNodeIndexSwitch' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(4, 1, 0)),
		NTPNodeSetting("index_switch_items", ST.INDEX_SWITCH_ITEMS, min_version=(4, 1, 0)),
	],

	'GeometryNodeInputActiveCamera' : [],

	'GeometryNodeInputCurveHandlePositions' : [],

	'GeometryNodeInputCurveTilt' : [],

	'GeometryNodeInputEdgeSmooth' : [],

	'GeometryNodeInputID' : [],

	'GeometryNodeInputImage' : [
		NTPNodeSetting("image", ST.IMAGE, min_version=(3, 5, 0)),
	],

	'GeometryNodeInputIndex' : [],

	'GeometryNodeInputInstanceRotation' : [],

	'GeometryNodeInputInstanceScale' : [],

	'GeometryNodeInputMaterial' : [
		NTPNodeSetting("material", ST.MATERIAL),
	],

	'GeometryNodeInputMaterialIndex' : [],

	'GeometryNodeInputMeshEdgeAngle' : [],

	'GeometryNodeInputMeshEdgeNeighbors' : [],

	'GeometryNodeInputMeshEdgeVertices' : [],

	'GeometryNodeInputMeshFaceArea' : [],

	'GeometryNodeInputMeshFaceIsPlanar' : [],

	'GeometryNodeInputMeshFaceNeighbors' : [],

	'GeometryNodeInputMeshIsland' : [],

	'GeometryNodeInputMeshVertexNeighbors' : [],

	'GeometryNodeInputNamedAttribute' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 2, 0)),
	],

	'GeometryNodeInputNamedLayerSelection' : [],

	'GeometryNodeInputNormal' : [],

	'GeometryNodeInputPosition' : [],

	'GeometryNodeInputRadius' : [],

	'GeometryNodeInputSceneTime' : [],

	'GeometryNodeInputShadeSmooth' : [],

	'GeometryNodeInputShortestEdgePaths' : [],

	'GeometryNodeInputSignedDistance' : [],

	'GeometryNodeInputSplineCyclic' : [],

	'GeometryNodeInputSplineResolution' : [],

	'GeometryNodeInputTangent' : [],

	'GeometryNodeInstanceOnPoints' : [],

	'GeometryNodeInstancesToPoints' : [],

	'GeometryNodeInterpolateCurves' : [],

	'GeometryNodeIsViewport' : [],

	'GeometryNodeJoinGeometry' : [],

	'GeometryNodeLegacyAlignRotationToVector' : [
		NTPNodeSetting("axis", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_factor", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_vector", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("pivot_axis", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeClamp' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeColorRamp' : [
		NTPNodeSetting("color_ramp", ST.COLOR_RAMP, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeCombineXYZ' : [
		NTPNodeSetting("input_type_x", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_y", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_z", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeCompare' : [
		NTPNodeSetting("input_type_a", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_b", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeConvert' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("domain", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeCurveMap' : [
		NTPNodeSetting("curve_rgb", ST.CURVE_MAPPING, max_version=(3, 2, 0)),
		NTPNodeSetting("curve_vec", ST.CURVE_MAPPING, max_version=(3, 2, 0)),
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeFill' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("domain", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeMapRange' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("interpolation_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeMath' : [
		NTPNodeSetting("input_type_a", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_b", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_c", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeMix' : [
		NTPNodeSetting("blend_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_a", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_b", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_factor", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeProximity' : [
		NTPNodeSetting("target_geometry_element", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeRandomize' : [
		NTPNodeSetting("data_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeSampleTexture' : [],

	'GeometryNodeLegacyAttributeSeparateXYZ' : [
		NTPNodeSetting("input_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeTransfer' : [
		NTPNodeSetting("domain", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("mapping", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeVectorMath' : [
		NTPNodeSetting("input_type_a", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_b", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_c", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("operation", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyAttributeVectorRotate' : [
		NTPNodeSetting("input_type_angle", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_axis", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_center", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_rotation", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_vector", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("rotation_mode", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyCurveEndpoints' : [],

	'GeometryNodeLegacyCurveReverse' : [],

	'GeometryNodeLegacyCurveSelectHandles' : [
		NTPNodeSetting("handle_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("mode", ST.ENUM_SET, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyCurveSetHandles' : [
		NTPNodeSetting("handle_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("mode", ST.ENUM_SET, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyCurveSplineType' : [
		NTPNodeSetting("spline_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyCurveSubdivide' : [
		NTPNodeSetting("cuts_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyCurveToPoints' : [
		NTPNodeSetting("mode", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyDeleteGeometry' : [],

	'GeometryNodeLegacyEdgeSplit' : [],

	'GeometryNodeLegacyMaterialAssign' : [],

	'GeometryNodeLegacyMeshToCurve' : [],

	'GeometryNodeLegacyPointDistribute' : [
		NTPNodeSetting("distribute_method", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyPointInstance' : [
		NTPNodeSetting("instance_type", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("use_whole_collection", ST.BOOL, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyPointScale' : [
		NTPNodeSetting("input_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyPointSeparate' : [],

	'GeometryNodeLegacyPointTranslate' : [
		NTPNodeSetting("input_type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyPointsToVolume' : [
		NTPNodeSetting("input_type_radius", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("resolution_mode", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyRaycast' : [
		NTPNodeSetting("input_type_ray_direction", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_ray_length", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("mapping", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyRotatePoints' : [
		NTPNodeSetting("input_type_angle", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_axis", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("input_type_rotation", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("space", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("type", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacySelectByMaterial' : [],

	'GeometryNodeLegacySubdivisionSurface' : [
		NTPNodeSetting("boundary_smooth", ST.ENUM, max_version=(3, 2, 0)),
		NTPNodeSetting("uv_smooth", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeLegacyVolumeToMesh' : [
		NTPNodeSetting("resolution_mode", ST.ENUM, max_version=(3, 2, 0)),
	],

	'GeometryNodeMaterialSelection' : [],

	'GeometryNodeMeanFilterSDFVolume' : [],

	'GeometryNodeMenuSwitch' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(4, 1, 0)),
		NTPNodeSetting("enum_definition", ST.ENUM_DEFINITION, min_version=(4, 1, 0)),
	],

	'GeometryNodeMergeByDistance' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 2, 0)),
	],

	'GeometryNodeMeshBoolean' : [
		NTPNodeSetting("operation", ST.ENUM),
	],

	'GeometryNodeMeshCircle' : [
		NTPNodeSetting("fill_type", ST.ENUM),
	],

	'GeometryNodeMeshCone' : [
		NTPNodeSetting("fill_type", ST.ENUM),
	],

	'GeometryNodeMeshCube' : [],

	'GeometryNodeMeshCylinder' : [
		NTPNodeSetting("fill_type", ST.ENUM),
	],

	'GeometryNodeMeshFaceSetBoundaries' : [],

	'GeometryNodeMeshGrid' : [],

	'GeometryNodeMeshIcoSphere' : [],

	'GeometryNodeMeshLine' : [
		NTPNodeSetting("count_mode", ST.ENUM),
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeMeshToCurve' : [],

	'GeometryNodeMeshToPoints' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeMeshToSDFVolume' : [
		NTPNodeSetting("resolution_mode", ST.ENUM, min_version=(3, 6, 0), max_version=(4, 1, 0)),
	],

	'GeometryNodeMeshToVolume' : [
		NTPNodeSetting("resolution_mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'GeometryNodeMeshUVSphere' : [],

	'GeometryNodeObjectInfo' : [
		NTPNodeSetting("transform_space", ST.ENUM),
	],

	'GeometryNodeOffsetCornerInFace' : [],

	'GeometryNodeOffsetPointInCurve' : [],

	'GeometryNodeOffsetSDFVolume' : [],

	'GeometryNodePoints' : [],

	'GeometryNodePointsOfCurve' : [],

	'GeometryNodePointsToCurves' : [],

	'GeometryNodePointsToSDFVolume' : [
		NTPNodeSetting("resolution_mode", ST.ENUM, min_version=(3, 6, 0), max_version=(4, 1, 0)),
	],

	'GeometryNodePointsToVertices' : [],

	'GeometryNodePointsToVolume' : [
		NTPNodeSetting("resolution_mode", ST.ENUM),
	],

	'GeometryNodeProximity' : [
		NTPNodeSetting("target_element", ST.ENUM),
	],

	'GeometryNodeRaycast' : [
		NTPNodeSetting("data_type", ST.ENUM),
		NTPNodeSetting("mapping", ST.ENUM),
	],

	'GeometryNodeRealizeInstances' : [
		NTPNodeSetting("legacy_behavior", ST.BOOL, min_version=(3, 1, 0), max_version=(4, 0, 0)),
	],

	'GeometryNodeRemoveAttribute' : [],

	'GeometryNodeRepeatInput' : [],

	'GeometryNodeRepeatOutput' : [
		NTPNodeSetting("active_index", ST.INT, min_version=(4, 0, 0)),
		NTPNodeSetting("inspection_index", ST.INT, min_version=(4, 0, 0)),
		NTPNodeSetting("repeat_items", ST.REPEAT_OUTPUT_ITEMS, min_version=(4, 0, 0)),
	],

	'GeometryNodeReplaceMaterial' : [],

	'GeometryNodeResampleCurve' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeReverseCurve' : [],

	'GeometryNodeRotateInstances' : [],

	'GeometryNodeSDFVolumeSphere' : [],

	'GeometryNodeSampleCurve' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 4, 0)),
		NTPNodeSetting("mode", ST.ENUM),
		NTPNodeSetting("use_all_curves", ST.BOOL, min_version=(3, 4, 0)),
	],

	'GeometryNodeSampleIndex' : [
		NTPNodeSetting("clamp", ST.BOOL, min_version=(3, 4, 0)),
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 4, 0)),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeSampleNearest' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeSampleNearestSurface' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeSampleUVSurface' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeSampleVolume' : [
		NTPNodeSetting("grid_type", ST.ENUM, min_version=(3, 6, 0), max_version=(4, 1, 0)),
		NTPNodeSetting("interpolation_mode", ST.ENUM, min_version=(3, 6, 0), max_version=(4, 1, 0)),
	],

	'GeometryNodeScaleElements' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("scale_mode", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeScaleInstances' : [],

	'GeometryNodeSelfObject' : [],

	'GeometryNodeSeparateComponents' : [],

	'GeometryNodeSeparateGeometry' : [
		NTPNodeSetting("domain", ST.ENUM),
	],

	'GeometryNodeSetCurveHandlePositions' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeSetCurveNormal' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeSetCurveRadius' : [],

	'GeometryNodeSetCurveTilt' : [],

	'GeometryNodeSetID' : [],

	'GeometryNodeSetMaterial' : [],

	'GeometryNodeSetMaterialIndex' : [],

	'GeometryNodeSetPointRadius' : [],

	'GeometryNodeSetPosition' : [],

	'GeometryNodeSetShadeSmooth' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(4, 0, 0)),
	],

	'GeometryNodeSetSplineCyclic' : [],

	'GeometryNodeSetSplineResolution' : [],

	'GeometryNodeSimulationInput' : [],

	'GeometryNodeSimulationOutput' : [
		NTPNodeSetting("active_index", ST.INT, min_version=(3, 6, 0)),
		NTPNodeSetting("state_items", ST.SIM_OUTPUT_ITEMS, min_version=(3, 6, 0)),
	],

	'GeometryNodeSortElements' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(4, 1, 0)),
	],

	'GeometryNodeSplineLength' : [],

	'GeometryNodeSplineParameter' : [],

	'GeometryNodeSplitEdges' : [],

	'GeometryNodeSplitToInstances' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(4, 1, 0)),
	],

	'GeometryNodeStoreNamedAttribute' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 2, 0)),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 2, 0)),
	],

	'GeometryNodeStoreNamedGrid' : [
		NTPNodeSetting("data_type", ST.ENUM, min_version=(4, 1, 0)),
	],

	'GeometryNodeStringJoin' : [],

	'GeometryNodeStringToCurves' : [
		NTPNodeSetting("align_x", ST.ENUM),
		NTPNodeSetting("align_y", ST.ENUM),
		NTPNodeSetting("font", ST.FONT),
		NTPNodeSetting("overflow", ST.ENUM),
		NTPNodeSetting("pivot_mode", ST.ENUM, min_version=(3, 1, 0)),
	],

	'GeometryNodeSubdivideCurve' : [],

	'GeometryNodeSubdivideMesh' : [],

	'GeometryNodeSubdivisionSurface' : [
		NTPNodeSetting("boundary_smooth", ST.ENUM),
		NTPNodeSetting("uv_smooth", ST.ENUM),
	],

	'GeometryNodeSwitch' : [
		NTPNodeSetting("input_type", ST.ENUM),
	],

	'GeometryNodeTool3DCursor' : [],

	'GeometryNodeToolFaceSet' : [],

	'GeometryNodeToolSelection' : [],

	'GeometryNodeToolSetFaceSet' : [],

	'GeometryNodeToolSetSelection' : [
		NTPNodeSetting("domain", ST.ENUM, min_version=(4, 0, 0)),
	],

	'GeometryNodeTransform' : [],

	'GeometryNodeTranslateInstances' : [],

	'GeometryNodeTriangulate' : [
		NTPNodeSetting("ngon_method", ST.ENUM),
		NTPNodeSetting("quad_method", ST.ENUM),
	],

	'GeometryNodeTrimCurve' : [
		NTPNodeSetting("mode", ST.ENUM),
	],

	'GeometryNodeUVPackIslands' : [],

	'GeometryNodeUVUnwrap' : [
		NTPNodeSetting("method", ST.ENUM, min_version=(3, 3, 0)),
	],

	'GeometryNodeVertexOfCorner' : [],

	'GeometryNodeViewer' : [
		NTPNodeSetting("data_type", ST.ENUM),
		NTPNodeSetting("domain", ST.ENUM, min_version=(3, 4, 0)),
	],

	'GeometryNodeVolumeCube' : [],

	'GeometryNodeVolumeToMesh' : [
		NTPNodeSetting("resolution_mode", ST.ENUM),
	],

	'NodeFrame' : [
		NTPNodeSetting("label_size", ST.INT),
		NTPNodeSetting("shrink", ST.BOOL),
		NTPNodeSetting("text", ST.TEXT),
	],

	'NodeGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'NodeGroupInput' : [],

	'NodeGroupOutput' : [
		NTPNodeSetting("is_active_output", ST.BOOL),
	],

	'NodeReroute' : [],

	'ShaderNodeAddShader' : [],

	'ShaderNodeAmbientOcclusion' : [
		NTPNodeSetting("inside", ST.BOOL),
		NTPNodeSetting("only_local", ST.BOOL),
		NTPNodeSetting("samples", ST.INT),
	],

	'ShaderNodeAttribute' : [
		NTPNodeSetting("attribute_name", ST.STRING),
		NTPNodeSetting("attribute_type", ST.ENUM),
	],

	'ShaderNodeBackground' : [],

	'ShaderNodeBevel' : [
		NTPNodeSetting("samples", ST.INT),
	],

	'ShaderNodeBlackbody' : [],

	'ShaderNodeBrightContrast' : [],

	'ShaderNodeBsdfAnisotropic' : [
		NTPNodeSetting("distribution", ST.ENUM),
	],

	'ShaderNodeBsdfDiffuse' : [],

	'ShaderNodeBsdfGlass' : [
		NTPNodeSetting("distribution", ST.ENUM),
	],

	'ShaderNodeBsdfGlossy' : [
		NTPNodeSetting("distribution", ST.ENUM, max_version=(4, 0, 0)),
	],

	'ShaderNodeBsdfHair' : [
		NTPNodeSetting("component", ST.ENUM),
	],

	'ShaderNodeBsdfHairPrincipled' : [
		NTPNodeSetting("model", ST.ENUM, min_version=(4, 0, 0)),
		NTPNodeSetting("parametrization", ST.ENUM),
	],

	'ShaderNodeBsdfPrincipled' : [
		NTPNodeSetting("distribution", ST.ENUM),
		NTPNodeSetting("subsurface_method", ST.ENUM),
	],

	'ShaderNodeBsdfRefraction' : [
		NTPNodeSetting("distribution", ST.ENUM),
	],

	'ShaderNodeBsdfSheen' : [
		NTPNodeSetting("distribution", ST.ENUM, min_version=(4, 0, 0)),
	],

	'ShaderNodeBsdfToon' : [
		NTPNodeSetting("component", ST.ENUM),
	],

	'ShaderNodeBsdfTranslucent' : [],

	'ShaderNodeBsdfTransparent' : [],

	'ShaderNodeBsdfVelvet' : [],

	'ShaderNodeBump' : [
		NTPNodeSetting("invert", ST.BOOL),
	],

	'ShaderNodeCameraData' : [],

	'ShaderNodeClamp' : [
		NTPNodeSetting("clamp_type", ST.ENUM),
	],

	'ShaderNodeCombineColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'ShaderNodeCombineHSV' : [],

	'ShaderNodeCombineRGB' : [],

	'ShaderNodeCombineXYZ' : [],

	'ShaderNodeCustomGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'ShaderNodeDisplacement' : [
		NTPNodeSetting("space", ST.ENUM),
	],

	'ShaderNodeEeveeSpecular' : [],

	'ShaderNodeEmission' : [],

	'ShaderNodeFloatCurve' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'ShaderNodeFresnel' : [],

	'ShaderNodeGamma' : [],

	'ShaderNodeGroup' : [
		NTPNodeSetting("node_tree", ST.NODE_TREE),
	],

	'ShaderNodeHairInfo' : [],

	'ShaderNodeHoldout' : [],

	'ShaderNodeHueSaturation' : [],

	'ShaderNodeInvert' : [],

	'ShaderNodeLayerWeight' : [],

	'ShaderNodeLightFalloff' : [],

	'ShaderNodeLightPath' : [],

	'ShaderNodeMapRange' : [
		NTPNodeSetting("clamp", ST.BOOL),
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 1, 0)),
		NTPNodeSetting("interpolation_type", ST.ENUM),
	],

	'ShaderNodeMapping' : [
		NTPNodeSetting("vector_type", ST.ENUM),
	],

	'ShaderNodeMath' : [
		NTPNodeSetting("operation", ST.ENUM),
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'ShaderNodeMix' : [
		NTPNodeSetting("blend_type", ST.ENUM, min_version=(3, 4, 0)),
		NTPNodeSetting("clamp_factor", ST.BOOL, min_version=(3, 4, 0)),
		NTPNodeSetting("clamp_result", ST.BOOL, min_version=(3, 4, 0)),
		NTPNodeSetting("data_type", ST.ENUM, min_version=(3, 4, 0)),
		NTPNodeSetting("factor_mode", ST.ENUM, min_version=(3, 4, 0)),
	],

	'ShaderNodeMixRGB' : [
		NTPNodeSetting("blend_type", ST.ENUM),
		NTPNodeSetting("use_alpha", ST.BOOL),
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'ShaderNodeMixShader' : [],

	'ShaderNodeNewGeometry' : [],

	'ShaderNodeNormal' : [],

	'ShaderNodeNormalMap' : [
		NTPNodeSetting("space", ST.ENUM),
		NTPNodeSetting("uv_map", ST.STRING),
	],

	'ShaderNodeObjectInfo' : [],

	'ShaderNodeOutputAOV' : [
		NTPNodeSetting("name", ST.STRING),
	],

	'ShaderNodeOutputLight' : [
		NTPNodeSetting("is_active_output", ST.BOOL),
		NTPNodeSetting("target", ST.ENUM),
	],

	'ShaderNodeOutputLineStyle' : [
		NTPNodeSetting("blend_type", ST.ENUM),
		NTPNodeSetting("is_active_output", ST.BOOL),
		NTPNodeSetting("target", ST.ENUM),
		NTPNodeSetting("use_alpha", ST.BOOL),
		NTPNodeSetting("use_clamp", ST.BOOL),
	],

	'ShaderNodeOutputMaterial' : [
		NTPNodeSetting("is_active_output", ST.BOOL),
		NTPNodeSetting("target", ST.ENUM),
	],

	'ShaderNodeOutputWorld' : [
		NTPNodeSetting("is_active_output", ST.BOOL),
		NTPNodeSetting("target", ST.ENUM),
	],

	'ShaderNodeParticleInfo' : [],

	'ShaderNodePointInfo' : [],

	'ShaderNodeRGB' : [],

	'ShaderNodeRGBCurve' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'ShaderNodeRGBToBW' : [],

	'ShaderNodeScript' : [
		NTPNodeSetting("bytecode", ST.STRING),
		NTPNodeSetting("bytecode_hash", ST.STRING),
		NTPNodeSetting("filepath", ST.STRING),
		NTPNodeSetting("mode", ST.ENUM),
		NTPNodeSetting("script", ST.TEXT),
		NTPNodeSetting("use_auto_update", ST.BOOL),
	],

	'ShaderNodeSeparateColor' : [
		NTPNodeSetting("mode", ST.ENUM, min_version=(3, 3, 0)),
	],

	'ShaderNodeSeparateHSV' : [],

	'ShaderNodeSeparateRGB' : [],

	'ShaderNodeSeparateXYZ' : [],

	'ShaderNodeShaderToRGB' : [],

	'ShaderNodeSqueeze' : [],

	'ShaderNodeSubsurfaceScattering' : [
		NTPNodeSetting("falloff", ST.ENUM),
	],

	'ShaderNodeTangent' : [
		NTPNodeSetting("axis", ST.ENUM),
		NTPNodeSetting("direction_type", ST.ENUM),
		NTPNodeSetting("uv_map", ST.STRING),
	],

	'ShaderNodeTexBrick' : [
		NTPNodeSetting("offset", ST.FLOAT),
		NTPNodeSetting("offset_frequency", ST.INT),
		NTPNodeSetting("squash", ST.FLOAT),
		NTPNodeSetting("squash_frequency", ST.INT),
	],

	'ShaderNodeTexChecker' : [],

	'ShaderNodeTexCoord' : [
		NTPNodeSetting("from_instancer", ST.BOOL),
		NTPNodeSetting("object", ST.OBJECT),
	],

	'ShaderNodeTexEnvironment' : [
		NTPNodeSetting("image", ST.IMAGE),
		NTPNodeSetting("image_user", ST.IMAGE_USER),
		NTPNodeSetting("interpolation", ST.ENUM),
		NTPNodeSetting("projection", ST.ENUM),
	],

	'ShaderNodeTexGradient' : [
		NTPNodeSetting("gradient_type", ST.ENUM),
	],

	'ShaderNodeTexIES' : [
		NTPNodeSetting("filepath", ST.STRING),
		NTPNodeSetting("ies", ST.TEXT),
		NTPNodeSetting("mode", ST.ENUM),
	],

	'ShaderNodeTexImage' : [
		NTPNodeSetting("extension", ST.ENUM),
		NTPNodeSetting("image", ST.IMAGE),
		NTPNodeSetting("image_user", ST.IMAGE_USER),
		NTPNodeSetting("interpolation", ST.ENUM),
		NTPNodeSetting("projection", ST.ENUM),
		NTPNodeSetting("projection_blend", ST.FLOAT),
	],

	'ShaderNodeTexMagic' : [
		NTPNodeSetting("turbulence_depth", ST.INT),
	],

	'ShaderNodeTexMusgrave' : [
		NTPNodeSetting("musgrave_dimensions", ST.ENUM, max_version=(4, 1, 0)),
		NTPNodeSetting("musgrave_type", ST.ENUM, max_version=(4, 1, 0)),
	],

	'ShaderNodeTexNoise' : [
		NTPNodeSetting("noise_dimensions", ST.ENUM),
		NTPNodeSetting("noise_type", ST.ENUM, min_version=(4, 1, 0)),
		NTPNodeSetting("normalize", ST.BOOL, min_version=(4, 0, 0)),
	],

	'ShaderNodeTexPointDensity' : [
		NTPNodeSetting("interpolation", ST.ENUM),
		NTPNodeSetting("object", ST.OBJECT),
		NTPNodeSetting("particle_color_source", ST.ENUM),
		NTPNodeSetting("particle_system", ST.PARTICLE_SYSTEM),
		NTPNodeSetting("point_source", ST.ENUM),
		NTPNodeSetting("radius", ST.FLOAT),
		NTPNodeSetting("resolution", ST.INT),
		NTPNodeSetting("space", ST.ENUM),
		NTPNodeSetting("vertex_attribute_name", ST.STRING),
		NTPNodeSetting("vertex_color_source", ST.ENUM),
	],

	'ShaderNodeTexSky' : [
		NTPNodeSetting("air_density", ST.FLOAT),
		NTPNodeSetting("altitude", ST.FLOAT),
		NTPNodeSetting("dust_density", ST.FLOAT),
		NTPNodeSetting("ground_albedo", ST.FLOAT),
		NTPNodeSetting("ozone_density", ST.FLOAT),
		NTPNodeSetting("sky_type", ST.ENUM),
		NTPNodeSetting("sun_direction", ST.VEC3),
		NTPNodeSetting("sun_disc", ST.BOOL),
		NTPNodeSetting("sun_elevation", ST.FLOAT),
		NTPNodeSetting("sun_intensity", ST.FLOAT),
		NTPNodeSetting("sun_rotation", ST.FLOAT),
		NTPNodeSetting("sun_size", ST.FLOAT),
		NTPNodeSetting("turbidity", ST.FLOAT),
	],

	'ShaderNodeTexVoronoi' : [
		NTPNodeSetting("distance", ST.ENUM),
		NTPNodeSetting("feature", ST.ENUM),
		NTPNodeSetting("normalize", ST.BOOL, min_version=(4, 0, 0)),
		NTPNodeSetting("voronoi_dimensions", ST.ENUM),
	],

	'ShaderNodeTexWave' : [
		NTPNodeSetting("bands_direction", ST.ENUM),
		NTPNodeSetting("rings_direction", ST.ENUM),
		NTPNodeSetting("wave_profile", ST.ENUM),
		NTPNodeSetting("wave_type", ST.ENUM),
	],

	'ShaderNodeTexWhiteNoise' : [
		NTPNodeSetting("noise_dimensions", ST.ENUM),
	],

	'ShaderNodeUVAlongStroke' : [
		NTPNodeSetting("use_tips", ST.BOOL),
	],

	'ShaderNodeUVMap' : [
		NTPNodeSetting("from_instancer", ST.BOOL),
		NTPNodeSetting("uv_map", ST.STRING),
	],

	'ShaderNodeValToRGB' : [
		NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
	],

	'ShaderNodeValue' : [],

	'ShaderNodeVectorCurve' : [
		NTPNodeSetting("mapping", ST.CURVE_MAPPING),
	],

	'ShaderNodeVectorDisplacement' : [
		NTPNodeSetting("space", ST.ENUM),
	],

	'ShaderNodeVectorMath' : [
		NTPNodeSetting("operation", ST.ENUM),
	],

	'ShaderNodeVectorRotate' : [
		NTPNodeSetting("invert", ST.BOOL),
		NTPNodeSetting("rotation_type", ST.ENUM),
	],

	'ShaderNodeVectorTransform' : [
		NTPNodeSetting("convert_from", ST.ENUM),
		NTPNodeSetting("convert_to", ST.ENUM),
		NTPNodeSetting("vector_type", ST.ENUM),
	],

	'ShaderNodeVertexColor' : [
		NTPNodeSetting("layer_name", ST.STRING),
	],

	'ShaderNodeVolumeAbsorption' : [],

	'ShaderNodeVolumeInfo' : [],

	'ShaderNodeVolumePrincipled' : [],

	'ShaderNodeVolumeScatter' : [],

	'ShaderNodeWavelength' : [],

	'ShaderNodeWireframe' : [
		NTPNodeSetting("use_pixel_size", ST.BOOL),
	],

}