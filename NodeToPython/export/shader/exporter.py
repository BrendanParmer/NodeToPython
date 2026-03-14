import bpy

from ..node_group_gatherer import NodeGroupType
from ..node_tree_exporter import NodeTreeExporter, NODE_TREE_NAMES
from ..ntp_operator import NTP_OT_Export, NodeTreeInfo
from ..utils import *

from .node_tree import NTP_ShaderNodeTree, NTP_NodeTree

NODE = "node"
LIGHT_OBJ = "light_obj"
SHADER_OP_RESERVED_NAMES = {
    NODE, 
    LIGHT_OBJ
}

class ShaderExporter(NodeTreeExporter):
    def __init__(
        self, 
        ntp_operator: NTP_OT_Export,
        node_tree_info: NodeTreeInfo
    ):
        if not node_tree_info._group_type.is_shader():
            ntp_operator.report(
                {'ERROR'},
                f"Cannot initialize ShaderExporter with group type "
                f"{node_tree_info._group_type}"
            )
        NodeTreeExporter.__init__(self, ntp_operator, node_tree_info)

        for name in SHADER_OP_RESERVED_NAMES:
            self._used_vars[name] = 0

    def _initialize_ntp_node_tree(
        self, 
        node_tree: bpy.types.NodeTree,
        nt_var: str
    ) -> NTP_NodeTree:
        return NTP_ShaderNodeTree(node_tree, nt_var)

    # NodeTreeExporter interface    
    def _create_obj(self):
        match self._node_tree_info._group_type:
            case NodeGroupType.MATERIAL:
                self._create_material()
            case NodeGroupType.LIGHT:
                self._create_light()
            case NodeGroupType.LINE_STYLE:
                self._create_line_style()
            case NodeGroupType.WORLD:
                self._create_world()

    # NodeTreeExporter interface
    def _initialize_node_tree(self, ntp_node_tree: NTP_NodeTree) -> None:
        nt_name = ntp_node_tree._node_tree.name
        self._node_tree_info._func = self._operator._create_var(
            f"{ntp_node_tree._var}_node_group"
        )
        #initialize node group
        self._write(f"def {self._node_tree_info._func}("
                    f"{NODE_TREE_NAMES}: dict[typing.Callable, str]):", 
                    self._operator._outer_indent_level)
        self._write(f'"""Initialize {nt_name} node group"""')

        if self._node_tree_info._group_type.is_obj():
            self._write(f"{ntp_node_tree._var} = {self._obj_var}.node_tree\n")
            self._write(f"# Start with a clean node tree")
            self._write(f"for {NODE} in {ntp_node_tree._var}.nodes:")
            self._write(f"{ntp_node_tree._var}.nodes.remove({NODE})", 
                        self._operator._inner_indent_level + 1)
        else:
            self._write((f"{ntp_node_tree._var} = bpy.data.node_groups.new("
                         f"type = \'ShaderNodeTree\', "
                         f"name = {str_to_py_str(nt_name)})"))
            self._write("", 0)
    
    def _create_material(self):
        indent_level = self._get_obj_creation_indent()
        
        mat: bpy.types.Material = self._node_tree_info._obj
        self._write(
            f"{self._obj_var} = bpy.data.materials.new("
            f"name = {str_to_py_str(mat.name)})", 
            indent_level
        )
        self._write("if bpy.app.version < (5, 0, 0):", indent_level)
        self._write(f"{self._obj_var}.use_nodes = True\n\n", indent_level + 1)

        regular_attrs = [
            "alpha_threshold",
            "line_priority",
            "max_vertex_displacement",
            "metallic",
            "paint_active_slot",
            "paint_clone_slot",
            "pass_index",
            "refraction_depth",
            "roughness",
            "show_transparent_back",
            "specular_intensity",
            "use_backface_culling",
            "use_backface_culling_lightprobe_volume",
            "use_backface_culling_shadow",
            "use_preview_world",
            "use_raytrace_refraction",
            "use_screen_refraction",
            "use_sss_translucency",
            "use_thickness_from_shadow",
            "use_transparency_overlap",
            "use_transparent_shadow"
        ]
        enum_attrs = [
            "blend_method",
            "displacement_method",
            "preview_render_type",
            "surface_render_method",
            "thickness_mode",
            "volume_intersection_method"
        ]
        if bpy.app.version < (4, 3, 0):
            enum_attrs.append("shadow_method")

        vec3_attrs = [
            "specular_color"
        ]
        vec4_attrs = [
            "diffuse_color",
            "line_color"
        ]
        for attr in regular_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {getattr(mat, attr)}",
                indent_level
            )
        for attr in enum_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {enum_to_py_str(getattr(mat, attr))}",
                indent_level
            )
        for attr in vec3_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {vec3_to_py_str(getattr(mat, attr))}",
                indent_level
            )
        for attr in vec4_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {vec4_to_py_str(getattr(mat, attr))}",
                indent_level
            )
        self._write("", 0)

    def _create_light(self):
        indent_level = self._get_obj_creation_indent()
        
        light : bpy.types.Light = self._node_tree_info._obj
        light_type = getattr(light, "type")
        self._write(
            f"{self._obj_var} = bpy.data.lights.new("
            f"name = {str_to_py_str(light.name)}, "
            f"type = {enum_to_py_str(light_type)})",
            indent_level
        )
        if bpy.app.version < (5, 1, 0):
            self._write(f"{self._obj_var}.use_nodes = True\n\n", indent_level)
        self._write(
            f"{LIGHT_OBJ} = bpy.data.objects.new("
            f"name = {str_to_py_str(light.name)}, "
            f"object_data={self._obj_var})",
            indent_level
        )
        self._write(
            f"bpy.context.collection.objects.link({LIGHT_OBJ})", 
            indent_level
        )
        
        regular_attrs = [
            "cutoff_distance",
            "diffuse_factor",
            "specular_factor",
            "transmission_factor",
            "use_custom_distance",
            "use_shadow",
            "volume_factor"
        ]
        if bpy.app.version >= (4, 5, 0):
            regular_attrs += [
                "exposure", 
                "normalize", 
                "temperature", 
                "use_temperature"
            ]

        enum_attrs = [
        ]

        vec3_attrs = [
            "color"
        ]

        point_regular_attrs = [
            "energy",
            "shadow_buffer_clip_start",
            "shadow_filter_radius",
            "shadow_jitter_overblur",
            "shadow_maximum_resolution",
            "shadow_soft_size",
            "use_shadow_jitter",
            "use_soft_falloff"
        ]

        area_regular_attrs = [
            "energy",
            "shadow_buffer_clip_start",
            "shadow_filter_radius",
            "shadow_jitter_overblur",
            "shadow_maximum_resolution",
            "shadow_soft_size",
            "size",
            "size_y",
            "spread",
            "use_absolute_resolution",
            "use_shadow_jitter"
        ]
        area_enum_attrs = [
            "shape"
        ]

        spot_regular_attrs = [
            "energy",
            "shadow_buffer_clip_start",
            "shadow_filter_radius",
            "shadow_jitter_overblur",
            "shadow_maximum_resolution",
            "shadow_soft_size",
            "show_cone",
            "spot_blend",
            "spot_size",
            "use_absolute_resolution",
            "use_shadow_jitter",
            "use_soft_falloff",
            "use_square"
        ]

        sun_regular_attrs = [
            "angle",
            "energy",
            "shadow_buffer_clip_start",
            "shadow_cascade_count",
            "shadow_cascade_exponent",
            "shadow_cascade_fade",
            "shadow_cascade_max_distance",
            "shadow_filter_radius",
            "shadow_jitter_overblur",
            "shadow_maximum_resolution",
            "shadow_soft_size",
            "use_shadow_jitter"
        ]
        if light.type == 'AREA':
            regular_attrs += area_regular_attrs
            enum_attrs += area_enum_attrs
        elif light.type == 'POINT':
            regular_attrs += point_regular_attrs
        elif light.type == 'SPOT':
            regular_attrs += spot_regular_attrs
        elif light.type == 'SUN':
            regular_attrs += sun_regular_attrs

        for attr in regular_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {getattr(light, attr)}",
                indent_level
            )
        for attr in enum_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {enum_to_py_str(getattr(light, attr))}",
                indent_level
            )
        for attr in vec3_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {vec3_to_py_str(getattr(light, attr))}",
                indent_level
            )
        
        self._write("", 0)

    def _create_line_style(self):
        indent_level = self._get_obj_creation_indent()

        linestyle: bpy.types.FreestyleLineStyle = self._node_tree_info._obj
        self._write(
            f"{self._obj_var} = bpy.data.linestyles.new("
            f"name = {str_to_py_str(linestyle.name)})", 
            indent_level
        )
        self._write(f"{self._obj_var}.use_nodes = True\n", indent_level)

        regular_attrs = [
            "active_texture_index",
            "alpha",
            "angle_max",
            "angle_min",
            "chain_count",
            "dash1",
            "dash2",
            "dash3",
            "gap1",
            "gap2",
            "gap3",
            "length_max",
            "length_min",
            "material_boundary",
            "rounds",
            "split_dash1",
            "split_dash2",
            "split_dash3",
            "split_gap1",
            "split_gap2",
            "split_gap3",
            "split_length",
            "texture_spacing",
            "thickness",
            "thickness_ratio",
            "use_angle_max",
            "use_angle_min",
            "use_chain_count",
            "use_chaining",
            "use_dashed_line",
            "use_length_max",
            "use_length_min",
            "use_same_object",
            "use_sorting",
            "use_split_length",
            "use_split_pattern",
            "use_texture"
        ]
        enum_attrs = [
            "caps",
            "chaining",
            "integration_type",
            "panel",
            "sort_key",
            "sort_order",
            "thickness_position"
        ]
        vec3_attrs = [
            "color"
        ]

        for attr in regular_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {getattr(linestyle, attr)}",
                indent_level
            )
        for attr in enum_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {enum_to_py_str(getattr(linestyle, attr))}",
                indent_level
            )
        for attr in vec3_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {vec3_to_py_str(getattr(linestyle, attr))}",
                indent_level
            )
        self._write("", 0)

    def _create_world(self):
        indent_level = self._get_obj_creation_indent()
        
        world: bpy.types.World = self._node_tree_info._obj
        self._write(
            f"{self._obj_var} = bpy.data.worlds.new("
            f"name = {str_to_py_str(world.name)})", 
            indent_level
        )
        self._write("if bpy.app.version < (5, 0, 0):", indent_level)
        self._write(f"{self._obj_var}.use_nodes = True\n\n", indent_level + 1)
        
        regular_attrs = [
            "sun_angle",
            "sun_shadow_filter_radius",
            "sun_shadow_jitter_overblur",
            "sun_shadow_maximum_resolution",
            "sun_threshold",
            "use_eevee_finite_volume",
            "use_sun_shadow",
            "use_sun_shadow_jitter"
        ]
        enum_attrs = [
            "probe_resolution"
        ]
        vec3_attrs = [
            "color"
        ]
        str_attrs = [
            "lightgroup"
        ]

        for attr in regular_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {getattr(world, attr)}",
                indent_level
            )
        for attr in enum_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {enum_to_py_str(getattr(world, attr))}",
                indent_level
            )
        for attr in vec3_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {vec3_to_py_str(getattr(world, attr))}",
                indent_level
            )
        for attr in str_attrs:
            self._write(
                f"{self._obj_var}.{attr} = {str_to_py_str(getattr(world, attr))}",
                indent_level
            )
        self._write("", 0)