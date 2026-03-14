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
	CLOSURE_INPUT_ITEMS = auto()
	CLOSURE_OUTPUT_ITEMS = auto()
	COLOR_MANAGED_DISPLAY_SETTINGS = auto()
	COLOR_MANAGED_VIEW_SETTINGS = auto()
	COLOR_RAMP = auto()
	COMBINE_BUNDLE_ITEMS = auto()
	COMPOSITOR_FILE_OUTPUT_ITEMS = auto()
	CURVE_MAPPING = auto()
	ENUM_DEFINITION = auto()
	ENUM_ITEM = auto()
	EVALUATE_CLOSURE_INPUT_ITEMS = auto()
	EVALUATE_CLOSURE_OUTPUT_ITEMS = auto()
	FIELD_TO_GRID_ITEMS = auto()
	FOREACH_GEO_ELEMENT_GENERATION_ITEMS = auto()
	FOREACH_GEO_ELEMENT_INPUT_ITEMS = auto()
	FOREACH_GEO_ELEMENT_MAIN_ITEMS = auto()
	FORMAT_STRING_ITEMS = auto()
	GEOMETRY_VIEWER_ITEMS = auto()
	INDEX_SWITCH_ITEMS = auto()
	MENU_SWITCH_ITEMS = auto()
	NODE_TREE = auto()
	REPEAT_OUTPUT_ITEMS = auto()
	SEPARATE_BUNDLE_ITEMS = auto()
	SIM_OUTPUT_ITEMS = auto()
	IMAGE = auto()
	IMAGE_USER = auto()
	COLLECTION = auto()
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
	min_version_: tuple = (4, 2, 0)
	max_version_: tuple = (5, 2, 0)

class NodeInfo(NamedTuple):
	attributes_: list[NTPNodeSetting]
	min_version_: tuple = (4, 2, 0)
	max_version_: tuple = (5, 2, 0)

