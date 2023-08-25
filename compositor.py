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

compositor_node_settings : dict[str, list[(str, str)]] = {
    # INPUT
    'CompositorNodeBokehImage' : [("angle", "float"),
                                  ("catadioptric", "float"),
                                  ("flaps", "int"),
                                  ("rounding", "float"),
                                  ("shift", "float")],
    'CompositorNodeImage'      : [("frame_duration", "int"),
                                  ("frame_offset", "int"),
                                  ("frame_start", "int"),
                                  ("image", "Image"),  #TODO: handle image selection
                                  ("layer", "enum"),
                                  ("use_auto_refresh", "bool"),
                                  ("use_cyclic", "bool"),
                                  ("use_straight_alpha_output", "bool"),
                                  ("view", "enum")],
    'CompositorNodeMask'       : [("mask", "Mask"), #TODO
                                  ("motion_blur_samples", "int"),
                                  ("motion_blur_shutter", "float"),
                                  ("size_source", "enum"),
                                  ("size_x", "int"),
                                  ("size_y", "int"),
                                  ("use_feather", "bool"),
                                  ("use_motion_blur", "bool")],
    'CompositorNodeMovieClip'  : [("clip", "MovieClip")], #TODO: handle movie clip selection
    'CompositorNodeRLayers'    : [("layer", "enum"),
                                  ("scene", "Scene")], #TODO
    'CompositorNodeRGB'        : [],
    'CompositorNodeSceneTime'  : [],
    'CompositorNodeTexture'    : [("node_output", "int"), #TODO: ??
                                  ("texture", "Texture")], #TODO: handle texture selection
    'CompositorNodeTime'       : [("curve", "CurveMapping"),
                                  ("frame_end", "int"),
                                  ("frame_start", "int")],
    'CompositorNodeTrackPos'   : [("clip", "MovieClip"), #TODO: this is probably wrong
                                  ("frame_relative", "int")
                                  ("position", "enum"),
                                  ("track_name", "str"),
                                  ("tracking_object", "str")], 
    'CompositorNodeValue'      : [], #should be handled by outputs (why is this a separate class??)


    # OUTPUT
    'CompositorNodeComposite'   : [("use_alpha", "bool")],
    'CompositorNodeOutputFile'  : [("active_input_index", "int"), #TODO: probably not right at all
                                   ("base_path", "str"),
                                   ("file_slots", "CompositorNodeOutputFileFileSlots"),
                                   ("format", "ImageFormatSettings"),
                                   ("layer_slots", "CompositorNodeOutputFileLayerSlots")],
    'CompositorNodeLevels'      : [("channel", "enum")],
    'CompositorNodeSplitViewer' : [("axis", "enum"),
                                   ("factor", "int")],
    'CompositorNodeViewer'      : [("center_x", "float"),
                                   ("center_y", "float"),
                                   ("tile_order", "enum"),
                                   ("use_alpha", "bool")],


    # COLOR
    'CompositorNodeAlphaOver'       : [("premul", "float"),
                                       ("use_premultiply", "bool")],
    'CompositorNodeBrightContrast'  : [("use_premultiply", "bool")],
    'CompositorNodeColorBalance'    : [("correction_method", "enum"),
                                       ("gain", "Vec3"),
                                       ("gamma", "Vec3"),
                                       ("lift", "Vec3"),
                                       ("offset", "Vec3"),
                                       ("offset_basis", "float"),
                                       ("power", "Vec3"),
                                       ("slope", "Vec3")],
    'CompositorNodeColorCorrection' : [("blue", "bool"),
                                       ("green", "bool"),
                                       ("highlights_contrast", "float"),
                                       ("highlights_gain", "float"),
                               CurveMapp            ("midtones_lift", "float"),
                                       ("midtones_saturation", "float"),
                                       ("midtones_start", "float"),
                                       ("red", "bool"),
                                       ("shadows_contrast", "float"),
                                       ("shadows_gain", "float"),
                                       ("shadows_gamma", "float"),
                                       ("shadows_lift", "float"),
                                       ("shadows_saturation", "float")],
    'CompositorNodeExposure'        : [],
    'CompositorNodeGamma'           : [],
    'CompositorNodeHueCorrect'      : [("mapping", "CurveMapping")],
    'CompositorNodeHueSat'          : [],
    'CompositorNodeInvert'          : [("invert_alpha", "bool"),
                                       ("invert_rgb", "bool")],
    'CompositorNodeMixRGB'          : [("blend_type", "enum"),
                                       ("use_alpha", "bool"),
                                       ("use_clamp", "bool")], #TODO: has an update() method, may need to figure out why...
    'CompositorNodePosterize'       : [],
    'CompositorNodeCurveRGB'        : [("mapping", "CurveMapping")],
    'CompositorNodeTonemap'         : [("adaptation", "float"),
                                       ("contrast", "float"),
                                       ("correction", "float"),
                                       ("gamma", "float"),
                                       ("intensity", "float"),
                                       ("key", "float"),
                                       ("offset", "float"),
                                       ("tonemap_type", "enum")],
    'CompositorNodeZcombine'        : [("use_alpha", "bool"),
                                       ("use_antialias_z", "bool")],


    # CONVERTER
    'CompositorNodePremulKey'         : [("mapping", "enum")],
    'CompositorNodeValToRGB'          : [("color_ramp", "ColorRamp")], #TODO: check to see if this'll work out of the box
    'CompositorNodeConvertColorSpace' : [("from_color_space", "enum"),
                                         ("to_color_space", "enum")],
    'CompositorNodeCombineColor'      : [("mode", "enum"),
                                         ("ycc_mode", "enum")], #why isn't this standardized across blender?
    'CompositorNodeCombineXYZ'        : [],
    'CompositorNodeIDMask'            : [("index", "int"),
                                         ("use_antialiasing", "bool")],
    'CompositorNodeMath'              : [("operation", "enum"),
                                         ("use_clamp", "bool")],
    'CompositorNodeRGBToBW'           : [],
    'CompositorNodeSeparateColor'     : [("mode", "enum"),
                                         ("ycc_mode", "enum")],
    'CompositorNodeSeparateXYZ'       : [],
    'CompositorNodeSetAlpha'          : [("mode", "enum")], 
    'CompositorNodeSwitchView'        : [],


    # FILTER
    'CompositorNodeAntiAliasing'  : [("contrast_limit", "float"),
                                     ("corner_rounding", "float"),
                                     ("threshold", "float")],
    'CompositorNodeBilateralblur' : [("iterations", "int"),
                                     ("sigma_color", "float"),
                                     ("sigma_space", "float")],
    'CompositorNodeBlur'          : [("aspect_correction", "enum"),
                                     ("factor", "float"),
                                     ("factor_x", "float"),
                                     ("factor_y", "float"),
                                     ("filter_type", "enum"),
                                     ("size_x", "int"),
                                     ("size_y", "int"),
                                     ("use_bokeh", "bool"),
                                     ("use_extended_bounds", "bool"),
                                     ("use_gamma_correction", "bool"),
                                     ("use_relative", "bool"),
                                     ("use_variable_size", "bool")],
    'CompositorNodeBokehBlur'     : [("blur_max", "float"),
                                     ("use_extended_bounds", "bool"), 
                                     ("use_variable_size", "bool")],
    'CompositorNodeDefocus'       : [("angle", "float"),
                                     ("blur_max", "float"),
                                     ("bokeh", "enum"),
                                     ("f_stop", "float"),
                                     ("scene", "Scene"), #TODO
                                     ("threshold", "float"),
                                     ("use_gamma_correction", "bool"),
                                     ("use_preview", "bool"),
                                     ("use_zbuffer", "bool"),
                                     ("z_scale", "float")],
    'CompositorNodeDespeckle'     : [("threshold", "float"),
                                     ("threshold_neighbor", "float")],
    'CompositorNodeDilateErode'   : [("distance", "int"),
                                     ("edge", "float"),
                                     ("falloff", "enum"),
                                     ("mode", "enum")],
    'CompositorNodeDBlur'         : [("angle", "float"),
                                     ("center_x", "float"),
                                     ("center_y", "float"),
                                     ("distance", "float"),
                                     ("iterations", "int"),
                                     ("spin", "float"),
                                     ("zoom", "float")],
    'CompositorNodeFilter'        : [("filter_type", "enum")], 
    'CompositorNodeGlare'         : [("angle_offset", "float"),
                                     ("color_modulation", "float"),
                                     ("fade", "float"),
                                     ("glare_type", "enum"),
                                     ("iterations", "int"),
                                     ("mix", "float"),
                                     ("quality", "enum"),
                                     ("size", "int"),
                                     ("streaks", "int"),
                                     ("threshold", "float"),
                                     ("use_rotate_45", "bool")],
    'CompositorNodeInpaint'       : [("distance", "int")],
    'CompositorNodePixelate'      : [],
    'CompositorNodeSunBeams'      : [("ray_length", "float"),
                                     ("source", "Vec2")],
    'CompositorNodeVecBlur'       : [("factor", "float"),
                                     ("samples", "int"),
                                     ("speed_max", "int"),
                                     ("speed_min", "int"),
                                     ("use_curved", "bool")],


    # VECTOR
    'CompositorNodeMapRange'  : [("use_clamp", "bool")], 
    'CompositorNodeMapValue'  : [("max", "Vec1"),
                                 ("min", "Vec1"),
                                 ("offset", "Vec1"),
                                 ("size", "Vec1"),
                                 ("use_max", "bool"),
                                 ("use_min", "bool")], #why are all these vectors?? TODO: check to make sure it doesn't flip
    'CompositorNodeNormal'    : [],
    'CompositorNodeNormalize' : [],
    'CompositorNodeCurveVec'  : [("mapping", "CurveMapping")],


    # MATTE
    'CompositorNodeBoxMask'        : [("height", "float"),
                                      ("mask_type", "enum"),
                                      ("rotation", "float"),
                                      ("width", "float"),
                                      ("x", "float"),
                                      ("y", "float")],
    'CompositorNodeChannelMatte'   : [("color_space", "enum"),
                                      ("limit_channel", "enum"),
                                      ("limit_max", "float"),
                                      ("limit_method", "enum"),
                                      ("limit_min", "float"),
                                      ("matte_channel", "enum")],
    'CompositorNodeChromaMatte'    : [("gain", "float"),
                                      ("lift", "float"),
                                      ("shadow_adjust", "float"),
                                      ("threshold", "float"),
                                      ("tolerance", "float")],
    'CompositorNodeColorMatte'     : [("color_hue", "float"),
                                      ("color_saturation", "float"),
                                      ("color_value", "float")],
    'CompositorNodeColorSpill'     : [("channel", "enum"),
                                      ("limit_channel", "enum"),
                                      ("limit_method", "enum"),
                                      ("ratio", "float"),
                                      ("unspill_blue", "float"),
                                      ("unspill_green", "float"),
                                      ("unspill_red", "float"),
                                      ("use_unspill", "bool")],
    'CompositorNodeCryptomatteV2'  : [("add", "Vec3"), #TODO: will need a lot of special handling
                                      ("entries", "CryptomatteEntry"), #TODO: (readonly?)
                                      ("frame_duration", "int"),
                                      ("frame_offset", "int"),
                                      ("frame_start", "int"),
                                      ("has_layers", "bool"), #TODO: readonly?
                                      ("has_views", "bool"), #TODO: readonly?
                                      ("image", "Image"),
                                      ("layer", "enum"),
                                      ("layer_name", "enum"),
                                      ("matte_id", "str"),
                                      ("remove", "Vec3"),
                                      ("scene", "Scene"),
                                      ("source", "enum"),
                                      ("use_auto_refresh", "bool"),
                                      ("use_cyclic", "bool"),
                                      ("view", "enum")],
    'CompositorNodeCryptomatte'    : [("add", "Vec3"), #TODO: will need a lot of special handling
                                      ("matte_id", "str"),
                                      ("remove", "Vec3")],
    'CompositorNodeDiffMatte'      : [("falloff", "float"),
                                      ("tolerance", "float")],
    'CompositorNodeDistanceMatte'  : [("channel", "enum"),
                                      ("falloff", "float"),
                                      ("tolerance", "float")],
    'CompositorNodeDoubleEdgeMask' : [("edge_mode", "enum"),
                                      ("inner_mode", "enum")],
    'CompositorNodeEllipseMask'    : [("height", "float"),
                                      ("mask_type", "enum"),
                                      ("rotation", "float"),
                                      ("width", "float"),
                                      ("x", "float"),
                                      ("y", "float")],
    'CompositorNodeKeying'         : [("blur_post", "int"),
                                      ("blur_pre", "int"),
                                      ("clip_black", "float"),
                                      ("clip_white", "float"),
                                      ("despill_balance", "float"),
                                      ("despill_factor", "float"),
                                      ("dilate_distance", "int"),
                                      ("edge_kernel_radius", "int"),
                                      ("edge_kernel_tolerance", "float"),
                                      ("feather_distance", "int"),
                                      ("feather_falloff", "enum"),
                                      ("screen_balance", "float")],
    'CompositorNodeKeyingScreen'   : [("clip", "MovieClip"),
                                      ("tracing_object", "str")], #TODO: movie stuff
    'CompositorNodeLumaMatte'      : [("limit_max", "float"),
                                      ("limit_min", "float")],


    # DISTORT
    'CompositorNodeCornerPin'        : [],
    'CompositorNodeCrop'             : [("max_x", "int"),
                                        ("max_y", "int"),
                                        ("min_x", "int"),
                                        ("min_y", "int"),
                                        ("rel_max_x", "float"),
                                        ("rel_max_y", "float"),
                                        ("rel_min_x", "float"),
                                        ("rel_min_y", "float"),
                                        ("relative", "bool"),
                                        ("use_crop_size", "bool")],
    'CompositorNodeDisplace'         : [],
    'CompositorNodeFlip'             : [("axis", "enum")],
    'CompositorNodeLensdist'         : [("use_fit", "bool"),
                                        ("use_jitter", "bool"),
                                        ("use_projector", "bool")],
    'CompositorNodeMapUV'            : [("alpha", "int")],
    'CompositorNodeMovieDistortion'  : [("clip", "MovieClip"),
                                        ("distortion_type", "enum")], #TODO: movie stuff
    'CompositorNodePlaneTrackDeform' : [("clip", "MovieClip"),
                                        ("motion_blur_samples", "int"),
                                        ("motion_blur_shutter", "float"),
                                        ("plane_track_name", "str"),
                                        ("tracking_object", "str"),
                                        ("use_motion_blur", "bool")], #TODO: movie stuff
    'CompositorNodeRotate'           : [("filter_type", "enum")],
    'CompositorNodeScale'            : [("frame_method", "enum"),
                                        ("offset_x", "float"),
                                        ("offset_y", "float"),
                                        ("space", "enum")],
    'CompositorNodeStablize'         : [("clip", "MovieClip"),
                                        ("filter_type", "enum"),
                                        ("invert", "bool")], #TODO: movie stuff
    'CompositorNodeTransform'        : [("filter_type", "enum")],
    'CompositorNodeTranslate'        : [("use_relative", "bool"),
                                        ("wrap_axis", "enum")],


    # LAYOUT
    'CompositorNodeSwitch' : ["check"]
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
                file.write(f"{indent}{SCENE_VAR} = bpy.context.window.scene.copy()\n\n") #TODO: see if using scene as name effects nodes named scene

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
                
                set_settings_defaults(node, node_settings, file, inner, node_var)
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

                # elif node.bl_idname in image_nodes and self.mode == 'ADDON':
                #     img = node.image
                #     if img is not None and img.source in {'FILE', 'GENERATED', 'TILED'}:
                #         save_image(img, addon_dir)
                #         load_image(img, file, inner, f"{node_var}.image")
                #         image_user_settings(node, file, inner, node_var)
               
                elif node.bl_idname == 'CompositorNodeValToRGB':
                    color_ramp_settings(node, file, inner, node_var)

                elif node.bl_idname in curve_nodes:
                    curve_node_settings(node, file, inner, node_var)

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
    
class NTPCompositingPanel(bpy.types.Panel):
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
