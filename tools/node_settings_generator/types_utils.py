from enum import Enum, auto

class ST(Enum):
    """
    Settings Types
    """
    # Primitives
    BOOL        = auto()
    COLOR       = auto()
    ENUM        = auto()
    ENUM_SET    = auto()
    FLOAT       = auto()
    INT         = auto()
    STRING      = auto()
    VEC1        = auto()
    VEC2        = auto()
    VEC3        = auto()
    VEC4        = auto()
    
    # Special settings
    BAKE_ITEMS          = auto()
    COLOR_RAMP          = auto()
    CURVE_MAPPING       = auto()
    ENUM_DEFINITION     = auto()
    INDEX_SWITCH_ITEMS  = auto()
    NODE_TREE           = auto()
    REPEAT_OUTPUT_ITEMS = auto()
    SIM_OUTPUT_ITEMS    = auto()

    # Image
    IMAGE       = auto() #needs refactor
    IMAGE_USER  = auto() #needs refactor

    # Currently unimplemented
    CAPTURE_ATTRIBUTE_ITEMS     = auto() #TODO NTP v3.2
    CRYPTOMATTE_ENTRIES         = auto()
    ENUM_ITEM                   = auto() #TODO NTP v3.2
    EULER                       = auto() #TODO NTP v3.2
    FILE_SLOTS                  = auto()
    FONT                        = auto()
    IMAGE_FORMAT_SETTINGS       = auto()
    LAYER_SLOTS                 = auto()
    MASK                        = auto()
    MATERIAL                    = auto() #TODO asset library
    MENU_SWITCH_ITEMS           = auto() #TODO NTP v3.2
    MOVIE_CLIP                  = auto() 
    OBJECT                      = auto() #TODO asset library
    PARTICLE_SYSTEM             = auto()
    SCENE                       = auto()
    TEXT                        = auto()
    TEXTURE                     = auto()

#types expected to be marked as read-only
READ_ONLY_TYPES : set[ST] = {
    ST.BAKE_ITEMS,
    ST.CAPTURE_ATTRIBUTE_ITEMS,
    ST.COLOR_RAMP,
    ST.CRYPTOMATTE_ENTRIES,
    ST.CURVE_MAPPING,
    ST.ENUM_DEFINITION,
    ST.FILE_SLOTS,
    ST.IMAGE_FORMAT_SETTINGS,
    ST.IMAGE_USER,
    ST.INDEX_SWITCH_ITEMS,
    ST.LAYER_SLOTS,
    ST.MENU_SWITCH_ITEMS,
    ST.REPEAT_OUTPUT_ITEMS,
    ST.SIM_OUTPUT_ITEMS,
} 

doc_to_NTP_type_dict : dict[str, ST] = {
    "" : "",
    "bpy_prop_collection of CryptomatteEntry": ST.CRYPTOMATTE_ENTRIES,
    "boolean" : ST.BOOL,
    "ColorMapping" : None, # Always read-only
    "ColorRamp" : ST.COLOR_RAMP,
    "CompositorNodeOutputFileFileSlots" : ST.FILE_SLOTS,
    "CompositorNodeOutputFileLayerSlots" : ST.LAYER_SLOTS,
    "CurveMapping" : ST.CURVE_MAPPING,
    "enum" : ST.ENUM,
    "enum set" : ST.ENUM_SET,
    "float" : ST.FLOAT,
    "float array of 1" : ST.VEC1,
    "float array of 2" : ST.VEC2,
    "float array of 3" : ST.VEC3,
    "float array of 4" : ST.VEC4,
    "Image" : ST.IMAGE,
    "ImageFormatSettings" : ST.IMAGE_FORMAT_SETTINGS,
    "ImageUser" : ST.IMAGE_USER,
    "int" : ST.INT,
    "Mask" : ST.MASK,
    "Material" : ST.MATERIAL,
    "mathutils.Color" : ST.COLOR,
    "mathutils.Euler" : ST.EULER, #TODO
    "mathutils.Vector of 3" : ST.VEC3,
    "MovieClip" : ST.MOVIE_CLIP,
    "Node" : None, # (<4.2) Always used with zone inputs, need to make sure 
                   # output nodes exist. Handled separately from NTP attr system
    "NodeEnumDefinition" : ST.ENUM_DEFINITION,
    "NodeEnumItem" : ST.ENUM_ITEM,
    "NodeGeometryBakeItems" : ST.BAKE_ITEMS,
    "NodeGeometryCaptureAttributeItems" : ST.CAPTURE_ATTRIBUTE_ITEMS,
    "NodeGeometryRepeatOutputItems" : ST.REPEAT_OUTPUT_ITEMS,
    "NodeGeometrySimulationOutputItems" : ST.SIM_OUTPUT_ITEMS,
    "NodeIndexSwitchItems" : ST.INDEX_SWITCH_ITEMS,
    "NodeMenuSwitchItems" : ST.MENU_SWITCH_ITEMS,
    "NodeTree" : ST.NODE_TREE,
    "Object" : ST.OBJECT,
    "ParticleSystem" : ST.PARTICLE_SYSTEM,
    "PropertyGroup" : None, #Always read-only
    "RepeatItem" : None, #Always set with index
    "Scene" : ST.SCENE,
    "SimulationStateItem" : None, #Always set with index
    "string" : ST.STRING,
    "TexMapping" : None, #Always read-only
    "Text" : ST.TEXT,
    "Texture" : ST.TEXTURE,
    "VectorFont" : ST.FONT
}

def get_NTP_type(type_str: str) -> str:
    """
    Time complexity isn't great, might be able to optimize with 
    a trie or similar data structure
    """
    longest_prefix = ""
    for key in doc_to_NTP_type_dict.keys():
        if type_str.startswith(key) and len(key) > len(longest_prefix):
            longest_prefix = key

    if longest_prefix == "":
        print(f"Couldn't find prefix of {type_str.strip()} in dictionary")

    result = doc_to_NTP_type_dict[longest_prefix]
    
    is_readonly = "read" in type_str
    if is_readonly and result not in READ_ONLY_TYPES:
        return None
    else:
        return result