import bpy
import mathutils
import os

from . import utils

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketCollection',
                     'NodeSocketGeometry',
                     'NodeSocketImage',
                     'NodeSocketMaterial',
                     'NodeSocketObject',
                     'NodeSocketShader',
                     'NodeSocketTexture',
                     'NodeSocketVirtual'}

node_settings = {
    #input
    "ShaderNodeAmbientOcclusion" : ["samples", "inside", "only_local"],
    "ShaderNodeAttribute" : ["attribute_type", "attribute_name"],
    "ShaderNodeBevel" : ["samples"],
    "ShaderNodeVertexColor" : ["layer_name"],
    "ShaderNodeTangent" : ["direction_type", "axis"],
    "ShaderNodeTexCoord" : ["from_instancer"],
    "ShaderNodeUVMap" : ["from_instancer", "uv_map"],
    "ShaderNodeWireframe" : ["use_pixel_size"],

    #output
    "ShaderNodeOutputAOV" : ["name"],
    "ShaderNodeOutputMaterial" : ["target"],

    #shader
    "ShaderNodeBsdfGlass" : ["distribution"],
    "ShaderNodeBsdfGlossy" : ["distribution"],
    "ShaderNodeBsdfPrincipled" : ["distribution", "subsurface_method"],
    "ShaderNodeBsdfRefraction" : ["distribution"],
    "ShaderNodeSubsurfaceScattering" : ["falloff"],

    #texture
    "ShaderNodeTexBrick" : ["offset", "offset_frequency", "squash", "squash_frequency"],
    "ShaderNodeTexEnvironment" : ["interpolation", "projection", "image_user.frame_duration", "image_user.frame_start", "image_user.frame_offset", "image_user.use_cyclic", "image_user.use_auto_refresh"],
    "ShaderNodeTexGradient" : ["gradient_type"],
    "ShaderNodeTexIES" : ["mode"],
    "ShaderNodeTexImage" : ["interpolation", "projection", "projection_blend", 
                            "extension"],
    "ShaderNodeTexMagic" : ["turbulence_depth"],
    "ShaderNodeTexMusgrave" : ["musgrave_dimensions", "musgrave_type"],
    "ShaderNodeTexNoise" : ["noise_dimensions"],
    "ShaderNodeTexPointDensity" : ["point_source", "space", "radius", 
                                    "interpolation", "resolution", 
                                    "vertex_color_source"],
    "ShaderNodeTexSky" : ["sky_type", "sun_direction", "turbidity",
                            "ground_albedo", "sun_disc", "sun_elevation", 
                            "sun_rotation", "altitude", "air_density", 
                            "dust_density", "ozone_density"],
    "ShaderNodeTexVoronoi" : ["voronoi_dimensions", "feature", "distance"],
    "ShaderNodeTexWave" : ["wave_type", "rings_direction", "wave_profile"],
    "ShaderNodeTexWhiteNoise" : ["noise_dimensions"],

    #color
    "ShaderNodeMix" : ["data_type", "clamp_factor", "factor_mode", "blend_type",
                        "clamp_result"],

    #vector
    "ShaderNodeBump" : ["invert"],
    "ShaderNodeDisplacement" : ["space"],
    "ShaderNodeMapping" : ["vector_type"],
    "ShaderNodeNormalMap" : ["space", "uv_map"],
    "ShaderNodeVectorDisplacement" : ["space"],
    "ShaderNodeVectorRotate" : ["rotation_type", "invert"],
    "ShaderNodeVectorTransform" : ["vector_type", "convert_from", "convert_to"],
    
    #converter
    "ShaderNodeClamp" : ["clamp_type"],
    "ShaderNodeCombineColor" : ["mode"],
    "ShaderNodeMapRange" : ["data_type", "interpolation_type", "clamp"],
    "ShaderNodeMath" : ["operation", "use_clamp"],
    "ShaderNodeSeparateColor" : ["mode"],
    "ShaderNodeVectorMath" : ["operation"]
}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}   

