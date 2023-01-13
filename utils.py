import bpy
import re
from typing import TextIO, Tuple

def clean_string(string: str) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    str: The input string with nasty characters converted to underscores
    """

    clean_str = string.lower()
    return re.sub(r"[^a-zA-Z0-9_]", '_', clean_str)

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

def create_node(node: bpy.types.Node, file: TextIO, inner: str, node_tree_var: str, unnamed_idx: int = 0) -> Tuple[str, int]:
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