import bpy
import os

from .utils import *
from io import StringIO

SCENE_VAR = "scene"
BASE_NAME_VAR = "base_name"
END_NAME_VAR = "end_name"

ntp_vars = {SCENE_VAR, BASE_NAME_VAR, END_NAME_VAR} 
#TODO: do something similar for geo nodes and materials, should be useful for
# possible conflicts between ntp_vars and node vars

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

    'CompositorNodeRLayers'    : [("layer", ST.ENUM),
                                  ("scene", ST.SCENE)],

    'CompositorNodeRGB'        : [],

    'CompositorNodeSceneTime'  : [],

    'CompositorNodeTexture'    : [("node_output", ST.INT), #TODO: ??
                                  ("texture",     ST.TEXTURE)],

    'CompositorNodeTime'       : [("curve",       ST.CURVE_MAPPING),
                                  ("frame_end",   ST.INT),
                                  ("frame_start", ST.INT)],

    'CompositorNodeTrackPos'   : [("clip",            ST.MOVIE_CLIP),
                                  ("frame_relative",  ST.INT),
                                  ("position",        ST.ENUM),
                                  ("track_name",      ST.STRING), #TODO: probably not right
                                  ("tracking_object", ST.STRING)], 

    'CompositorNodeValue'      : [],


    # OUTPUT
    'CompositorNodeComposite'   : [("use_alpha",          ST.BOOL)],

    'CompositorNodeOutputFile'  : [("active_input_index", ST.INT), #TODO: probably not right at all

                                   ("base_path",   ST.STRING),
                                   ("file_slots",  ST.FILE_SLOTS),
                                   ("format",      ST.IMAGE_FORMAT_SETTINGS),
                                   ("layer_slots", ST.LAYER_SLOTS)],

    'CompositorNodeLevels'      : [("channel", ST.ENUM)],

    'CompositorNodeSplitViewer' : [("axis",   ST.ENUM),
                                   ("factor", ST.INT)],

    'CompositorNodeViewer'      : [("center_x",   ST.FLOAT),
                                   ("center_y",   ST.FLOAT),
                                   ("tile_order", ST.ENUM),
                                   ("use_alpha",  ST.BOOL)],


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

    'CompositorNodeStablize'         : [("clip",        ST.MOVIE_CLIP),
                                        ("filter_type", ST.ENUM),
                                        ("invert",      ST.BOOL)],

    'CompositorNodeTransform'        : [("filter_type", ST.ENUM)],

    'CompositorNodeTranslate'        : [("use_relative", ST.BOOL),
                                        ("wrap_axis",    ST.ENUM)],


    # LAYOUT
    'CompositorNodeSwitch' : [("check", ST.BOOL)]
}

