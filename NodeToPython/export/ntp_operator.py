import datetime
from io import StringIO
import os
import pathlib
import shutil
from typing import TextIO, Callable

import bpy

from .node_group_gatherer import *
from .license_templates import license_templates
from .ntp_options import NTP_PG_Options
from .utils import *

IMAGE_DIR_NAME = "imgs"
BASE_DIR = "base_dir"
CLASS = "cls"
CLASSES = "classes"
NODE_TREE_NAMES = "node_tree_names"

RESERVED_NAMES = {
    IMAGE_DIR_NAME,
    BASE_DIR,
    CLASS,
    CLASSES,
    NODE_TREE_NAMES
}

MIN_BLENDER_VERSION = (4, 2, 0)
MAX_BLENDER_VERSION = (5, 2, 0)

class NodeTreeInfo():
    def __init__(self):
        self._func : str = ""
        self._module : str = ""
        self._is_base : bool = False
        # Dictionary acts as an ordered set
        self._dependencies: dict[bpy.types.NodeTree, None] = {}
        self._base_dependents: set[bpy.types.NodeTree] = set()
        self._lib_dependencies: dict[pathlib.Path, list[bpy.types.NodeTree]] = {}
        self._obj: NTPObject = None
        self._base_tree : bpy.types.NodeTree = None
        self._group_type: NodeGroupType = NodeGroupType.GEOMETRY_NODE_GROUP

