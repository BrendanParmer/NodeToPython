import bpy
from bpy.types import Context, Operator
from bpy.types import Node, NodeTree

if bpy.app.version < (4, 0, 0):
    from bpy.types import NodeSocketInterface
else:
    from bpy.types import NodeTreeInterfacePanel, NodeTreeInterfaceSocket
    from bpy.types import NodeTreeInterfaceItem

from bpy.types import bpy_prop_array

import datetime
import os
import shutil
from typing import TextIO, Callable

from .license_templates import license_templates
from .ntp_node_tree import NTP_NodeTree
from .options import NTP_PG_Options
from .node_settings import NodeInfo, ST
from .utils import *

INDEX = "i"
IMAGE_DIR_NAME = "imgs"
IMAGE_PATH = "image_path"
ITEM = "item"
BASE_DIR = "base_dir"

RESERVED_NAMES = {
                  INDEX,
                  IMAGE_DIR_NAME,
                  IMAGE_PATH,
                  ITEM,
                  BASE_DIR
                 }

#node input sockets that are messy to set default values for
DONT_SET_DEFAULTS = {'NodeSocketGeometry',
                     'NodeSocketShader',
                     'NodeSocketMatrix',
                     'NodeSocketVirtual'}

MAX_BLENDER_VERSION = (5, 0, 0)

