import bpy
import os

from .utils import *

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketCollection',
                     'NodeSocketGeometry',
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
        nt = bpy.data.materials[self.material_name].node_tree
        if nt is None:
            self.report({'ERROR'},
                        ("NodeToPython: This doesn't seem to be a valid "
                            "material. Is Use Nodes selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        mat_var = clean_string(self.material_name)
        class_name = nt.name.replace(" ", "")
        
        dir = bpy.path.abspath("//")
        if not dir or dir == "":
            self.report({'ERROR'},
                        ("NodeToPython: Save your blender file before using "
                        "NodeToPython!"))
            return {'CANCELLED'}
        zip_dir = os.path.join(dir, "addons", mat_var)
        addon_dir = os.path.join(zip_dir, mat_var)
        if not os.path.exists(addon_dir):
            os.makedirs(addon_dir)
        file = open(f"{addon_dir}/__init__.py", "w")

        create_header(file, self.material_name)  
        init_operator(file, class_name, mat_var, self.material_name)

        file.write("\tdef execute(self, context):\n")

        def create_material():
            file.write((f"\t\tmat = bpy.data.materials.new("
                        f"name = \"{self.material_name}\")\n"))
            file.write(f"\t\tmat.use_nodes = True\n")
        create_material()
        
        node_trees = set()

        def process_mat_node_group(node_tree, level):
            nt_var = clean_string(node_tree.name)
            nt_name = node_tree.name

            if level == 2: #outermost node group
                nt_var = clean_string(self.material_name)
                nt_name = self.material_name

            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {nt_var} node group\n")
            file.write(f"{outer}def {nt_var}_node_group():\n")

            if level == 2: #outermost node group
                file.write(f"{inner}{nt_var} = mat.node_tree\n")
                file.write(f"{inner}#start with a clean node tree\n")
                file.write(f"{inner}for node in {nt_var}.nodes:\n")
                file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
            else:
                file.write((f"{inner}{nt_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \"ShaderNodeTree\", "
                        f"name = \"{nt_name}\")\n"))
                file.write("\n")

            #initialize nodes
            file.write(f"{inner}#initialize {nt_var} nodes\n")

            node_vars = {}
            for node in node_tree.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_mat_node_group(node_nt, level + 1)
                        node_trees.add(node_nt)
                
                node_var, node_vars = create_node(node, file, inner, nt_var,
                                                  node_vars)
                
                set_settings_defaults(node, node_settings, file, inner, node_var)
                hide_sockets(node, file, inner, node_var)

                if node.bl_idname == 'ShaderNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'ShaderNodeTexImage':
                    save_image(node.image, addon_dir)
                    load_image(node.image, file, inner, f"{node_var}.image")
                elif node.bl_idname == 'ShaderNodeValToRGB':
                    color_ramp_settings(node, file, inner, node_var)
                elif node.bl_idname in curve_nodes:
                    curve_node_settings(node, file, inner, node_var)

                set_input_defaults(node, dont_set_defaults, file, inner, 
                                    node_var, addon_dir)
            set_parents(node_tree, file, inner, node_vars)
            set_locations(node_tree, file, inner, node_vars)
            set_dimensions(node_tree, file, inner, node_vars)
            
            init_links(node_tree, file, inner, nt_var, node_vars)
            
            file.write(f"\n{outer}{nt_var}_node_group()\n\n")
                
        process_mat_node_group(nt, 2)

        file.write("\t\treturn {'FINISHED'}\n\n")

        create_menu_func(file, class_name)
        create_register_func(file, class_name)
        create_unregister_func(file, class_name)
        create_main_func(file)

        file.close()
        zip_addon(zip_dir)
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