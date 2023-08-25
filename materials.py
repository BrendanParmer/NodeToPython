import bpy
import os

from .utils import *
from io import StringIO

shader_node_settings : dict[str, list[(str, str)]] = {
    # INPUT
    'ShaderNodeAmbientOcclusion' : [("inside", "bool"),
                                    ("only_local", "bool"),
                                    ("samples", "int")],
    'ShaderNodeAttribute'        : [("attribute_name", "str"),
                                    ("attribute_type", "enum")],
    'ShaderNodeBevel'            : [("samples", "int")],
    'ShaderNodeCameraData'       : [],
    'ShaderNodeVertexColor'      : [("layer_name", "str")],
    'ShaderNodeHairInfo'         : [],
    'ShaderNodeFresnel'          : [],
    'ShaderNodeNewGeometry'      : [],
    'ShaderNodeLayerWeight'      : [],
    'ShaderNodeLightPath'        : [],
    'ShaderNodeObjectInfo'       : [],
    'ShaderNodeParticleInfo'     : [],
    'ShaderNodePointInfo'        : [],
    'ShaderNodeRGB'              : [],
    'ShaderNodeTangent'          : [("axis", "enum"),
                                    ("direction_type", "enum"),
                                    ("uv_map", "str")], #TODO: makes sense? maybe make special type
    'ShaderNodeTexCoord'         : [("from_instancer", "bool"),
                                    ("object", "Object")],
    'ShaderNodeUVAlongStroke'     : [("use_tips", "bool")],
    'ShaderNodeUVMap'            : [("from_instancer", "bool"), 
                                    ("uv_map", "str")], #TODO: see ShaderNodeTangent
    'ShaderNodeValue'            : [],
    'ShaderNodeVolumeInfo'       : [],
    'ShaderNodeWireframe'        : [("use_pixel_size", "bool")],


    # OUTPUT
    'ShaderNodeOutputAOV'       : [("name", "str")],
    'ShaderNodeOutputLight'     : [("is_active_output", "bool"),
                                   ("target", "enum")],
    'ShaderNodeOutputLineStyle' : [("blend_type", "enum"),
                                   ("is_active_output", "bool"),
                                   ("target", "enum"),
                                   ("use_alpha", "bool"),
                                   ("use_clamp", "bool")],
    'ShaderNodeOutputMaterial'  : [("is_active_output", "bool"),
                                   ("target", "enum")],
    'ShaderNodeOutputWorld'     : [("is_active_output", "bool"),
                                   ("target", "enum")],


    # SHADER
    'ShaderNodeAddShader'            : [],
    'ShaderNodeBsdfAnisotropic'      : [("distribution", "enum")],
    'ShaderNodeBackground'           : [],
    'ShaderNodeBsdfDiffuse'          : [],
    'ShaderNodeEmission'             : [],
    'ShaderNodeBsdfGlass'            : [("distribution", "enum")],
    'ShaderNodeBsdfGlossy'           : [("distribution", "enum")],
    'ShaderNodeBsdfHair'             : [("component", "enum")],
    'ShaderNodeHoldout'              : [],
    'ShaderNodeMixShader'            : [],
    'ShaderNodeBsdfPrincipled'       : [("distribution", "enum"),
                                        ("subsurface_method", "enum")],
    'ShaderNodeBsdfHairPrincipled'   : [("parametrization", "enum")],
    'ShaderNodeVolumePrincipled'     : [],
    'ShaderNodeBsdfRefraction'       : [("distribution", "enum")],
    'ShaderNodeEeveeSpecular'        : [],
    'ShaderNodeSubsurfaceScattering' : [("falloff", "enum")],
    'ShaderNodeBsdfToon'             : [("component", "enum")],
    'ShaderNodeBsdfTranslucent'      : [],
    'ShaderNodeBsdfTransparent'      : [],
    'ShaderNodeBsdfVelvet'           : [],
    'ShaderNodeVolumeAbsorption'     : [],
    'ShaderNodeVolumeScatter'        : [],


    # TEXTURE
    'ShaderNodeTexBrick'        : [("offset", "float"), 
                                   ("offset_frequency", "int"),
                                   ("squash", "float"),
                                   ("squash_frequency", "int")],
    'ShaderNodeTexChecker'      : [],
    'ShaderNodeTexEnvironment'  : [("image", "Image"),
                                   ("image_user", "ImageUser"),
                                   ("interpolation", "enum"),
                                   ("projection", "enum")],
    'ShaderNodeTexGradient'     : [("gradient_type", "enum")],
    'ShaderNodeTexIES'          : [("filepath", "str"), #TODO
                                   ("ies", "Text"),
                                   ("mode", "enum")],
    'ShaderNodeTexImage'        : [("extension", "enum"),
                                   ("image", "Image"),
                                   ("image_user", "ImageUser"),
                                   ("interpolation", "enum"),
                                   ("projection", "enum"),
                                   ("projection_blend", "float")],
    'ShaderNodeTexMagic'        : [("turbulence_depth", "int")],
    'ShaderNodeTexMusgrave'     : [("musgrave_dimensions", "enum"),
                                   ("musgrave_type", "enum")],
    'ShaderNodeTexNoise'        : [("noise_dimensions", "enum")],
    'ShaderNodeTexPointDensity' : [("interpolation", "enum"),
                                   ("object", "Object"),
                                   ("particle_color_source", "enum"),
                                   ("particle_system", "ParticleSystem"),
                                   ("point_source", "enum"),
                                   ("radius", "float"),
                                   ("resolution", "int"),
                                   ("space", "enum"),
                                   ("vertex_attribute_name", "str"), #TODO
                                   ("vertex_color_source", "enum")],
    'ShaderNodeTexSky'          : [("air_density", "float"),
                                   ("altitude", "float"),
                                   ("dust_density", "float"),
                                   ("ground_albedo", "float"),
                                   ("ozone_density", "float"),
                                   ("sky_type", "enum"),
                                   ("sun_direction", "Vec3"),
                                   ("sun_disc", "bool"),
                                   ("sun_elevation", "float"),
                                   ("sun_intensity", "float"),
                                   ("sun_rotation", "float"),
                                   ("sun_size", "float")
                                   ("turbidity", "float")],
    'ShaderNodeTexVoronoi'      : [("distance", "enum"),
                                   ("feature", "enum"),
                                   ("voronoi_dimensions", "enum")],
    'ShaderNodeTexWave'         : [("bands_direction", "enum"),
                                   ("rings_direction", "enum"),
                                   ("wave_profile", "enum"),
                                   ("wave_type", "enum")],
    'ShaderNodeTexWhiteNoise'   : [("noise_dimensions", "enum")],


    # COLOR
    'ShaderNodeBrightContrast' : [],
    'ShaderNodeGamma'          : [],
    'ShaderNodeHueSaturation'  : [],
    'ShaderNodeInvert'         : [],
    'ShaderNodeLightFalloff'   : [],
    'ShaderNodeMix'            : [("blend_type", "enum"),
                                  ("clamp_factor", "bool"),
                                  ("clamp_result", "bool"),
                                  ("data_type", "enum"),
                                  ("factor_mode", "enum")],
    'ShaderNodeRGBCurve'       : [("mapping", "CurveMapping")],


    # VECTOR
    'ShaderNodeBump'               : [("invert", "bool")],
    'ShaderNodeDisplacement'       : [("space", "enum")],
    'ShaderNodeMapping'            : [("vector_type", "enum")],
    'ShaderNodeNormalMap'          : [("space", "enum"),
                                      ("uv_map", "str")], #TODO
    'ShaderNodeVectorCurve'        : [("mapping", "CurveMapping")],
    'ShaderNodeVectorDisplacement' : [("space", "enum")],
    'ShaderNodeVectorRotate'       : [("invert", "bool"),
                                      ("rotation_type", "enum")],
    'ShaderNodeVectorTransform'    : [("convert_from", "enum"),
                                      ("convert_to", "enum"),
                                      ("vector_type", "enum")],
    

    # CONVERTER
    'ShaderNodeBlackbody'     : [],
    'ShaderNodeClamp'         : [("clamp_type", "enum")],
    'ShaderNodeValToRGB'      : [("color_ramp", "ColorRamp")],
    'ShaderNodeCombineColor'  : [("mode", "enum")],
    'ShaderNodeCombineXYZ'    : [],
    'ShaderNodeFloatCurve'    : [("mapping", "CurveMapping")],
    'ShaderNodeMapRange'      : [("clamp", "bool"),
                                 ("data_type", "enum"),
                                 ("interpolation_type", "enum")],
    'ShaderNodeMath'          : [("operation", "enum"), 
                                 ("use_clamp", "bool")],
    'ShaderNodeRGBToBW'       : [],
    'ShaderNodeSeparateColor' : [("mode", "enum")],
    'ShaderNodeSeparateXYZ'   : [],
    'ShaderNodeShaderToRGB'   : [],
    'ShaderNodeVectorMath'    : [("operation", "enum")],
    'ShaderNodeWavelength'    : [],


    # SCRIPT
    'ShaderNodeScript' : [("bytecode", "str"), #TODO: test all that
                          ("bytecode_hash", "str"),
                          ("filepath", "str"),
                          ("mode", "enum"),
                          ("script", "text"),
                          ("use_auto_update", "bool")]
}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}

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
            file.write((f"{indent}mat = bpy.data.materials.new(" #TODO: see if using mat effects nodes named mat
                        f"name = {str_to_py_str(self.material_name)})\n"))
            file.write(f"{indent}mat.use_nodes = True\n")
        
        if self.mode == 'ADDON':
            create_material("\t\t")
        elif self.mode == 'SCRIPT': #TODO: should add option for just creating the node group
            create_material("")
        
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

        def process_mat_node_group(node_tree, level, node_vars, used_vars):
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
                file.write(f"{inner}{nt_var} = mat.node_tree\n")
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
                        process_mat_node_group(node_nt, level + 1, node_vars, 
                                               used_vars)
                        node_trees.add(node_nt)
                
                node_var = create_node(node, file, inner, nt_var, node_vars, 
                                       used_vars)
                
                set_settings_defaults(node, node_settings, file, inner, node_var)
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
        process_mat_node_group(nt, level, node_vars, used_vars)

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