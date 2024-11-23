from enum import Enum, auto
from typing import NamedTuple

class ST(Enum):
	"""
	Settings Types
	"""
	BOOL = auto()
	COLOR = auto()
	ENUM = auto()
	ENUM_SET = auto()
	EULER = auto()
	FLOAT = auto()
	INT = auto()
	STRING = auto()
	VEC1 = auto()
	VEC2 = auto()
	VEC3 = auto()
	VEC4 = auto()
	BAKE_ITEMS = auto()
	CAPTURE_ATTRIBUTE_ITEMS = auto()
	COLOR_RAMP = auto()
	CURVE_MAPPING = auto()
	ENUM_DEFINITION = auto()
	ENUM_ITEM = auto()
	FOREACH_GEO_ELEMENT_GENERATION_ITEMS = auto()
	FOREACH_GEO_ELEMENT_INPUT_ITEMS = auto()
	FOREACH_GEO_ELEMENT_MAIN_ITEMS = auto()
	INDEX_SWITCH_ITEMS = auto()
	MENU_SWITCH_ITEMS = auto()
	NODE_TREE = auto()
	REPEAT_OUTPUT_ITEMS = auto()
	SIM_OUTPUT_ITEMS = auto()
	IMAGE = auto()
	IMAGE_USER = auto()
	CRYPTOMATTE_ENTRIES = auto()
	FILE_SLOTS = auto()
	FONT = auto()
	IMAGE_FORMAT_SETTINGS = auto()
	LAYER_SLOTS = auto()
	MASK = auto()
	MATERIAL = auto()
	MOVIE_CLIP = auto()
	OBJECT = auto()
	PARTICLE_SYSTEM = auto()
	SCENE = auto()
	TEXT = auto()
	TEXTURE = auto()

class NTPNodeSetting(NamedTuple):
	name_: str
	st_: ST
	min_version_: tuple = (3, 0, 0)
	max_version_: tuple = (4, 4, 0)

class NodeInfo(NamedTuple):
	attributes_: list[NTPNodeSetting]
	min_version_: tuple = (3, 0, 0)
	max_version_: tuple = (4, 4, 0)