class NTPCompositorOperator(bpy.types.Operator):
    bl_idname = "node.compositor_to_python"
    bl_label =  "Compositor to Python"
    bl_options = {'REGISTER', 'UNDO'}

    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )
    
    compositor_name: bpy.props.StringProperty(name="Node Group")
    is_scene : bpy.props.BoolProperty(name="Is Scene", description="Blender stores compositing node trees differently for scenes and in groups")

    def execute(self, context):
        #find node group to replicate
        if self.is_scene:
            nt = bpy.data.scenes[self.compositor_name].node_tree
        else:
            nt = bpy.data.node_groups[self.compositor_name]
        if nt is None:
            #shouldn't happen
            self.report({'ERROR'},("NodeToPython: This doesn't seem to be a "
                                   "valid compositor node tree. Is Use Nodes "
                                   "selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        comp_var = clean_string(self.compositor_name)
        
        addon_dir = None
        if self.mode == 'ADDON':
            dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
            if not dir or dir == "":
                self.report({'ERROR'},
                            ("NodeToPython: Save your blender file before using "
                            "NodeToPython!"))
                return {'CANCELLED'}

            zip_dir = os.path.join(dir, comp_var)
            addon_dir = os.path.join(zip_dir, comp_var)
            if not os.path.exists(addon_dir):
                os.makedirs(addon_dir)
            file = open(f"{addon_dir}/__init__.py", "w")

            create_header(file, self.compositor_name)
            class_name = clean_string(self.compositor_name, lower=False)
            init_operator(file, class_name, comp_var, self.compositor_name)

            file.write("\tdef execute(self, context):\n")
        else:
            file = StringIO("")

        if self.is_scene:
            def create_scene(indent: str):
                #TODO: wrap in more general unique name util function
                file.write(f"{indent}# Generate unique scene name\n")
                file.write(f"{indent}{BASE_NAME_VAR} = {str_to_py_str(self.compositor_name)}\n")
                file.write(f"{indent}{END_NAME_VAR} = {BASE_NAME_VAR}\n")
                file.write(f"{indent}if bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
                file.write(f"{indent}\ti = 1\n")
                file.write(f"{indent}\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
                file.write(f"{indent}\twhile bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
                file.write(f"{indent}\t\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
                file.write(f"{indent}\t\ti += 1\n\n")

                file.write(f"{indent}{SCENE_VAR} = bpy.context.window.scene.copy()\n\n") 
                file.write(f"{indent}{SCENE_VAR}.name = {END_NAME_VAR}\n")
                file.write(f"{indent}{SCENE_VAR}.use_fake_user = True\n")
                file.write(f"{indent}bpy.context.window.scene = {SCENE_VAR}\n")
            
            if self.mode == 'ADDON':
                create_scene("\t\t")
            elif self.mode == 'SCRIPT':
                create_scene("")
        
        #set to keep track of already created node trees
        node_trees = set()

        #dictionary to keep track of node->variable name pairs
        node_vars = {}

        #keeps track of all used variables
        used_vars = {}

        def is_outermost_node_group(level: int) -> bool:
            if self.mode == 'ADDON' and level == 2:
                return True
            elif self.mode == 'SCRIPT' and level == 0:
                return True
            return False
        
        def process_comp_node_group(node_tree, level, node_vars, used_vars):       
            if is_outermost_node_group(level):
                nt_var = create_var(self.compositor_name, used_vars)
                nt_name = self.compositor_name
            else:
                nt_var = create_var(node_tree.name, used_vars)
                nt_name = node_tree.name

            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {nt_var} node group\n")
            file.write(f"{outer}def {nt_var}_node_group():\n")

            if is_outermost_node_group(level): #outermost node group
                file.write(f"{inner}{nt_var} = {SCENE_VAR}.node_tree\n")
                file.write(f"{inner}#start with a clean node tree\n")
                file.write(f"{inner}for node in {nt_var}.nodes:\n")
                file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
            else:
                file.write((f"{inner}{nt_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \'CompositorNodeTree\', "
                        f"name = {str_to_py_str(nt_name)})\n"))
                file.write("\n")
            
            inputs_set = False
            outputs_set = False

            #initialize nodes
            file.write(f"{inner}#initialize {nt_var} nodes\n")

            #dictionary to keep track of node->variable name pairs
            node_vars = {}

            for node in node_tree.nodes:
                if node.bl_idname == 'CompositorNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_comp_node_group(node_nt, level + 1, node_vars, 
                                               used_vars)
                        node_trees.add(node_nt)
                
                node_var = create_node(node, file, inner, nt_var, node_vars, 
                                       used_vars)
                
                if node.bl_idname == 'CompositorNodeColorBalance':
                    if node.correction_method == 'LIFT_GAMMA_GAIN':
                        lst = [("correction_method", ST.ENUM),                 
                               ("gain",              ST.COLOR),
                               ("gamma",             ST.COLOR),
                               ("lift",              ST.COLOR)]
                    else:
                        lst = [("correction_method", ST.ENUM),
                               ("offset",            ST.COLOR),
                               ("offset_basis",      ST.FLOAT),
                               ("power",             ST.COLOR),
                               ("slope",             ST.COLOR)]

                    compositor_node_settings['CompositorNodeColorBalance'] = lst

                set_settings_defaults(node, compositor_node_settings, file, 
                                      addon_dir, inner, node_var)
                hide_sockets(node, file, inner, node_var)

                if node.bl_idname == 'CompositorNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'NodeGroupInput' and not inputs_set:
                    group_io_settings(node, file, inner, "input", nt_var, node_tree)
                    inputs_set = True

                elif node.bl_idname == 'NodeGroupOutput' and not outputs_set:
                    group_io_settings(node, file, inner, "output", nt_var, node_tree)
                    outputs_set = True
                if self.mode == 'ADDON':
                    set_input_defaults(node, file, inner, node_var, addon_dir)
                else:
                    set_input_defaults(node, file, inner, node_var)
                set_output_defaults(node, file, inner, node_var)

            set_parents(node_tree, file, inner, node_vars)
            set_locations(node_tree, file, inner, node_vars)
            set_dimensions(node_tree, file, inner, node_vars)
            
            init_links(node_tree, file, inner, nt_var, node_vars)
            
            file.write(f"\n{outer}{nt_var}_node_group()\n\n")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0        
        process_comp_node_group(nt, level, node_vars, used_vars)

        if self.mode == 'ADDON':
            file.write("\t\treturn {'FINISHED'}\n\n")

            create_menu_func(file, class_name)
            create_register_func(file, class_name)
            create_unregister_func(file, class_name)
            create_main_func(file)
        else:
            context.window_manager.clipboard = file.getvalue()

        file.close()
        
        if self.mode == 'ADDON':
            zip_addon(zip_dir)
        
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = dir
        self.report({'INFO'}, f"NodeToPython: Saved compositor nodes to {location}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        self.layout.prop(self, "mode")

class NTPCompositorScenesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_comp_scenes"
    bl_label = "Select "
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for scene in bpy.data.scenes:
            if scene.node_tree:
                op = layout.operator(NTPCompositorOperator.bl_idname, text=scene.name)
                op.compositor_name = scene.name
                op.is_scene = True
                print(scene.node_tree.name)

class NTPCompositorGroupsMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_comp_groups"
    bl_label = "Select "
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for node_group in bpy.data.node_groups:
            if isinstance(node_group, bpy.types.CompositorNodeTree):
                op = layout.operator(NTPCompositorOperator.bl_idname, text=node_group.name)
                op.compositor_name = node_group.name
                op.is_scene = False
    
class NTPCompositorPanel(bpy.types.Panel):
    bl_label = "Compositor to Python"
    bl_idname = "NODE_PT_ntp_compositor"
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
        scenes_row = layout.row()
        
        # Disables menu when there are no materials
        scenes = [scene for scene in bpy.data.scenes 
                    if scene.node_tree is not None]
        scenes_exist = len(scenes) > 0
        scenes_row.enabled = scenes_exist
        
        scenes_row.alignment = 'EXPAND'
        scenes_row.operator_context = 'INVOKE_DEFAULT'
        scenes_row.menu("NODE_MT_ntp_comp_scenes", 
                        text="Scene Compositor Nodes")

        groups_row = layout.row()
        groups = [ng for ng in bpy.data.node_groups 
                            if isinstance(ng, bpy.types.CompositorNodeTree)]
        groups_exist = len(groups) > 0
        groups_row.enabled = groups_exist

        groups_row.alignment = 'EXPAND'
        groups_row.operator_context = 'INVOKE_DEFAULT'
        groups_row.menu("NODE_MT_ntp_comp_groups", 
                        text="Group Compositor Nodes")