class MaterialToPython(bpy.types.Operator):
    bl_idname = "node.material_to_python"
    bl_label =  "Material to Python"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(name="Node Group")

    def execute(self, context):
        #find node group to replicate
        ng = bpy.data.materials[self.material_name].node_tree
        if ng is None:
            self.report({'ERROR'},
                        ("NodeToPython: This doesn't seem to be a valid "
                            "material. Is Use Nodes selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        ng_name = utils.clean_string(self.material_name)
        class_name = ng.name.replace(" ", "")
        
        dir = bpy.path.abspath("//")
        if not dir or dir == "":
            self.report({'ERROR'},
                        ("NodeToPython: Save your blender file before using "
                        "NodeToPython!"))
            return {'CANCELLED'}
        addon_dir = os.path.join(dir, "addons")
        if not os.path.exists(addon_dir):
            os.mkdir(addon_dir)
        file = open(f"{addon_dir}/{ng_name}_addon.py", "w")

        utils.create_header(file, ng)  
        utils.init_operator(file, class_name, ng_name, self.material_name)

        file.write("\tdef execute(self, context):\n")

        def create_material():
            file.write((f"\t\tmat = bpy.data.materials.new("
                        f"name = \"{self.material_name}\")\n"))
            file.write(f"\t\tmat.use_nodes = True\n")
        create_material()
        
        node_trees = {}

        def process_mat_node_group(node_tree, level):
            ng_name = utils.clean_string(node_tree.name)
            ng_label = node_tree.name

            if level == 2: #outermost node group
                ng_name = utils.clean_string(self.material_name)
                ng_label = self.material_name

            outer, inner = utils.make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {ng_name} node group\n")
            file.write(f"{outer}def {ng_name}_node_group():\n")

            if level == 2: #outermost node group
                file.write(f"{inner}{ng_name} = mat.node_tree\n")
            else:
                file.write((f"{inner}{ng_name}"
                        f"= bpy.data.node_groups.new("
                        f"type = \"ShaderNodeTree\", "
                        f"name = \"{ng_label}\")\n"))
                file.write("\n")

            #initialize nodes
            file.write(f"{inner}#initialize {ng_name} nodes\n")

            unnamed_idx = 0
            for node in node_tree.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_mat_node_group(node_nt, level + 1)
                        node_trees.add(node_nt)
                
                node_var, unnamed_idx = utils.create_node(node, file, inner, ng_name, unnamed_idx)
                
                utils.set_settings_defaults(node, node_settings, file, inner, node_var)

                if node.bl_idname == 'ShaderNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'ShaderNodeValToRGB':
                    utils.color_ramp_settings(node, file, inner, node_var)
                elif node.bl_idname in curve_nodes:
                    utils.curve_node_settings(node, file, inner, node_var)

                utils.set_input_defaults(node, dont_set_defaults, file, inner, 
                                         node_var)

            utils.init_links(node_tree, file, inner, ng_name)
            
            file.write(f"\n{outer}{ng_name}_node_group()\n\n")
                
        process_mat_node_group(ng, 2)

        file.write("\t\treturn {'FINISHED'}\n\n")

        utils.create_menu_func(file, class_name)
        utils.create_register_func(file, class_name)
        utils.create_unregister_func(file, class_name)
        utils.create_main_func(file, class_name)

        file.close()
        return {'FINISHED'}

class SelectMaterialMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_npt_mat_selection"
    bl_label = "Select Material"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for mat in bpy.data.materials:
            op = layout.operator(MaterialToPython.bl_idname, text=mat.name)
            op.material_name = mat.name
    
class MaterialToPythonPanel(bpy.types.Panel):
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
        materials = bpy.data.materials
        materials_exist = len(materials) > 0
        row.enabled = materials_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_npt_mat_selection", text="Materials")