import bpy
import mathutils

import os
import re
import shutil
from typing import TextIO, Tuple

image_dir_name = "imgs"

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketGeometry',
                     'NodeSocketShader',
                     'NodeSocketVirtual'}

#node tree input sockets that have default properties
default_sockets = {'VALUE', 'INT', 'BOOLEAN', 'VECTOR', 'RGBA'}

def clean_string(string: str, lower: bool = True) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    clean_str: The input string with nasty characters converted to underscores
    """

    if lower:
        string = string.lower()
    clean_str = re.sub(r"[^a-zA-Z0-9_]", '_', string)
    return clean_str

def enum_to_py_str(enum: str) -> str:
    """
    Converts an enum into a string usuable in the add-on

    Parameters:
    enum (str): enum to be converted

    Returns:
    (str): converted string
    """
    return f"\'{enum}\'"
    
def str_to_py_str(string: str) -> str:
    """
    Converts a regular string into one usuable in the add-on

    Parameters:
    string (str): string to be converted

    Returns:
    (str): converted string
    """
    return f"\"{string}\""

def vec3_to_py_str(vec) -> str:
    """
    Converts a 3D vector to a string usable by the add-on

    Parameters:
    vec (mathutils.Vector): a 3d vector

    Returns:
    (str): string version
    """
    return f"({vec[0]}, {vec[1]}, {vec[2]})"

def vec4_to_py_str(vec) -> str:
    """
    Converts a 4D vector to a string usable by the add-on

    Parameters:
    vec (mathutils.Vector): a 4d vector

    Returns:
    (str): string version
    """
    return f"({vec[0]}, {vec[1]}, {vec[2]}, {vec[3]})"

def img_to_py_str(img) -> str:
    """
    Converts a Blender image into its string

    Paramters:
    img (bpy.types.Image): a Blender image
    
    Returns:
    (str): string version
    """
    name = img.name.split('.', 1)[0]
    format = img.file_format.lower()
    return f"{name}.{format}"

def create_header(file: TextIO, name: str):
    """
    Sets up the bl_info and imports the Blender API

    Parameters:
    file (TextIO): the file for the generated add-on
    name (str): name of the add-on
    """

    file.write("bl_info = {\n")
    file.write(f"\t\"name\" : \"{name}\",\n")
    file.write("\t\"author\" : \"Node To Python\",\n")
    file.write("\t\"version\" : (1, 0, 0),\n")
    file.write(f"\t\"blender\" : {bpy.app.version},\n")
    file.write("\t\"location\" : \"Object\",\n")
    file.write("\t\"category\" : \"Node\"\n")
    file.write("}\n")
    file.write("\n")
    file.write("import bpy\n")
    file.write("import os\n")
    file.write("\n")

def init_operator(file: TextIO, name: str, idname: str, label: str):
    """
    Initializes the add-on's operator 

    Parameters:
    file (TextIO): the file for the generated add-on
    name (str): name for the class
    idname (str): name for the operator
    label (str): appearence inside Blender
    """
    file.write(f"class {name}(bpy.types.Operator):\n")
    file.write(f"\tbl_idname = \"object.{idname}\"\n")
    file.write(f"\tbl_label = \"{label}\"\n")
    file.write("\tbl_options = {\'REGISTER\', \'UNDO\'}\n")
    file.write("\n")

def create_var(name: str, used_vars: dict) -> str:
    """
    Creates a unique variable name for a node tree

    Parameters:
    name (str): basic string we'd like to create the variable name out of
    used_vars (dict): dictionary containing variable names and usage counts

    Returns:
    clean_name (str): variable name for the node tree
    """
    if name == "":
        name = "unnamed"
    clean_name = clean_string(name)
    var = clean_name
    if var in used_vars:
        used_vars[var] += 1
        return f"{clean_name}_{used_vars[var]}"
    else:
        used_vars[var] = 0
        return clean_name

def make_indents(level: int) -> Tuple[str, str]:
    """
    Returns strings with the correct number of indentations 
    given the level in the function.

    Node groups need processed recursively, 
    so there can sometimes be functions in functions.

    Parameters:
    level (int): base number of indentations need

    Returns:
    outer (str): a basic level of indentation for a node group.
    inner (str): a level of indentation beyond outer
    """
    outer = "\t"*level
    inner = "\t"*(level + 1)
    return outer, inner

def create_node(node, file: TextIO, inner: str, node_tree_var: str, 
                node_vars: dict, used_vars: set) -> str:
    """
    Initializes a new node with location, dimension, and label info

    Parameters:
    node (bpy.types.Node): node to be copied
    file (TextIO): file containing the generated add-on
    inner (str): indentation level for this logic
    node_tree_var (str): variable name for the node tree
    node_vars (dict): dictionary containing (bpy.types.Node, str)
        pairs, with a Node and its corresponding variable name
    used_vars (set): set of used variable names

    Returns:
    node_var (str): variable name for the node
    """

    file.write(f"{inner}#node {node.name}\n")

    node_var = create_var(node.name, used_vars)
    node_vars[node] = node_var

    file.write((f"{inner}{node_var} "
                f"= {node_tree_var}.nodes.new(\"{node.bl_idname}\")\n"))
    #label
    if node.label:
        file.write(f"{inner}{node_var}.label = \"{node.label}\"\n")

    #color
    if node.use_custom_color:
        file.write(f"{inner}{node_var}.use_custom_color = True\n")
        file.write(f"{inner}{node_var}.color = {vec3_to_py_str(node.color)}\n")

    #mute
    if node.mute:
        file.write(f"{inner}{node_var}.mute = True\n")
        
    return node_var

def set_settings_defaults(node, settings: dict, file: TextIO, inner: str, 
                            node_var: str):
    """
    Sets the defaults for any settings a node may have

    Parameters:
    node (bpy.types.Node): the node object we're copying settings from
    settings (dict): a predefined dictionary of all settings every node has
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): name of the variable we're using for the node in our add-on
    """
    if node.bl_idname in settings:
        for setting in settings[node.bl_idname]:
            attr = getattr(node, setting, None)
            if attr:
                if type(attr) == str:
                    attr = enum_to_py_str(attr)
                if type(attr) == mathutils.Vector:
                    attr = vec3_to_py_str(attr)
                if type(attr) == bpy.types.bpy_prop_array:
                    attr = vec4_to_py_str(list(attr))
                if type(attr) == bpy.types.Material:
                    name = str_to_py_str(attr.name)
                    file.write((f"{inner}if {name} in bpy.data.materials:\n"))
                    file.write((f"{inner}\t{node_var}.{setting} = "
                                f"bpy.data.materials[{name}]\n"))
                    continue
                if type(attr) == bpy.types.Object:
                    name = str_to_py_str(attr.name)
                    file.write((f"{inner}if {name} in bpy.data.objects:\n"))
                    file.write((f"{inner}\t{node_var}.{setting} = "
                                f"bpy.data.objects[{name}]\n"))
                    continue
                file.write((f"{inner}{node_var}.{setting} "
                            f"= {attr}\n"))

def hide_sockets(node, file: TextIO, inner: str, node_var: str):
    """
    Hide hidden sockets

    Parameters:
    node (bpy.types.Node): node object we're copying socket settings from
    file (TextIO): file we're generating the add-on into
    inner (str): indentation string
    node_var (str): name of the variable we're using for this node
    """
    for i, socket in enumerate(node.inputs):
        if socket.hide is True:
            file.write(f"{inner}{node_var}.inputs[{i}].hide = True\n")
    for i, socket in enumerate(node.outputs):
        if socket.hide is True:
            file.write(f"{inner}{node_var}.outputs[{i}].hide = True\n") 

def group_io_settings(node, file: TextIO, inner: str, io: str, node_tree_var: str, node_tree):
    if io == "input":
        ios = node.outputs
        ntio = node_tree.inputs
    else:
        ios = node.inputs
        ntio = node_tree.outputs
    file.write(f"{inner}#{node_tree_var} {io}s\n")
    for i, inout in enumerate(ios):
        if inout.bl_idname == 'NodeSocketVirtual':
            continue
        file.write(f"{inner}#{io} {inout.name}\n")
        idname = enum_to_py_str(inout.bl_idname)
        name = str_to_py_str(inout.name)
        file.write(f"{inner}{node_tree_var}.{io}s.new({idname}, {name})\n")
        socket = ntio[i]
        socket_var = f"{node_tree_var}.{io}s[{i}]"

        if inout.type in default_sockets:
            #default value
            if inout.type == 'RGBA':
                dv = vec4_to_py_str(socket.default_value)
            elif inout.type == 'VECTOR':
                dv = vec3_to_py_str(socket.default_value)
            else:
                dv = socket.default_value
            file.write(f"{inner}{socket_var}.default_value = {dv}\n")

            #min value
            if hasattr(socket, "min_value"):
                file.write(f"{inner}{socket_var}.min_value = {socket.min_value}\n")
            #max value
            if hasattr(socket, "min_value"):
                file.write((f"{inner}{socket_var}.max_value = {socket.max_value}\n"))
        
        #default attribute name
        if hasattr(socket, "default_attribute_name"):
            if socket.default_attribute_name != "":
                dan = str_to_py_str(socket.default_attribute_name)
                file.write((f"{inner}{socket_var}"
                            f".default_attribute_name = {dan}\n"))

        #attribute domain
        if hasattr(socket, "attribute_domain"):
            ad = enum_to_py_str(socket.attribute_domain)
            file.write(f"{inner}{socket_var}.attribute_domain = {ad}\n")

        #tooltip
        if socket.description != "":
            description = str_to_py_str(socket.description)
            file.write((f"{inner}{socket_var}.description = {description}\n"))

        #hide_value
        if socket.hide_value is True:
            file.write(f"{inner}{socket_var}.hide_value = True\n")

        #hide in modifier
        if hasattr(socket, "hide_in_modifier"):
            if socket.hide_in_modifier is True:
                file.write(f"{inner}{socket_var}.hide_in_modifier = True\n")

        file.write("\n")
    file.write("\n")

def color_ramp_settings(node, file: TextIO, inner: str, node_var: str):
    """
    Replicate a color ramp node

    Parameters
    node (bpy.types.Node): node object we're copying settings from
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): name of the variable we're using for the color ramp
    """

    color_ramp = node.color_ramp
    #settings
    color_mode = enum_to_py_str(color_ramp.color_mode)
    file.write(f"{inner}{node_var}.color_ramp.color_mode = {color_mode}\n")

    hue_interpolation = enum_to_py_str(color_ramp.hue_interpolation)
    file.write((f"{inner}{node_var}.color_ramp.hue_interpolation = "
                f"{hue_interpolation}\n"))
    interpolation = enum_to_py_str(color_ramp.interpolation)
    file.write((f"{inner}{node_var}.color_ramp.interpolation "
                f"= {interpolation}\n"))
    file.write("\n")

    #key points
    file.write((f"{inner}{node_var}.color_ramp.elements.remove"
                f"({node_var}.color_ramp.elements[0])\n"))
    for i, element in enumerate(color_ramp.elements):
        element_var = f"{node_var}_cre_{i}"
        if i == 0:
            file.write(f"{inner}{element_var} = "
                       f"{node_var}.color_ramp.elements[{i}]\n")
            file.write(f"{inner}{element_var}.position = {element.position}\n")
        else:
            file.write((f"{inner}{element_var} = "
                        f"{node_var}.color_ramp.elements"
                        f".new({element.position})\n"))
        file.write((f"{inner}{element_var}.alpha = "
                    f"{element.alpha}\n"))
        color_str = vec4_to_py_str(element.color)
        file.write((f"{inner}{element_var}.color = {color_str}\n\n"))

def curve_node_settings(node, file: TextIO, inner: str, node_var: str):
    """
    Sets defaults for Float, Vector, and Color curves

    Parameters:
    node (bpy.types.Node): curve node we're copying settings from
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): variable name for the add-on's curve node
    """

    #mapping settings
    file.write(f"{inner}#mapping settings\n")
    mapping_var = f"{inner}{node_var}.mapping"

    #extend
    extend = enum_to_py_str(node.mapping.extend)
    file.write(f"{mapping_var}.extend = {extend}\n")
    #tone
    tone = enum_to_py_str(node.mapping.tone)
    file.write(f"{mapping_var}.tone = {tone}\n")

    #black level
    b_lvl_str = vec3_to_py_str(node.mapping.black_level)
    file.write((f"{mapping_var}.black_level = {b_lvl_str}\n"))
    #white level
    w_lvl_str = vec3_to_py_str(node.mapping.white_level)
    file.write((f"{mapping_var}.white_level = {w_lvl_str}\n"))

    #minima and maxima
    min_x = node.mapping.clip_min_x
    file.write(f"{mapping_var}.clip_min_x = {min_x}\n")
    min_y = node.mapping.clip_min_y
    file.write(f"{mapping_var}.clip_min_y = {min_y}\n")
    max_x = node.mapping.clip_max_x
    file.write(f"{mapping_var}.clip_max_x = {max_x}\n")
    max_y = node.mapping.clip_max_y
    file.write(f"{mapping_var}.clip_max_y = {max_y}\n")

    #use_clip
    use_clip = node.mapping.use_clip
    file.write(f"{mapping_var}.use_clip = {use_clip}\n")

    #create curves
    for i, curve in enumerate(node.mapping.curves):
        file.write(f"{inner}#curve {i}\n")
        curve_i = f"{node_var}_curve_{i}"
        file.write((f"{inner}{curve_i} = {node_var}.mapping.curves[{i}]\n"))
        for j, point in enumerate(curve.points):
            point_j = f"{inner}{curve_i}_point_{j}"

            loc = point.location
            loc_str = f"{loc[0]}, {loc[1]}"
            if j < 2:
                file.write(f"{point_j} = {curve_i}.points[{j}]\n")
                file.write(f"{point_j}.location = ({loc_str})\n")
            else:
                file.write((f"{point_j} = {curve_i}.points.new({loc_str})\n"))

            handle = enum_to_py_str(point.handle_type)
            file.write(f"{point_j}.handle_type = {handle}\n")
    
    #update curve
    file.write(f"{inner}#update curve after changes\n")
    file.write(f"{mapping_var}.update()\n")

def set_input_defaults(node, file: TextIO, inner: str, node_var: str, 
                       addon_dir: str = ""):
    """
    Sets defaults for input sockets

    Parameters:
    node (bpy.types.Node): node we're setting inputs for
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): variable name we're using for the copied node
    addon_dir (str): directory of the add-on, for if we need to save other
        objects for the add-on
    """
    if node.bl_idname == 'NodeReroute':
        return

    for i, input in enumerate(node.inputs):
        if input.bl_idname not in dont_set_defaults and not input.is_linked:
            socket_var = f"{node_var}.inputs[{i}]"

            #colors
            if input.bl_idname == 'NodeSocketColor':
                default_val = vec4_to_py_str(input.default_value)

            #vector types
            elif "Vector" in input.bl_idname:
                default_val = vec3_to_py_str(input.default_value)

            #strings
            elif input.bl_idname == 'NodeSocketString':
                default_val = str_to_py_str(input.default_value)

            #images
            elif input.bl_idname == 'NodeSocketImage':
                img = input.default_value
                if img is not None and addon_dir != "": #write in a better way
                    save_image(img, addon_dir)
                    load_image(img, file, inner, f"{socket_var}.default_value")
                default_val = None

            #materials 
            elif input.bl_idname == 'NodeSocketMaterial':
                in_file_inputs(input, file, inner, socket_var, "materials")
                default_val = None

            #collections
            elif input.bl_idname == 'NodeSocketCollection':
                in_file_inputs(input, file, inner, socket_var, "collections")
                default_val = None

            #objects
            elif input.bl_idname == 'NodeSocketObject':
                in_file_inputs(input, file, inner, socket_var, "objects")
                default_val = None
            
            #textures
            elif input.bl_idname == 'NodeSocketTexture':
                in_file_inputs(input, file, inner, socket_var, "textures")
                default_val = None

            else:
                default_val = input.default_value
            if default_val is not None:
                file.write(f"{inner}#{input.identifier}\n")
                file.write((f"{inner}{socket_var}.default_value"
                            f" = {default_val}\n"))
    file.write("\n")

def in_file_inputs(input, file: TextIO, inner: str, socket_var: str, type: str):
    """
    Sets inputs for a node input if one already exists in the blend file

    Parameters:
    input (bpy.types.NodeSocket): input socket we're setting the value for
    file (TextIO): file we're writing the add-on into
    inner (str): indentation string
    socket_var (str): variable name we're using for the socket
    type (str): from what section of bpy.data to pull the default value from
    """

    if input.default_value is not None:
        name = str_to_py_str(input.default_value.name)
        file.write(f"{inner}if {name} in bpy.data.{type}:\n")
        file.write((f"{inner}\t{socket_var}.default_value = "
                                f"bpy.data.{type}[{name}]\n"))

def set_output_defaults(node, file: TextIO, inner: str, node_var: str):
    """
    Some output sockets need default values set. It's rather annoying

    Parameters:
    node (bpy.types.Node): node for the output we're setting
    file (TextIO): file we're generating the add-on into
    inner (str): indentation string
    node_var (str): variable name for the node we're setting output defaults for
    """
    output_default_nodes = {'ShaderNodeValue', 
                            'ShaderNodeRGB', 
                            'ShaderNodeNormal'}

    if node.bl_idname in output_default_nodes:
        dv = node.outputs[0].default_value
        if node.bl_idname == 'ShaderNodeRGB':
            dv = vec4_to_py_str(list(dv))
        if node.bl_idname == 'ShaderNodeNormal':
            dv = vec3_to_py_str(dv)
        file.write((f"{inner}{node_var}.outputs[0].default_value = {dv}\n"))

def set_parents(node_tree, file: TextIO, inner: str, node_vars: dict):
    """
    Sets parents for all nodes, mostly used to put nodes in frames

    Parameters:
    node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
    file (TextIO): file for the generated add-on
    inner (str): indentation string
    node_vars (dict): dictionary for (node, variable) name pairs
    """
    parent_comment = False
    for node in node_tree.nodes:
        if node is not None and node.parent is not None:
            if not parent_comment:
                file.write(f"{inner}#Set parents\n")
                parent_comment = True
            node_var = node_vars[node]
            parent_var = node_vars[node.parent]
            file.write(f"{inner}{node_var}.parent = {parent_var}\n")
    file.write("\n")

def set_locations(node_tree, file: TextIO, inner: str, node_vars: dict):
    """
    Set locations for all nodes

    Parameters:
    node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
    file (TextIO): file for the generated add-on
    inner (str): indentation string
    node_vars (dict): dictionary for (node, variable) name pairs
    """

    file.write(f"{inner}#Set locations\n")
    for node in node_tree.nodes:
        node_var = node_vars[node]
        file.write((f"{inner}{node_var}.location "
                    f"= ({node.location.x}, {node.location.y})\n"))
    file.write("\n")

def set_dimensions(node_tree, file: TextIO, inner: str, node_vars: dict):
    """
    Set dimensions for all nodes

    Parameters:
    node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
    file (TextIO): file for the generated add-on
    inner (str): indentation string
    node_vars (dict): dictionary for (node, variable) name pairs
    """

    file.write(f"{inner}#Set dimensions\n")
    for node in node_tree.nodes:
        node_var = node_vars[node]
        file.write((f"{inner}{node_var}.width, {node_var}.height "
                        f"= {node.width}, {node.height}\n"))
    file.write("\n")

def init_links(node_tree, file: TextIO, inner: str, node_tree_var: str, 
                node_vars: dict):
    """
    Create all the links between nodes

    Parameters:
    node_tree (bpy.types.NodeTree): node tree we're copying
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_tree_var (str): variable name we're using for the copied node tree
    node_vars (dict): dictionary containing node to variable name pairs
    """

    if node_tree.links:
        file.write(f"{inner}#initialize {node_tree_var} links\n")     
    for link in node_tree.links:
        in_node_var = node_vars[link.from_node]
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
        
        out_node_var = node_vars[link.to_node]
        output_socket = link.to_socket
        
        for i, item in enumerate(link.to_node.inputs.items()):
            if item[1] == output_socket:
                output_idx = i
                break
        
        file.write((f"{inner}#{in_node_var}.{input_socket.name} "
                    f"-> {out_node_var}.{output_socket.name}\n"))
        file.write((f"{inner}{node_tree_var}.links.new({in_node_var}"
                    f".outputs[{input_idx}], "
                    f"{out_node_var}.inputs[{output_idx}])\n"))

def create_menu_func(file: TextIO, name: str):
    """
    Creates the menu function

    Parameters:
    file (TextIO): file we're generating the add-on into
    name (str): name of the generated operator class
    """

    file.write("def menu_func(self, context):\n")
    file.write(f"\tself.layout.operator({name}.bl_idname)\n")
    file.write("\n")

def create_register_func(file: TextIO, name: str):
    """
    Creates the register function

    Parameters:
    file (TextIO): file we're generating the add-on into
    name (str): name of the generated operator class
    """
    file.write("def register():\n")
    file.write(f"\tbpy.utils.register_class({name})\n")
    file.write("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
    file.write("\n")

def create_unregister_func(file: TextIO, name: str):
    """
    Creates the unregister function

    Parameters:
    file (TextIO): file we're generating the add-on into
    name (str): name of the generated operator class
    """
    file.write("def unregister():\n")
    file.write(f"\tbpy.utils.unregister_class({name})\n")
    file.write("\tbpy.types.VIEW3D_MT_object.remove(menu_func)\n")
    file.write("\n")

def create_main_func(file: TextIO):
    """
    Creates the main function

    Parameters:
    file (TextIO): file we're generating the add-on into
    """
    file.write("if __name__ == \"__main__\":\n")
    file.write("\tregister()")

def save_image(img, addon_dir: str):
    """
    Saves an image to an image directory of the add-on

    Parameters:
    img (bpy.types.Image): image to be saved
    addon_dir (str): directory of the addon
    """

    if img is None:
        return

    #create image dir if one doesn't exist
    img_dir = os.path.join(addon_dir, image_dir_name)
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    #save the image
    img_str = img_to_py_str(img)
    img_path = f"{img_dir}/{img_str}"
    if not os.path.exists(img_path):
        img.save_render(img_path)

def load_image(img, file: TextIO, inner: str, img_var: str):
    """
    Loads an image from the add-on into a blend file and assigns it

    Parameters:
    img (bpy.types.Image): Blender image from the original node group
    file (TextIO): file for the generated add-on
    inner (str): indentation string
    img_var (str): variable name to be used for the image
    """

    if img is None:
        return
        
    img_str = img_to_py_str(img)

    file.write(f"{inner}#load image {img_str}\n")
    file.write((f"{inner}base_dir = "
                f"os.path.dirname(os.path.abspath(__file__))\n"))
    file.write((f"{inner}image_path = "
                f"os.path.join(base_dir, \"{image_dir_name}\", "
                f"\"{img_str}\")\n"))
    file.write((f"{inner}{img_var} = "
                f"bpy.data.images.load(image_path, check_existing = True)\n"))

    #copy image settings
    file.write(f"{inner}#set image settings\n")

    #source
    source = enum_to_py_str(img.source)
    file.write(f"{inner}{img_var}.source = {source}\n")

    #color space settings
    color_space = enum_to_py_str(img.colorspace_settings.name)
    file.write(f"{inner}{img_var}.colorspace_settings.name = {color_space}\n")
    
    #alpha mode
    alpha_mode = enum_to_py_str(img.alpha_mode)
    file.write(f"{inner}{img_var}.alpha_mode = {alpha_mode}\n")

def image_user_settings(node, file: TextIO, inner: str, node_var: str):
    """
    Replicate the image user of an image node

    Parameters
    node (bpy.types.Node): node object we're copying settings from
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): name of the variable we're using for the color ramp
    """

    if not hasattr(node, "image_user"):
        raise ValueError("Node must have attribute \"image_user\"")

    img_usr = node.image_user
    img_usr_var = f"{node_var}.image_user"

    img_usr_attrs = ["frame_current", "frame_duration", "frame_offset",
                     "frame_start", "tile", "use_auto_refresh", "use_cyclic"]
    
    for img_usr_attr in img_usr_attrs:
        file.write((f"{inner}{img_usr_var}.{img_usr_attr} = "
                    f"{getattr(img_usr, img_usr_attr)}\n"))
    
def zip_addon(zip_dir: str):
    """
    Zips up the addon and removes the directory

    Parameters:
    zip_dir (str): path to the top-level addon directory
    """
    shutil.make_archive(zip_dir, "zip", zip_dir)
    shutil.rmtree(zip_dir)