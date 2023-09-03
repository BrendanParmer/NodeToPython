import bpy
import os

from .utils import *
from io import StringIO

MAT_VAR = "mat"

#TODO: move to a json, different ones for each blender version?
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
                          ("use_auto_update", ST.BOOL)]
}

image_nodes = {'ShaderNodeTexEnvironment',
               'ShaderNodeTexImage'}

class NTPMaterialOperator(bpy.types.Operator):
    bl_idname = "node.ntp_material"
    bl_label =  "Material to Python"
    bl_options = {'REGISTER', 'UNDO'}

    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )
    material_name: bpy.props.StringProperty(name="Node Group")

    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.materials[self.material_name].node_tree
        if nt is None:
            self.report({'ERROR'},("NodeToPython: This doesn't seem to be a "
                                   "valid material. Is Use Nodes selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        mat_var = clean_string(self.material_name)
        
        addon_dir = None
        if self.mode == 'ADDON':
            dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
            if not dir or dir == "":
                self.report({'ERROR'},
                            ("NodeToPython: Save your blender file before using "
                            "NodeToPython!"))
                return {'CANCELLED'}

            zip_dir = os.path.join(dir, mat_var)
            addon_dir = os.path.join(zip_dir, mat_var)
            if not os.path.exists(addon_dir):
                os.makedirs(addon_dir)
            file = open(f"{addon_dir}/__init__.py", "w")

            create_header(file, self.material_name)
            class_name = clean_string(self.material_name, lower=False)
            init_operator(file, class_name, mat_var, self.material_name)

            file.write("\tdef execute(self, context):\n")
        else:
            file = StringIO("")

        def create_material(indent: str):
            file.write((f"{indent}{MAT_VAR} = bpy.data.materials.new("
                        f"name = {str_to_py_str(self.material_name)})\n"))
            file.write(f"{indent}{MAT_VAR}.use_nodes = True\n")
        
        if self.mode == 'ADDON':
            create_material("\t\t")
        elif self.mode == 'SCRIPT': #TODO: should add option for just creating the node group
            create_material("")
        
        #set to keep track of already created node trees
        node_trees: set[bpy.types.NodeTree] = set()

        #dictionary to keep track of node->variable name pairs
        node_vars: dict[bpy.types.Node, str] = {}

        #keeps track of all used base variable names and usage counts
        used_vars: dict[str, int] = {}

        def is_outermost_node_group(level: int) -> bool:
            if self.mode == 'ADDON' and level == 2:
                return True
            elif self.mode == 'SCRIPT' and level == 0:
                return True
            return False

        def process_mat_node_group(node_tree: bpy.types.NodeTree, 
                                   level: int
                                  ) -> None:
            """
            Generates a Python function to recreate a node tree

            Parameters:
            node_tree (bpy.types.NodeTree): node tree to be recreated
            level (int): number of tabs to use for each line, used with
                node groups within node groups and script/add-on differences
            """

            if is_outermost_node_group(level):
                nt_var = create_var(self.material_name, used_vars)
                nt_name = self.material_name
            else:
                nt_var = create_var(node_tree.name, used_vars)
                nt_name = node_tree.name

            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {nt_var} node group\n")
            file.write(f"{outer}def {nt_var}_node_group():\n")

            if is_outermost_node_group(level): #outermost node group
                file.write(f"{inner}{nt_var} = {MAT_VAR}.node_tree\n")
                file.write(f"{inner}#start with a clean node tree\n")
                file.write(f"{inner}for node in {nt_var}.nodes:\n")
                file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
            else:
                file.write((f"{inner}{nt_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \'ShaderNodeTree\', "
                        f"name = {str_to_py_str(nt_name)})\n"))
                file.write("\n")

            inputs_set = False
            outputs_set = False

            #initialize nodes
            file.write(f"{inner}#initialize {nt_var} nodes\n")

            #dictionary to keep track of node->variable name pairs
            node_vars = {}

            for node in node_tree.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_mat_node_group(node_nt, level + 1)
                        node_trees.add(node_nt)
                
                node_var = create_node(node, file, inner, nt_var, node_vars, 
                                       used_vars)
                
                set_settings_defaults(node, shader_node_settings, file, 
                                      addon_dir, inner, node_var)
                hide_sockets(node, file, inner, node_var)

                if node.bl_idname == 'ShaderNodeGroup':
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
        process_mat_node_group(nt, level)

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
        self.report({'INFO'}, f"NodeToPython: Saved material to {location}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        self.layout.prop(self, "mode")

class NTPMaterialMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_material"
    bl_label = "Select Material"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for mat in bpy.data.materials: #TODO: filter by node tree exists
            op = layout.operator(NTPMaterialOperator.bl_idname, text=mat.name)
            op.material_name = mat.name
    
class NTPMaterialPanel(bpy.types.Panel):
    bl_label = "Material to Python"
    bl_idname = "NODE_PT_mat_to_python"
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
        row = layout.row()
        
        # Disables menu when there are no materials
        materials = bpy.data.materials #TODO: filter by node tree exist
        materials_exist = len(materials) > 0
        row.enabled = materials_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_ntp_material", text="Materials")