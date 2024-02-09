import bpy
from bpy_types import bpy_types
import mathutils

from enum import Enum, auto
import keyword
import re
from typing import NamedTuple

class ST(Enum):
    """
    Settings Types
    """
    # Primitives
    ENUM = auto()
    ENUM_SET = auto()
    STRING = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    VEC1 = auto()
    VEC2 = auto()
    VEC3 = auto()
    VEC4 = auto()
    COLOR = auto()
    
    # Special settings
    COLOR_RAMP = auto()
    CURVE_MAPPING = auto()
    NODE_TREE = auto()

    ENUM_DEFINITION = auto() #TODO: unimplemented
    INDEX_SWITCH_ITEMS = auto() #TODO: unimplemented

    # Asset Library
    MATERIAL = auto() # Handle with asset library
    OBJECT = auto() # Handle with asset library

    # Image
    IMAGE = auto() #needs refactor
    IMAGE_USER = auto() #needs refactor
    MOVIE_CLIP = auto() #unimplmented

    TEXTURE = auto() #unimplemented
    TEXT = auto() #unimplemented
    SCENE = auto() #unimplemented
    PARTICLE_SYSTEM = auto() #unimplemented
    FONT = auto() #unimplemented
    MASK = auto() #unimplemented
    CRYPTOMATTE_ENTRIES = auto() #unimplemented
    IMAGE_FORMAT_SETTINGS = auto() #unimplemented
    FILE_SLOTS = auto() #unimplemented
    LAYER_SLOTS = auto() #unimplemented

class NTPNodeSetting(NamedTuple):
    name: str
    st: ST
    min_version: tuple = (3, 0, 0)
    max_version: tuple = (4, 2, 0) #first version where a setting is invalid


def clean_string(string: str, lower: bool = True) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    string (str): The input string ready to be used as a variable/file
    """

    if lower:
        string = string.lower()
    string = re.sub(r"[^a-zA-Z0-9_]", '_', string)

    if keyword.iskeyword(string):
        string = "_" + string
    elif not (string[0].isalpha() or string[0] == '_'):
        string = "_" + string

    return string

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

def vec1_to_py_str(vec1) -> str:
    """
    Converts a 1D vector to a string usable by the add-on

    Parameters:
    vec1: a 1d vector

    Returns:
    (str): string representation of the vector
    """
    return f"[{vec1[0]}]"

def vec2_to_py_str(vec2) -> str:
    """
    Converts a 2D vector to a string usable by the add-on

    Parameters:
    vec2: a 2D vector

    Returns:
    (str): string representation of the vector
    """
    return f"({vec2[0]}, {vec2[1]})"

def vec3_to_py_str(vec3) -> str:
    """
    Converts a 3D vector to a string usable by the add-on

    Parameters:
    vec3: a 3d vector

    Returns:
    (str): string representation of the vector
    """
    return f"({vec3[0]}, {vec3[1]}, {vec3[2]})"

def vec4_to_py_str(vec4) -> str:
    """
    Converts a 4D vector to a string usable by the add-on

    Parameters:
    vec4: a 4d vector

    Returns:
    (str): string version
    """
    return f"({vec4[0]}, {vec4[1]}, {vec4[2]}, {vec4[3]})"

def array_to_py_str(array: bpy_types.bpy_prop_array) -> str:
    """
    Converts a bpy_prop_array into a string

    Parameters:
    array (bpy_prop_array): Blender Python array

    Returns:
    (str): string version
    """
    string = "("
    for i in range(0, array.__len__()):
        if i > 0:
            string += ", "
        string += f"{array[i]}"
    string += ")"
    return string

def color_to_py_str(color: mathutils.Color) -> str:
    """
    Converts a mathutils.Color into a string

    Parameters:
    color (mathutils.Color): a Blender color

    Returns:
    (str): string version
    """
    return f"mathutils.Color(({color.r}, {color.g}, {color.b}))"

def img_to_py_str(img : bpy.types.Image) -> str:
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