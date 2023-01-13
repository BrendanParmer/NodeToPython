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
        
        def process_mat_node_group(node_group, level):
            ng_name = utils.clean_string(node_group.name)
            ng_label = node_group.name

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
            for node in node_group.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    if node.node_tree is not None:
                        process_mat_node_group(node.node_tree, level + 1)
                
                node_var, unnamed_idx = utils.create_node(node, file, inner, ng_name, unnamed_idx)
                
                utils.set_settings_defaults(node, node_settings, file, inner, node_var)

                if node.bl_idname == 'ShaderNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'ShaderNodeValToRGB':
                    color_ramp = node.color_ramp
                    file.write("\n")
                    file.write((f"{inner}{node_var}.color_ramp.color_mode = "
                                f"\'{color_ramp.color_mode}\'\n"))
                    file.write((f"{inner}{node_var}.color_ramp"
                                f".hue_interpolation = "
                                f"\'{color_ramp.hue_interpolation}\'\n"))
                    file.write((f"{inner}{node_var}.color_ramp.interpolation "
                                f"= '{color_ramp.interpolation}'\n"))
                    file.write("\n")
                    for i, element in enumerate(color_ramp.elements):
                        file.write((f"{inner}{node_var}_cre_{i} = "
                                    f"{node_var}.color_ramp.elements"
                                    f".new({element.position})\n"))
                        file.write((f"{inner}{node_var}_cre_{i}.alpha = "
                                    f"{element.alpha}\n"))
                        col = element.color
                        r, g, b, a = col[0], col[1], col[2], col[3]
                        file.write((f"{inner}{node_var}_cre_{i}.color = "
                                    f"({r}, {g}, {b}, {a})\n\n"))
                elif node.bl_idname in curve_nodes:
                    file.write(f"{inner}#mapping settings\n")
                    mapping = f"{inner}{node_var}.mapping"

                    extend = f"\'{node.mapping.extend}\'"
                    file.write(f"{mapping}.extend = {extend}\n")
                    tone = f"\'{node.mapping.tone}\'"
                    file.write(f"{mapping}.tone = {tone}\n")

                    b_lvl = node.mapping.black_level
                    b_lvl_str = f"({b_lvl[0]}, {b_lvl[1]}, {b_lvl[2]})"
                    file.write((f"{mapping}.black_level = {b_lvl_str}\n"))
                    w_lvl = node.mapping.white_level
                    w_lvl_str = f"({w_lvl[0]}, {w_lvl[1]}, {w_lvl[2]})"
                    file.write((f"{mapping}.white_level = {w_lvl_str}\n"))

                    min_x = node.mapping.clip_min_x
                    file.write(f"{mapping}.clip_min_x = {min_x}\n")
                    min_y = node.mapping.clip_min_y
                    file.write(f"{mapping}.clip_min_y = {min_y}\n")
                    max_x = node.mapping.clip_max_x
                    file.write(f"{mapping}.clip_max_x = {max_x}\n")
                    max_y = node.mapping.clip_max_y
                    file.write(f"{mapping}.clip_max_y = {max_y}\n")

                    use_clip = node.mapping.use_clip
                    file.write(f"{mapping}.use_clip = {use_clip}\n")

                    for i, curve in enumerate(node.mapping.curves):
                        file.write(f"{inner}#curve {i}\n")
                        curve_i = f"{node_var}_curve_{i}"
                        file.write((f"{inner}{curve_i} = "
                                    f"{node_var}.mapping.curves[{i}]\n"))
                        for j, point in enumerate(curve.points):
                            point_j = f"{inner}{curve_i}_point_{j}"

                            loc = point.location
                            file.write((f"{point_j} = "
                                        f"{curve_i}.points.new"
                                        f"({loc[0]}, {loc[1]})\n"))

                            handle = f"\'{point.handle_type}\'"
                            file.write(f"{point_j}.handle_type = {handle}\n")
                    file.write(f"{inner}#update curve after changes\n")
                    file.write(f"{mapping}.update()\n")

                if node.bl_idname != 'NodeReroute':
                    def default_value(i, socket, list_name):
                        if socket.bl_idname not in dont_set_defaults:
                            dv = None
                            if socket.bl_idname == 'NodeSocketColor':
                                col = socket.default_value
                                dv = f"({col[0]}, {col[1]}, {col[2]}, {col[3]})"
                            elif "Vector" in socket.bl_idname:
                                vector = socket.default_value
                                dv = f"({vector[0]}, {vector[1]}, {vector[2]})"
                            elif socket.bl_idname == 'NodeSocketString':
                                dv = f"\"\""
                            else:
                                dv = socket.default_value
                            if dv is not None:
                                file.write(f"{inner}#{socket.identifier}\n")
                                file.write((f"{inner}{node_var}"
                                            f".{list_name}[{i}]"
                                            f".default_value = {dv}\n"))  
                    for i, input in enumerate(node.inputs):
                        default_value(i, input, "inputs")
                    """
                    TODO: some shader nodes require you set the default value in the output.
                    this will need to be handled case by case it looks like though

                    for i, output in enumerate(node.outputs):
                        default_value(i, output, "outputs")
                    """

            #initialize links
            if node_group.links:
                file.write(f"{inner}#initialize {ng_name} links\n")     
            for link in node_group.links:
                input_node = utils.clean_string(link.from_node.name)
                input_socket = link.from_socket
                
                """
                Blender's socket dictionary doesn't guarantee 
                unique keys, which has caused much wailing and
                gnashing of teeth. This is a quick fix that
                doesn't run quick
                """
                for i, item in enumerate(link.from_node.outputs.items()):
                    if item[1] == input_socket:
                        input_idx = i
                        break
                
                output_node = utils.clean_string(link.to_node.name)
                output_socket = link.to_socket
                
                for i, item in enumerate(link.to_node.inputs.items()):
                    if item[1] == output_socket:
                        output_idx = i
                        break
                
                file.write((f"{inner}#{input_node}.{input_socket.name} "
                            f"-> {output_node}.{output_socket.name}\n"))
                file.write((f"{inner}{ng_name}.links.new({input_node}"
                            f".outputs[{input_idx}], "
                            f"{output_node}.inputs[{output_idx}])\n"))
            
            file.write(f"{outer}{ng_name}_node_group()\n")
                
        process_mat_node_group(ng, 2)

        file.write("\t\treturn {'FINISHED'}\n\n")

        """Create the function that adds the addon to the menu"""
        def create_menu_func():
            file.write("def menu_func(self, context):\n")
            file.write(f"\tself.layout.operator({class_name}.bl_idname)\n")
            file.write("\n")
        create_menu_func()

        """Create the register function"""
        def create_register():
            file.write("def register():\n")
            file.write(f"\tbpy.utils.register_class({class_name})\n")
            file.write("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
            file.write("\n")
        create_register()

        """Create the unregister function"""
        def create_unregister():
            file.write("def unregister():\n")
            file.write(f"\tbpy.utils.unregister_class({class_name})\n")
            file.write("\tbpy.types.VIEW3D_MT_objects.remove(menu_func)\n")
            file.write("\n")
        create_unregister()

        """Create the main function"""
        def create_main():
            file.write("if __name__ == \"__main__\":\n")
            file.write("\tregister()")
        create_main()

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