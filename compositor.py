import bpy
import os

from .utils import *
from io import StringIO

node_settings = {
    #Input
    'CompositorNodeBokehImage' : ["flaps", "angle", "rounding", "catadioptric", 
                                  "shift"],
    'CompositorNodeImage' : [], #TODO: handle image selection
    'CompositorNodeMask' : ["use_feather", "size_source", "size_x", "size_y", 
                            "use_motion_blur", 
                            "motion_blur_samples", "motion_blur_shutter"], #TODO: handle mask selection
    'CompositorNodeMovieClip' : [], #TODO: handle movie clip selection
    'CompositorNodeRLayers' : ["name", "layer"],
    'CompositorNodeRGB' : [], #should be handled by outputs
    'CompositorNodeSceneTime' : [], #should be good
    'CompositorNodeTexture' : [], #TODO: handle texture selection
    'CompositorNodeTime' : ["frame_start", "frame_end"],
    'CompositorNodeTrackPos' : [], #TODO: handle movie selection
    'CompositorNodeValue' : [], #should be handled by outputs (why is this a separate class??)

    #Output
    'CompositorNodeComposite' : ["use_alpha"],
    'CompositorNodeOutputFile' : ["base_path"], #TODO: doesn't seem portable
    'CompositorNodeLevels' : ["channel"],
    'CompositorNodeSplitViewer' : ["axis", "factor"],
    'CompositorNodeViewer' : ["use_alpha"],

    #Color
    'CompositorNodeAlphaOver' : ["use_premultiply", "premul"],
    'CompositorNodeBrightContrast' : ["use_premultiply"],
    'CompositorNodeColorBalance' : ["correction_method", "lift", "gamma", 
                                    "gain", "offset", "power", "slope", 
                                    "offset_basis"],
    'CompositorNodeColorCorrection' : ["red", "green", "blue", 
                                       "master_saturation", "master_contrast", 
                                       "master_gamma", "master_gain", 
                                       "master_lift", 
                                       "highlights_saturation", "highlights_contrast",
                                       "highlights_gamma", "highlights_gain",
                                       "highlights_lift",
                                       "midtones_saturation", "midtones_contrast",
                                       "midtones_gamma", "midtones_gain",
                                       "midtones_lift",
                                       "shadows_saturation", "shadows_contrast",
                                       "shadows_gamma", "shadows_gain",
                                       "shadows_lift",
                                       "midtones_start", "midtones_end"],
    'CompositorNodeExposure' : [],
    'CompositorNodeGamma' : [],
    'CompositorNodeHueCorrect' : [],
    'CompositorNodeHueSat' : [],
    'CompositorNodeInvert' : ["invert_rgb", "invert_alpha"],
    'CompositorNodeMixRGB' : ["blend_type", "use_alpha", "use_clamp"], #TODO: has an update() method, may need to figure out why...
    'CompositorNodePosterize' : [],
    'CompositorNodeCurveRGB' : [],
    'CompositorNodeTonemap' : ["tonemap_type", "intensity", "contrast", "adaptation", "correction", "key", "offset", "gamma"],
    'CompositorNodeZcombine' : ["use_alpha", "use_antialias_z"],

    #Converter
    'CompositorNodePremulKey' : ["mapping"],
    'CompositorNodeValToRGB' : [], #TODO: check to see if this'll work out of the box
    'CompositorNodeConvertColorSpace' : ["from_color_space", "to_color_space"],
    'CompositorNodeCombineColor' : ["mode", "ycc_mode"], #why isn't this standardized across blender?
    'CompositorNodeCombineXYZ' : [],
    'CompositorNodeIDMask' : ["index", "use_antialiasing"],
    'CompositorNodeMath' : ["operation", "use_clamp"],
    'CompositorNodeRGBToBW' : [],
    'CompositorNodeSeparateColor' : ["mode", "ycc_mode"],
    'CompositorNodeSeparateXYZ' : [],
    'CompositorNodeSetAlpha' : ["mode"], 
    'CompositorNodeSwitchView' : [],

    #Filter
    'CompositorNodeAntiAliasing' : ["threshold", "contrast_limit", "corner_rounding"],
    'CompositorNodeBilateralblur' : ["iterations", "sigma_color", "sigma_space"],
    'CompositorNodeBlur' : ["filter_type", "use_variable_size", "use_gamma_correction", "use_relative", "aspect_correction", "factor", "factor_x", "factor_y", "use_extended_bounds"],
    'CompositorNodeBokehBlur' : ["use_variable_size", "blur_max", "use_extended_bounds"],
    'CompositorNodeDefocus' : ["bokeh", "angle", "use_gamma_correction", "f_stop", "blur_max", "threshold", "use_preview", "use_zbuffer", "z_scale"],
    'CompositorNodeDespeckle' : ["threshold", "threshold_neighbor"],
    'CompositorNodeDilateErode' : ["mode", "distance", "edge", "falloff"],
    'CompositorNodeDBlur' : ["iterations", "center_x", "center_y", "distance", "angle", "spin", "zoom"],
    'CompositorNodeFilter' : ["filter_type"], 
    'CompositorNodeGlare' : ["glare_type", "quality", "iterations", "color_modulation", "mix", "threshold", "streaks", "angle_offset", "fade", "size", "use_rotate_45"],
    'CompositorNodeInpaint' : ["distance"],
    'CompositorNodePixelate' : [],
    'CompositorNodeSunBeams' : ["source", "ray_length"], #TODO: check that source doesn't freak out
    'CompositorNodeVecBlur' : ["samples", "factor", "speed_min", "speed_max", "use_curved"],

    #Vector
    'CompositorNodeMapRange' : ["use_clamp"], 
    'CompositorNodeMapValue' : ["offset", "size", "use_min", "min", "use_max", "max"], #why are all these vectors?? TODO: check to make sure it doesn't flip
    'CompositorNodeNormal' : [], #should be handled with io system
    'CompositorNodeNormalize' : [],
    'CompositorNodeCurveVec' : [],

    #Matte
    'CompositorNodeBoxMask' : ["x", "y", "width", "height", "rotation", "mask_type"],
    'CompositorNodeChannelMatte' : ["color_space", "matte_channel", "limit_method", "limit_channel", "limit_max", "limit_min"],
    'CompositorNodeChromaMatte' : ["tolerance", "threshold", "gain"],
    'CompositorNodeColorMatte' : ["color_hue", "color_saturation", "color_value"],
    'CompositorNodeColorSpill' : ["channel", "limit_method", "ratio", "use_unspill", "unspill_red", "unspill_green", "unspill_blue"],
    'CompositorNodeCryptomatteV2' : ["source"], #TODO: will need a lot of special handling
    'CompositorNodeCryptomatte' : [], #TODO: will likely need same handling as above
    'CompositorNodeDiffMatte' : ["tolerance", "falloff"],
    'CompositorNodeDistanceMatte' : ["tolerance", "falloff", "channel"],
    'CompositorNodeDoubleEdgeMask' : ["inner_mode", "edge_mode"],
    'CompositorNodeEllipseMask' : ["x", "y", "width", "height", "rotation", "mask_type"],
    'CompositorNodeKeying' : ["blur_pre", "screen_balance", "despill_factor", "despill_balance", "edge_kernel_radius", "edge_kernel_tolerance", "clip_black", "clip_white", "dilate_distance", "feather_falloff", "feather_distance", "blur_post"],
    'CompositorNodeKeyingScreen' : [], #TODO: movie stuff
    'CompositorNodeLumaMatte' : ["limit_max", "limit_min"],

    #Distort
    'CompositorNodeCornerPin' : [],
    'CompositorNodeCrop' : ["use_crop_size", "relative", "min_x", "max_x", "min_y", "max_y", "rel_min_x", "rel_max_x", "rel_min_y", "rel_max_y"],
    'CompositorNodeDisplace' : [],
    'CompositorNodeFlip' : ["axis"],
    'CompositorNodeLensdist' : ["use_projector", "use_jitter", "use_fit"],
    'CompositorNodeMapUV' : ["alpha"],
    'CompositorNodeMovieDistortion' : [], #TODO: movie stuff
    'CompositorNodePlaneTrackDeform' : ["use_motion_blur", "motion_blur_samples", "motion_blur_shutter"], #TODO: movie stuff
    'CompositorNodeRotate' : ["filter_type"],
    'CompositorNodeScale' : ["space", "frame_method", "offset_x", "offset_y"],
    'CompositorNodeStablize' : [], #TODO: movie stuff
    'CompositorNodeTransform' : ["filter_type"],
    'CompositorNodeTranslate' : ["use_relative", "wrapping"],

    #Layout
    'CompositorNodeSwitch' : ["check"]
}

curve_nodes = {
    'CompositorNodeTime', #TODO: check this works
    'CompositorNodeHueCorrect', #TODO: probbably will need custom work
    'CompositorNodeCurveRGB', #may just work out of the box
    'CompositorNodeCurveVec', #may just work out of the box
}

image_nodes = {'CompositorNodeImage',}

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
        """
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
                file.write((f"{indent}scene = bpy.data.scenes.new(" #TODO: see if using scene as name effects nodes named scene
                            f"name = {str_to_py_str(self.compositor_name)})\n"))
                file.write(f"{indent}scene.use_nodes = True\n")
            
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
                file.write(f"{inner}{nt_var} = scene.node_tree\n")
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

                elif node.bl_idname in image_nodes and self.mode == 'ADDON':
                    img = node.image
                    if img is not None and img.source in {'FILE', 'GENERATED', 'TILED'}:
                        save_image(img, addon_dir)
                        load_image(img, file, inner, f"{node_var}.image")
                        image_user_settings(node, file, inner, node_var)

                elif node.bl_idname == 'ShaderNodeValToRGB':
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
        """
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
