import bpy
import typing 

def clean_string(string: str) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    str: The input string with nasty characters converted to underscores
    """

    bad_chars = [' ', '.', '/']
    clean_str = string.lower()
    for char in bad_chars:
        clean_str = clean_str.replace(char, '_')
    return clean_str

def create_header(file: typing.TextIO, node_group):
    """
    Sets up the bl_info and imports the Blender API

    Parameters:
    file (typing.TextIO): the file for the generated add-on
    node_group: the node group object we're converting into an add-on
    """

    file.write("bl_info = {\n")
    file.write(f"\t\"name\" : \"{node_group.name}\",\n")
    file.write("\t\"author\" : \"Node To Python\",\n")
    file.write("\t\"version\" : (1, 0, 0),\n")
    file.write(f"\t\"blender\" : {bpy.app.version},\n")
    file.write("\t\"location\" : \"Object\",\n")
    file.write("\t\"category\" : \"Object\"\n")
    file.write("}\n")
    file.write("\n")
    file.write("import bpy\n")
    file.write("\n")

