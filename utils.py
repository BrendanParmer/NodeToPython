import bpy
import mathutils

import re
from typing import TextIO, Tuple

def clean_string(string: str) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    clean_str: The input string with nasty characters converted to underscores
    """

    clean_str = re.sub(r"[^a-zA-Z0-9_]", '_', string.lower())
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

def vec3_to_py_str(vec: mathutils.Vector) -> str:
    """
    Converts a 3D vector to a string usable by the add-on

    Parameters:
    vec (mathutils.Vector): a 3d vector

    Returns:
    (str): string version
    """
    return f"({vec[0]}, {vec[1]}, {vec[2]})"

def vec4_to_py_str(vec: mathutils.Vector) -> str:
    """
    Converts a 4D vector to a string usable by the add-on

    Parameters:
    vec (mathutils.Vector): a 4d vector

    Returns:
    (str): string version
    """
    return f"({vec[0]}, {vec[1]}, {vec[2]}, {vec[3]})"

def create_header(file: TextIO, node_tree: bpy.types.NodeTree):
    """
    Sets up the bl_info and imports the Blender API

    Parameters:
    file (TextIO): the file for the generated add-on
    node_tree (bpy.types.NodeTree): the node group object we're converting into an add-on
    """

    file.write("bl_info = {\n")
    file.write(f"\t\"name\" : \"{node_tree.name}\",\n")
    file.write("\t\"author\" : \"Node To Python\",\n")
    file.write("\t\"version\" : (1, 0, 0),\n")
    file.write(f"\t\"blender\" : {bpy.app.version},\n")
    file.write("\t\"location\" : \"Object\",\n")
    file.write("\t\"category\" : \"Object\"\n")
    file.write("}\n")
    file.write("\n")
    file.write("import bpy\n")
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

def create_node(node: bpy.types.Node, file: TextIO, inner: str, 
                node_tree_var: str, unnamed_idx: int = 0) -> Tuple[str, int]:
    """
    Initializes a new node with location, dimension, and label info

    Parameters:
    node (bpy.types.Node): node to be copied
    file (TextIO): file containing the generated add-on
    inner (str): indentation level for this logic
    node_tree_var (str): variable name for the node tree

    Returns:
    node_var (str): variable name for the node
    unnamed_idx (int): unnamed index. if a node doesn't have a name, this will be used to give it a variable name
    """

    file.write(f"{inner}#node {node.name}\n")

    node_var = clean_string(node.name)
    if node_var == "":
        node_var = f"node_{unnamed_idx}"
        unnamed_idx += 1

    file.write((f"{inner}{node_var} "
                f"= {node_tree_var}.nodes.new(\"{node.bl_idname}\")\n"))

    #location
    file.write((f"{inner}{node_var}.location "
                f"= ({node.location.x}, {node.location.y})\n"))
    #dimensions
    file.write((f"{inner}{node_var}.width, {node_var}.height "
                f"= {node.width}, {node.height}\n"))
    #label
    if node.label:
        file.write(f"{inner}{node_var}.label = \"{node.label}\"\n")

    return node_var, unnamed_idx

def set_settings_defaults(node: bpy.types.Node, settings: dict, file: TextIO, 
                            inner: str, node_var: str):
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
                    attr = f"\'{attr}\'"
                if type(attr) == mathutils.Vector:
                    attr = f"({attr[0]}, {attr[1]}, {attr[2]})"
                file.write((f"{inner}{node_var}.{setting} "
                            f"= {attr}\n"))

def color_ramp_settings(node: bpy.types.Node, file: TextIO, inner: str, 
                    node_var: str):
    """
    node (bpy.types.Node): node object we're copying settings from
    file (TextIO): file we're generating the add-on into
    inner (str): indentation
    node_var (str): name of the variable we're using for the color ramp
    """

    color_ramp = node.color_ramp
    #settings
    file.write((f"{inner}{node_var}.color_ramp.color_mode = "
                f"\'{color_ramp.color_mode}\'\n"))
    file.write((f"{inner}{node_var}.color_ramp.hue_interpolation = "
                f"\'{color_ramp.hue_interpolation}\'\n"))
    file.write((f"{inner}{node_var}.color_ramp.interpolation "
                f"= '{color_ramp.interpolation}'\n"))
    file.write("\n")

    #key points
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

def curve_node_settings(node: bpy.types.Node, file: TextIO, inner: str, 
                        node_var: str):
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
    mapping = f"{inner}{node_var}.mapping"

    #extend
    extend = f"\'{node.mapping.extend}\'"
    file.write(f"{mapping}.extend = {extend}\n")
    #tone
    tone = f"\'{node.mapping.tone}\'"
    file.write(f"{mapping}.tone = {tone}\n")

    #black level
    b_lvl = node.mapping.black_level
    b_lvl_str = f"({b_lvl[0]}, {b_lvl[1]}, {b_lvl[2]})"
    file.write((f"{mapping}.black_level = {b_lvl_str}\n"))
    #white level
    w_lvl = node.mapping.white_level
    w_lvl_str = f"({w_lvl[0]}, {w_lvl[1]}, {w_lvl[2]})"
    file.write((f"{mapping}.white_level = {w_lvl_str}\n"))

    #minima and maxima
    min_x = node.mapping.clip_min_x
    file.write(f"{mapping}.clip_min_x = {min_x}\n")
    min_y = node.mapping.clip_min_y
    file.write(f"{mapping}.clip_min_y = {min_y}\n")
    max_x = node.mapping.clip_max_x
    file.write(f"{mapping}.clip_max_x = {max_x}\n")
    max_y = node.mapping.clip_max_y
    file.write(f"{mapping}.clip_max_y = {max_y}\n")

    #use_clip
    use_clip = node.mapping.use_clip
    file.write(f"{mapping}.use_clip = {use_clip}\n")

    #create curves
    for i, curve in enumerate(node.mapping.curves):
        file.write(f"{inner}#curve {i}\n")
        curve_i = f"{node_var}_curve_{i}"
        file.write((f"{inner}{curve_i} = {node_var}.mapping.curves[{i}]\n"))
        for j, point in enumerate(curve.points):
            point_j = f"{inner}{curve_i}_point_{j}"

            loc = point.location
            file.write((f"{point_j} = {curve_i}.points.new({loc[0]}, {loc[1]})\n"))

            handle = f"\'{point.handle_type}\'"
            file.write(f"{point_j}.handle_type = {handle}\n")
    
    #update curve
    file.write(f"{inner}#update curve after changes\n")
    file.write(f"{mapping}.update()\n")

def set_input_defaults(node: bpy.typesNode, dont_set_defaults: dict, 
                        file: TextIO, inner: str, node_var: str):
    for i, input in enumerate(node.inputs):
        if input.bl_idname not in dont_set_defaults:
            if input.bl_idname == 'NodeSocketColor':
                dv = vec4_to_py_str(input.default_value)
            elif "Vector" in input.bl_idname:
                dv = vec3_to_py_str(input.default_value)
            elif input.bl_idname == 'NodeSocketString':
                dv = f"\"{input.default_value}\""
            else:
                dv = input.default_value
            if dv is not None:
                file.write(f"{inner}#{input.identifier}\n")
                file.write((f"{inner}{node_var}.inputs[{i}].default_value = "
                            f"{dv}\n"))