node_settings : dict[str, NodeInfo] = {
	'CompositorNodeAlphaOver' : NodeInfo(
		[
			NTPNodeSetting("premul", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_premultiply", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeAntiAliasing' : NodeInfo(
		[
			NTPNodeSetting("contrast_limit", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("corner_rounding", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("threshold", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBilateralblur' : NodeInfo(
		[
			NTPNodeSetting("iterations", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("sigma_color", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("sigma_space", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBlur' : NodeInfo(
		[
			NTPNodeSetting("aspect_correction", ST.ENUM, max_version_=(4, 5, 0)),
			NTPNodeSetting("factor", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("factor_x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("factor_y", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("size_x", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("size_y", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_bokeh", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_extended_bounds", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_gamma_correction", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_relative", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_variable_size", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBokehBlur' : NodeInfo(
		[
			NTPNodeSetting("blur_max", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_extended_bounds", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_variable_size", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBokehImage' : NodeInfo(
		[
			NTPNodeSetting("angle", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("catadioptric", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("flaps", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rounding", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shift", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBoxMask' : NodeInfo(
		[
			NTPNodeSetting("mask_height", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("mask_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("mask_width", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rotation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("y", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeBrightContrast' : NodeInfo(
		[
			NTPNodeSetting("use_premultiply", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeChannelMatte' : NodeInfo(
		[
			NTPNodeSetting("color_space", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_channel", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_max", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("limit_method", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_min", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("matte_channel", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeChromaMatte' : NodeInfo(
		[
			NTPNodeSetting("gain", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("lift", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadow_adjust", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("threshold", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("tolerance", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeColorBalance' : NodeInfo(
		[
			NTPNodeSetting("correction_method", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("gain", ST.COLOR, max_version_=(4, 5, 0)),
			NTPNodeSetting("gamma", ST.COLOR, max_version_=(4, 5, 0)),
			NTPNodeSetting("input_temperature", ST.FLOAT, min_version_=(4, 3, 0), max_version_=(4, 5, 0)),
			NTPNodeSetting("input_tint", ST.FLOAT, min_version_=(4, 3, 0), max_version_=(4, 5, 0)),
			NTPNodeSetting("input_whitepoint", ST.COLOR, min_version_=(4, 3, 0)),
			NTPNodeSetting("lift", ST.COLOR, max_version_=(4, 5, 0)),
			NTPNodeSetting("offset", ST.COLOR, max_version_=(4, 5, 0)),
			NTPNodeSetting("offset_basis", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("output_temperature", ST.FLOAT, min_version_=(4, 3, 0), max_version_=(4, 5, 0)),
			NTPNodeSetting("output_tint", ST.FLOAT, min_version_=(4, 3, 0), max_version_=(4, 5, 0)),
			NTPNodeSetting("output_whitepoint", ST.COLOR, min_version_=(4, 3, 0)),
			NTPNodeSetting("power", ST.COLOR, max_version_=(4, 5, 0)),
			NTPNodeSetting("slope", ST.COLOR, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeColorCorrection' : NodeInfo(
		[
			NTPNodeSetting("blue", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("green", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("highlights_contrast", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("highlights_gain", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("highlights_gamma", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("highlights_lift", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("highlights_saturation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("master_contrast", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("master_gain", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("master_gamma", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("master_lift", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("master_saturation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_contrast", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_end", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_gain", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_gamma", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_lift", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_saturation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("midtones_start", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("red", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadows_contrast", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadows_gain", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadows_gamma", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadows_lift", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("shadows_saturation", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeColorMatte' : NodeInfo(
		[
			NTPNodeSetting("color_hue", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("color_saturation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("color_value", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeColorSpill' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_channel", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_method", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("ratio", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("unspill_blue", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("unspill_green", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("unspill_red", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_unspill", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeCombHSVA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeCombRGBA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeCombYCCA' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeCombYUVA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeCombineColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("ycc_mode", ST.ENUM),
		]
	),

	'CompositorNodeCombineXYZ' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeComposite' : NodeInfo(
		[
			NTPNodeSetting("use_alpha", ST.BOOL, max_version_=(4, 5, 0)),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeConvertColorSpace' : NodeInfo(
		[
			NTPNodeSetting("from_color_space", ST.ENUM),
			NTPNodeSetting("to_color_space", ST.ENUM),
		]
	),

	'CompositorNodeConvertToDisplay' : NodeInfo(
		[
			NTPNodeSetting("display_settings", ST.COLOR_MANAGED_DISPLAY_SETTINGS),
			NTPNodeSetting("view_settings", ST.COLOR_MANAGED_VIEW_SETTINGS),
		],
		min_version_ = (5, 0, 0)
	),

	'CompositorNodeConvolve' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'CompositorNodeCornerPin' : NodeInfo(
		[
			NTPNodeSetting("interpolation", ST.ENUM, min_version_=(4, 5, 0), max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeCrop' : NodeInfo(
		[
			NTPNodeSetting("max_x", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("max_y", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("min_x", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("min_y", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rel_max_x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rel_max_y", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rel_min_x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rel_min_y", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("relative", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_crop_size", ST.BOOL, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeCryptomatte' : NodeInfo(
		[
			NTPNodeSetting("add", ST.COLOR),
			NTPNodeSetting("matte_id", ST.STRING),
			NTPNodeSetting("remove", ST.COLOR),
		]
	),

	'CompositorNodeCryptomatteV2' : NodeInfo(
		[
			NTPNodeSetting("add", ST.COLOR),
			NTPNodeSetting("entries", ST.CRYPTOMATTE_ENTRIES),
			NTPNodeSetting("frame_duration", ST.INT),
			NTPNodeSetting("frame_offset", ST.INT),
			NTPNodeSetting("frame_start", ST.INT),
			NTPNodeSetting("image", ST.IMAGE),
			NTPNodeSetting("layer", ST.ENUM),
			NTPNodeSetting("layer_name", ST.ENUM),
			NTPNodeSetting("matte_id", ST.STRING),
			NTPNodeSetting("remove", ST.COLOR),
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
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeCustomGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'CompositorNodeDBlur' : NodeInfo(
		[
			NTPNodeSetting("angle", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("center_x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("center_y", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("distance", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("iterations", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("spin", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("zoom", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeDefocus' : NodeInfo(
		[
			NTPNodeSetting("angle", ST.FLOAT),
			NTPNodeSetting("blur_max", ST.FLOAT),
			NTPNodeSetting("bokeh", ST.ENUM),
			NTPNodeSetting("f_stop", ST.FLOAT),
			NTPNodeSetting("scene", ST.SCENE),
			NTPNodeSetting("threshold", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_gamma_correction", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_preview", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_zbuffer", ST.BOOL),
			NTPNodeSetting("z_scale", ST.FLOAT),
		]
	),

	'CompositorNodeDenoise' : NodeInfo(
		[
			NTPNodeSetting("prefilter", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("quality", ST.ENUM, min_version_=(4, 4, 0), max_version_=(5, 0, 0)),
			NTPNodeSetting("use_hdr", ST.BOOL, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeDespeckle' : NodeInfo(
		[
			NTPNodeSetting("threshold", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("threshold_neighbor", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeDiffMatte' : NodeInfo(
		[
			NTPNodeSetting("falloff", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("tolerance", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeDilateErode' : NodeInfo(
		[
			NTPNodeSetting("distance", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("edge", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("falloff", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeDisplace' : NodeInfo(
		[]
	),

	'CompositorNodeDistanceMatte' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("falloff", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("tolerance", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeDoubleEdgeMask' : NodeInfo(
		[
			NTPNodeSetting("edge_mode", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("inner_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeEllipseMask' : NodeInfo(
		[
			NTPNodeSetting("mask_height", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("mask_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("mask_width", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("rotation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("y", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeExposure' : NodeInfo(
		[]
	),

	'CompositorNodeFilter' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeFlip' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeGamma' : NodeInfo(
		[]
	),

	'CompositorNodeGlare' : NodeInfo(
		[
			NTPNodeSetting("angle_offset", ST.FLOAT, max_version_=(4, 4, 0)),
			NTPNodeSetting("color_modulation", ST.FLOAT, max_version_=(4, 4, 0)),
			NTPNodeSetting("fade", ST.FLOAT, max_version_=(4, 4, 0)),
			NTPNodeSetting("glare_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("iterations", ST.INT, max_version_=(4, 4, 0)),
			NTPNodeSetting("mix", ST.FLOAT, max_version_=(4, 4, 0)),
			NTPNodeSetting("quality", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("size", ST.INT, max_version_=(4, 4, 0)),
			NTPNodeSetting("streaks", ST.INT, max_version_=(4, 4, 0)),
			NTPNodeSetting("threshold", ST.FLOAT, max_version_=(4, 4, 0)),
			NTPNodeSetting("use_rotate_45", ST.BOOL, max_version_=(4, 5, 0)),
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
			NTPNodeSetting("index", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_antialiasing", ST.BOOL, max_version_=(4, 5, 0)),
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
			NTPNodeSetting("use_straight_alpha_output", ST.BOOL, max_version_=(5, 0, 0)),
			NTPNodeSetting("view", ST.ENUM),
		]
	),

	'CompositorNodeImageCoordinates' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'CompositorNodeImageInfo' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'CompositorNodeInpaint' : NodeInfo(
		[
			NTPNodeSetting("distance", ST.INT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeInvert' : NodeInfo(
		[
			NTPNodeSetting("invert_alpha", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("invert_rgb", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeKeying' : NodeInfo(
		[
			NTPNodeSetting("blur_post", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("blur_pre", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("clip_black", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("clip_white", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("despill_balance", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("despill_factor", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("dilate_distance", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("edge_kernel_radius", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("edge_kernel_tolerance", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("feather_distance", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("feather_falloff", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("screen_balance", ST.FLOAT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeKeyingScreen' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("smoothness", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("tracking_object", ST.STRING),
		]
	),

	'CompositorNodeKuwahara' : NodeInfo(
		[
			NTPNodeSetting("eccentricity", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("sharpness", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("uniformity", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_high_precision", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("variation", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeLensdist' : NodeInfo(
		[
			NTPNodeSetting("distortion_type", ST.ENUM, min_version_=(4, 5, 0), max_version_=(5, 0, 0)),
			NTPNodeSetting("use_fit", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_jitter", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_projector", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeLevels' : NodeInfo(
		[
			NTPNodeSetting("channel", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeLumaMatte' : NodeInfo(
		[
			NTPNodeSetting("limit_max", ST.FLOAT, max_version_=(5, 0, 0)),
			NTPNodeSetting("limit_min", ST.FLOAT, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeMapRange' : NodeInfo(
		[
			NTPNodeSetting("use_clamp", ST.BOOL),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeMapUV' : NodeInfo(
		[
			NTPNodeSetting("alpha", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
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
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeMask' : NodeInfo(
		[
			NTPNodeSetting("mask", ST.MASK),
			NTPNodeSetting("motion_blur_samples", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("motion_blur_shutter", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("size_source", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("size_x", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("size_y", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_feather", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_motion_blur", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeMaskToSDF' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'CompositorNodeMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
			NTPNodeSetting("use_clamp", ST.BOOL),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeMixRGB' : NodeInfo(
		[
			NTPNodeSetting("blend_type", ST.ENUM),
			NTPNodeSetting("use_alpha", ST.BOOL),
			NTPNodeSetting("use_clamp", ST.BOOL),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeMovieClip' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
		]
	),

	'CompositorNodeMovieDistortion' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("distortion_type", ST.ENUM, max_version_=(5, 0, 0)),
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
			NTPNodeSetting("active_input_index", ST.INT, max_version_=(5, 0, 0)),
			NTPNodeSetting("active_item_index", ST.INT, min_version_=(5, 0, 0)),
			NTPNodeSetting("base_path", ST.STRING, max_version_=(5, 0, 0)),
			NTPNodeSetting("directory", ST.STRING, min_version_=(5, 0, 0)),
			NTPNodeSetting("file_name", ST.STRING, min_version_=(5, 0, 0)),
			NTPNodeSetting("file_output_items", ST.COMPOSITOR_FILE_OUTPUT_ITEMS, min_version_=(5, 0, 0)),
			NTPNodeSetting("file_slots", ST.FILE_SLOTS, max_version_=(5, 0, 0)),
			NTPNodeSetting("format", ST.IMAGE_FORMAT_SETTINGS),
			NTPNodeSetting("layer_slots", ST.LAYER_SLOTS, max_version_=(5, 0, 0)),
			NTPNodeSetting("save_as_render", ST.BOOL, min_version_=(4, 3, 0)),
		]
	),

	'CompositorNodePixelate' : NodeInfo(
		[
			NTPNodeSetting("pixel_size", ST.INT, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodePlaneTrackDeform' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("motion_blur_samples", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("motion_blur_shutter", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("plane_track_name", ST.STRING),
			NTPNodeSetting("tracking_object", ST.STRING),
			NTPNodeSetting("use_motion_blur", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodePosterize' : NodeInfo(
		[]
	),

	'CompositorNodePremulKey' : NodeInfo(
		[
			NTPNodeSetting("mapping", ST.ENUM, max_version_=(5, 0, 0)),
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

	'CompositorNodeRelativeToPixel' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("reference_dimension", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'CompositorNodeRotate' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeScale' : NodeInfo(
		[
			NTPNodeSetting("frame_method", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("interpolation", ST.ENUM, min_version_=(4, 5, 0), max_version_=(5, 0, 0)),
			NTPNodeSetting("offset_x", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("offset_y", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("space", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeSceneTime' : NodeInfo(
		[]
	),

	'CompositorNodeSepHSVA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSepRGBA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSepYCCA' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSepYUVA' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSeparateColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("ycc_mode", ST.ENUM),
		]
	),

	'CompositorNodeSeparateXYZ' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSequencerStripInfo' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'CompositorNodeSetAlpha' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeSplit' : NodeInfo(
		[
			NTPNodeSetting("axis", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("factor", ST.INT, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeStabilize' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("invert", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeSunBeams' : NodeInfo(
		[
			NTPNodeSetting("ray_length", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("source", ST.VEC2, max_version_=(4, 5, 0)),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeSwitch' : NodeInfo(
		[
			NTPNodeSetting("check", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeSwitchView' : NodeInfo(
		[]
	),

	'CompositorNodeTexture' : NodeInfo(
		[
			NTPNodeSetting("node_output", ST.INT),
			NTPNodeSetting("texture", ST.TEXTURE),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeTime' : NodeInfo(
		[
			NTPNodeSetting("curve", ST.CURVE_MAPPING),
			NTPNodeSetting("frame_end", ST.INT, max_version_=(5, 0, 0)),
			NTPNodeSetting("frame_start", ST.INT, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeTonemap' : NodeInfo(
		[
			NTPNodeSetting("adaptation", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("contrast", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("correction", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("gamma", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("intensity", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("key", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("offset", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("tonemap_type", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeTrackPos' : NodeInfo(
		[
			NTPNodeSetting("clip", ST.MOVIE_CLIP),
			NTPNodeSetting("frame_relative", ST.INT, max_version_=(5, 0, 0)),
			NTPNodeSetting("position", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("track_name", ST.STRING),
			NTPNodeSetting("tracking_object", ST.STRING),
		]
	),

	'CompositorNodeTransform' : NodeInfo(
		[
			NTPNodeSetting("filter_type", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeTranslate' : NodeInfo(
		[
			NTPNodeSetting("interpolation", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("use_relative", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("wrap_axis", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'CompositorNodeValToRGB' : NodeInfo(
		[
			NTPNodeSetting("color_ramp", ST.COLOR_RAMP),
		],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeValue' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'CompositorNodeVecBlur' : NodeInfo(
		[
			NTPNodeSetting("factor", ST.FLOAT, max_version_=(4, 5, 0)),
			NTPNodeSetting("samples", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("speed_max", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("speed_min", ST.INT, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_curved", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeViewer' : NodeInfo(
		[
			NTPNodeSetting("ui_shortcut", ST.INT, min_version_=(4, 4, 0)),
			NTPNodeSetting("use_alpha", ST.BOOL, max_version_=(4, 5, 0)),
		]
	),

	'CompositorNodeZcombine' : NodeInfo(
		[
			NTPNodeSetting("use_alpha", ST.BOOL, max_version_=(4, 5, 0)),
			NTPNodeSetting("use_antialias_z", ST.BOOL, max_version_=(4, 5, 0)),
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
		]
	),

	'FunctionNodeAxesToRotation' : NodeInfo(
		[
			NTPNodeSetting("primary_axis", ST.ENUM),
			NTPNodeSetting("secondary_axis", ST.ENUM),
		]
	),

	'FunctionNodeAxisAngleToRotation' : NodeInfo(
		[]
	),

	'FunctionNodeBitMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'FunctionNodeBooleanMath' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM),
		]
	),

	'FunctionNodeCombineColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'FunctionNodeCombineMatrix' : NodeInfo(
		[]
	),

	'FunctionNodeCombineTransform' : NodeInfo(
		[]
	),

	'FunctionNodeCompare' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("operation", ST.ENUM),
		]
	),

	'FunctionNodeEulerToRotation' : NodeInfo(
		[]
	),

	'FunctionNodeFindInString' : NodeInfo(
		[],
		min_version_ = (4, 4, 0)
	),

	'FunctionNodeFloatToInt' : NodeInfo(
		[
			NTPNodeSetting("rounding_mode", ST.ENUM),
		]
	),

	'FunctionNodeFormatString' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("format_items", ST.FORMAT_STRING_ITEMS),
		],
		min_version_ = (4, 5, 0)
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
			NTPNodeSetting("value", ST.VEC4),
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
		]
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
		[]
	),

	'FunctionNodeInvertRotation' : NodeInfo(
		[]
	),

	'FunctionNodeMatchString' : NodeInfo(
		[
			NTPNodeSetting("operation", ST.ENUM, max_version_=(5, 0, 0)),
		],
		min_version_ = (4, 5, 0)
	),

	'FunctionNodeMatrixDeterminant' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'FunctionNodeMatrixMultiply' : NodeInfo(
		[]
	),

	'FunctionNodeMatrixSVD' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'FunctionNodeProjectPoint' : NodeInfo(
		[]
	),

	'FunctionNodeQuaternionToRotation' : NodeInfo(
		[]
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
			NTPNodeSetting("rotation_type", ST.ENUM),
			NTPNodeSetting("space", ST.ENUM),
		]
	),

	'FunctionNodeRotateRotation' : NodeInfo(
		[
			NTPNodeSetting("rotation_space", ST.ENUM),
		]
	),

	'FunctionNodeRotateVector' : NodeInfo(
		[]
	),

	'FunctionNodeRotationToAxisAngle' : NodeInfo(
		[]
	),

	'FunctionNodeRotationToEuler' : NodeInfo(
		[]
	),

	'FunctionNodeRotationToQuaternion' : NodeInfo(
		[]
	),

	'FunctionNodeSeparateColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'FunctionNodeSeparateMatrix' : NodeInfo(
		[]
	),

	'FunctionNodeSeparateTransform' : NodeInfo(
		[]
	),

	'FunctionNodeSliceString' : NodeInfo(
		[]
	),

	'FunctionNodeStringLength' : NodeInfo(
		[]
	),

	'FunctionNodeStringToValue' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'FunctionNodeTransformDirection' : NodeInfo(
		[]
	),

	'FunctionNodeTransformPoint' : NodeInfo(
		[]
	),

	'FunctionNodeTransposeMatrix' : NodeInfo(
		[]
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
		]
	),

	'GeometryNodeAttributeDomainSize' : NodeInfo(
		[
			NTPNodeSetting("component", ST.ENUM),
		]
	),

	'GeometryNodeAttributeStatistic' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeBake' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("bake_items", ST.BAKE_ITEMS),
		]
	),

	'GeometryNodeBlurAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeBoneInfo' : NodeInfo(
		[
			NTPNodeSetting("transform_space", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeBoundBox' : NodeInfo(
		[]
	),

	'GeometryNodeCameraInfo' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeCaptureAttribute' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("capture_items", ST.CAPTURE_ATTRIBUTE_ITEMS),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeClosureInput' : NodeInfo(
		[],
		min_version_ = (4, 5, 0),
		max_version_ = (5, 0, 0)
	),

	'GeometryNodeClosureOutput' : NodeInfo(
		[
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("active_output_index", ST.INT),
		],
		min_version_ = (4, 5, 0),
		max_version_ = (5, 0, 0)
	),

	'GeometryNodeCollectionInfo' : NodeInfo(
		[
			NTPNodeSetting("transform_space", ST.ENUM),
		]
	),

	'GeometryNodeCombineBundle' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
		],
		min_version_ = (4, 5, 0),
		max_version_ = (5, 0, 0)
	),

	'GeometryNodeConvexHull' : NodeInfo(
		[]
	),

	'GeometryNodeCornersOfEdge' : NodeInfo(
		[]
	),

	'GeometryNodeCornersOfFace' : NodeInfo(
		[]
	),

	'GeometryNodeCornersOfVertex' : NodeInfo(
		[]
	),

	'GeometryNodeCubeGridTopology' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeCurveArc' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
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
		[]
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
		[]
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
		]
	),

	'GeometryNodeDistributePointsInVolume' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeDistributePointsOnFaces' : NodeInfo(
		[
			NTPNodeSetting("distribute_method", ST.ENUM),
			NTPNodeSetting("use_legacy_normal", ST.BOOL),
		]
	),

	'GeometryNodeDualMesh' : NodeInfo(
		[]
	),

	'GeometryNodeDuplicateElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeEdgePathsToCurves' : NodeInfo(
		[]
	),

	'GeometryNodeEdgePathsToSelection' : NodeInfo(
		[]
	),

	'GeometryNodeEdgesOfCorner' : NodeInfo(
		[]
	),

	'GeometryNodeEdgesOfVertex' : NodeInfo(
		[]
	),

	'GeometryNodeEdgesToFaceGroups' : NodeInfo(
		[]
	),

	'GeometryNodeEvaluateClosure' : NodeInfo(
		[
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("active_output_index", ST.INT),
		],
		min_version_ = (4, 5, 0),
		max_version_ = (5, 0, 0)
	),

	'GeometryNodeExtrudeMesh' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeFaceOfCorner' : NodeInfo(
		[]
	),

	'GeometryNodeFieldAtIndex' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeFieldAverage' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeFieldMinAndMax' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeFieldOnDomain' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeFieldToGrid' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("grid_items", ST.FIELD_TO_GRID_ITEMS),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeFieldToList' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeFieldVariance' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeFillCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeFilletCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeFlipFaces' : NodeInfo(
		[]
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
		[]
	),

	'GeometryNodeGetGeometryBundle' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGetNamedGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
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

	'GeometryNodeGridAdvect' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridClip' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGridCurl' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridDilateAndErode' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGridDivergence' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridGradient' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridInfo' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeGridLaplacian' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridMean' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGridMedian' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGridPrune' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGridToMesh' : NodeInfo(
		[]
	),

	'GeometryNodeGridToPoints' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeGridVoxelize' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeGroup' : NodeInfo(
		[
			NTPNodeSetting("node_tree", ST.NODE_TREE),
		]
	),

	'GeometryNodeImageInfo' : NodeInfo(
		[]
	),

	'GeometryNodeImageTexture' : NodeInfo(
		[
			NTPNodeSetting("extension", ST.ENUM),
			NTPNodeSetting("interpolation", ST.ENUM),
		]
	),

	'GeometryNodeImportCSV' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
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

	'GeometryNodeImportText' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeImportVDB' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeIndexOfNearest' : NodeInfo(
		[]
	),

	'GeometryNodeIndexSwitch' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("index_switch_items", ST.INDEX_SWITCH_ITEMS),
		]
	),

	'GeometryNodeInputActiveCamera' : NodeInfo(
		[]
	),

	'GeometryNodeInputCollection' : NodeInfo(
		[
			NTPNodeSetting("collection", ST.COLLECTION),
		],
		min_version_ = (4, 4, 0)
	),

	'GeometryNodeInputCurveHandlePositions' : NodeInfo(
		[]
	),

	'GeometryNodeInputCurveTilt' : NodeInfo(
		[]
	),

	'GeometryNodeInputEdgeSmooth' : NodeInfo(
		[]
	),

	'GeometryNodeInputID' : NodeInfo(
		[]
	),

	'GeometryNodeInputImage' : NodeInfo(
		[
			NTPNodeSetting("image", ST.IMAGE),
		]
	),

	'GeometryNodeInputIndex' : NodeInfo(
		[]
	),

	'GeometryNodeInputInstanceBounds' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeInputInstanceRotation' : NodeInfo(
		[]
	),

	'GeometryNodeInputInstanceScale' : NodeInfo(
		[]
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
		[]
	),

	'GeometryNodeInputMeshEdgeNeighbors' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshEdgeVertices' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshFaceArea' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshFaceIsPlanar' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshFaceNeighbors' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshIsland' : NodeInfo(
		[]
	),

	'GeometryNodeInputMeshVertexNeighbors' : NodeInfo(
		[]
	),

	'GeometryNodeInputNamedAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeInputNamedLayerSelection' : NodeInfo(
		[]
	),

	'GeometryNodeInputNormal' : NodeInfo(
		[
			NTPNodeSetting("legacy_corner_normals", ST.BOOL, min_version_=(4, 4, 0)),
		]
	),

	'GeometryNodeInputObject' : NodeInfo(
		[
			NTPNodeSetting("object", ST.OBJECT),
		],
		min_version_ = (4, 4, 0)
	),

	'GeometryNodeInputPosition' : NodeInfo(
		[]
	),

	'GeometryNodeInputRadius' : NodeInfo(
		[]
	),

	'GeometryNodeInputSceneTime' : NodeInfo(
		[]
	),

	'GeometryNodeInputShadeSmooth' : NodeInfo(
		[]
	),

	'GeometryNodeInputShortestEdgePaths' : NodeInfo(
		[]
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

	'GeometryNodeInputVoxelIndex' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeInstanceOnPoints' : NodeInfo(
		[]
	),

	'GeometryNodeInstanceTransform' : NodeInfo(
		[]
	),

	'GeometryNodeInstancesToPoints' : NodeInfo(
		[]
	),

	'GeometryNodeInterpolateCurves' : NodeInfo(
		[]
	),

	'GeometryNodeIsViewport' : NodeInfo(
		[]
	),

	'GeometryNodeJoinGeometry' : NodeInfo(
		[]
	),

	'GeometryNodeList' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0),
		max_version_ = (5, 1, 0)
	),

	'GeometryNodeListGetItem' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM, max_version_=(5, 1, 0)),
			NTPNodeSetting("socket_type", ST.ENUM, min_version_=(5, 1, 0)),
			NTPNodeSetting("structure_type", ST.ENUM, min_version_=(5, 1, 0)),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeListLength' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeMaterialSelection' : NodeInfo(
		[]
	),

	'GeometryNodeMenuSwitch' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("active_item", ST.ENUM_ITEM),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("enum_items", ST.MENU_SWITCH_ITEMS),
		]
	),

	'GeometryNodeMergeByDistance' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
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
			NTPNodeSetting("solver", ST.ENUM),
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
		[]
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
		[
			NTPNodeSetting("mode", ST.ENUM, min_version_=(4, 5, 0)),
		]
	),

	'GeometryNodeMeshToDensityGrid' : NodeInfo(
		[]
	),

	'GeometryNodeMeshToPoints' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeMeshToSDFGrid' : NodeInfo(
		[]
	),

	'GeometryNodeMeshToVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
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
		[]
	),

	'GeometryNodeOffsetPointInCurve' : NodeInfo(
		[]
	),

	'GeometryNodePoints' : NodeInfo(
		[]
	),

	'GeometryNodePointsOfCurve' : NodeInfo(
		[]
	),

	'GeometryNodePointsToCurves' : NodeInfo(
		[]
	),

	'GeometryNodePointsToSDFGrid' : NodeInfo(
		[]
	),

	'GeometryNodePointsToVertices' : NodeInfo(
		[]
	),

	'GeometryNodePointsToVolume' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM, max_version_=(5, 0, 0)),
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
			NTPNodeSetting("mapping", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeRealizeInstances' : NodeInfo(
		[
			NTPNodeSetting("realize_to_point_domain", ST.BOOL, min_version_=(5, 1, 0)),
		]
	),

	'GeometryNodeRemoveAttribute' : NodeInfo(
		[
			NTPNodeSetting("pattern_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeRepeatInput' : NodeInfo(
		[]
	),

	'GeometryNodeRepeatOutput' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("inspection_index", ST.INT),
			NTPNodeSetting("repeat_items", ST.REPEAT_OUTPUT_ITEMS),
		]
	),

	'GeometryNodeReplaceMaterial' : NodeInfo(
		[]
	),

	'GeometryNodeResampleCurve' : NodeInfo(
		[
			NTPNodeSetting("keep_last_segment", ST.BOOL, min_version_=(4, 4, 0)),
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
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
		]
	),

	'GeometryNodeSDFGridFillet' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSDFGridLaplacian' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSDFGridMean' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSDFGridMeanCurvature' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSDFGridMedian' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSDFGridOffset' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSampleCurve' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
			NTPNodeSetting("use_all_curves", ST.BOOL),
		]
	),

	'GeometryNodeSampleGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("interpolation_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeSampleGridIndex' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeSampleIndex' : NodeInfo(
		[
			NTPNodeSetting("clamp", ST.BOOL),
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeSampleNearest' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeSampleNearestSurface' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeSampleUVSurface' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeScaleElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("scale_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeScaleInstances' : NodeInfo(
		[]
	),

	'GeometryNodeSelfObject' : NodeInfo(
		[]
	),

	'GeometryNodeSeparateBundle' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
		],
		min_version_ = (4, 5, 0),
		max_version_ = (5, 0, 0)
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
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeSetCurveRadius' : NodeInfo(
		[]
	),

	'GeometryNodeSetCurveTilt' : NodeInfo(
		[]
	),

	'GeometryNodeSetGeometryBundle' : NodeInfo(
		[],
		min_version_ = (5, 1, 0)
	),

	'GeometryNodeSetGeometryName' : NodeInfo(
		[],
		min_version_ = (4, 3, 0)
	),

	'GeometryNodeSetGreasePencilColor' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeSetGreasePencilDepth' : NodeInfo(
		[
			NTPNodeSetting("depth_order", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeSetGreasePencilSoftness' : NodeInfo(
		[],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeSetGridBackground' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSetGridTransform' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeSetID' : NodeInfo(
		[]
	),

	'GeometryNodeSetInstanceTransform' : NodeInfo(
		[]
	),

	'GeometryNodeSetMaterial' : NodeInfo(
		[]
	),

	'GeometryNodeSetMaterialIndex' : NodeInfo(
		[]
	),

	'GeometryNodeSetMeshNormal' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("mode", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
	),

	'GeometryNodeSetPointRadius' : NodeInfo(
		[]
	),

	'GeometryNodeSetPosition' : NodeInfo(
		[]
	),

	'GeometryNodeSetShadeSmooth' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeSetSplineCyclic' : NodeInfo(
		[]
	),

	'GeometryNodeSetSplineResolution' : NodeInfo(
		[]
	),

	'GeometryNodeSimulationInput' : NodeInfo(
		[]
	),

	'GeometryNodeSimulationOutput' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("state_items", ST.SIM_OUTPUT_ITEMS),
		]
	),

	'GeometryNodeSortElements' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeSplineLength' : NodeInfo(
		[]
	),

	'GeometryNodeSplineParameter' : NodeInfo(
		[]
	),

	'GeometryNodeSplitEdges' : NodeInfo(
		[]
	),

	'GeometryNodeSplitToInstances' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeStoreNamedAttribute' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeStoreNamedGrid' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		]
	),

	'GeometryNodeStringJoin' : NodeInfo(
		[]
	),

	'GeometryNodeStringToCurves' : NodeInfo(
		[
			NTPNodeSetting("align_x", ST.ENUM, max_version_=(5, 1, 0)),
			NTPNodeSetting("align_y", ST.ENUM, max_version_=(5, 1, 0)),
			NTPNodeSetting("font", ST.FONT, max_version_=(5, 1, 0)),
			NTPNodeSetting("overflow", ST.ENUM, max_version_=(5, 1, 0)),
			NTPNodeSetting("pivot_mode", ST.ENUM, max_version_=(5, 1, 0)),
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
			NTPNodeSetting("boundary_smooth", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("uv_smooth", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeSwitch' : NodeInfo(
		[
			NTPNodeSetting("input_type", ST.ENUM),
		]
	),

	'GeometryNodeTool3DCursor' : NodeInfo(
		[]
	),

	'GeometryNodeToolActiveElement' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
		]
	),

	'GeometryNodeToolFaceSet' : NodeInfo(
		[]
	),

	'GeometryNodeToolMousePosition' : NodeInfo(
		[]
	),

	'GeometryNodeToolSelection' : NodeInfo(
		[]
	),

	'GeometryNodeToolSetFaceSet' : NodeInfo(
		[]
	),

	'GeometryNodeToolSetSelection' : NodeInfo(
		[
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("selection_type", ST.ENUM, min_version_=(4, 3, 0)),
		]
	),

	'GeometryNodeTransform' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeTranslateInstances' : NodeInfo(
		[]
	),

	'GeometryNodeTriangulate' : NodeInfo(
		[
			NTPNodeSetting("ngon_method", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("quad_method", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeTrimCurve' : NodeInfo(
		[
			NTPNodeSetting("mode", ST.ENUM),
		]
	),

	'GeometryNodeUVPackIslands' : NodeInfo(
		[]
	),

	'GeometryNodeUVTangent' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'GeometryNodeUVUnwrap' : NodeInfo(
		[
			NTPNodeSetting("method", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeVertexOfCorner' : NodeInfo(
		[]
	),

	'GeometryNodeViewer' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT, min_version_=(5, 0, 0)),
			NTPNodeSetting("data_type", ST.ENUM, max_version_=(5, 0, 0)),
			NTPNodeSetting("domain", ST.ENUM),
			NTPNodeSetting("ui_shortcut", ST.INT, min_version_=(4, 5, 0)),
			NTPNodeSetting("viewer_items", ST.GEOMETRY_VIEWER_ITEMS, min_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeViewportTransform' : NodeInfo(
		[]
	),

	'GeometryNodeVolumeCube' : NodeInfo(
		[]
	),

	'GeometryNodeVolumeToMesh' : NodeInfo(
		[
			NTPNodeSetting("resolution_mode", ST.ENUM, max_version_=(5, 0, 0)),
		]
	),

	'GeometryNodeWarning' : NodeInfo(
		[
			NTPNodeSetting("warning_type", ST.ENUM),
		],
		min_version_ = (4, 3, 0)
	),

	'NodeClosureInput' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'NodeClosureOutput' : NodeInfo(
		[
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("active_output_index", ST.INT),
			NTPNodeSetting("define_signature", ST.BOOL),
			NTPNodeSetting("input_items", ST.CLOSURE_INPUT_ITEMS),
			NTPNodeSetting("output_items", ST.CLOSURE_OUTPUT_ITEMS),
		],
		min_version_ = (5, 0, 0)
	),

	'NodeCombineBundle' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("bundle_items", ST.COMBINE_BUNDLE_ITEMS),
			NTPNodeSetting("define_signature", ST.BOOL),
		],
		min_version_ = (5, 0, 0)
	),

	'NodeEnableOutput' : NodeInfo(
		[
			NTPNodeSetting("data_type", ST.ENUM),
		],
		min_version_ = (5, 0, 0)
	),

	'NodeEvaluateClosure' : NodeInfo(
		[
			NTPNodeSetting("active_input_index", ST.INT),
			NTPNodeSetting("active_output_index", ST.INT),
			NTPNodeSetting("define_signature", ST.BOOL),
			NTPNodeSetting("input_items", ST.EVALUATE_CLOSURE_OUTPUT_ITEMS),
			NTPNodeSetting("output_items", ST.EVALUATE_CLOSURE_OUTPUT_ITEMS),
		],
		min_version_ = (5, 0, 0)
	),

	'NodeFrame' : NodeInfo(
		[
			NTPNodeSetting("label_size", ST.INT),
			NTPNodeSetting("shrink", ST.BOOL),
			NTPNodeSetting("text", ST.TEXT),
		]
	),

	'NodeGetBundleItem' : NodeInfo(
		[
			NTPNodeSetting("socket_type", ST.ENUM),
			NTPNodeSetting("structure_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
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

	'NodeJoinBundle' : NodeInfo(
		[],
		min_version_ = (5, 0, 0)
	),

	'NodeReroute' : NodeInfo(
		[
			NTPNodeSetting("socket_idname", ST.STRING, min_version_=(4, 3, 0)),
		]
	),

	'NodeSeparateBundle' : NodeInfo(
		[
			NTPNodeSetting("active_index", ST.INT),
			NTPNodeSetting("bundle_items", ST.SEPARATE_BUNDLE_ITEMS),
			NTPNodeSetting("define_signature", ST.BOOL),
		],
		min_version_ = (5, 0, 0)
	),

	'NodeStoreBundleItem' : NodeInfo(
		[
			NTPNodeSetting("socket_type", ST.ENUM),
			NTPNodeSetting("structure_type", ST.ENUM),
		],
		min_version_ = (5, 1, 0)
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

	'ShaderNodeBsdfHair' : NodeInfo(
		[
			NTPNodeSetting("component", ST.ENUM),
		]
	),

	'ShaderNodeBsdfHairPrincipled' : NodeInfo(
		[
			NTPNodeSetting("model", ST.ENUM),
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
		[]
	),

	'ShaderNodeBsdfRefraction' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		]
	),

	'ShaderNodeBsdfSheen' : NodeInfo(
		[
			NTPNodeSetting("distribution", ST.ENUM),
		]
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
		]
	),

	'ShaderNodeCombineHSV' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'ShaderNodeCombineRGB' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
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
			NTPNodeSetting("data_type", ST.ENUM),
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
		]
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
			NTPNodeSetting("convention", ST.ENUM, min_version_=(5, 1, 0)),
			NTPNodeSetting("space", ST.ENUM),
			NTPNodeSetting("uv_map", ST.STRING),
		]
	),

	'ShaderNodeObjectInfo' : NodeInfo(
		[]
	),

	'ShaderNodeOutputAOV' : NodeInfo(
		[
			NTPNodeSetting("aov_name", ST.STRING),
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
		[]
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

	'ShaderNodeRadialTiling' : NodeInfo(
		[
			NTPNodeSetting("normalize", ST.BOOL),
		],
		min_version_ = (5, 0, 0)
	),

	'ShaderNodeRaycast' : NodeInfo(
		[
			NTPNodeSetting("only_local", ST.BOOL),
		],
		min_version_ = (5, 1, 0)
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
		]
	),

	'ShaderNodeSeparateHSV' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
	),

	'ShaderNodeSeparateRGB' : NodeInfo(
		[],
		max_version_ = (5, 0, 0)
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

	'ShaderNodeTexNoise' : NodeInfo(
		[
			NTPNodeSetting("noise_dimensions", ST.ENUM),
			NTPNodeSetting("noise_type", ST.ENUM),
			NTPNodeSetting("normalize", ST.BOOL),
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
		],
		max_version_ = (5, 0, 0)
	),

	'ShaderNodeTexSky' : NodeInfo(
		[
			NTPNodeSetting("aerosol_density", ST.FLOAT, min_version_=(5, 0, 0)),
			NTPNodeSetting("air_density", ST.FLOAT),
			NTPNodeSetting("altitude", ST.FLOAT),
			NTPNodeSetting("dust_density", ST.FLOAT, max_version_=(5, 0, 0)),
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
			NTPNodeSetting("normalize", ST.BOOL),
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

	'ShaderNodeVolumeCoefficients' : NodeInfo(
		[
			NTPNodeSetting("phase", ST.ENUM),
		],
		min_version_ = (4, 5, 0)
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