class NTP_Operator(Operator):
    """
    "Abstract" base class for all NTP operators. Blender types and abstraction
    don't seem to mix well, but this should only be inherited from
    """

    bl_idname = ""
    bl_label = ""

    # node tree input sockets that have default properties
    if bpy.app.version < (4, 0, 0):
        default_sockets_v3 = {'VALUE', 'INT', 'BOOLEAN', 'VECTOR', 'RGBA'}
    else:
        nondefault_sockets_v4 = {
            bpy.types.NodeTreeInterfaceSocketCollection,
            bpy.types.NodeTreeInterfaceSocketGeometry,
            bpy.types.NodeTreeInterfaceSocketImage,
            bpy.types.NodeTreeInterfaceSocketMaterial,
            bpy.types.NodeTreeInterfaceSocketObject,
            bpy.types.NodeTreeInterfaceSocketShader,
            bpy.types.NodeTreeInterfaceSocketTexture
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Write functions after nodes are mostly initialized and linked up
        self._write_after_links: list[Callable] = []

        # File (TextIO) or string (StringIO) the add-on/script is generated into
        self._file: TextIO = None

        # Path to the directory of the zip file
        self._zip_dir: str = None

        # Path to the directory for the generated addon
        self._addon_dir: str = None

        # Class named for the generated operator
        self._class_name: str = None

        # Indentation to use for the default write function
        self._outer_indent_level: int = 0
        self._inner_indent_level: int = 1

        # Base node tree we're converting
        self._base_node_tree: NodeTree = None

        # Dictionary to keep track of node tree->variable name pairs
        self._node_tree_vars: dict[NodeTree, str] = {}

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}

        # Dictionary used for setting node properties
        self._node_infos: dict[str, NodeInfo] = {}

        for name in RESERVED_NAMES:
            self._used_vars[name] = 0

        # Generate socket default, min, and max values
        self._include_group_socket_values = True

        # Set dimensions of generated nodes
        self._should_set_dimensions = True

        # Indentation string (default four spaces)
        self._indentation = "    "

        if bpy.app.version >= (3, 4, 0):
            # Set default values for hidden sockets
            self._set_unavailable_defaults = False

    def _write(self, string: str, indent_level: int = None):
        if indent_level is None:
            indent_level = self._inner_indent_level
        indent_str = indent_level * self._indentation
        self._file.write(f"{indent_str}{string}\n")

    def _setup_options(self, options: NTP_PG_Options) -> bool:
        if bpy.app.version >= MAX_BLENDER_VERSION:
            self.report({'WARNING'},
                        f"Blender version {bpy.app.version} is not supported yet!\n"
                        "NodeToPython is currently supported up to Blender 4.5.\n"
                        "Some nodes, settings, and features may not work yet. See:")
            self.report({'WARNING'},
                        "\t\thttps://github.com/BrendanParmer/NodeToPython/blob/main/docs/README.md#supported-versions ")
            self.report({'WARNING'}, "for more details")

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

        if bpy.app.version >= (3, 4, 0):
            self._set_unavailable_defaults = options.set_unavailable_defaults

        #Script
        if options.mode == 'SCRIPT':
            self._include_imports = options.include_imports
        #Addon
        elif options.mode == 'ADDON':
            self._dir_path = bpy.path.abspath(options.dir_path)
            self._name_override = options.name_override
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

    def _setup_addon_directories(self, context: Context, nt_var: str) -> bool:
        """
        Finds/creates directories to save add-on to

        Parameters:
        context (Context): the current scene context
        nt_var (str): variable name of the ndoe tree

        Returns:
        (bool): success of addon directory setup
        """
        if not self._dir_path or self._dir_path == "":
            self.report({'ERROR'},
                        ("NodeToPython: No save location found. Please select "
                         "one in the NodeToPython Options panel"))
            return False

        self._zip_dir = os.path.join(self._dir_path, nt_var)
        self._addon_dir = os.path.join(self._zip_dir, nt_var)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)
        
        return True

    def _create_header(self, name: str) -> None:
        """
        Sets up the bl_info and imports the Blender API

        Parameters:
        file (TextIO): the file for the generated add-on
        name (str): name of the add-on
        """

        self._write("bl_info = {", 0)
        self._name = name
        if self._name_override and self._name_override != "":
            self._name = self._name_override
        self._write(f"\"name\" : {str_to_py_str(self._name)},", 1)
        if self._description and self._description != "":
            self._write(f"\"description\" : {str_to_py_str(self._description)},", 1)
        self._write(f"\"author\" : {str_to_py_str(self._author_name)},", 1)
        self._write(f"\"version\" : {vec3_to_py_str(self._version)},", 1)
        self._write(f"\"blender\" : {bpy.app.version},", 1)
        self._write(f"\"location\" : {str_to_py_str(self._location)},", 1)
        category = self._category
        if category == "Custom":
            category = self._custom_category
        self._write(f"\"category\" : {str_to_py_str(category)},", 1)
        self._write("}\n", 0)
        self._write("import bpy", 0)
        self._write("import mathutils", 0)
        self._write("import os\n", 0)

    def _init_operator(self, idname: str, label: str) -> None:
        """
        Initializes the add-on's operator 

        Parameters:
        file (TextIO): the file for the generated add-on
        name (str): name for the class
        idname (str): name for the operator
        label (str): appearence inside Blender
        """
        self._idname = idname
        self._write(f"class {self._class_name}(bpy.types.Operator):", 0)
        self._write("def __init__(self, *args, **kwargs):", 1)
        self._write("super().__init__(*args, **kwargs)\n", 2)

        self._write(f"bl_idname = \"node.{idname}\"", 1)
        self._write(f"bl_label = {str_to_py_str(label)}", 1)
        self._write("bl_options = {\'REGISTER\', \'UNDO\'}\n", 1)

    def _topological_sort(self, node_tree: NodeTree) -> list[NodeTree]:
        """
        Perform a topological sort on the node graph to determine dependencies 
        and which node groups need processed first

        Parameters:
        node_tree (NodeTree): the base node tree to convert

        Returns:
        (list[NodeTree]): the node trees in order of processing
        """
        if isinstance(node_tree, bpy.types.CompositorNodeTree):
            group_node_type = 'CompositorNodeGroup'
        elif isinstance(node_tree, bpy.types.GeometryNodeTree):
            group_node_type = 'GeometryNodeGroup'
        elif isinstance(node_tree, bpy.types.ShaderNodeTree):
            group_node_type = 'ShaderNodeGroup'
        
        visited = set()
        result: list[NodeTree] = []

        def dfs(nt: NodeTree) -> None:
            """
            Helper function to perform depth-first search on a NodeTree

            Parameters:
            nt (NodeTree): current node tree in the dependency graph
            """
            if nt is None:
                self.report({'ERROR'}, "NodeToPython: Found an invalid node tree. "
                            "Are all data blocks valid?")
                return
            if nt not in visited:
                visited.add(nt)
                for group_node in [node for node in nt.nodes
                                   if node.bl_idname == group_node_type]:
                    if group_node.node_tree not in visited:
                        dfs(group_node.node_tree)
                result.append(nt)
        
        dfs(node_tree)

        return result

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

    def _create_node(self, node: Node, node_tree_var: str) -> str:
        """
        Initializes a new node with location, dimension, and label info

        Parameters:
        node (Node): node to be copied
        node_tree_var (str): variable name for the node tree
        Returns:
        node_var (str): variable name for the node
        """

        self._write(f"# Node {node.name}")

        node_var = self._create_var(node.name)
        self._node_vars[node] = node_var

        idname = str_to_py_str(node.bl_idname)
        self._write(f"{node_var} = {node_tree_var}.nodes.new({idname})")

        # label
        if node.label:
            self._write(f"{node_var}.label = {str_to_py_str(node.label)}")

        # name
        self._write(f"{node_var}.name = {str_to_py_str(node.name)}")

        # color
        if node.use_custom_color:
            self._write(f"{node_var}.use_custom_color = True")
            self._write(f"{node_var}.color = {vec3_to_py_str(node.color)}")

        # mute
        if node.mute:
            self._write(f"{node_var}.mute = True")

        # hide
        if node.hide:
            self._write(f"{node_var}.hide = True")

        # Warning propagation
        if bpy.app.version >= (4, 3, 0):
            if node.warning_propagation != 'ALL':
                self._write(f"{node_var}.warning_propagation = "
                            f"{enum_to_py_str(node.warning_propagation)}")
        return node_var

    def _set_settings_defaults(self, node: Node) -> None:
        """
        Sets the defaults for any settings a node may have

        Parameters:
        node (Node): the node object we're copying settings from
        node_var (str): name of the variable we're using for the node in our add-on
        """
        if node.bl_idname not in self._node_infos:
            self.report({'WARNING'},
                        (f"NodeToPython: couldn't find {node.bl_idname} in "
                         f"settings. Your Blender version may not be supported"))
            return

        node_var = self._node_vars[node]

        node_info = self._node_infos[node.bl_idname]
        for attr_info in node_info.attributes_:
            attr_name = attr_info.name_
            st = attr_info.st_

            version_gte_min = bpy.app.version >= max(attr_info.min_version_, node_info.min_version_)
            version_lt_max = bpy.app.version < min(attr_info.max_version_, node_info.max_version_)
            
            is_version_valid = version_gte_min and version_lt_max
            if not is_version_valid:
                continue

            if not hasattr(node, attr_name):
                self.report({'WARNING'},
                            f"NodeToPython: Couldn't find attribute "
                            f"\"{attr_name}\" for node {node.name} of type "
                            f"{node.bl_idname}")
                continue
            
            attr = getattr(node, attr_name, None)
            if attr is None:
                continue

            setting_str = f"{node_var}.{attr_name}"
            """
            A switch statement would've been nice here, 
            but Blender 3.0 was on Python v3.9
            """
            if st == ST.ENUM:
                if attr != '':
                    self._write(f"{setting_str} = {enum_to_py_str(attr)}")
            elif st == ST.ENUM_SET:
                self._write(f"{setting_str} = {attr}")
            elif st == ST.STRING:
                self._write(f"{setting_str} = {str_to_py_str(attr)}")
            elif st == ST.BOOL or st == ST.INT or st == ST.FLOAT:
                self._write(f"{setting_str} = {attr}")
            elif st == ST.VEC1:
                self._write(f"{setting_str} = {vec1_to_py_str(attr)}")
            elif st == ST.VEC2:
                self._write(f"{setting_str} = {vec2_to_py_str(attr)}")
            elif st == ST.VEC3:
                self._write(f"{setting_str} = {vec3_to_py_str(attr)}")
            elif st == ST.VEC4:
                self._write(f"{setting_str} = {vec4_to_py_str(attr)}")
            elif st == ST.COLOR:
                self._write(f"{setting_str} = {color_to_py_str(attr)}")
            elif st == ST.MATERIAL:
                self._set_if_in_blend_file(attr, setting_str, "materials")
            elif st == ST.OBJECT:
                self._set_if_in_blend_file(attr, setting_str, "objects")
            elif st == ST.COLLECTION:
                self._set_if_in_blend_file(attr, setting_str, "collections")
            elif st == ST.COLOR_RAMP:
                self._color_ramp_settings(node, attr_name)
            elif st == ST.CURVE_MAPPING:
                self._curve_mapping_settings(node, attr_name)
            elif st == ST.NODE_TREE:
                self._node_tree_settings(node, attr_name)
            elif st == ST.IMAGE:
                if attr is None:
                    continue
                if self._addon_dir is not None:
                    if attr.source in {'FILE', 'GENERATED', 'TILED'}:
                        if self._save_image(attr):
                            self._load_image(attr, f"{node_var}.{attr_name}")
                else:
                    self._set_if_in_blend_file(attr, setting_str, "images")

            elif st == ST.IMAGE_USER:
                self._image_user_settings(attr, f"{node_var}.{attr_name}")
            elif st == ST.SIM_OUTPUT_ITEMS:
                self._output_zone_items(attr, f"{node_var}.{attr_name}", True)
            elif st == ST.REPEAT_OUTPUT_ITEMS:
                self._output_zone_items(attr, f"{node_var}.{attr_name}", False)
            elif st == ST.INDEX_SWITCH_ITEMS:
                self._index_switch_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.ENUM_DEFINITION:
                self._enum_definition(attr, f"{node_var}.{attr_name}")
            elif st == ST.BAKE_ITEMS:
                self._bake_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.CAPTURE_ATTRIBUTE_ITEMS:
                self._capture_attribute_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.MENU_SWITCH_ITEMS:
                self._menu_switch_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.FOREACH_GEO_ELEMENT_GENERATION_ITEMS:
                self._foreach_geo_element_generation_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.FOREACH_GEO_ELEMENT_INPUT_ITEMS:
                self._foreach_geo_element_input_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.FOREACH_GEO_ELEMENT_MAIN_ITEMS:
                self._foreach_geo_element_main_items(attr, f"{node_var}.{attr_name}")
            elif st == ST.FORMAT_STRING_ITEMS:
                self._format_string_items(attr, f"{node_var}.{attr_name}")

    if bpy.app.version < (4, 0, 0):
        def _set_group_socket_defaults(self, socket_interface: NodeSocketInterface,
                                       socket_var: str) -> None:
            """
            Set a node group input/output's default properties if they exist
            Helper function to _group_io_settings()

            Parameters:
            socket_interface (NodeSocketInterface): socket interface associated
                with the input/output
            socket_var (str): variable name for the socket
            """
            if not self._include_group_socket_values:
                return

            if socket_interface.type not in self.default_sockets_v3:
                return
            
            if not hasattr(socket_interface, "default_value"):
                self.report({'WARNING'},
                            f"Socket {socket_interface.type} had no default value")
                return

            if socket_interface.type == 'RGBA':
                dv = vec4_to_py_str(socket_interface.default_value)
            elif socket_interface.type == 'VECTOR':
                dv = vec3_to_py_str(socket_interface.default_value)
            else:
                dv = socket_interface.default_value
            self._write(f"{socket_var}.default_value = {dv}")

            # min value
            if hasattr(socket_interface, "min_value"):
                min_val = socket_interface.min_value
                self._write(f"{socket_var}.min_value = {min_val}")
            # max value
            if hasattr(socket_interface, "min_value"):
                max_val = socket_interface.max_value
                self._write(f"{socket_var}.max_value = {max_val}")

        def _group_io_settings(self, node: Node, 
                               io: str,  # TODO: convert to enum
                               ntp_node_tree: NTP_NodeTree) -> None:
            """
            Set the settings for group input and output sockets

            Parameters:
            node (Node) : group input/output node
            io (str): whether we're generating the input or output settings
            ntp_node_tree (NTP_NodeTree): node tree that we're generating 
                input and output settings for
            """
            node_tree_var = ntp_node_tree.var
            node_tree = ntp_node_tree.node_tree

            if io == "input":
                io_sockets = node.outputs
                io_socket_interfaces = node_tree.inputs
            else:
                io_sockets = node.inputs
                io_socket_interfaces = node_tree.outputs

            self._write(f"# {node_tree_var} {io}s")
            for i, inout in enumerate(io_sockets):
                if inout.bl_idname == 'NodeSocketVirtual':
                    continue
                self._write(f"# {io.capitalize()} {inout.name}")
                idname = enum_to_py_str(inout.bl_idname)
                name = str_to_py_str(inout.name)
                self._write(f"{node_tree_var}.{io}s.new({idname}, {name})")
                socket_interface = io_socket_interfaces[i]
                socket_var = f"{node_tree_var}.{io}s[{i}]"

                self._set_group_socket_defaults(socket_interface, socket_var)

                # default attribute name
                if hasattr(socket_interface, "default_attribute_name"):
                    if socket_interface.default_attribute_name != "":
                        dan = str_to_py_str(socket_interface.default_attribute_name)
                        self._write(f"{socket_var}.default_attribute_name = {dan}")

                # attribute domain
                if hasattr(socket_interface, "attribute_domain"):
                    ad = enum_to_py_str(socket_interface.attribute_domain)
                    self._write(f"{socket_var}.attribute_domain = {ad}")

                # tooltip
                if socket_interface.description != "":
                    description = str_to_py_str(socket_interface.description)
                    self._write(f"{socket_var}.description = {description}")

                # hide_value
                if socket_interface.hide_value is True:
                    self._write(f"{socket_var}.hide_value = True")

                # hide in modifier
                if hasattr(socket_interface, "hide_in_modifier"):
                    if socket_interface.hide_in_modifier is True:
                        self._write(f"{socket_var}.hide_in_modifier = True")

                self._write("", 0)
            self._write("", 0)

    elif bpy.app.version >= (4, 0, 0):
        def _set_tree_socket_defaults(self, socket_interface: NodeTreeInterfaceSocket,
                                      socket_var: str) -> None:
            """
            Set a node tree input/output's default properties if they exist

            Helper function to _create_socket()

            Parameters:
            socket_interface (NodeTreeInterfaceSocket): socket interface associated
                with the input/output
            socket_var (str): variable name for the socket
            """
            if not self._include_group_socket_values:
                return
            if type(socket_interface) in self.nondefault_sockets_v4:
                return

            dv = socket_interface.default_value

            if bpy.app.version >= (4, 1, 0):
                if type(socket_interface) is bpy.types.NodeTreeInterfaceSocketMenu:
                    if dv == "":
                        self.report({'WARNING'},
                            "NodeToPython: No menu found for socket "
                            f"{socket_interface.name}"
                        )
                        return

                    self._write_after_links.append(
                        lambda _socket_var=socket_var, _dv=enum_to_py_str(dv): (
                            self._write(f"{_socket_var}.default_value = {_dv}")
                        )
                    )
                    return
            if type(socket_interface) == bpy.types.NodeTreeInterfaceSocketColor:
                dv = vec4_to_py_str(dv)
            elif type(dv) in {mathutils.Vector, mathutils.Euler}:
                dv = vec3_to_py_str(dv)
            elif type(dv) == bpy_prop_array:
                dv = array_to_py_str(dv)
            elif type(dv) == str:
                dv = str_to_py_str(dv)
            self._write(f"{socket_var}.default_value = {dv}")

            # min value
            if hasattr(socket_interface, "min_value"):
                min_val = socket_interface.min_value
                self._write(f"{socket_var}.min_value = {min_val}")
            # max value
            if hasattr(socket_interface, "min_value"):
                max_val = socket_interface.max_value
                self._write(f"{socket_var}.max_value = {max_val}")

        def _create_socket(self, socket: NodeTreeInterfaceSocket, 
                           parent: NodeTreeInterfacePanel, 
                           panel_dict: dict[NodeTreeInterfacePanel, str], 
                           ntp_nt: NTP_NodeTree) -> None:
            """
            Initialize a new tree socket

            Helper function to _process_items()

            Parameters:
            socket (NodeTreeInterfaceSocket): the socket to recreate
            parent (NodeTreeInterfacePanel): parent panel of the socket
                (possibly None)
            panel_dict (dict[NodeTreeInterfacePanel, str]: panel -> variable
            ntp_nt (NTP_NodeTree): owner of the socket
            """

            self._write(f"# Socket {socket.name}")
            # initialization
            socket_var = self._create_var(socket.name + "_socket") 
            name = str_to_py_str(socket.name)
            in_out_enum = enum_to_py_str(socket.in_out)

            socket_type = enum_to_py_str(socket.bl_socket_idname)
            """
            I might be missing something, but the Python API's set up a bit 
            weird here now. The new socket initialization only accepts types
            from a list of basic ones, but there doesn't seem to be a way of
            retrieving just this basic type without the subtype information.
            """
            if 'Float' in socket_type:
                socket_type = enum_to_py_str('NodeSocketFloat')
            elif 'Int' in socket_type:
                socket_type = enum_to_py_str('NodeSocketInt')
            elif 'Vector' in socket_type:
                socket_type = enum_to_py_str('NodeSocketVector')

            if parent is None:
                optional_parent_str = ""
            else:
                optional_parent_str = f", parent = {panel_dict[parent]}"

            self._write(f"{socket_var} = "
                        f"{ntp_nt.var}.interface.new_socket("
                        f"name={name}, in_out={in_out_enum}, "
                        f"socket_type={socket_type}"
                        f"{optional_parent_str})")

            # vector dimensions
            if hasattr(socket, "dimensions"):
                dimensions = socket.dimensions
                if socket.dimensions != 3:
                    self._write(f"{socket_var}.dimensions = {dimensions}")
                    self._write("# Get the socket again, as its default value could have been updated")
                    self._write(f"{socket_var} = {ntp_nt.var}.interface.items_tree[{socket_var}.index]")

            self._set_tree_socket_defaults(socket, socket_var)

            # subtype
            if hasattr(socket, "subtype"):
                if socket.subtype != '':
                    subtype = enum_to_py_str(socket.subtype)
                    self._write(f"{socket_var}.subtype = {subtype}")

            # default attribute name
            if socket.default_attribute_name != "":
                dan = str_to_py_str(
                    socket.default_attribute_name)
                self._write(f"{socket_var}.default_attribute_name = {dan}")

            # attribute domain
            ad = enum_to_py_str(socket.attribute_domain)
            self._write(f"{socket_var}.attribute_domain = {ad}")

            # hide_value
            if socket.hide_value is True:
                self._write(f"{socket_var}.hide_value = True")

            # hide in modifier
            if socket.hide_in_modifier is True:
                self._write(f"{socket_var}.hide_in_modifier = True")

            # force non field
            if socket.force_non_field is True:
                self._write(f"{socket_var}.force_non_field = True")
            
            # tooltip
            if socket.description != "":
                description = str_to_py_str(socket.description)
                self._write(f"{socket_var}.description = {description}")

            # layer selection field
            if socket.layer_selection_field:
                self._write(f"{socket_var}.layer_selection_field = True")

            if bpy.app.version >= (4, 2, 0):
                # is inspect output
                if socket.is_inspect_output:
                    self._write(f"{socket_var}.is_inspect_output = True")

            if bpy.app.version >= (4, 5, 0):
                # default input
                default_input = enum_to_py_str(socket.default_input)
                self._write(f"{socket_var}.default_input = {default_input}")

                # is panel toggle
                if socket.is_panel_toggle:
                    self._write(f"{socket_var}.is_panel_toggle = True")

                # menu expanded
                if socket.menu_expanded:
                    self._write(f"{socket_var}.menu_expanded = True")

                # structure type
                structure_type = enum_to_py_str(socket.structure_type)
                self._write(f"{socket_var}.structure_type = {structure_type}")

            self._write("", 0)

        def _create_panel(self, panel: NodeTreeInterfacePanel, 
                          panel_dict: dict[NodeTreeInterfacePanel], 
                          items_processed: set[NodeTreeInterfacePanel], 
                          parent: NodeTreeInterfacePanel, ntp_nt: NTP_NodeTree):
            """
            Initialize a new tree panel and its subitems

            Helper function to _process_items()

            Parameters:
            panel (NodeTreeInterfacePanel): the panel to recreate
            panel_dict (dict[NodeTreeInterfacePanel, str]: panel -> variable
            items_processed (set[NodeTreeInterfacePanel]): set of already
                processed items, so none are done twice
            parent (NodeTreeInterfacePanel): parent panel of the socket
                (possibly None)
            ntp_nt (NTP_NodeTree): owner of the socket
            """

            self._write(f"# Panel {panel.name}")

            panel_var = self._create_var(panel.name + "_panel")
            panel_dict[panel] = panel_var

            closed_str = ""
            if panel.default_closed is True:
                closed_str = f", default_closed=True"
                
            parent_str = ""
            if parent is not None and bpy.app.version < (4, 2, 0):
                parent_str = f", parent = {panel_dict[parent]}"     

            self._write(f"{panel_var} = "
                        f"{ntp_nt.var}.interface.new_panel("
                        f"{str_to_py_str(panel.name)}"
                        f"{closed_str}{parent_str})")

            # tooltip
            if panel.description != "":
                description = str_to_py_str(panel.description)
                self._write(f"{panel_var}.description = {description}")

            panel_dict[panel] = panel_var

            if len(panel.interface_items) > 0:
                self._process_items(panel, panel_dict, items_processed, ntp_nt)
            
            self._write("", 0)

        def _process_items(self, parent: NodeTreeInterfacePanel, 
                           panel_dict: dict[NodeTreeInterfacePanel], 
                           items_processed: set[NodeTreeInterfacePanel], 
                           ntp_nt: NTP_NodeTree) -> None:
            """
            Recursive function to process all node tree interface items in a 
            given layer

            Helper function to _tree_interface_settings()

            Parameters:
            parent (NodeTreeInterfacePanel): parent panel of the layer
                (possibly None to signify the base)
            panel_dict (dict[NodeTreeInterfacePanel, str]: panel -> variable
            items_processed (set[NodeTreeInterfacePanel]): set of already
                processed items, so none are done twice
            ntp_nt (NTP_NodeTree): owner of the socket
            """
            
            if parent is None:
                items = ntp_nt.node_tree.interface.items_tree
            else:
                items = parent.interface_items

            for item in items:
                if item.parent.index != -1 and item.parent not in panel_dict:
                    continue # child of panel not processed yet
                if item in items_processed:
                    continue
                
                items_processed.add(item)

                if item.item_type in {'SOCKET', 'PANEL_TOGGLE'}:
                    self._create_socket(item, parent, panel_dict, ntp_nt)

                elif item.item_type == 'PANEL':
                    self._create_panel(item, panel_dict, items_processed,
                                       parent, ntp_nt)
                    if bpy.app.version >= (4, 4, 0) and parent is not None:
                        nt_var = self._node_tree_vars[ntp_nt.node_tree]
                        interface_var = f"{nt_var}.interface"
                        panel_var = panel_dict[item]
                        parent_var = panel_dict[parent]
                        self._write(f"{interface_var}.move_to_parent("
                                    f"{panel_var}, {parent_var}, {item.index})")
                                    

        def _tree_interface_settings(self, ntp_nt: NTP_NodeTree) -> None:
            """
            Set the settings for group input and output sockets

            Parameters:
            ntp_nt (NTP_NodeTree): the node tree to set the interface for
            """

            self._write(f"# {ntp_nt.var} interface\n")
            panel_dict: dict[NodeTreeInterfacePanel, str] = {}
            items_processed: set[NodeTreeInterfaceItem] = set()

            self._process_items(None, panel_dict, items_processed, ntp_nt)

    def _set_input_defaults(self, node: Node) -> None:
        """
        Sets defaults for input sockets

        Parameters:
        node (Node): node we're setting inputs for
        """
        if node.bl_idname == 'NodeReroute':
            return

        node_var = self._node_vars[node]

        for i, input in enumerate(node.inputs):
            if input.bl_idname not in DONT_SET_DEFAULTS and not input.is_linked:
                if bpy.app.version >= (3, 4, 0):
                    if (not self._set_unavailable_defaults) and input.is_unavailable:
                        continue
                    
                # TODO: this could be cleaner
                socket_var = f"{node_var}.inputs[{i}]"

                # colors
                if input.bl_idname == 'NodeSocketColor':
                    default_val = vec4_to_py_str(input.default_value)

                # vector types
                elif "Vector" in input.bl_idname:
                    if "2D" in input.bl_idname:
                        default_val = vec2_to_py_str(input.default_value)
                    elif "4D" in input.bl_idname:
                        default_val = vec4_to_py_str(input.default_value)
                    else:
                        default_val = vec3_to_py_str(input.default_value)

                # rotation types
                elif input.bl_idname == 'NodeSocketRotation':
                    default_val = vec3_to_py_str(input.default_value)

                # strings
                elif input.bl_idname in {'NodeSocketString', 'NodeSocketStringFilePath'}:
                    default_val = str_to_py_str(input.default_value)

                #menu
                elif input.bl_idname == 'NodeSocketMenu':
                    if input.default_value == '':
                        continue
                    default_val = enum_to_py_str(input.default_value)

                # images
                elif input.bl_idname == 'NodeSocketImage':
                    img = input.default_value
                    if img is not None:
                        if self._addon_dir != None:  # write in a better way
                            if self._save_image(img):
                                self._load_image(img, f"{socket_var}.default_value")
                        else:
                            self._in_file_inputs(input, socket_var, "images")
                    default_val = None

                # materials
                elif input.bl_idname == 'NodeSocketMaterial':
                    self._in_file_inputs(input, socket_var, "materials")
                    default_val = None

                # collections
                elif input.bl_idname == 'NodeSocketCollection':
                    self._in_file_inputs(input, socket_var, "collections")
                    default_val = None

                # objects
                elif input.bl_idname == 'NodeSocketObject':
                    self._in_file_inputs(input, socket_var, "objects")
                    default_val = None

                # textures
                elif input.bl_idname == 'NodeSocketTexture':
                    self._in_file_inputs(input, socket_var, "textures")
                    default_val = None

                else:
                    default_val = input.default_value
                if default_val is not None:
                    self._write(f"# {input.identifier}")
                    self._write(f"{socket_var}.default_value = {default_val}")
        self._write("", 0)

    def _set_output_defaults(self, node: Node) -> None:
        """
        Some output sockets need default values set. It's rather annoying

        Parameters:
        node (Node): node for the output we're setting
        """
        # TODO: probably should define elsewhere
        output_default_nodes = {'ShaderNodeValue',
                                'ShaderNodeRGB',
                                'ShaderNodeNormal',
                                'CompositorNodeValue',
                                'CompositorNodeRGB',
                                'CompositorNodeNormal'}

        if node.bl_idname not in output_default_nodes:
            return

        node_var = self._node_vars[node]

        dv = node.outputs[0].default_value
        if node.bl_idname in {'ShaderNodeRGB', 'CompositorNodeRGB'}:
            dv = vec4_to_py_str(list(dv))
        if node.bl_idname in {'ShaderNodeNormal', 'CompositorNodeNormal'}:
            dv = vec3_to_py_str(dv)
        self._write(f"{node_var}.outputs[0].default_value = {dv}")

    def _in_file_inputs(self, input: bpy.types.NodeSocket, socket_var: str,
                        type: str) -> None:
        """
        Sets inputs for a node input if one already exists in the blend file

        Parameters:
        input (bpy.types.NodeSocket): input socket we're setting the value for
        socket_var (str): variable name we're using for the socket
        type (str): from what section of bpy.data to pull the default value from
        """

        if input.default_value is None:
            return
        name = str_to_py_str(input.default_value.name)
        self._write(f"if {name} in bpy.data.{type}:")
        self._write(f"{socket_var}.default_value = bpy.data.{type}[{name}]",
                    self._inner_indent_level + 1)

    def _set_socket_defaults(self, node: Node):
        """
        Set input and output socket defaults
        """
        self._set_input_defaults(node)
        self._set_output_defaults(node)

    def _set_if_in_blend_file(self, attr, setting_str: str, data_type: str
                              ) -> None:
        """
        Attempts to grab referenced thing from blend file
        """
        name = str_to_py_str(attr.name)
        self._write(f"if {name} in bpy.data.{data_type}:")
        self._write(f"{setting_str} = bpy.data.{data_type}[{name}]",
                    self._inner_indent_level + 1)
        
    def _color_ramp_settings(self, node: Node, color_ramp_name: str) -> None:
        """
        Replicate a color ramp node

        Parameters
        node (Node): node object we're copying settings from
        color_ramp_name (str): name of the color ramp to be copied
        """

        color_ramp: bpy.types.ColorRamp = getattr(node, color_ramp_name)
        if not color_ramp:
            raise ValueError(f"No color ramp named \"{color_ramp_name}\" found")

        node_var = self._node_vars[node]

        # settings
        ramp_str = f"{node_var}.{color_ramp_name}"

        #color mode
        color_mode = enum_to_py_str(color_ramp.color_mode)
        self._write(f"{ramp_str}.color_mode = {color_mode}")

        #hue interpolation
        hue_interpolation = enum_to_py_str(color_ramp.hue_interpolation)
        self._write(f"{ramp_str}.hue_interpolation = {hue_interpolation}")

        #interpolation
        interpolation = enum_to_py_str(color_ramp.interpolation)
        self._write(f"{ramp_str}.interpolation = {interpolation}")
        self._write("", 0)

        # key points
        self._write(f"# Initialize color ramp elements")
        self._write((f"{ramp_str}.elements.remove"
                    f"({ramp_str}.elements[0])"))
        for i, element in enumerate(color_ramp.elements):
            element_var = self._create_var(f"{node_var}_cre_{i}")
            if i == 0:
                self._write(f"{element_var} = {ramp_str}.elements[{i}]")
                self._write(f"{element_var}.position = {element.position}")
            else:
                self._write(f"{element_var} = {ramp_str}.elements"
                            f".new({element.position})")

            self._write(f"{element_var}.alpha = {element.alpha}")
            color_str = vec4_to_py_str(element.color)
            self._write(f"{element_var}.color = {color_str}\n")

    def _curve_mapping_settings(self, node: Node,
                                curve_mapping_name: str) -> None:
        """
        Sets defaults for Float, Vector, and Color curves

        Parameters:
        node (Node): curve node we're copying settings from
        curve_mapping_name (str): name of the curve mapping to be set
        """

        mapping = getattr(node, curve_mapping_name)
        if not mapping:
            raise ValueError((f"Curve mapping \"{curve_mapping_name}\" not found "
                              f"in node \"{node.bl_idname}\""))

        node_var = self._node_vars[node]

        # mapping settings
        self._write(f"# Mapping settings")
        mapping_var = f"{node_var}.{curve_mapping_name}"

        # extend
        extend = enum_to_py_str(mapping.extend)
        self._write(f"{mapping_var}.extend = {extend}")
        # tone
        tone = enum_to_py_str(mapping.tone)
        self._write(f"{mapping_var}.tone = {tone}")

        # black level
        b_lvl_str = vec3_to_py_str(mapping.black_level)
        self._write(f"{mapping_var}.black_level = {b_lvl_str}")
        # white level
        w_lvl_str = vec3_to_py_str(mapping.white_level)
        self._write(f"{mapping_var}.white_level = {w_lvl_str}")

        # minima and maxima
        min_x = mapping.clip_min_x
        self._write(f"{mapping_var}.clip_min_x = {min_x}")
        min_y = mapping.clip_min_y
        self._write(f"{mapping_var}.clip_min_y = {min_y}")
        max_x = mapping.clip_max_x
        self._write(f"{mapping_var}.clip_max_x = {max_x}")
        max_y = mapping.clip_max_y
        self._write(f"{mapping_var}.clip_max_y = {max_y}")

        # use_clip
        use_clip = mapping.use_clip
        self._write(f"{mapping_var}.use_clip = {use_clip}")

        # create curves
        for i, curve in enumerate(mapping.curves):
            self._create_curve_map(node, i, curve, curve_mapping_name)

        # update curve
        self._write(f"# Update curve after changes")
        self._write(f"{mapping_var}.update()")

    def _create_curve_map(self, node: Node, i: int, curve: bpy.types.CurveMap,
                          curve_mapping_name: str) -> None:
        """
        Helper function to create the ith curve of a node's curve mapping

        Parameters:
        node (Node): the node with a curve mapping
        i (int): index of the CurveMap within the mapping
        curve (bpy.types.CurveMap): the curve map to recreate
        curve_mapping_name (str): attribute name of the recreated curve mapping
        """
        node_var = self._node_vars[node]
        
        self._write(f"# Curve {i}")
        curve_i_var = self._create_var(f"{node_var}_curve_{i}")
        self._write(f"{curve_i_var} = "
                    f"{node_var}.{curve_mapping_name}.curves[{i}]")

        # Remove default points when CurveMap is initialized with more than
        # two points (just CompositorNodeHueCorrect)
        if (node.bl_idname == 'CompositorNodeHueCorrect'):
            self._write(f"for {INDEX} in range"
                        f"(len({curve_i_var}.points.values()) - 1, 1, -1):")
            self._write(f"{curve_i_var}.points.remove("
                        f"{curve_i_var}.points[{INDEX}])",
                        self._inner_indent_level + 1)

        for j, point in enumerate(curve.points):
            self._create_curve_map_point(j, point, curve_i_var)

    def _create_curve_map_point(self, j: int, point: bpy.types.CurveMapPoint,
                                curve_i_var: str) -> None:
        """
        Helper function to recreate a curve map point

        Parameters:
        j (int): index of the point within the curve map
        point (CurveMapPoint): point to recreate
        curve_i_var (str): variable name of the point's curve map
        """
        point_j_var = self._create_var(f"{curve_i_var}_point_{j}")

        loc = point.location
        loc_str = f"{loc[0]}, {loc[1]}"
        if j < 2:
            self._write(f"{point_j_var} = {curve_i_var}.points[{j}]")
            self._write(f"{point_j_var}.location = ({loc_str})")
        else:
            self._write(f"{point_j_var} = {curve_i_var}.points.new({loc_str})")

        handle = enum_to_py_str(point.handle_type)
        self._write(f"{point_j_var}.handle_type = {handle}")
    
    def _node_tree_settings(self, node: Node, attr_name: str) -> None:
        """
        Processes node tree of group node if one is present

        Parameters:
        node (Node): the group node
        attr_name (str): name of the node tree attribute
        """
        node_tree = getattr(node, attr_name)
        if node_tree is None:
            return
        if node_tree in self._node_tree_vars:
            nt_var = self._node_tree_vars[node_tree]
            node_var = self._node_vars[node]
            self._write(f"{node_var}.{attr_name} = {nt_var}")
        else:
            self.report({'WARNING'}, (f"NodeToPython: Node tree dependency graph " 
                                    f"wasn't properly initialized"))

    def _save_image(self, img: bpy.types.Image) -> bool:
        """
        Saves an image to an image directory of the add-on

        Parameters:
        img (bpy.types.Image): image to be saved
        """

        if img is None:
            return False

        img_str = img_to_py_str(img)

        if not img.has_data:
            self.report({'WARNING'}, f"{img_str} has no data")
            return False

        # create image dir if one doesn't exist
        img_dir = os.path.join(self._addon_dir, IMAGE_DIR_NAME)
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        # save the image
        
        img_path = f"{img_dir}/{img_str}"
        if not os.path.exists(img_path):
            img.save_render(img_path)
        return True

    def _load_image(self, img: bpy.types.Image, img_var: str) -> None:
        """
        Loads an image from the add-on into a blend file and assigns it

        Parameters:
        img (bpy.types.Image): Blender image from the original node group
        img_var (str): variable name to be used for the image
        """

        if img is None:
            return

        img_str = img_to_py_str(img)

        # TODO: convert to special variables
        self._write(f"# Load image {img_str}")
        self._write(f"{BASE_DIR} = "
                    f"os.path.dirname(os.path.abspath(__file__))")
        self._write(f"{IMAGE_PATH} = "
                    f"os.path.join({BASE_DIR}, {str_to_py_str(IMAGE_DIR_NAME)}, "
                    f"{str_to_py_str(img_str)})")
        self._write(f"{img_var} = bpy.data.images.load"
                    f"({IMAGE_PATH}, check_existing = True)")

        # copy image settings
        self._write(f"# Set image settings")

        # source
        source = enum_to_py_str(img.source)
        self._write(f"{img_var}.source = {source}")

        # color space settings
        color_space = enum_to_py_str(img.colorspace_settings.name)
        self._write(f"{img_var}.colorspace_settings.name = {color_space}")

        # alpha mode
        alpha_mode = enum_to_py_str(img.alpha_mode)
        self._write(f"{img_var}.alpha_mode = {alpha_mode}")

    def _image_user_settings(self, img_user: bpy.types.ImageUser,
                             img_user_var: str) -> None:
        """
        Replicate the image user of an image node

        Parameters
        img_usr (bpy.types.ImageUser): image user to be copied
        img_usr_var (str): variable name for the generated image user
        """

        img_usr_attrs = ["frame_current", "frame_duration", "frame_offset",
                         "frame_start", "tile", "use_auto_refresh", "use_cyclic"]

        for img_usr_attr in img_usr_attrs:
            self._write(f"{img_user_var}.{img_usr_attr} = "
                        f"{getattr(img_user, img_usr_attr)}")

    if bpy.app.version >= (3, 6, 0):
        def _output_zone_items(self, output_items, items_str: str, 
                               is_sim: bool) -> None:
            """
            Set items for a zone's output

            output_items (NodeGeometry(Simulation/Repeat)OutputItems): items
                to copy
            items_str (str): 
            """
            self._write(f"{items_str}.clear()")
            for i, item in enumerate(output_items):
                socket_type = enum_to_py_str(item.socket_type)
                name = str_to_py_str(item.name)
                self._write(f"# Create item {name}")
                self._write(f"{items_str}.new({socket_type}, {name})")

                if is_sim:
                    item_var = f"{items_str}[{i}]"
                    ad = enum_to_py_str(item.attribute_domain)
                    self._write(f"{item_var}.attribute_domain = {ad}")

    if bpy.app.version >= (4, 1, 0):
        def _index_switch_items(self, switch_items: bpy.types.NodeIndexSwitchItems,   
                                items_str: str) -> None:
            """
            Set the proper amount of index switch items

            Parameters:
            switch_items (bpy.types.NodeIndexSwitchItems): switch items to copy
            items_str (str): string for the generated switch items attribute
            """
            num_items = len(switch_items)
            self._write(f"{items_str}.clear()")
            for i in range(num_items):
                self._write(f"{items_str}.new()")

        def _bake_items(self, bake_items: bpy.types.NodeGeometryBakeItems,
                        bake_items_str: str) -> None:
            """
            Set bake items for a node
            
            Parameters:
            bake_items (bpy.types.NodeGeometryBakeItems): bake items to replicate
            bake_items_str (str): string for the generated bake items
            """
            self._write(f"{bake_items_str}.clear()")
            for i, bake_item in enumerate(bake_items):
                socket_type = enum_to_py_str(bake_item.socket_type)
                name = str_to_py_str(bake_item.name)
                self._write(f"{bake_items_str}.new({socket_type}, {name})")
                
                ad = enum_to_py_str(bake_item.attribute_domain)
                self._write(f"{bake_items_str}[{i}].attribute_domain = {ad}")

                if bake_item.is_attribute:
                    self._write(f"{bake_items_str}[{i}].is_attribute = True")

    if bpy.app.version >= (4, 1, 0) and bpy.app.version < (4, 2, 0):
        def _enum_definition(self, enum_def: bpy.types.NodeEnumDefinition, 
                             enum_def_str: str) -> None:
            """
            Set enum definition item for a node
            
            Parameters:
            enum_def (bpy.types.NodeEnumDefinition): enum definition to replicate
            enum_def_str (str): string for the generated enum definition
            """
            self._write(f"{enum_def_str}.enum_items.clear()")
            for i, enum_item in enumerate(enum_def.enum_items):
                name = str_to_py_str(enum_item.name)
                self._write(f"{enum_def_str}.enum_items.new({name})")
                if enum_item.description != "":
                    self._write(f"{enum_def_str}.enum_items[{i}].description = "
                                f"{str_to_py_str(enum_item.description)}")

    if bpy.app.version >= (4, 2, 0):
        def _capture_attribute_items(self, capture_attribute_items: bpy.types.NodeGeometryCaptureAttributeItems, capture_attrs_str: str) -> None:
            """
            Sets capture attribute items
            """
            self._write(f"{capture_attrs_str}.clear()")
            for item in capture_attribute_items:
                name = str_to_py_str(item.name)
                self._write(f"{capture_attrs_str}.new('FLOAT', {name})")

                # Need to initialize capture attribute item with a socket,
                # which has a slightly different enum to the attribute type
                data_type = enum_to_py_str(item.data_type)
                self._write(f"{capture_attrs_str}[{name}].data_type = {data_type}")

        def _menu_switch_items(self, menu_switch_items: bpy.types.NodeMenuSwitchItems, menu_switch_items_str: str) -> None:
            self._write(f"{menu_switch_items_str}.clear()")
            for i, item in enumerate(menu_switch_items):
                name_str = str_to_py_str(item.name)
                self._write(f"{menu_switch_items_str}.new({name_str})")
                desc_str = str_to_py_str(item.description)
                self._write(f"{menu_switch_items_str}[{i}].description = {desc_str}")

    if bpy.app.version >= (4, 3, 0):
        def _foreach_geo_element_generation_items(self,
            generation_items: bpy.types.NodeGeometryForeachGeometryElementGenerationItems,
            generation_items_str: str
        ) -> None:
            self._write(f"{generation_items_str}.clear()")
            for i, item in enumerate(generation_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write(f"{generation_items_str}.new({socket_type}, {name_str})")
                
                item_str = f"{generation_items_str}[{i}]"
                
                ad = enum_to_py_str(item.domain)
                self._write(f"{item_str}.domain = {ad}")

        def _foreach_geo_element_input_items(self,
            input_items: bpy.types.NodeGeometryForeachGeometryElementInputItems,
            input_items_str: str
        ) -> None:
            self._write(f"{input_items_str}.clear()")
            for i, item in enumerate(input_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write(f"{input_items_str}.new({socket_type}, {name_str})")

        def _foreach_geo_element_main_items(self,
            main_items: bpy.types.NodeGeometryForeachGeometryElementMainItems,
            main_items_str: str
        ) -> None:
            self._write(f"{main_items_str}.clear()")
            for i, item in enumerate(main_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write(f"{main_items_str}.new({socket_type}, {name_str})")

    if bpy.app.version >= (4, 5, 0):
        def _format_string_items(self,
                          format_items : bpy.types.NodeFunctionFormatStringItems,
                          format_items_str: str) -> None:
            self._write(f"{format_items_str}.clear()")
            for i, item in enumerate(format_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write(f"{format_items_str}.new({socket_type}, {name_str})")


    def _set_parents(self, node_tree: NodeTree) -> None:
        """
        Sets parents for all nodes, mostly used to put nodes in frames

        Parameters:
        node_tree (NodeTree): node tree we're obtaining nodes from
        """
        parent_comment = False
        for node in node_tree.nodes:
            if node is not None and node.parent is not None:
                if not parent_comment:
                    self._write(f"# Set parents")
                    parent_comment = True
                node_var = self._node_vars[node]
                parent_var = self._node_vars[node.parent]
                self._write(f"{node_var}.parent = {parent_var}")
        if parent_comment:
            self._write("", 0)

    def _set_locations(self, node_tree: NodeTree) -> None:
        """
        Set locations for all nodes

        Parameters:
        node_tree (NodeTree): node tree we're obtaining nodes from
        """

        self._write(f"# Set locations")
        for node in node_tree.nodes:
            node_var = self._node_vars[node]
            self._write(f"{node_var}.location "
                        f"= ({node.location.x}, {node.location.y})")
        if node_tree.nodes:
            self._write("", 0)

    def _set_dimensions(self, node_tree: NodeTree) -> None:
        """
        Set dimensions for all nodes

        Parameters:
        node_tree (NodeTree): node tree we're obtaining nodes from
        """
        if not self._should_set_dimensions:
            return

        self._write(f"# Set dimensions")
        for node in node_tree.nodes:
            node_var = self._node_vars[node]
            self._write(f"{node_var}.width, {node_var}.height "
                        f"= {node.width}, {node.height}")
        if node_tree.nodes:
            self._write("", 0)

    def _init_links(self, node_tree: NodeTree) -> None:
        """
        Create all the links between nodes

        Parameters:
        node_tree (NodeTree): node tree to copy, with variable
        """

        nt_var = self._node_tree_vars[node_tree]

        links = node_tree.links
        if links:
            self._write(f"# Initialize {nt_var} links\n")
            if hasattr(links[0], "multi_input_sort_id"):
                # generate links in the correct order for multi input sockets
                links = sorted(links, key=lambda link: link.multi_input_sort_id)

        for link in links:
            in_node_var = self._node_vars[link.from_node]
            input_socket = link.from_socket

            """
            Blender's socket dictionary doesn't guarantee 
            unique keys, which has caused much wailing and
            gnashing of teeth. This is a quick fix that
            doesn't run quick
            """
            # TODO: try using index() method
            for i, item in enumerate(link.from_node.outputs.items()):
                if item[1] == input_socket:
                    input_idx = i
                    break

            out_node_var = self._node_vars[link.to_node]
            output_socket = link.to_socket

            for i, item in enumerate(link.to_node.inputs.items()):
                if item[1] == output_socket:
                    output_idx = i
                    break

            self._write(f"# {in_node_var}.{input_socket.name} "
                        f"-> {out_node_var}.{output_socket.name}")
            self._write(f"{nt_var}.links.new({in_node_var}"
                        f".outputs[{input_idx}], "
                        f"{out_node_var}.inputs[{output_idx}])")

        for _func in self._write_after_links:
            _func()
        self._write_after_links = []
        self._write("", 0)
            

    def _set_node_tree_properties(self, node_tree: NodeTree) -> None:
        nt_var = self._node_tree_vars[node_tree]

        if bpy.app.version >= (4, 2, 0):
            color_tag_str = enum_to_py_str(node_tree.color_tag)
            self._write(f"{nt_var}.color_tag = {color_tag_str}")
            desc_str = str_to_py_str(node_tree.description)
            self._write(f"{nt_var}.description = {desc_str}")
        if bpy.app.version >= (4, 3, 0):
            default_width = node_tree.default_group_node_width
            self._write(f"{nt_var}.default_group_node_width = {default_width}")

    def _hide_hidden_sockets(self, node: Node) -> None:
        """
        Hide hidden sockets

        Parameters:
        node (Node): node object we're copying socket settings from
        """
        node_var = self._node_vars[node]

        for i, socket in enumerate(node.inputs):
            if socket.hide is True:
                self._write(f"{node_var}.inputs[{i}].hide = True")
        for i, socket in enumerate(node.outputs):
            if socket.hide is True:
                self._write(f"{node_var}.outputs[{i}].hide = True")

    def _create_menu_func(self) -> None:
        """
        Creates the menu function
        """
        self._write("def menu_func(self, context):", 0)
        self._write(f"self.layout.operator({self._class_name}.bl_idname)\n", 1)

    def _create_register_func(self) -> None:
        """
        Creates the register function
        """
        self._write("def register():", 0)
        self._write(f"bpy.utils.register_class({self._class_name})", 1)
        self._write(f"bpy.types.{self._menu_id}.append(menu_func)\n", 1)

    def _create_unregister_func(self) -> None:
        """
        Creates the unregister function
        """
        self._write("def unregister():", 0)
        self._write(f"bpy.utils.unregister_class({self._class_name})", 1)
        self._write(f"bpy.types.{self._menu_id}.remove(menu_func)\n", 1)

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

    if bpy.app.version >= (4, 2, 0):
        def _create_manifest(self) -> None:
            manifest = open(f"{self._addon_dir}/blender_manifest.toml", "w")
            manifest.write("schema_version = \"1.0.0\"\n\n")
            manifest.write(f"id = {str_to_py_str(self._idname)}\n")

            manifest.write(f"version = {version_to_manifest_str(self._version)}\n")
            manifest.write(f"name = {str_to_py_str(self._name)}\n")
            if self._description == "":
                self._description = self._name
            manifest.write(f"tagline = {str_to_py_str(self._description)}\n")
            manifest.write(f"maintainer = {str_to_py_str(self._author_name)}\n")
            manifest.write("type = \"add-on\"\n")
            manifest.write(f"blender_version_min = {version_to_manifest_str(bpy.app.version)}\n")
            if self._license != 'OTHER':
                manifest.write(f"license = [{str_to_py_str(self._license)}]\n")
            else:
                self.report({'WARNING'}, "No license selected. Please add a license to the manifest file")

            manifest.close()

    def _zip_addon(self) -> None:
        """
        Zips up the addon and removes the directory
        """
        shutil.make_archive(self._zip_dir, "zip", self._zip_dir)
        shutil.rmtree(self._zip_dir)

    # ABSTRACT
    def _process_node(self, node: Node, ntp_node_tree: NTP_NodeTree) -> None:
        return

    # ABSTRACT
    def _process_node_tree(self, node_tree: NodeTree) -> None:
        return

    def _report_finished(self, object: str):
        """
        Alert user that NTP is finished

        Parameters:
        object (str): the copied node tree or encapsulating structure
            (geometry node modifier, material, scene, etc.)
        """
        if self._mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = self._dir_path
        self.report({'INFO'}, f"NodeToPython: Saved {object} to {location}")

    # ABSTRACT
    def execute(self):
        return {'FINISHED'}