class NTP_OT_Export(bpy.types.Operator):
    bl_idname = "ntp.export"
    bl_label = "Export"
    bl_description = "Export node group(s) to Python"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Write functions after nodes are mostly initialized and linked up
        self._write_after_links: list[Callable] = []

        # File (TextIO) or string (StringIO) the add-on/script is generated into
        self._file: TextIO | StringIO = StringIO()

        # Path to the directory of the zip file
        self._zip_dir: str = ""

        # Path to the directory for the generated addon
        self._addon_dir: str = ""

        # Modules with list operators to import and register
        self._modules: dict[str, list[str]] = {}

        self._name: str = ""

        # Indentation to use for the default write function
        self._outer_indent_level: int = 0
        self._inner_indent_level: int = 1

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}

        for name in RESERVED_NAMES:
            self._used_vars[name] = 0
        
        # Useful information about exported node trees
        self._node_trees: dict[bpy.types.NodeTree, NodeTreeInfo] = {}

        # Number of objects we end up exporting
        self._num_objs: int = 0

        # Generate socket default, min, and max values
        self._include_group_socket_values = True

        # Set dimensions of generated nodes
        self._should_set_dimensions = True

        # Indentation string (default: four spaces)
        self._indentation = "    "

        # Should we link external libraries (True), or recreate them (False)
        self._link_external_node_groups = True

        # Set default values for hidden sockets
        self._set_unavailable_defaults = False

    def execute(self, context: bpy.types.Context):
        if bpy.app.version >= MAX_BLENDER_VERSION:
            self.report(
                {'WARNING'},
                f"Blender version {bpy.app.version} is not supported yet!\n"
                f"NodeToPython is currently supported up to "
                f"{vec3_to_py_str(MAX_BLENDER_VERSION)}.\n"
                f"Some nodes, settings, and features may not work yet. "
                f"For more details, visit "
            )
            self.report(
                {'WARNING'},
                "\t\thttps://github.com/BrendanParmer/NodeToPython/blob/main/"
                "docs/README.md#supported-versions "
            )
            return {'CANCELLED'}
        elif bpy.app.version < MIN_BLENDER_VERSION:
            self.report(
                {'WARNING'},
                f"Blender version {bpy.app.version} has been deprecated.\n"
                f"NodeToPython currently requires a minimum version of "
                f"{vec3_to_py_str(MIN_BLENDER_VERSION)}.\n"
                f"Some nodes, settings, and features may not work. "
                f"For more details, visit "
            )
            self.report(
                {'WARNING'},
                "\t\thttps://github.com/BrendanParmer/NodeToPython/blob/main/"
                "docs/README.md#supported-versions "
            )
        
        if not self._setup_options(getattr(context.scene, "ntp_options")):
            return {'CANCELLED'}
        
        if self._mode == 'ADDON':
            self._outer_indent_level = 2
            self._inner_indent_level = 3

            if not self._setup_addon_directories(self._name):
                return {'CANCELLED'}

        elif self._mode == 'SCRIPT':
            self._file = StringIO("")
            if self._include_imports:
                self._create_imports()
        
        # Imported here to avoid circular dependency issues
        from .compositor.exporter import CompositorExporter
        from .geometry.exporter import GeometryNodesExporter
        from .shader.exporter import ShaderExporter

        self._calculate_export_order(context)

        if self._mode == 'ADDON':
            # Create files
            for module in self._modules:
                self._file.close()
                self._file = open(f"{self._addon_dir}/{module}.py", 'w')
                self._create_imports()

            # Import dependencies
            for nt_info in self._export_order:
                if nt_info._is_base:
                    self._file.close()
                    self._file = open(f"{self._addon_dir}/{nt_info._module}.py", 'a')
                    self._import_modules(nt_info)
            
        # Export objects
        for nt_info in self._export_order:
            if self._mode == 'ADDON':
                self._file.close()
                self._file = open(f"{self._addon_dir}/{nt_info._module}.py", 'a')
                self._outer_indent_level = 0
                self._inner_indent_level = 1

            if nt_info._group_type.is_compositor():
                exporter = CompositorExporter(self, nt_info)
            elif nt_info._group_type.is_geometry():
                exporter = GeometryNodesExporter(self, nt_info)
            elif nt_info._group_type.is_shader():
                exporter = ShaderExporter(self, nt_info)
            else:
                self.report(
                    {'ERROR'}, 
                    "Couldn't match group type (should be unreachable)"
                )
                return
            exporter.export()

        if self._mode == 'ADDON':
            self._file.close()
            self._file = open(f"{self._addon_dir}/__init__.py", 'w')
            self._create_operator_module_imports()
            self._create_imports()
            self._create_menu_func()
            self._create_registration_funcs()
            self._create_main_func()
            self._create_license()
            self._create_manifest()
        else:
            # node tree names
            self._write("if __name__ == \"__main__\":", 0)
            self._write("# Maps node tree creation functions to the node tree ", 1)
            self._write("# name, such that we don't recreate node trees unnecessarily", 1)
            self._write(f"{NODE_TREE_NAMES} : dict[typing.Callable, str] = {{}}", 1)
            self._write("", 0)
            for nt_info in self._export_order:
                self._call_node_tree_creation(nt_info._base_tree, 1)
            context.window_manager.clipboard = self._file.getvalue()

        self._file.close()
        
        if self._mode == 'ADDON':
            self._zip_addon()

        self._report_finished()

        return {'FINISHED'}
    
    def _write(self, string: str, indent_level: int = -1):
        if indent_level == -1:
            indent_level = self._inner_indent_level
        indent_str = indent_level * self._indentation
        self._file.write(f"{indent_str}{string}\n")

    def _setup_options(self, options: NTP_PG_Options) -> bool:
        # General
        self._mode = options.mode
        self._include_group_socket_values = options.set_group_defaults
        self._should_set_dimensions = options.set_node_sizes

        if options.indentation_type == 'SPACES_2':
            self._indentation = "  "
        elif options.indentation_type == 'SPACES_4':
            self._indentation = "    "
        elif options.indentation_type == 'SPACES_8':
            self._indentation = "        "
        elif options.indentation_type == 'TABS':
            self._indentation = "\t"

        self._link_external_node_groups = options.link_external_node_groups

        self._set_unavailable_defaults = options.set_unavailable_defaults

        #Script
        if options.mode == 'SCRIPT':
            self._include_imports = options.include_imports
        #Addon
        elif options.mode == 'ADDON':
            self._dir_path = bpy.path.abspath(options.dir_path)
            self._name = options.name
            self._description = options.description
            self._author_name = options.author_name
            self._version = options.version
            self._location = options.location
            self._license = options.license
            self._should_create_license = options.should_create_license
            self._category = options.category
            self._custom_category = options.custom_category
            if options.menu_id in dir(bpy.types):
                self._menu_id = options.menu_id
            else:
                self.report({'ERROR'}, f"{options.menu_id} is not a valid menu")
                return False
        return True

    def _setup_addon_directories(
        self,
        addon_name: str
    ) -> bool:
        """
        Finds/creates directories to save add-on to

        Parameters:
        context (Context): the current scene context
        obj_var (str): variable name of the object

        Returns:
        (bool): success of addon directory setup
        """
        if not self._dir_path or self._dir_path == "":
            self.report({'ERROR'},
                        ("NodeToPython: No save location found. Please select "
                         "one in the NodeToPython Options panel"))
            return False

        self._zip_dir = os.path.join(self._dir_path, addon_name)
        self._addon_dir = os.path.join(self._zip_dir, addon_name)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)
        
        return True

    def _create_imports(self) -> None:
        self._write("import bpy", 0)
        self._write("import mathutils", 0)
        self._write("import os", 0)
        self._write("import typing", 0)
        self._write("\n", 0)
    
    def _calculate_export_order(
        self, context: bpy.types.Context
    ) -> None:
        # TODO: this is really messy
        gatherer = NodeGroupGatherer()
        gatherer.gather_node_groups(context)

        self._num_objs = gatherer.get_number_node_groups()

        # Peform topological sort on node groups to determine export order
        for group_type, groups in gatherer.node_groups.items():
            for obj in groups:
                base_tree = get_base_node_tree(obj, group_type)
                if base_tree not in self._node_trees:
                    self._node_trees[base_tree] = NodeTreeInfo()
                node_info = self._node_trees[base_tree]
                node_info._base_tree = base_tree

                if self._mode == 'ADDON':
                    node_info._module = self._create_var(obj.name)

                node_info._is_base = True
                node_info._obj = obj
                node_info._group_type = group_type

        self._visited : set[bpy.types.NodeTree] = set()
        self._export_order : list[NodeTreeInfo] = []

        for group_type, groups in gatherer.node_groups.items():
            for obj in groups:
                base_tree = get_base_node_tree(obj, group_type)
                self._topological_sort(base_tree)

        # Probably a better way algorithmically of handling this,
        # need to move on though. Should be fast enough for reasonably sized
        # node tree dependency graphs
        for group_type, groups in gatherer.node_groups.items():
            common_module = ""
            if group_type.is_compositor():
                common_module = "compositor_common"
            elif group_type.is_geometry():
                common_module = "geometry_common"
            elif group_type.is_shader():
                common_module = "shader_common"

            for obj in groups:
                base_tree = get_base_node_tree(obj, group_type)
                nt_info = self._node_trees[base_tree]
                self._modules[nt_info._module] = []
                for dependency in nt_info._dependencies.keys():
                    dependency_info = self._node_trees[dependency]
                    base_dependents = dependency_info._base_dependents
                    base_dependents.add(base_tree)
                    if len(base_dependents) > 1 and not dependency_info._is_base:
                        dependency_info._module = common_module
                        if common_module not in self._used_vars:
                            self._used_vars[common_module] = 0
                    self._modules[dependency_info._module] = []

    def _topological_sort(
        self, 
        node_tree: bpy.types.NodeTree
    ):
        """
        Perform a topological sort on the node graph to determine dependencies 
        and which node groups need processed first

        Parameters:
        node_tree (NodeTree): the base node tree to convert
        """
        group_node_type = ''
        group_type = NodeGroupType.GEOMETRY_NODE_GROUP
        if isinstance(node_tree, bpy.types.CompositorNodeTree):
            group_node_type = 'CompositorNodeGroup'
            group_type = NodeGroupType.COMPOSITOR_NODE_GROUP
        elif isinstance(node_tree, bpy.types.GeometryNodeTree):
            group_node_type = 'GeometryNodeGroup'
            group_type = NodeGroupType.GEOMETRY_NODE_GROUP
        elif isinstance(node_tree, bpy.types.ShaderNodeTree):
            group_node_type = 'ShaderNodeGroup'
            group_type = NodeGroupType.SHADER_NODE_GROUP

        node_info = self._node_trees[node_tree]

        def dfs(nt: bpy.types.NodeTree) -> None:
            """
            Helper function to perform depth-first search on a NodeTree
            Parameters:
            nt (NodeTree): current node tree in the dependency graph
            """
            if nt is None:
                self.report(
                    {'ERROR'}, 
                    "NodeToPython: Found an invalid node tree. "
                    "Are all data blocks valid?"
                )
                return
            
            if (self._link_external_node_groups 
                and nt.library is not None):
                bpy_lib_path = bpy.path.abspath(nt.library.filepath)
                lib_path = pathlib.Path(os.path.realpath(bpy_lib_path))
                bpy_datafiles_path = bpy.path.abspath(
                    bpy.utils.system_resource('DATAFILES')
                )
                datafiles_path = pathlib.Path(os.path.realpath(bpy_datafiles_path))
                is_lib_essential = lib_path.is_relative_to(datafiles_path)
                if is_lib_essential:
                    relative_path = lib_path.relative_to(datafiles_path)
                    if relative_path not in node_info._lib_dependencies:
                        node_info._lib_dependencies[relative_path] = []
                    node_info._lib_dependencies[relative_path].append(nt)
                    return
                else:
                    self.report(
                        {'WARNING'},
                        f"Performing deep copy of node group \"{nt.name}\". "
                        f"Library {lib_path} was not included with current "
                        f"Blender version. If this node group came with Blender, "
                        f"please upgrade your node group to the current version"
                    )

            if nt not in self._visited:
                self._visited.add(nt)
                if nt not in self._node_trees:
                    self._node_trees[nt] = NodeTreeInfo()
                    self._node_trees[nt]._obj = nt
                    self._node_trees[nt]._module = clean_string(node_info._module)
                    self._node_trees[nt]._base_tree = nt
                    self._node_trees[nt]._group_type = group_type
                group_nodes = [node for node in nt.nodes
                               if node.bl_idname == group_node_type]
                for group_node in group_nodes:
                    node_nt = getattr(group_node, "node_tree")
                    if node_nt is None:
                        self.report(
                            {'ERROR'}, 
                            "NodeToPython: Found an invalid node tree. "
                            "Are all data blocks valid?"
                        )
                        continue
                    if node_nt not in self._visited:
                        dfs(node_nt)
                    if (node_nt.library is None or 
                        (not self._link_external_node_groups)
                    ):
                        self._node_trees[nt]._dependencies[node_nt] = None
                self._export_order.append(self._node_trees[nt])
                node_info._dependencies |= self._node_trees[nt]._dependencies
        dfs(node_tree)

    def _import_modules(self, node_tree_info: NodeTreeInfo) -> None:
        modules = set()
        for dependency in node_tree_info._dependencies.keys():
            modules.add(self._node_trees[dependency]._module)
        if node_tree_info._module in modules:
            modules.remove(node_tree_info._module)

        for module in modules:
            self._write(f"from . import {module}", 0)
        self._write("", 0)

    def _create_operator_module_imports(self) -> None:
        visited_modules: set[str] = set()
        module_order: list[str] = []
        for nt_info in self._export_order:
            if nt_info._module not in visited_modules:
                visited_modules.add(nt_info._module)
                module_order.append(nt_info._module)

        self._write("if \"bpy\" in locals():", 0)
        self._write("import importlib", 1)
        for module in module_order:
            self._write(f"importlib.reload({module})", 1)
        self._write("else:", 0)
        for module in module_order:
            self._write(f"from . import {module}", 1)
        self._write("", 0)

    def _create_menu_func(self) -> None:
        """
        Creates the menu function
        """
        self._write("def menu_func(self, context):", 0)
        for module, classes in self._modules.items():
            for cls in classes:
                self._write(f"self.layout.operator({module}.{cls}.bl_idname)", 1)
        self._write("")

    def _create_registration_funcs(self) -> None:
        """
        Creates the register function
        """
        # classes
        self._write(f"{CLASSES} = [", 0)
        for module, classes in self._modules.items():
            for cls in classes:
                self._write(f"{module}.{cls},", 1)
        self._write("]", 0)
        self._write("")

        # register()
        self._write("def register():", 0)
        self._write(f"for {CLASS} in {CLASSES}:", 1)
        self._write(f"bpy.utils.register_class({CLASS})", 2)
        self._write(f"bpy.types.{self._menu_id}.append(menu_func)", 1)
        self._write("")

        # unregister()
        self._write("def unregister():", 0)
        self._write(f"bpy.types.{self._menu_id}.remove(menu_func)", 1)
        self._write(f"for {CLASS} in {CLASSES}:", 1)
        self._write(f"bpy.utils.unregister_class({CLASS})", 2)
        self._write("")

    def _create_main_func(self) -> None:
        """
        Creates the main function
        """
        self._write("if __name__ == \"__main__\":", 0)
        self._write("register()", 1)

    def _create_license(self) -> None:
        if not self._should_create_license:
            return
        if self._license == 'OTHER':
            return
        license_file = open(f"{self._addon_dir}/LICENSE", "w")
        year = datetime.date.today().year
        license_txt = license_templates[self._license](year, self._author_name)
        license_file.write(license_txt)
        license_file.close()

    def _create_manifest(self) -> None:
        manifest = open(f"{self._addon_dir}/blender_manifest.toml", "w")
        manifest.write("schema_version = \"1.0.0\"\n\n")
        idname = clean_string(self._name)
        manifest.write(f"id = {str_to_py_str(idname)}\n")
        manifest.write(f"version = {version_to_manifest_str(self._version)}\n")
        manifest.write(f"name = {str_to_py_str(self._name)}\n")
        if self._description == "":
            self._description = self._name
        manifest.write(f"tagline = {str_to_py_str(self._description)}\n")
        manifest.write(f"maintainer = {str_to_py_str(self._author_name)}\n")
        manifest.write("type = \"add-on\"\n")
        min_version_str = f"{version_to_manifest_str(bpy.app.version)}"
        manifest.write(f"blender_version_min = {min_version_str}\n")
        if self._license != 'OTHER':
            manifest.write(f"license = [{str_to_py_str(self._license)}]\n")
        else:
            self.report(
                {'WARNING'}, 
                "No license selected. Please add a license to "
                "the manifest file"
            )
        manifest.close()

    def _call_node_tree_creation(
        self, 
        node_tree: bpy.types.NodeTree,
        indent_level: int
    ) -> None:
        node_tree_info = self._node_trees[node_tree]
        nt_var = self._create_var(f"{node_tree.name}")

        func = node_tree_info._func
        self._write(
            f"{nt_var} = {func}({NODE_TREE_NAMES})", 
            indent_level
        )
        self._write(
            f"{NODE_TREE_NAMES}[{func}] = {nt_var}.name\n",
            indent_level
        )

    def _create_var(self, name: str) -> str:
        """
        Creates a unique variable name for a node tree

        Parameters:
        name (str): basic string we'd like to create the variable name out of

        Returns:
        clean_name (str): variable name for the node tree
        """
        if name == "":
            name = "unnamed"
        clean_name = clean_string(name)
        var = clean_name
        if var in self._used_vars:
            self._used_vars[var] += 1
            return f"{clean_name}_{self._used_vars[var]}"
        else:
            self._used_vars[var] = 0
            return clean_name

    def _zip_addon(self) -> None:
        """
        Zips up the addon and removes the directory
        """
        shutil.make_archive(self._zip_dir, "zip", self._zip_dir)
        shutil.rmtree(self._zip_dir)

    def _report_finished(self):
        """
        Alert user that NTP is finished

        Parameters:
        object (str): the copied node tree or encapsulating structure
            (geometry node modifier, material, scene, etc.)
        """
        if self._mode == 'SCRIPT':
            location = "clipboard"
            if self._num_objs > 1:
                save_obj = f"{self._num_objs} objects"
            else:
                save_obj = self._export_order[0]._obj.name
        else:
            location = self._dir_path
            save_obj = self._name
        self.report({'INFO'}, f"NodeToPython: Saved {save_obj} to {location}")

classes = [
    NTP_OT_Export
]