import typing

import bpy

from .node_group_gatherer import *
from .utils import *

UNEXPORTABLE_PROPS : set[str] = {
    "rna_type",
    "original"
}

class NTP_OT_Export(bpy.types.Operator):
    bl_idname = "ntp.export"
    bl_label = "Export"
    bl_description = "Export node group(s) to Python"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._exported_objs : set[bpy.types.bpy_struct] = set()


    def execute(self, context: bpy.types.Context) -> set[str]:

        gatherer = NodeGroupGatherer()
        gatherer.gather_node_groups(context)

        file = open("test.txt", 'w')

        for groups in gatherer.node_groups.values():
            for obj in groups:
                if obj.id_data is not None:
                    my_str = (NTP_OT_Export._pythonize_bpy_struct(
                        obj, obj.id_data.name, self._exported_objs
                    ))
                    file.write(my_str)
                else:
                    print("No ID data!")

        print("DONE")
        return {'FINISHED'}

    @staticmethod
    def _pythonize_bpy_struct(
        obj: bpy.types.bpy_struct,
        var: str,
        exported_objs: set[bpy.types.bpy_struct]
    ) -> str:
        if obj is None:
            return ""

        if obj in exported_objs:
            return ""
        
        exported_objs.add(obj)
        
        obj_type = type(obj)

        prop_strs : list[str] = []
        for prop in obj_type.bl_rna.properties:
            if prop.identifier in UNEXPORTABLE_PROPS:
                continue

            attr = getattr(obj, prop.identifier)

            if (
                (hasattr(prop, "default") and attr == getattr(prop, "default"))
                or (
                    hasattr(prop, "default_array") and 
                    attr == getattr(prop, "default_array")
                )
            ):
                continue

            prop_var = f"{var}.{prop.identifier}"
            
            NTP_OT_Export._pythonize_rna_prop(
                prop, attr, prop_var, exported_objs, prop_strs
            )
        return "".join(prop_strs) + "\n"

    def _pythonize_rna_prop(
        prop: bpy.types.Property,
        attr,
        prop_var: str,
        exported_objs: set[bpy.types.bpy_struct],
        prop_strs: list[str]
    ) -> None:
        match prop.type:
            case 'BOOLEAN' | 'INT' | 'FLOAT':
                if prop.is_array:
                    prop_strs.append(
                        f"{prop_var} = {vec_to_py_str(attr, len(attr))}\n"
                    )
                else:
                    prop_strs.append(f"{prop_var} = {attr}\n")
            case 'STRING':
                prop_strs.append(f"{prop_var} = \"{attr}\"\n")
            case 'ENUM':
                prop_strs.append(f"{prop_var} = \'{attr}\'\n")
            case 'POINTER':
                attr_obj = typing.cast(bpy.types.bpy_struct, attr)
                prop_strs.append(NTP_OT_Export._pythonize_bpy_struct(
                    attr_obj,
                    prop_var,
                    exported_objs
                ))
            case 'COLLECTION':
                prop_strs.append(f"{prop_var}.clear()\n")

                collection = typing.cast(bpy.types.bpy_prop_collection, attr)

                # TODO: how to effectively create new items in the collection?
                prop_strs.extend(NTP_OT_Export._pythonize_bpy_struct(
                    item,
                    f"{prop_var}[{i}]",
                    exported_objs
                ) for i, item in enumerate(collection))

classes = [
    NTP_OT_Export
]