node_settings : dict[str, NodeInfo] = {
	'CompositorNodeAlphaOver' : NodeInfo(
		[
			NTPNodeSetting("premul", ST.FLOAT),
			NTPNodeSetting("use_premultiply", ST.BOOL),
		]
	),

	'CompositorNodeAntiAliasing' : NodeInfo(
		[
			NTPNodeSetting("contrast_limit", ST.FLOAT),
			NTPNodeSetting("corner_rounding", ST.FLOAT),
			NTPNodeSetting("threshold", ST.FLOAT),
		]
	),

	'CompositorNodeBilateralblur' : NodeInfo(
		[
			NTPNodeSetting("iterations", ST.INT),
			NTPNodeSetting("sigma_color", ST.FLOAT),
			NTPNodeSetting("sigma_space", ST.FLOAT),
		]
	),

	'CompositorNodeBlur' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeBokehBlur' : NodeInfo(
		[
			NTPNodeSetting("blur_max", ST.FLOAT),
			NTPNodeSetting("use_extended_bounds", ST.BOOL),
			NTPNodeSetting("use_variable_size", ST.BOOL),
		]
	),

	'CompositorNodeBokehImage' : NodeInfo(
		[
			NTPNodeSetting("angle", ST.FLOAT),
			NTPNodeSetting("catadioptric", ST.FLOAT),
			NTPNodeSetting("flaps", ST.INT),
			NTPNodeSetting("rounding", ST.FLOAT),
			NTPNodeSetting("shift", ST.FLOAT),
		]
	),

	'CompositorNodeBoxMask' : NodeInfo(
		[
			NTPNodeSetting("height", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("mask_height", ST.FLOAT, min_version_=(4, 2, 0)),
			NTPNodeSetting("mask_type", ST.ENUM),
			NTPNodeSetting("mask_width", ST.FLOAT, min_version_=(4, 2, 0)),
			NTPNodeSetting("rotation", ST.FLOAT),
			NTPNodeSetting("width", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("x", ST.FLOAT),
			NTPNodeSetting("y", ST.FLOAT),
		]
	),

	'CompositorNodeBrightContrast' : NodeInfo(
		[
			NTPNodeSetting("use_premultiply", ST.BOOL),
		]
	),

	'CompositorNodeChannelMatte' : NodeInfo(
		[
			NTPNodeSetting("color_space", ST.ENUM),
			NTPNodeSetting("limit_channel", ST.ENUM),
			NTPNodeSetting("limit_max", ST.FLOAT),
			NTPNodeSetting("limit_method", ST.ENUM),
			NTPNodeSetting("limit_min", ST.FLOAT),
			NTPNodeSetting("matte_channel", ST.ENUM),
		]
	),

	'CompositorNodeChromaMatte' : NodeInfo(
		[
			NTPNodeSetting("gain", ST.FLOAT),
			NTPNodeSetting("lift", ST.FLOAT),
			NTPNodeSetting("shadow_adjust", ST.FLOAT),
			NTPNodeSetting("threshold", ST.FLOAT),
			NTPNodeSetting("tolerance", ST.FLOAT),
		]
	),

	'CompositorNodeColorBalance' : NodeInfo(
		[
			NTPNodeSetting("correction_method", ST.ENUM),
			NTPNodeSetting("gain", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("gain", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("gamma", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("gamma", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("input_temperature", ST.FLOAT, min_version_=(4, 3, 0)),
			NTPNodeSetting("input_tint", ST.FLOAT, min_version_=(4, 3, 0)),
			NTPNodeSetting("input_whitepoint", ST.COLOR, min_version_=(4, 3, 0)),
			NTPNodeSetting("lift", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("lift", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("offset", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("offset", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("offset_basis", ST.FLOAT),
			NTPNodeSetting("output_temperature", ST.FLOAT, min_version_=(4, 3, 0)),
			NTPNodeSetting("output_tint", ST.FLOAT, min_version_=(4, 3, 0)),
			NTPNodeSetting("output_whitepoint", ST.COLOR, min_version_=(4, 3, 0)),
			NTPNodeSetting("power", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("power", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("slope", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("slope", ST.COLOR, min_version_=(3, 5, 0)),
		]
	),

	'CompositorNodeColorCorrection' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeColorMatte' : NodeInfo(
		[
			NTPNodeSetting("color_hue", ST.FLOAT),
			NTPNodeSetting("color_saturation", ST.FLOAT),
			NTPNodeSetting("color_value", ST.FLOAT),
		]
	),

	'CompositorNodeColorSpill' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM),
			NTPNodeSetting("limit_channel", ST.ENUM),
			NTPNodeSetting("limit_method", ST.ENUM),
			NTPNodeSetting("ratio", ST.FLOAT),
			NTPNodeSetting("unspill_blue", ST.FLOAT),
			NTPNodeSetting("unspill_green", ST.FLOAT),
			NTPNodeSetting("unspill_red", ST.FLOAT),
			NTPNodeSetting("use_unspill", ST.BOOL),
		]
	),

	'CompositorNodeCombHSVA' : NodeInfo(
		[]
	),

	'CompositorNodeCombRGBA' : NodeInfo(
		[]
	),

	'CompositorNodeCombYCCA' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'CompositorNodeCombYUVA' : NodeInfo(
		[]
	),

	'CompositorNodeCombineColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("ycc_mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'CompositorNodeCombineXYZ' : NodeInfo(
		[],
		min_version_ = (3, 2, 0)
	),

	'CompositorNodeComposite' : NodeInfo(
		[
			NTPNodeSetting("use_alpha", ST.BOOL),
		]
	),

	'CompositorNodeConvertColorSpace' : NodeInfo(
		[
			NTPNodeSetting("from_color_space", ST.ENUM),
			NTPNodeSetting("to_color_space", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'CompositorNodeCornerPin' : NodeInfo(
		[]
	),

	'CompositorNodeCrop' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeCryptomatte' : NodeInfo(
		[
			NTPNodeSetting("add", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("add", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("matte_id", ST.STRING),
			NTPNodeSetting("remove", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("remove", ST.COLOR, min_version_=(3, 5, 0)),
		]
	),

	'CompositorNodeCryptomatteV2' : NodeInfo(
		[
			NTPNodeSetting("add", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("add", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("entries", ST.CRYPTOMATTE_ENTRIES),
			NTPNodeSetting("frame_duration", ST.INT),
			NTPNodeSetting("frame_offset", ST.INT),
			NTPNodeSetting("frame_start", ST.INT),
			NTPNodeSetting("image", ST.IMAGE),
			NTPNodeSetting("layer", ST.ENUM),
			NTPNodeSetting("layer_name", ST.ENUM),
			NTPNodeSetting("matte_id", ST.STRING),
			NTPNodeSetting("remove", ST.VEC3, max_version_=(3, 5, 0)),
			NTPNodeSetting("remove", ST.COLOR, min_version_=(3, 5, 0)),
			NTPNodeSetting("scene", ST.SCENE),
			NTPNodeSetting("source", ST.ENUM),
			NTPNodeSetting("use_auto_refresh", ST.BOOL),
			NTPNodeSetting("use_cyclic", ST.BOOL),
			NTPNodeSetting("view", ST.ENUM),
		]
	),

	'CompositorNodeCurveRGB' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'CompositorNodeCurveVec' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'CompositorNodeCustomGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'CompositorNodeDBlur' : NodeInfo(
		[
			NTPNodeSetting("angle", ST.FLOAT),
			NTPNodeSetting("center_x", ST.FLOAT),
			NTPNodeSetting("center_y", ST.FLOAT),
			NTPNodeSetting("distance", ST.FLOAT),
			NTPNodeSetting("iterations", ST.INT),
			NTPNodeSetting("spin", ST.FLOAT),
			NTPNodeSetting("use_wrap", ST.BOOL, max_version_=(3, 5, 0)),
			NTPNodeSetting("zoom", ST.FLOAT),
		]
	),

	'CompositorNodeDefocus' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeDenoise' : NodeInfo(
		[
			NTPNodeSetting("prefilter", ST.ENUM),
			NTPNodeSetting("use_hdr", ST.BOOL),
		]
	),

	'CompositorNodeDespeckle' : NodeInfo(
		[
			NTPNodeSetting("threshold", ST.FLOAT),
			NTPNodeSetting("threshold_neighbor", ST.FLOAT),
		]
	),

	'CompositorNodeDiffMatte' : NodeInfo(
		[
			NTPNodeSetting("falloff", ST.FLOAT),
			NTPNodeSetting("tolerance", ST.FLOAT),
		]
	),

	'CompositorNodeDilateErode' : NodeInfo(
		[
			NTPNodeSetting("distance", ST.INT),
			NTPNodeSetting("edge", ST.FLOAT),
			NTPNodeSetting("falloff", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'CompositorNodeDisplace' : NodeInfo(
		[]
	),

	'CompositorNodeDistanceMatte' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM),
			NTPNodeSetting("falloff", ST.FLOAT),
			NTPNodeSetting("tolerance", ST.FLOAT),
		]
	),

	'CompositorNodeDoubleEdgeMask' : NodeInfo(
		[
			NTPNodeSetting("edge_mode", ST.ENUM),
			NTPNodeSetting("inner_mode", ST.ENUM),
		]
	),

	'CompositorNodeEllipseMask' : NodeInfo(
		[
			NTPNodeSetting("height", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("mask_height", ST.FLOAT, min_version_=(4, 2, 0)),
			NTPNodeSetting("mask_type", ST.ENUM),
			NTPNodeSetting("mask_width", ST.FLOAT, min_version_=(4, 2, 0)),
			NTPNodeSetting("rotation", ST.FLOAT),
			NTPNodeSetting("width", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("x", ST.FLOAT),
			NTPNodeSetting("y", ST.FLOAT),
		]
	),

	'CompositorNodeExposure' : NodeInfo(
		[]
	),

	'CompositorNodeFilter' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM),
		]
	),

	'CompositorNodeFlip' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
		]
	),

	'CompositorNodeGamma' : NodeInfo(
		[]
	),

	'CompositorNodeGlare' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'CompositorNodeHueCorrect' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'CompositorNodeHueSat' : NodeInfo(
		[]
	),

	'CompositorNodeIDMask' : NodeInfo(
		[
			NTPNodeSetting("index", ST.INT),
			NTPNodeSetting("use_antialiasing", ST.BOOL),
		]
	),

	'CompositorNodeImage' : NodeInfo(
		[
			NTPNodeSetting("frame_duration", ST.INT),
			NTPNodeSetting("frame_offset", ST.INT),
			NTPNodeSetting("frame_start", ST.INT),
			NTPNodeSetting("image", ST.IMAGE),
			NTPNodeSetting("layer", ST.ENUM),
			NTPNodeSetting("use_auto_refresh", ST.BOOL),
			NTPNodeSetting("use_cyclic", ST.BOOL),
			NTPNodeSetting("use_straight_alpha_output", ST.BOOL),
			NTPNodeSetting("view", ST.ENUM),
		]
	),

	'CompositorNodeInpaint' : NodeInfo(
		[
			NTPNodeSetting("distance", ST.INT),
		]
	),

	'CompositorNodeInvert' : NodeInfo(
		[
			NTPNodeSetting("invert_alpha", ST.BOOL),
			NTPNodeSetting("invert_rgb", ST.BOOL),
		]
	),

	'CompositorNodeKeying' : NodeInfo(
		[
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
		]
	),

	'CompositorNodeKeyingScreen' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("smoothness", ST.FLOAT, min_version_=(4, 1, 0)),
			NTPNodeSetting("tracking_object", ST.STRING),
		]
	),

	'CompositorNodeKuwahara' : NodeInfo(
		[
			NTPNodeSetting("eccentricity", ST.FLOAT),
			NTPNodeSetting("sharpness", ST.FLOAT),
			NTPNodeSetting("size", ST.INT, max_version_=(4, 1, 0)),
			NTPNodeSetting("uniformity", ST.INT),
			NTPNodeSetting("use_high_precision", ST.BOOL, min_version_=(4, 1, 0)),
			NTPNodeSetting("variation", ST.ENUM),
		],
		min_version_ = (4, 0, 0)
	),

	'CompositorNodeLensdist' : NodeInfo(
		[
			NTPNodeSetting("use_fit", ST.BOOL),
			NTPNodeSetting("use_jitter", ST.BOOL),
			NTPNodeSetting("use_projector", ST.BOOL),
		]
	),

	'CompositorNodeLevels' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM),
		]
	),

	'CompositorNodeLumaMatte' : NodeInfo(
		[
			NTPNodeSetting("limit_max", ST.FLOAT),
			NTPNodeSetting("limit_min", ST.FLOAT),
		]
	),

	'CompositorNodeMapRange' : NodeInfo(
		[
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'CompositorNodeMapUV' : NodeInfo(
		[
			NTPNodeSetting("alpha", ST.INT),
			NTPNodeSetting("filter_type", ST.ENUM, min_version_=(4, 1, 0)),
		]
	),

	'CompositorNodeMapValue' : NodeInfo(
		[
			NTPNodeSetting("max", ST.VEC1),
			NTPNodeSetting("min", ST.VEC1),
			NTPNodeSetting("offset", ST.VEC1),
			NTPNodeSetting("size", ST.VEC1),
			NTPNodeSetting("use_max", ST.BOOL),
			NTPNodeSetting("use_min", ST.BOOL),
		]
	),

	'CompositorNodeMask' : NodeInfo(
		[
			NTPNodeSetting("mask", ST.MASK),
			NTPNodeSetting("motion_blur_samples", ST.INT),
			NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
			NTPNodeSetting("size_source", ST.ENUM),
			NTPNodeSetting("size_x", ST.INT),
			NTPNodeSetting("size_y", ST.INT),
			NTPNodeSetting("use_feather", ST.BOOL),
			NTPNodeSetting("use_motion_blur", ST.BOOL),
		]
	),

	'CompositorNodeMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'CompositorNodeMixRGB' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("use_alpha", ST.BOOL),
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'CompositorNodeMovieClip' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
		]
	),

	'CompositorNodeMovieDistortion' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("distortion_type", ST.ENUM),
		]
	),

	'CompositorNodeNormal' : NodeInfo(
		[]
	),

	'CompositorNodeNormalize' : NodeInfo(
		[]
	),

	'CompositorNodeOutputFile' : NodeInfo(
		[
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("base_path", ST.STRING),
			NTPNodeSetting("file_slots", ST.FILE_SLOTS),
			NTPNodeSetting("format", ST.IMAGE_FORMAT_SETTINGS),
			NTPNodeSetting("layer_slots", ST.LAYER_SLOTS),
			NTPNodeSetting("save_as_render", ST.BOOL, min_version_=(4, 3, 0)),
		]
	),

	'CompositorNodePixelate' : NodeInfo(
		[
			NTPNodeSetting("pixel_size", ST.INT, min_version_=(4, 1, 0)),
		]
	),

	'CompositorNodePlaneTrackDeform' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("motion_blur_samples", ST.INT),
			NTPNodeSetting("motion_blur_shutter", ST.FLOAT),
			NTPNodeSetting("plane_track_name", ST.STRING),
			NTPNodeSetting("tracking_object", ST.STRING),
			NTPNodeSetting("use_motion_blur", ST.BOOL),
		]
	),

	'CompositorNodePosterize' : NodeInfo(
		[]
	),

	'CompositorNodePremulKey' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.ENUM),
		]
	),

	'CompositorNodeRGB' : NodeInfo(
		[]
	),

	'CompositorNodeRGBToBW' : NodeInfo(
		[]
	),

	'CompositorNodeRLayers' : NodeInfo(
		[
			NTPNodeSetting("layer", ST.ENUM),
			NTPNodeSetting("scene", ST.SCENE),
		]
	),

	'CompositorNodeRotate' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM),
		]
	),

	'CompositorNodeScale' : NodeInfo(
		[
			NTPNodeSetting("frame_method", ST.ENUM),
			NTPNodeSetting("offset_x", ST.FLOAT),
			NTPNodeSetting("offset_y", ST.FLOAT),
			NTPNodeSetting("space", ST.ENUM),
		]
	),

	'CompositorNodeSceneTime' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'CompositorNodeSepHSVA' : NodeInfo(
		[]
	),

	'CompositorNodeSepRGBA' : NodeInfo(
		[]
	),

	'CompositorNodeSepYCCA' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'CompositorNodeSepYUVA' : NodeInfo(
		[]
	),

	'CompositorNodeSeparateColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("ycc_mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'CompositorNodeSeparateXYZ' : NodeInfo(
		[],
		min_version_ = (3, 2, 0)
	),

	'CompositorNodeSetAlpha' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'CompositorNodeSplit' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("factor", ST.INT),
		],
		min_version_ = (4, 1, 0)
	),

	'CompositorNodeSplitViewer' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("factor", ST.INT),
		],
		max_version_ = (4, 1, 0)
	),

	'CompositorNodeStabilize' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("filter_type", ST.ENUM),
			NTPNodeSetting("invert", ST.BOOL),
		]
	),

	'CompositorNodeSunBeams' : NodeInfo(
		[
			NTPNodeSetting("ray_length", ST.FLOAT),
			NTPNodeSetting("source", ST.VEC2),
		]
	),

	'CompositorNodeSwitch' : NodeInfo(
		[
			NTPNodeSetting("check", ST.BOOL),
		]
	),

	'CompositorNodeSwitchView' : NodeInfo(
		[]
	),

	'CompositorNodeTexture' : NodeInfo(
		[
			NTPNodeSetting("node_output", ST.INT),
			NTPNodeSetting("texture", ST.TEXTURE),
		]
	),

	'CompositorNodeTime' : NodeInfo(
		[
			NTPNodeSetting("curve", ST.CURVE_MAPPING),
			NTPNodeSetting("frame_end", ST.INT),
			NTPNodeSetting("frame_start", ST.INT),
		]
	),

	'CompositorNodeTonemap' : NodeInfo(
		[
			NTPNodeSetting("adaptation", ST.FLOAT),
			NTPNodeSetting("contrast", ST.FLOAT),
			NTPNodeSetting("correction", ST.FLOAT),
			NTPNodeSetting("gamma", ST.FLOAT),
			NTPNodeSetting("intensity", ST.FLOAT),
			NTPNodeSetting("key", ST.FLOAT),
			NTPNodeSetting("offset", ST.FLOAT),
			NTPNodeSetting("tonemap_type", ST.ENUM),
		]
	),

	'CompositorNodeTrackPos' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("frame_relative", ST.INT),
			NTPNodeSetting("position", ST.ENUM),
			NTPNodeSetting("track_name", ST.STRING),
			NTPNodeSetting("tracking_object", ST.STRING),
		]
	),

	'CompositorNodeTransform' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM),
		]
	),

	'CompositorNodeTranslate' : NodeInfo(
		[
			NTPNodeSetting("interpolation", ST.ENUM, min_version_=(4, 2, 0)),
			NTPNodeSetting("use_relative", ST.BOOL),
			NTPNodeSetting("wrap_axis", ST.ENUM),
		]
	),

	'CompositorNodeValToRGB' : NodeInfo(
		[
			NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
		]
	),

	'CompositorNodeValue' : NodeInfo(
		[]
	),

	'CompositorNodeVecBlur' : NodeInfo(
		[
			NTPNodeSetting("factor", ST.FLOAT),
			NTPNodeSetting("samples", ST.INT),
			NTPNodeSetting("speed_max", ST.INT),
			NTPNodeSetting("speed_min", ST.INT),
			NTPNodeSetting("use_curved", ST.BOOL),
		]
	),

	'CompositorNodeViewer' : NodeInfo(
		[
			NTPNodeSetting("center_x", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("center_y", ST.FLOAT, max_version_=(4, 2, 0)),
			NTPNodeSetting("tile_order", ST.ENUM, max_version_=(4, 2, 0)),
			NTPNodeSetting("use_alpha", ST.BOOL),
		]
	),

	'CompositorNodeZcombine' : NodeInfo(
		[
			NTPNodeSetting("use_alpha", ST.BOOL),
			NTPNodeSetting("use_antialias_z", ST.BOOL),
		]
	),

	'FunctionNodeAlignEulerToVector' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("pivot_axis", ST.ENUM),
		]
	),

	'FunctionNodeAlignRotationToVector' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("pivot_axis", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeAxesToRotation' : NodeInfo(
		[
			NTPNodeSetting("primary_axis", ST.ENUM),
			NTPNodeSetting("secondary_axis", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeAxisAngleToRotation' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeBooleanMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		]
	),

	'FunctionNodeCombineColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'FunctionNodeCombineMatrix' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeCombineTransform' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeCompare' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'FunctionNodeCompareFloats' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 1, 0)
	),

	'FunctionNodeEulerToRotation' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeFloatToInt' : NodeInfo(
		[
			NTPNodeSetting("rounding_mode", ST.ENUM),
		]
	),

	'FunctionNodeHashValue' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'FunctionNodeInputBool' : NodeInfo(
		[
			NTPNodeSetting("boolean", ST.BOOL),
		]
	),

	'FunctionNodeInputColor' : NodeInfo(
		[
			NTPNodeSetting("color", ST.VEC4, max_version_=(4, 2, 0)),
			NTPNodeSetting("value", ST.VEC4, min_version_=(4, 2, 0)),
		]
	),

	'FunctionNodeInputInt' : NodeInfo(
		[
			NTPNodeSetting("integer", ST.INT),
		]
	),

	'FunctionNodeInputRotation' : NodeInfo(
		[
			NTPNodeSetting("rotation_euler", ST.EULER),
		],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeInputSpecialCharacters' : NodeInfo(
		[]
	),

	'FunctionNodeInputString' : NodeInfo(
		[
			NTPNodeSetting("string", ST.STRING),
		]
	),

	'FunctionNodeInputVector' : NodeInfo(
		[
			NTPNodeSetting("vector", ST.VEC3),
		]
	),

	'FunctionNodeIntegerMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'FunctionNodeInvertMatrix' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeInvertRotation' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeLegacyRandomFloat' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'FunctionNodeMatrixDeterminant' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'FunctionNodeMatrixMultiply' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeProjectPoint' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeQuaternionToRotation' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeRandomValue' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'FunctionNodeReplaceString' : NodeInfo(
		[]
	),

	'FunctionNodeRotateEuler' : NodeInfo(
		[
			NTPNodeSetting("rotation_type", ST.ENUM, min_version_=(4, 1, 0)),
			NTPNodeSetting("space", ST.ENUM),
			NTPNodeSetting("type", ST.ENUM, max_version_=(4, 1, 0)),
		]
	),

	'FunctionNodeRotateRotation' : NodeInfo(
		[
			NTPNodeSetting("rotation_space", ST.ENUM),
		],
		min_version_ = (4, 1, 0)
	),

	'FunctionNodeRotateVector' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeRotationToAxisAngle' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeRotationToEuler' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeRotationToQuaternion' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'FunctionNodeSeparateColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'FunctionNodeSeparateMatrix' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeSeparateTransform' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeSliceString' : NodeInfo(
		[]
	),

	'FunctionNodeStringLength' : NodeInfo(
		[]
	),

	'FunctionNodeTransformDirection' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeTransformPoint' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeTransposeMatrix' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'FunctionNodeValueToString' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM, min_version_=(4, 3, 0)),
		]
	),

	'GeometryNodeAccumulateField' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeAttributeDomainSize' : NodeInfo(
		[
			NTPNodeSetting("component", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeAttributeRemove' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeAttributeStatistic' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeAttributeTransfer' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("mapping", ST.ENUM),
		],
		max_version_ = (3, 4, 0)
	),

	'GeometryNodeBake' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("bake_items", ST.BAKE_ITEMS),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeBlurAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (3, 5, 0)
	),

	'GeometryNodeBoundBox' : NodeInfo(
		[]
	),

	'GeometryNodeCaptureAttribute' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT, min_version_=(4, 2, 0)),
			NTPNodeSetting("capture_items", ST.CAPTURE_ATTRIBUTE_ITEMS, min_version_=(4, 2, 0)),
			NTPNodeSetting("data_type", ST.ENUM, max_version_=(4, 2, 0)),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeCollectionInfo' : NodeInfo(
		[
			NTPNodeSetting("transform_space", ST.ENUM),
		]
	),

	'GeometryNodeConvexHull' : NodeInfo(
		[]
	),

	'GeometryNodeCornersOfEdge' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeCornersOfFace' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeCornersOfVertex' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeCurveArc' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeCurveEndpointSelection' : NodeInfo(
		[]
	),

	'GeometryNodeCurveHandleTypeSelection' : NodeInfo(
		[
			NTPNodeSetting("handle_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM_SET),
		]
	),

	'GeometryNodeCurveLength' : NodeInfo(
		[]
	),

	'GeometryNodeCurveOfPoint' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeCurveParameter' : NodeInfo(
		[],
		max_version_ = (3, 1, 0)
	),

	'GeometryNodeCurvePrimitiveBezierSegment' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeCurvePrimitiveCircle' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeCurvePrimitiveLine' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeCurvePrimitiveQuadrilateral' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeCurveQuadraticBezier' : NodeInfo(
		[]
	),

	'GeometryNodeCurveSetHandles' : NodeInfo(
		[
			NTPNodeSetting("handle_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM_SET),
		]
	),

	'GeometryNodeCurveSpiral' : NodeInfo(
		[]
	),

	'GeometryNodeCurveSplineType' : NodeInfo(
		[
			NTPNodeSetting("spline_type", ST.ENUM),
		]
	),

	'GeometryNodeCurveStar' : NodeInfo(
		[]
	),

	'GeometryNodeCurveToMesh' : NodeInfo(
		[]
	),

	'GeometryNodeCurveToPoints' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeCurvesToGreasePencil' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeCustomGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'GeometryNodeDeformCurvesOnSurface' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeDeleteGeometry' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeDistributePointsInGrid' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeDistributePointsInVolume' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeDistributePointsOnFaces' : NodeInfo(
		[
			NTPNodeSetting("distribute_method", ST.ENUM),
			NTPNodeSetting("use_legacy_normal", ST.BOOL, min_version_=(3, 5, 0)),
		]
	),

	'GeometryNodeDualMesh' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeDuplicateElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 2, 0)
	),

	'GeometryNodeEdgePathsToCurves' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeEdgePathsToSelection' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeEdgesOfCorner' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeEdgesOfVertex' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeEdgesToFaceGroups' : NodeInfo(
		[],
		min_version_ = (3, 5, 0)
	),

	'GeometryNodeExtrudeMesh' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeFaceOfCorner' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeFieldAtIndex' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeFieldOnDomain' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeFillCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeFilletCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeFlipFaces' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeForeachGeometryElementInput' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeForeachGeometryElementOutput' : NodeInfo(
		[
			NTPNodeSetting("active_generation_index", ST.INT),
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("active_main_index", ST.INT),
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("generation_items", ST.FOREACH_GEO_ELEMENT_GENERATION_ITEMS),
			NTPNodeSetting("input_items", ST.FOREACH_GEO_ELEMENT_INPUT_ITEMS),
			NTPNodeSetting("inspection_index", ST.INT),
			NTPNodeSetting("main_items", ST.FOREACH_GEO_ELEMENT_MAIN_ITEMS),
		],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeGeometryToInstance' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeGetNamedGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeGizmoDial' : NodeInfo(
		[
			NTPNodeSetting("color_id", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeGizmoLinear' : NodeInfo(
		[
			NTPNodeSetting("color_id", ST.ENUM),
			NTPNodeSetting("draw_style", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeGizmoTransform' : NodeInfo(
		[
			NTPNodeSetting("use_rotation_x", ST.BOOL),
			NTPNodeSetting("use_rotation_y", ST.BOOL),
			NTPNodeSetting("use_rotation_z", ST.BOOL),
			NTPNodeSetting("use_scale_x", ST.BOOL),
			NTPNodeSetting("use_scale_y", ST.BOOL),
			NTPNodeSetting("use_scale_z", ST.BOOL),
			NTPNodeSetting("use_translation_x", ST.BOOL),
			NTPNodeSetting("use_translation_y", ST.BOOL),
			NTPNodeSetting("use_translation_z", ST.BOOL),
		],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeGreasePencilToCurves' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeGridToMesh' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'GeometryNodeImageInfo' : NodeInfo(
		[],
		min_version_ = (3, 5, 0)
	),

	'GeometryNodeImageTexture' : NodeInfo(
		[
			NTPNodeSetting("extension", ST.ENUM),
			NTPNodeSetting("interpolation", ST.ENUM),
		]
	),

	'GeometryNodeImportOBJ' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeImportPLY' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeImportSTL' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeIndexOfNearest' : NodeInfo(
		[],
		min_version_ = (3, 6, 0)
	),

	'GeometryNodeIndexSwitch' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("index_switch_items", ST.INDEX_SWITCH_ITEMS),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeInputActiveCamera' : NodeInfo(
		[],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeInputCurveHandlePositions' : NodeInfo(
		[]
	),

	'GeometryNodeInputCurveTilt' : NodeInfo(
		[]
	),

	'GeometryNodeInputEdgeSmooth' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeInputID' : NodeInfo(
		[]
	),

	'GeometryNodeInputImage' : NodeInfo(
		[
			NTPNodeSetting("image", ST.IMAGE),
		],
		min_version_ = (3, 5, 0)
	),

	'GeometryNodeInputIndex' : NodeInfo(
		[]
	),

	'GeometryNodeInputInstanceRotation' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeInputInstanceScale' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeInputMaterial' : NodeInfo(
		[
			NTPNodeSetting("material", ST.MATERIAL),
		]
	),

	'GeometryNodeInputMaterialIndex' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshEdgeAngle' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshEdgeNeighbors' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshEdgeVertices' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshFaceArea' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshFaceIsPlanar' : NodeInfo(
		[],
		min_version_ = (3, 2, 0)
	),

	'GeometryNodeInputMeshFaceNeighbors' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshIsland' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputMeshVertexNeighbors' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputNamedAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (3, 2, 0)
	),

	'GeometryNodeInputNamedLayerSelection' : NodeInfo(
		[],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeInputNormal' : NodeInfo(
		[]
	),

	'GeometryNodeInputPosition' : NodeInfo(
		[]
	),

	'GeometryNodeInputRadius' : NodeInfo(
		[]
	),

	'GeometryNodeInputSceneTime' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeInputShadeSmooth' : NodeInfo(
		[]
	),

	'GeometryNodeInputShortestEdgePaths' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeInputSignedDistance' : NodeInfo(
		[],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodeInputSplineCyclic' : NodeInfo(
		[]
	),

	'GeometryNodeInputSplineResolution' : NodeInfo(
		[]
	),

	'GeometryNodeInputTangent' : NodeInfo(
		[]
	),

	'GeometryNodeInstanceOnPoints' : NodeInfo(
		[]
	),

	'GeometryNodeInstanceTransform' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeInstancesToPoints' : NodeInfo(
		[]
	),

	'GeometryNodeInterpolateCurves' : NodeInfo(
		[],
		min_version_ = (3, 5, 0)
	),

	'GeometryNodeIsViewport' : NodeInfo(
		[]
	),

	'GeometryNodeJoinGeometry' : NodeInfo(
		[]
	),

	'GeometryNodeLegacyAlignRotationToVector' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("input_type_factor", ST.ENUM),
			NTPNodeSetting("input_type_vector", ST.ENUM),
			NTPNodeSetting("pivot_axis", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeClamp' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeColorRamp' : NodeInfo(
		[
			NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeCombineXYZ' : NodeInfo(
		[
			NTPNodeSetting("input_type_x", ST.ENUM),
			NTPNodeSetting("input_type_y", ST.ENUM),
			NTPNodeSetting("input_type_z", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeCompare' : NodeInfo(
		[
			NTPNodeSetting("input_type_a", ST.ENUM),
			NTPNodeSetting("input_type_b", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeConvert' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeCurveMap' : NodeInfo(
		[
			NTPNodeSetting("curve_rgb", ST.CURVE_MAPPING),
			NTPNodeSetting("curve_vec", ST.CURVE_MAPPING),
			NTPNodeSetting("data_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeFill' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeMapRange' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("interpolation_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeMath' : NodeInfo(
		[
			NTPNodeSetting("input_type_a", ST.ENUM),
			NTPNodeSetting("input_type_b", ST.ENUM),
			NTPNodeSetting("input_type_c", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeMix' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("input_type_a", ST.ENUM),
			NTPNodeSetting("input_type_b", ST.ENUM),
			NTPNodeSetting("input_type_factor", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeProximity' : NodeInfo(
		[
			NTPNodeSetting("target_geometry_element", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeRandomize' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeSampleTexture' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeSeparateXYZ' : NodeInfo(
		[
			NTPNodeSetting("input_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeTransfer' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("mapping", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeVectorMath' : NodeInfo(
		[
			NTPNodeSetting("input_type_a", ST.ENUM),
			NTPNodeSetting("input_type_b", ST.ENUM),
			NTPNodeSetting("input_type_c", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyAttributeVectorRotate' : NodeInfo(
		[
			NTPNodeSetting("input_type_angle", ST.ENUM),
			NTPNodeSetting("input_type_axis", ST.ENUM),
			NTPNodeSetting("input_type_center", ST.ENUM),
			NTPNodeSetting("input_type_rotation", ST.ENUM),
			NTPNodeSetting("input_type_vector", ST.ENUM),
			NTPNodeSetting("rotation_mode", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveEndpoints' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveReverse' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveSelectHandles' : NodeInfo(
		[
			NTPNodeSetting("handle_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM_SET),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveSetHandles' : NodeInfo(
		[
			NTPNodeSetting("handle_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM_SET),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveSplineType' : NodeInfo(
		[
			NTPNodeSetting("spline_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveSubdivide' : NodeInfo(
		[
			NTPNodeSetting("cuts_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyCurveToPoints' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyDeleteGeometry' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyEdgeSplit' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyMaterialAssign' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyMeshToCurve' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointDistribute' : NodeInfo(
		[
			NTPNodeSetting("distribute_method", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointInstance' : NodeInfo(
		[
			NTPNodeSetting("instance_type", ST.ENUM),
			NTPNodeSetting("use_whole_collection", ST.BOOL),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointScale' : NodeInfo(
		[
			NTPNodeSetting("input_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointSeparate' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointTranslate' : NodeInfo(
		[
			NTPNodeSetting("input_type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyPointsToVolume' : NodeInfo(
		[
			NTPNodeSetting("input_type_radius", ST.ENUM),
			NTPNodeSetting("resolution_mode", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyRaycast' : NodeInfo(
		[
			NTPNodeSetting("input_type_ray_direction", ST.ENUM),
			NTPNodeSetting("input_type_ray_length", ST.ENUM),
			NTPNodeSetting("mapping", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyRotatePoints' : NodeInfo(
		[
			NTPNodeSetting("input_type_angle", ST.ENUM),
			NTPNodeSetting("input_type_axis", ST.ENUM),
			NTPNodeSetting("input_type_rotation", ST.ENUM),
			NTPNodeSetting("space", ST.ENUM),
			NTPNodeSetting("type", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacySelectByMaterial' : NodeInfo(
		[],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacySubdivisionSurface' : NodeInfo(
		[
			NTPNodeSetting("boundary_smooth", ST.ENUM),
			NTPNodeSetting("uv_smooth", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeLegacyVolumeToMesh' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		],
		max_version_ = (3, 2, 0)
	),

	'GeometryNodeMaterialSelection' : NodeInfo(
		[]
	),

	'GeometryNodeMeanFilterSDFVolume' : NodeInfo(
		[],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodeMenuSwitch' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT, min_version_=(4, 2, 0)),
			NTPNodeSetting("active_item", ST.ENUM_ITEM, min_version_=(4, 2, 0)),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("enum_definition", ST.ENUM_DEFINITION, max_version_=(4, 2, 0)),
			NTPNodeSetting("enum_items", ST.MENU_SWITCH_ITEMS, min_version_=(4, 2, 0)),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeMergeByDistance' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, min_version_=(3, 2, 0)),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeMergeLayers' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeMeshBoolean' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
			NTPNodeSetting("solver", ST.ENUM, min_version_=(4, 2, 0)),
		]
	),

	'GeometryNodeMeshCircle' : NodeInfo(
		[
			NTPNodeSetting("fill_type", ST.ENUM),
		]
	),

	'GeometryNodeMeshCone' : NodeInfo(
		[
			NTPNodeSetting("fill_type", ST.ENUM),
		]
	),

	'GeometryNodeMeshCube' : NodeInfo(
		[]
	),

	'GeometryNodeMeshCylinder' : NodeInfo(
		[
			NTPNodeSetting("fill_type", ST.ENUM),
		]
	),

	'GeometryNodeMeshFaceSetBoundaries' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeMeshGrid' : NodeInfo(
		[]
	),

	'GeometryNodeMeshIcoSphere' : NodeInfo(
		[]
	),

	'GeometryNodeMeshLine' : NodeInfo(
		[
			NTPNodeSetting("count_mode", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeMeshToCurve' : NodeInfo(
		[]
	),

	'GeometryNodeMeshToDensityGrid' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeMeshToPoints' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeMeshToSDFGrid' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeMeshToSDFVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodeMeshToVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeMeshUVSphere' : NodeInfo(
		[]
	),

	'GeometryNodeObjectInfo' : NodeInfo(
		[
			NTPNodeSetting("transform_space", ST.ENUM),
		]
	),

	'GeometryNodeOffsetCornerInFace' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeOffsetPointInCurve' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeOffsetSDFVolume' : NodeInfo(
		[],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodePoints' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodePointsOfCurve' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodePointsToCurves' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodePointsToSDFGrid' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodePointsToSDFVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodePointsToVertices' : NodeInfo(
		[]
	),

	'GeometryNodePointsToVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		]
	),

	'GeometryNodeProximity' : NodeInfo(
		[
			NTPNodeSetting("target_element", ST.ENUM),
		]
	),

	'GeometryNodeRaycast' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("mapping", ST.ENUM),
		]
	),

	'GeometryNodeRealizeInstances' : NodeInfo(
		[
			NTPNodeSetting("legacy_behavior", ST.BOOL, min_version_=(3, 1, 0), max_version_=(4, 0, 0)),
		]
	),

	'GeometryNodeRemoveAttribute' : NodeInfo(
		[
			NTPNodeSetting("pattern_mode", ST.ENUM, min_version_=(4, 2, 0)),
		],
		min_version_ = (3, 2, 0)
	),

	'GeometryNodeRepeatInput' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeRepeatOutput' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("inspection_index", ST.INT),
			NTPNodeSetting("repeat_items", ST.REPEAT_OUTPUT_ITEMS),
		],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeReplaceMaterial' : NodeInfo(
		[]
	),

	'GeometryNodeResampleCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeReverseCurve' : NodeInfo(
		[]
	),

	'GeometryNodeRotateInstances' : NodeInfo(
		[]
	),

	'GeometryNodeSDFGridBoolean' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeSDFVolumeSphere' : NodeInfo(
		[],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodeSampleCurve' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM, min_version_=(3, 4, 0)),
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("use_all_curves", ST.BOOL, min_version_=(3, 4, 0)),
		]
	),

	'GeometryNodeSampleGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("interpolation_mode", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeSampleGridIndex' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeSampleIndex' : NodeInfo(
		[
			NTPNodeSetting("clamp", ST.BOOL),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSampleNearest' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSampleNearestSurface' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSampleUVSurface' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSampleVolume' : NodeInfo(
		[
			NTPNodeSetting("grid_type", ST.ENUM),
			NTPNodeSetting("interpolation_mode", ST.ENUM),
		],
		min_version_ = (3, 6, 0),
		max_version_ = (4, 1, 0)
	),

	'GeometryNodeScaleElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("scale_mode", ST.ENUM),
		],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeScaleInstances' : NodeInfo(
		[]
	),

	'GeometryNodeSelfObject' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSeparateComponents' : NodeInfo(
		[]
	),

	'GeometryNodeSeparateGeometry' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeSetCurveHandlePositions' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeSetCurveNormal' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeSetCurveRadius' : NodeInfo(
		[]
	),

	'GeometryNodeSetCurveTilt' : NodeInfo(
		[]
	),

	'GeometryNodeSetGeometryName' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeSetID' : NodeInfo(
		[]
	),

	'GeometryNodeSetInstanceTransform' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeSetMaterial' : NodeInfo(
		[]
	),

	'GeometryNodeSetMaterialIndex' : NodeInfo(
		[]
	),

	'GeometryNodeSetPointRadius' : NodeInfo(
		[]
	),

	'GeometryNodeSetPosition' : NodeInfo(
		[]
	),

	'GeometryNodeSetShadeSmooth' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM, min_version_=(4, 0, 0)),
		]
	),

	'GeometryNodeSetSplineCyclic' : NodeInfo(
		[]
	),

	'GeometryNodeSetSplineResolution' : NodeInfo(
		[]
	),

	'GeometryNodeSimulationInput' : NodeInfo(
		[],
		min_version_ = (3, 6, 0)
	),

	'GeometryNodeSimulationOutput' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("state_items", ST.SIM_OUTPUT_ITEMS),
		],
		min_version_ = (3, 6, 0)
	),

	'GeometryNodeSortElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeSplineLength' : NodeInfo(
		[]
	),

	'GeometryNodeSplineParameter' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'GeometryNodeSplitEdges' : NodeInfo(
		[]
	),

	'GeometryNodeSplitToInstances' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeStoreNamedAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (3, 2, 0)
	),

	'GeometryNodeStoreNamedGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (4, 1, 0)
	),

	'GeometryNodeStringJoin' : NodeInfo(
		[]
	),

	'GeometryNodeStringToCurves' : NodeInfo(
		[
			NTPNodeSetting("align_x", ST.ENUM),
			NTPNodeSetting("align_y", ST.ENUM),
			NTPNodeSetting("font", ST.FONT),
			NTPNodeSetting("overflow", ST.ENUM),
			NTPNodeSetting("pivot_mode", ST.ENUM, min_version_=(3, 1, 0)),
		]
	),

	'GeometryNodeSubdivideCurve' : NodeInfo(
		[]
	),

	'GeometryNodeSubdivideMesh' : NodeInfo(
		[]
	),

	'GeometryNodeSubdivisionSurface' : NodeInfo(
		[
			NTPNodeSetting("boundary_smooth", ST.ENUM),
			NTPNodeSetting("uv_smooth", ST.ENUM),
		]
	),

	'GeometryNodeSwitch' : NodeInfo(
		[
			NTPNodeSetting("input_type", ST.ENUM),
		]
	),

	'GeometryNodeTool3DCursor' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeToolActiveElement' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeToolFaceSet' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeToolMousePosition' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeToolSelection' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeToolSetFaceSet' : NodeInfo(
		[],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeToolSetSelection' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("selection_type", ST.ENUM, min_version_=(4, 3, 0)),
		],
		min_version_ = (4, 0, 0)
	),

	'GeometryNodeTransform' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, min_version_=(4, 2, 0)),
		]
	),

	'GeometryNodeTranslateInstances' : NodeInfo(
		[]
	),

	'GeometryNodeTriangulate' : NodeInfo(
		[
			NTPNodeSetting("ngon_method", ST.ENUM),
			NTPNodeSetting("quad_method", ST.ENUM),
		]
	),

	'GeometryNodeTrimCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeUVPackIslands' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeUVUnwrap' : NodeInfo(
		[
			NTPNodeSetting("method", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeVertexOfCorner' : NodeInfo(
		[],
		min_version_ = (3, 4, 0)
	),

	'GeometryNodeViewer' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM, min_version_=(3, 4, 0)),
		]
	),

	'GeometryNodeViewportTransform' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'GeometryNodeVolumeCube' : NodeInfo(
		[],
		min_version_ = (3, 3, 0)
	),

	'GeometryNodeVolumeToMesh' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM),
		]
	),

	'GeometryNodeWarning' : NodeInfo(
		[
			NTPNodeSetting("warning_type", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'NodeFrame' : NodeInfo(
		[
			NTPNodeSetting("label_size", ST.INT),
			NTPNodeSetting("shrink", ST.BOOL),
			NTPNodeSetting("text", ST.TEXT),
		]
	),

	'NodeGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'NodeGroupInput' : NodeInfo(
		[]
	),

	'NodeGroupOutput' : NodeInfo(
		[
			NTPNodeSetting("is_active_output", ST.BOOL),
		]
	),

	'NodeReroute' : NodeInfo(
		[
			NTPNodeSetting("socket_idname", ST.STRING, min_version_=(4, 3, 0)),
		]
	),

	'ShaderNodeAddShader' : NodeInfo(
		[]
	),

	'ShaderNodeAmbientOcclusion' : NodeInfo(
		[
			NTPNodeSetting("inside", ST.BOOL),
			NTPNodeSetting("only_local", ST.BOOL),
			NTPNodeSetting("samples", ST.INT),
		]
	),

	'ShaderNodeAttribute' : NodeInfo(
		[
			NTPNodeSetting("attribute_name", ST.STRING),
			NTPNodeSetting("attribute_type", ST.ENUM),
		]
	),

	'ShaderNodeBackground' : NodeInfo(
		[]
	),

	'ShaderNodeBevel' : NodeInfo(
		[
			NTPNodeSetting("samples", ST.INT),
		]
	),

	'ShaderNodeBlackbody' : NodeInfo(
		[]
	),

	'ShaderNodeBrightContrast' : NodeInfo(
		[]
	),

	'ShaderNodeBsdfAnisotropic' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		]
	),

	'ShaderNodeBsdfDiffuse' : NodeInfo(
		[]
	),

	'ShaderNodeBsdfGlass' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		]
	),

	'ShaderNodeBsdfGlossy' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		],
		max_version_ = (4, 0, 0)
	),

	'ShaderNodeBsdfHair' : NodeInfo(
		[
			NTPNodeSetting("component", ST.ENUM),
		]
	),

	'ShaderNodeBsdfHairPrincipled' : NodeInfo(
		[
			NTPNodeSetting("model", ST.ENUM, min_version_=(4, 0, 0)),
			NTPNodeSetting("parametrization", ST.ENUM),
		]
	),

	'ShaderNodeBsdfMetallic' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
			NTPNodeSetting("fresnel_type", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'ShaderNodeBsdfPrincipled' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
			NTPNodeSetting("subsurface_method", ST.ENUM),
		]
	),

	'ShaderNodeBsdfRayPortal' : NodeInfo(
		[],
		min_version_ = (4, 2, 0)
	),

	'ShaderNodeBsdfRefraction' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		]
	),

	'ShaderNodeBsdfSheen' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		],
		min_version_ = (4, 0, 0)
	),

	'ShaderNodeBsdfToon' : NodeInfo(
		[
			NTPNodeSetting("component", ST.ENUM),
		]
	),

	'ShaderNodeBsdfTranslucent' : NodeInfo(
		[]
	),

	'ShaderNodeBsdfTransparent' : NodeInfo(
		[]
	),

	'ShaderNodeBsdfVelvet' : NodeInfo(
		[],
		max_version_ = (4, 0, 0)
	),

	'ShaderNodeBump' : NodeInfo(
		[
			NTPNodeSetting("invert", ST.BOOL),
		]
	),

	'ShaderNodeCameraData' : NodeInfo(
		[]
	),

	'ShaderNodeClamp' : NodeInfo(
		[
			NTPNodeSetting("clamp_type", ST.ENUM),
		]
	),

	'ShaderNodeCombineColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'ShaderNodeCombineHSV' : NodeInfo(
		[]
	),

	'ShaderNodeCombineRGB' : NodeInfo(
		[]
	),

	'ShaderNodeCombineXYZ' : NodeInfo(
		[]
	),

	'ShaderNodeCustomGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'ShaderNodeDisplacement' : NodeInfo(
		[
			NTPNodeSetting("space", ST.ENUM),
		]
	),

	'ShaderNodeEeveeSpecular' : NodeInfo(
		[]
	),

	'ShaderNodeEmission' : NodeInfo(
		[]
	),

	'ShaderNodeFloatCurve' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'ShaderNodeFresnel' : NodeInfo(
		[]
	),

	'ShaderNodeGamma' : NodeInfo(
		[]
	),

	'ShaderNodeGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'ShaderNodeHairInfo' : NodeInfo(
		[]
	),

	'ShaderNodeHoldout' : NodeInfo(
		[]
	),

	'ShaderNodeHueSaturation' : NodeInfo(
		[]
	),

	'ShaderNodeInvert' : NodeInfo(
		[]
	),

	'ShaderNodeLayerWeight' : NodeInfo(
		[]
	),

	'ShaderNodeLightFalloff' : NodeInfo(
		[]
	),

	'ShaderNodeLightPath' : NodeInfo(
		[]
	),

	'ShaderNodeMapRange' : NodeInfo(
		[
			NTPNodeSetting("clamp", ST.BOOL),
			NTPNodeSetting("data_type", ST.ENUM, min_version_=(3, 1, 0)),
			NTPNodeSetting("interpolation_type", ST.ENUM),
		]
	),

	'ShaderNodeMapping' : NodeInfo(
		[
			NTPNodeSetting("vector_type", ST.ENUM),
		]
	),

	'ShaderNodeMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'ShaderNodeMix' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("clamp_factor", ST.BOOL),
			NTPNodeSetting("clamp_result", ST.BOOL),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("factor_mode", ST.ENUM),
		],
		min_version_ = (3, 4, 0)
	),

	'ShaderNodeMixRGB' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("use_alpha", ST.BOOL),
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'ShaderNodeMixShader' : NodeInfo(
		[]
	),

	'ShaderNodeNewGeometry' : NodeInfo(
		[]
	),

	'ShaderNodeNormal' : NodeInfo(
		[]
	),

	'ShaderNodeNormalMap' : NodeInfo(
		[
			NTPNodeSetting("space", ST.ENUM),
			NTPNodeSetting("uv_map", ST.STRING),
		]
	),

	'ShaderNodeObjectInfo' : NodeInfo(
		[]
	),

	'ShaderNodeOutputAOV' : NodeInfo(
		[
			NTPNodeSetting("aov_name", ST.STRING, min_version_=(4, 2, 0)),
			NTPNodeSetting("name", ST.STRING, max_version_=(4, 2, 0)),
		]
	),

	'ShaderNodeOutputLight' : NodeInfo(
		[
			NTPNodeSetting("is_active_output", ST.BOOL),
			NTPNodeSetting("target", ST.ENUM),
		]
	),

	'ShaderNodeOutputLineStyle' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("is_active_output", ST.BOOL),
			NTPNodeSetting("target", ST.ENUM),
			NTPNodeSetting("use_alpha", ST.BOOL),
			NTPNodeSetting("use_clamp", ST.BOOL),
		]
	),

	'ShaderNodeOutputMaterial' : NodeInfo(
		[
			NTPNodeSetting("is_active_output", ST.BOOL),
			NTPNodeSetting("target", ST.ENUM),
		]
	),

	'ShaderNodeOutputWorld' : NodeInfo(
		[
			NTPNodeSetting("is_active_output", ST.BOOL),
			NTPNodeSetting("target", ST.ENUM),
		]
	),

	'ShaderNodeParticleInfo' : NodeInfo(
		[]
	),

	'ShaderNodePointInfo' : NodeInfo(
		[],
		min_version_ = (3, 1, 0)
	),

	'ShaderNodeRGB' : NodeInfo(
		[]
	),

	'ShaderNodeRGBCurve' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'ShaderNodeRGBToBW' : NodeInfo(
		[]
	),

	'ShaderNodeScript' : NodeInfo(
		[
			NTPNodeSetting("bytecode", ST.STRING),
			NTPNodeSetting("bytecode_hash", ST.STRING),
			NTPNodeSetting("filepath", ST.STRING),
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("script", ST.TEXT),
			NTPNodeSetting("use_auto_update", ST.BOOL),
		]
	),

	'ShaderNodeSeparateColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (3, 3, 0)
	),

	'ShaderNodeSeparateHSV' : NodeInfo(
		[]
	),

	'ShaderNodeSeparateRGB' : NodeInfo(
		[]
	),

	'ShaderNodeSeparateXYZ' : NodeInfo(
		[]
	),

	'ShaderNodeShaderToRGB' : NodeInfo(
		[]
	),

	'ShaderNodeSqueeze' : NodeInfo(
		[]
	),

	'ShaderNodeSubsurfaceScattering' : NodeInfo(
		[
			NTPNodeSetting("falloff", ST.ENUM),
		]
	),

	'ShaderNodeTangent' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM),
			NTPNodeSetting("direction_type", ST.ENUM),
			NTPNodeSetting("uv_map", ST.STRING),
		]
	),

	'ShaderNodeTexBrick' : NodeInfo(
		[
			NTPNodeSetting("offset", ST.FLOAT),
			NTPNodeSetting("offset_frequency", ST.INT),
			NTPNodeSetting("squash", ST.FLOAT),
			NTPNodeSetting("squash_frequency", ST.INT),
		]
	),

	'ShaderNodeTexChecker' : NodeInfo(
		[]
	),

	'ShaderNodeTexCoord' : NodeInfo(
		[
			NTPNodeSetting("from_instancer", ST.BOOL),
			NTPNodeSetting("object", ST.OBJECT),
		]
	),

	'ShaderNodeTexEnvironment' : NodeInfo(
		[
			NTPNodeSetting("image", ST.IMAGE),
			NTPNodeSetting("image_user", ST.IMAGE_USER),
			NTPNodeSetting("interpolation", ST.ENUM),
			NTPNodeSetting("projection", ST.ENUM),
		]
	),

	'ShaderNodeTexGabor' : NodeInfo(
		[
			NTPNodeSetting("gabor_type", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'ShaderNodeTexGradient' : NodeInfo(
		[
			NTPNodeSetting("gradient_type", ST.ENUM),
		]
	),

	'ShaderNodeTexIES' : NodeInfo(
		[
			NTPNodeSetting("filepath", ST.STRING),
			NTPNodeSetting("ies", ST.TEXT),
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'ShaderNodeTexImage' : NodeInfo(
		[
			NTPNodeSetting("extension", ST.ENUM),
			NTPNodeSetting("image", ST.IMAGE),
			NTPNodeSetting("image_user", ST.IMAGE_USER),
			NTPNodeSetting("interpolation", ST.ENUM),
			NTPNodeSetting("projection", ST.ENUM),
			NTPNodeSetting("projection_blend", ST.FLOAT),
		]
	),

	'ShaderNodeTexMagic' : NodeInfo(
		[
			NTPNodeSetting("turbulence_depth", ST.INT),
		]
	),

	'ShaderNodeTexMusgrave' : NodeInfo(
		[
			NTPNodeSetting("musgrave_dimensions", ST.ENUM),
			NTPNodeSetting("musgrave_type", ST.ENUM),
		],
		max_version_ = (4, 1, 0)
	),

	'ShaderNodeTexNoise' : NodeInfo(
		[
			NTPNodeSetting("noise_dimensions", ST.ENUM),
			NTPNodeSetting("noise_type", ST.ENUM, min_version_=(4, 1, 0)),
			NTPNodeSetting("normalize", ST.BOOL, min_version_=(4, 0, 0)),
		]
	),

	'ShaderNodeTexPointDensity' : NodeInfo(
		[
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
		]
	),

	'ShaderNodeTexSky' : NodeInfo(
		[
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
		]
	),

	'ShaderNodeTexVoronoi' : NodeInfo(
		[
			NTPNodeSetting("distance", ST.ENUM),
			NTPNodeSetting("feature", ST.ENUM),
			NTPNodeSetting("normalize", ST.BOOL, min_version_=(4, 0, 0)),
			NTPNodeSetting("voronoi_dimensions", ST.ENUM),
		]
	),

	'ShaderNodeTexWave' : NodeInfo(
		[
			NTPNodeSetting("bands_direction", ST.ENUM),
			NTPNodeSetting("rings_direction", ST.ENUM),
			NTPNodeSetting("wave_profile", ST.ENUM),
			NTPNodeSetting("wave_type", ST.ENUM),
		]
	),

	'ShaderNodeTexWhiteNoise' : NodeInfo(
		[
			NTPNodeSetting("noise_dimensions", ST.ENUM),
		]
	),

	'ShaderNodeUVAlongStroke' : NodeInfo(
		[
			NTPNodeSetting("use_tips", ST.BOOL),
		]
	),

	'ShaderNodeUVMap' : NodeInfo(
		[
			NTPNodeSetting("from_instancer", ST.BOOL),
			NTPNodeSetting("uv_map", ST.STRING),
		]
	),

	'ShaderNodeValToRGB' : NodeInfo(
		[
			NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
		]
	),

	'ShaderNodeValue' : NodeInfo(
		[]
	),

	'ShaderNodeVectorCurve' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.CURVE_MAPPING),
		]
	),

	'ShaderNodeVectorDisplacement' : NodeInfo(
		[
			NTPNodeSetting("space", ST.ENUM),
		]
	),

	'ShaderNodeVectorMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		]
	),

	'ShaderNodeVectorRotate' : NodeInfo(
		[
			NTPNodeSetting("invert", ST.BOOL),
			NTPNodeSetting("rotation_type", ST.ENUM),
		]
	),

	'ShaderNodeVectorTransform' : NodeInfo(
		[
			NTPNodeSetting("convert_from", ST.ENUM),
			NTPNodeSetting("convert_to", ST.ENUM),
			NTPNodeSetting("vector_type", ST.ENUM),
		]
	),

	'ShaderNodeVertexColor' : NodeInfo(
		[
			NTPNodeSetting("layer_name", ST.STRING),
		]
	),

	'ShaderNodeVolumeAbsorption' : NodeInfo(
		[]
	),

	'ShaderNodeVolumeInfo' : NodeInfo(
		[]
	),

	'ShaderNodeVolumePrincipled' : NodeInfo(
		[]
	),

	'ShaderNodeVolumeScatter' : NodeInfo(
		[
			NTPNodeSetting("phase", ST.ENUM, min_version_=(4, 3, 0)),
		]
	),

	'ShaderNodeWavelength' : NodeInfo(
		[]
	),

	'ShaderNodeWireframe' : NodeInfo(
		[
			NTPNodeSetting("use_pixel_size", ST.BOOL),
		]
	),

}