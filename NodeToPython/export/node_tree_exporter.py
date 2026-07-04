import abc
import copy
import os
from typing import Callable

import bpy

from .node_settings import node_settings, ST
from .ntp_node_tree import *
from .ntp_operator import NTP_OT_Export, NodeTreeInfo, NODE_TREE_NAMES
from .utils import *

BASE_DIR = "base_dir"
DATA_DST = "data_dst"
DATA_SRC = "data_src"
DATAFILES_PATH = "datafiles_path"
IMAGE_DIR_NAME = "imgs"
IMAGE_PATH = "image_path"
INDEX = "i"
ITEM = "item"
LIB_RELPATH = "lib_relpath"
LIB_PATH = "lib_path"
NODE = "node"
NODE_GROUP = "node_group"

RESERVED_NAMES = {
    BASE_DIR,
    DATA_DST,
    DATA_SRC,
    DATAFILES_PATH,
    IMAGE_DIR_NAME,
    IMAGE_PATH,
    INDEX,
    ITEM,
    LIB_RELPATH,
    LIB_PATH,
    NODE_TREE_NAMES,
    NODE_GROUP
}

NO_DEFAULT_SOCKETS = {
    bpy.types.NodeTreeInterfaceSocketCollection,
    bpy.types.NodeTreeInterfaceSocketGeometry,
    bpy.types.NodeTreeInterfaceSocketImage,
    bpy.types.NodeTreeInterfaceSocketMaterial,
    bpy.types.NodeTreeInterfaceSocketMatrix,
    bpy.types.NodeTreeInterfaceSocketObject,
    bpy.types.NodeTreeInterfaceSocketShader,
    bpy.types.NodeTreeInterfaceSocketTexture,
}

if bpy.app.version >= (5, 0, 0):
    NO_DEFAULT_SOCKETS.add(bpy.types.NodeTreeInterfaceSocketBundle)
    NO_DEFAULT_SOCKETS.add(bpy.types.NodeTreeInterfaceSocketClosure)

if bpy.app.version >= (5, 1, 0):
    NO_DEFAULT_SOCKETS.add(bpy.types.NodeTreeInterfaceSocketFont)

if bpy.app.version >= (5, 2, 0):
    NO_DEFAULT_SOCKETS.add(bpy.types.NodeTreeInterfaceSocketSound)

#node input sockets that are messy to set default values for
DONT_SET_DEFAULTS = {
    'NodeSocketGeometry',
    'NodeSocketShader',
    'NodeSocketMatrix',
    'NodeSocketVirtual',
    'NodeSocketBundle',
    'NodeSocketClosure'
}

class NodeTreeExporter(metaclass=abc.ABCMeta):
    _type = ""

    def __init__(
        self, 
        ntp_op: NTP_OT_Export,
        node_tree_info: NodeTreeInfo
    ):
        # Operator executing the conversion
        self._operator : NTP_OT_Export = ntp_op
        
        # Info for the node tree being exported
        self._node_tree_info : NodeTreeInfo = node_tree_info

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = copy.copy(self._operator._used_vars)
        for name in RESERVED_NAMES:
            self._used_vars[name] = 0

        # Variable name to be used for object
        self._obj_var : str = self._create_var(self._node_tree_info._obj.name)
    
        # Class name for the operator, if it exists
        if self._operator._mode == 'ADDON' and self._node_tree_info._is_base:
            self._class_name : str = (
                f"{clean_string(self._operator._name, lower=False)}_OT_"
                f"{clean_string(self._node_tree_info._obj.name, lower=False)}"
            )
            self._operator._modules[self._node_tree_info._module].append(
                self._class_name
            )

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[bpy.types.Node, str] = {}

        # Dictionary to keep track of node tree->variable name pairs
        self._node_tree_vars: dict[bpy.types.NodeTree, str] = {}

        # Write functions after nodes are mostly initialized and linked up
        self._write_after_links: list[Callable] = []
    
        # Copy of node settings (may have to modify for some nodes)
        self._node_settings = node_settings

    def export(self) -> None:
        # TODO: cleanup
        if self._operator._mode == 'SCRIPT':
            self._import_essential_libs()

        if self._node_tree_info._group_type.is_group():
            self._process_node_tree()

        if self._operator._mode == 'ADDON' and self._node_tree_info._is_base:
            self._init_operator(self._obj_var, self._node_tree_info._obj.name)
            self._write("def execute(self, context: bpy.types.Context):", 1)

            self._import_essential_libs()

            # node tree names
            self._write("# Maps node tree creation functions to the node tree ", 2)
            self._write("# name, such that we don't recreate node trees unnecessarily", 2)
            self._write(f"{NODE_TREE_NAMES} : dict[typing.Callable, str] = {{}}", 2)
            self._write("", 0)

            for dependency in self._node_tree_info._dependencies.keys():
                self._call_node_tree_creation(dependency, 2)
            
        if self._node_tree_info._group_type.is_obj():
            self._create_obj()
            self._process_node_tree()

        if self._operator._mode == 'ADDON' and self._node_tree_info._is_base:
            self._call_node_tree_creation(self._node_tree_info._base_tree, 2)
            self._write("return {'FINISHED'}", self._operator._outer_indent_level)

        self._write("", self._operator._outer_indent_level)

    def _write(self, string: str, indent_level: int = -1):
        self._operator._write(string, indent_level)

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
    
    def _init_operator(self, idname: str, label: str) -> None:
        """
        Initializes the add-on's operator 

        Parameters:
        idname (str): name for the operator
        label (str): appearence inside Blender
        """
        self._idname = idname
        self._write(f"class {self._class_name}(bpy.types.Operator):", 0)

        idname_str = f"{clean_string(self._operator._name)}.{idname}"
        self._write(f"bl_idname = {str_to_py_str(idname_str)}", 1)
        self._write(f"bl_label = {str_to_py_str(label)}", 1)
        self._write("bl_options = {\'REGISTER\', \'UNDO\'}\n", 1)

        self._write("def __init__(self, *args, **kwargs):", 1)
        self._write("super().__init__(*args, **kwargs)\n", 2)
        self._operator._outer_indent_level = 2
        self._operator._inner_indent_level = 3

    @abc.abstractmethod
    def _create_obj(self):
        pass

    def _get_obj_creation_indent(self) -> int:
        indent_level = -1
        if self._operator._mode == 'ADDON':
            indent_level = 2
        elif self._operator._mode == 'SCRIPT':
            indent_level = 0
        return indent_level

    def _import_essential_libs(self) -> None:
        if len(self._node_tree_info._lib_dependencies) == 0:
            return
        self._operator._inner_indent_level -= 1
        self._write("# Import node groups from Blender essentials library")
        self._write(f"{DATAFILES_PATH} = bpy.utils.system_resource('DATAFILES')")
        for path, node_trees in self._node_tree_info._lib_dependencies.items():
            self._write(f"{LIB_RELPATH} = {str_to_py_str(str(path))}")
            self._write(f"{LIB_PATH} = os.path.join({DATAFILES_PATH}, {LIB_RELPATH})")
            self._write(f"with bpy.data.libraries.load({LIB_PATH}, link=True) "
                        f" as ({DATA_SRC}, {DATA_DST}):")
            self._write(f"\t{DATA_DST}.node_groups = []")
            for node_tree in node_trees:
                name_str = str_to_py_str(node_tree.name)
                self._write(f"\tif {name_str} in {DATA_SRC}.node_groups:")
                self._write(f"\t\t{DATA_DST}.node_groups.append({name_str})")
                # TODO: handle bad case with warning (in both script and addon mode)
        self._write("\n")
        self._operator._inner_indent_level += 1

    
    def _initialize_ntp_node_tree(
        self, 
        node_tree: bpy.types.NodeTree,
        nt_var: str
    ) -> NTP_NodeTree:
        return NTP_NodeTree(node_tree, nt_var)

    def _process_node_tree(self) -> None:
        """
        Generates a Python function to recreate a compositor node tree

        Parameters:
        node_tree (NodeTree): node tree to be recreated
        """
        node_tree = self._node_tree_info._base_tree
        nt_var = self._create_var(node_tree.name)
        self._node_tree_vars[node_tree] = nt_var

        ntp_nt = self._initialize_ntp_node_tree(node_tree, nt_var)

        self._initialize_node_tree(ntp_nt)

        self._set_node_tree_properties(node_tree)
        
        self._tree_interface_settings(ntp_nt)

        #initialize nodes
        self._write(f"# Initialize {nt_var} nodes\n")

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt)

        for zone_list in ntp_nt._zone_inputs.values():
            self._process_zones(zone_list)
        
        #set look of nodes
        self._set_parents(node_tree)
        self._set_locations(node_tree)
        self._set_dimensions(node_tree)

        #create connections
        self._init_links(node_tree)
        
        self._write(f"return {nt_var}\n")
    
    @abc.abstractmethod
    def _initialize_node_tree(
        self, 
        ntp_node_tree: NTP_NodeTree
    ) -> None:
        pass

    def _set_node_tree_properties(self, node_tree: bpy.types.NodeTree) -> None:
        nt_var = self._node_tree_vars[node_tree]

        color_tag_str = enum_to_py_str(node_tree.color_tag)
        self._write(f"{nt_var}.color_tag = {color_tag_str}")

        desc_str = str_to_py_str(node_tree.description)
        self._write(f"{nt_var}.description = {desc_str}")

        if bpy.app.version >= (4, 3, 0):
            default_width = node_tree.default_group_node_width
            self._write(f"{nt_var}.default_group_node_width = {default_width}")

    def _tree_interface_settings(self, ntp_nt: NTP_NodeTree) -> None:
        """
        Set the settings for group input and output sockets

        Parameters:
        ntp_nt (NTP_NodeTree): the node tree to set the interface for
        """
        if len(ntp_nt._node_tree.interface.items_tree) == 0:
            return
        
        self._write(f"# {ntp_nt._var} interface\n")
        panel_dict: dict[bpy.types.NodeTreeInterfacePanel, str] = {}
        items_processed: set[bpy.types.NodeTreeInterfaceItem] = set()

        self._process_items(None, panel_dict, items_processed, ntp_nt)

    def _process_items(
            self, 
            parent: bpy.types.NodeTreeInterfacePanel | None, 
            panel_dict: dict[bpy.types.NodeTreeInterfacePanel, str], 
            items_processed: set[bpy.types.NodeTreeInterfaceItem], 
            ntp_nt: NTP_NodeTree
    ) -> None:
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
            items = ntp_nt._node_tree.interface.items_tree
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
                self._create_panel(
                    item, 
                    panel_dict, 
                    items_processed,
                    parent, 
                    ntp_nt
                )
                if bpy.app.version >= (4, 4, 0) and parent is not None:
                    nt_var = self._node_tree_vars[ntp_nt._node_tree]
                    interface_var = f"{nt_var}.interface"
                    panel_var = panel_dict[item]
                    parent_var = panel_dict[parent]
                    self._write(f"{interface_var}.move_to_parent("
                                f"{panel_var}, {parent_var}, {item.index})")

    def _create_socket(
        self, 
        socket: bpy.types.NodeTreeInterfaceSocket, 
        parent: bpy.types.NodeTreeInterfacePanel, 
        panel_dict: dict[bpy.types.NodeTreeInterfacePanel, str], 
        ntp_nt: NTP_NodeTree
    ) -> None:
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
                    f"{ntp_nt._var}.interface.new_socket("
                    f"name={name}, in_out={in_out_enum}, "
                    f"socket_type={socket_type}"
                    f"{optional_parent_str})")

        # vector dimensions
        if hasattr(socket, "dimensions"):
            dimensions : int = getattr(socket, "dimensions")
            if dimensions != 3:
                self._write(f"{socket_var}.dimensions = {dimensions}")
                self._write("# Get the socket again, as its default value may "
                            "have been updated")
                self._write(f"{socket_var} = {ntp_nt._var}.interface.items_tree[{socket_var}.index]")

        self._set_tree_socket_defaults(socket, socket_var)

        # subtype
        if hasattr(socket, "subtype"):
            subtype : str = getattr(socket, "subtype")
            if subtype != '':
                subtype = enum_to_py_str(subtype)
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

        if bpy.app.version >= (5, 0, 0):
            # optional label
            if socket.optional_label:
                self._write(f"{socket_var}.optional_label = True")

        self._write("", 0)

    def _create_panel(
        self, 
        panel: bpy.types.NodeTreeInterfacePanel,
        panel_dict: dict[bpy.types.NodeTreeInterfacePanel, str],
        items_processed: set[bpy.types.NodeTreeInterfacePanel], 
        parent: bpy.types.NodeTreeInterfacePanel, 
        ntp_nt: NTP_NodeTree):
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

            self._write(
                f"{panel_var} = {ntp_nt._var}.interface.new_panel("
                f"{str_to_py_str(panel.name)}{closed_str})"
            )

            # tooltip
            if panel.description != "":
                description = str_to_py_str(panel.description)
                self._write(f"{panel_var}.description = {description}")

            panel_dict[panel] = panel_var

            if len(panel.interface_items) > 0:
                self._process_items(panel, panel_dict, items_processed, ntp_nt)
            
            self._write("", 0)

    def _set_tree_socket_defaults(
        self, 
        socket_interface: bpy.types.NodeTreeInterfaceSocket,
        socket_var: str
    ) -> None:
        """
        Set a node tree input/output's default properties if they exist

        Helper function to _create_socket()

        Parameters:
        socket_interface (NodeTreeInterfaceSocket): socket interface associated
            with the input/output
        socket_var (str): variable name for the socket
        """
        if not self._operator._include_group_socket_values:
            return
        
        if type(socket_interface) in NO_DEFAULT_SOCKETS:
            return

        dv = getattr(socket_interface, "default_value")

        if type(socket_interface) is bpy.types.NodeTreeInterfaceSocketMenu:
            if dv == "":
                self._operator.report(
                    {'WARNING'},
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
        elif type(dv) == mathutils.Euler:
            dv = vec3_to_py_str(dv)
        elif type(dv) == bpy_prop_array:
            if hasattr(socket_interface, "dimensions"):
                dimensions = getattr(socket_interface, "dimensions")
                if dimensions != len(dv):
                    self._operator.report(
                        {'WARNING'},
                        f"Mismatched dimensions ({dimensions}) and "
                        f"default value ({len(dv)}) for socket {socket_var}"
                    )
                if dimensions <= len(dv):
                    dv = vec_to_py_str(dv, dimensions)
                else:
                    return
            else:
                dv = array_to_py_str(dv)
        elif type(dv) == str:
            dv = str_to_py_str(dv)
        elif type(dv) == mathutils.Vector:
            dimensions = getattr(socket_interface, "dimensions")
            if dimensions != len(dv):
                self._operator.report(
                    {'WARNING'},
                    f"Mismatched dimensions ({dimensions}) and "
                    f"default value ({len(dv)}) for socket {socket_var}"
                )
                return
            if dimensions in {2, 3, 4}:
                dv = vec_to_py_str(dv, dimensions)
            else:
                self._operator.report(
                    {'WARNING'},
                    f"Incorrect number of dimensions {dimensions} "
                    f"found for socket {socket_var}"
                )
                return
        self._write(f"{socket_var}.default_value = {dv}")

        # min value
        if hasattr(socket_interface, "min_value"):
            min_val = getattr(socket_interface, "min_value")
            self._write(f"{socket_var}.min_value = {min_val}")
        # max value
        if hasattr(socket_interface, "max_value"):
            max_val = getattr(socket_interface, "max_value")
            self._write(f"{socket_var}.max_value = {max_val}")

    def _process_node(self, node: bpy.types.Node, ntp_nt: NTP_NodeTree) -> None:
        """
        Create node and set settings, defaults, and cosmetics

        Parameters:
        node (Node): node to process
        ntp_nt (NTP_NodeTree): the node tree that node belongs to
        """
        node_var: str = self._create_node(node, ntp_nt._var)
        self._set_settings_defaults(node)

        if node.bl_idname in ntp_nt._zone_inputs:
            ntp_nt._zone_inputs[node.bl_idname].append(node)
        
        self._hide_hidden_sockets(node)

        if node.bl_idname not in ntp_nt._zone_inputs:
            self._set_socket_defaults(node)

    def _create_node(self, node: bpy.types.Node, node_tree_var: str) -> str:
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

        bool_flags = [
            "mute", "hide", "show_options", "show_preview","show_texture"
        ]

        for flag in bool_flags:
            if getattr(node, flag, False):
                self._write(f"{node_var}.{flag} = True")

        # Warning propagation
        if bpy.app.version >= (4, 3, 0):
            if node.warning_propagation != 'ALL':
                self._write(f"{node_var}.warning_propagation = "
                            f"{enum_to_py_str(node.warning_propagation)}")
        return node_var
    
    def _set_settings_defaults(self, node: bpy.types.Node) -> None:
        """
        Sets the defaults for any settings a node may have

        Parameters:
        node (Node): the node object we're copying settings from
        node_var (str): name of the variable we're using for the node in our add-on
        """
        if node.bl_idname not in self._node_settings:
            self._operator.report({'WARNING'},
                        (f"NodeToPython: couldn't find {node.bl_idname} in "
                         f"settings. Your Blender version may not be supported"))
            return

        node_var = self._node_vars[node]

        node_info = self._node_settings[node.bl_idname]
        for attr_info in node_info.attributes_:
            attr_name = attr_info.name_
            st = attr_info.st_

            version_gte_min = bpy.app.version >= max(attr_info.min_version_, node_info.min_version_)
            version_lt_max = bpy.app.version < min(attr_info.max_version_, node_info.max_version_)
            
            is_version_valid = version_gte_min and version_lt_max
            if not is_version_valid:
                continue

            if not hasattr(node, attr_name):
                self._operator.report({'WARNING'},
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
            elif st == ST.VEC:
                self._write(f"{setting_str} = {vec_to_py_str(attr, len(attr))}")
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
            elif st == ST.EULER:
                self._write(f"{setting_str} = {vec3_to_py_str(attr)}")
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
                if self._operator._addon_dir != "":
                    if attr.source in {'FILE', 'GENERATED', 'TILED'}:
                        if self._save_image(attr):
                            self._load_image(attr, setting_str)
                else:
                    self._set_if_in_blend_file(attr, setting_str, "images")

            elif st == ST.IMAGE_USER:
                self._image_user_settings(attr, setting_str)
            elif st == ST.SIM_OUTPUT_ITEMS:
                self._output_zone_items(attr, setting_str, True)
            elif st == ST.REPEAT_OUTPUT_ITEMS:
                self._output_zone_items(attr, setting_str, False)
            elif st == ST.INDEX_SWITCH_ITEMS:
                self._index_switch_items(attr, setting_str)
            elif st == ST.ENUM_DEFINITION:
                self._enum_definition(attr, setting_str)
            elif st == ST.BAKE_ITEMS:
                self._bake_items(attr, setting_str)
            elif st == ST.CAPTURE_ATTRIBUTE_ITEMS:
                self._capture_attribute_items(attr, setting_str)
            elif st == ST.MENU_SWITCH_ITEMS:
                self._menu_switch_items(attr, setting_str)
            elif st == ST.FOREACH_GEO_ELEMENT_GENERATION_ITEMS:
                self._foreach_geo_element_generation_items(attr, setting_str)
            elif st == ST.FOREACH_GEO_ELEMENT_INPUT_ITEMS:
                self._foreach_geo_element_input_items(attr, setting_str)
            elif st == ST.FOREACH_GEO_ELEMENT_MAIN_ITEMS:
                self._foreach_geo_element_main_items(attr, setting_str)
            elif st == ST.FORMAT_STRING_ITEMS:
                self._format_string_items(attr, setting_str)
            elif st == ST.CLOSURE_INPUT_ITEMS:
                self._closure_input_items(attr, setting_str)
            elif st == ST.CLOSURE_OUTPUT_ITEMS:
                self._closure_output_items(attr, setting_str)
            elif st == ST.COLOR_MANAGED_DISPLAY_SETTINGS:
                self._color_managed_display_settings(attr, setting_str)
            elif st == ST.COLOR_MANAGED_VIEW_SETTINGS:
                self._color_managed_view_settings(attr, setting_str)
            elif st == ST.COMPOSITOR_FILE_OUTPUT_ITEMS:
                self._compositor_file_output_items(attr, setting_str)
            elif st == ST.EVALUATE_CLOSURE_INPUT_ITEMS:
                self._evaluate_closure_input_items(attr, setting_str)
            elif st == ST.EVALUATE_CLOSURE_OUTPUT_ITEMS:
                self._evaluate_closure_output_items(attr, setting_str)
            elif st == ST.FIELD_TO_GRID_ITEMS:
                self._field_to_grid_items(attr, setting_str)
            elif st == ST.GEOMETRY_VIEWER_ITEMS:
                self._geometry_viewer_items(attr, setting_str)
            elif st == ST.COMBINE_BUNDLE_ITEMS:
                self._combine_bundle_items(attr, setting_str)
            elif st == ST.SEPARATE_BUNDLE_ITEMS:
                self._separate_bundle_items(attr, setting_str)

    def _set_if_in_blend_file(self, attr, setting_str: str, data_type: str
                              ) -> None:
        """
        Attempts to grab referenced thing from blend file
        """
        name = str_to_py_str(attr.name)
        self._write(f"if {name} in bpy.data.{data_type}:")
        self._write(f"{setting_str} = bpy.data.{data_type}[{name}]",
                    self._operator._inner_indent_level + 1)   
         
    def _color_ramp_settings(self, node: bpy.types.Node, color_ramp_name: str) -> None:
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

    def _curve_mapping_settings(self, node: bpy.types.Node,
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

    def _create_curve_map(self, node: bpy.types.Node, i: int, curve: bpy.types.CurveMap,
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
                        self._operator._inner_indent_level + 1)

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
    
    def _node_tree_settings(self, node: bpy.types.Node, attr_name: str) -> None:
        """
        Processes node tree of group node if one is present

        Parameters:
        node (Node): the group node
        attr_name (str): name of the node tree attribute
        """
        node_tree = getattr(node, attr_name)
        if node_tree is None:
            return
        
        node_var = self._node_vars[node]
        if node_tree in self._operator._node_trees:
            # TODO: probably should be done similar to lib trees
            node_tree_info = self._operator._node_trees[node_tree]

            if (self._operator._mode == 'SCRIPT' or 
                node_tree_info._module == self._node_tree_info._module):
                func = node_tree_info._func
            else:
                func = f"{node_tree_info._module}.{node_tree_info._func}"

            name_var = f"{NODE_TREE_NAMES}[{func}]"

            self._write(
                f"{node_var}.{attr_name} = bpy.data.node_groups[{name_var}]"
            )
            return
        else:
            # Library nodes

            # Keys don't seem to be unique for linked groups, 
            # need to do this nonsense
            self._write(f"# Finding linked library node group")
            self._write(f"for {NODE_GROUP} in bpy.data.node_groups:")
            self._write(f"if (", self._operator._inner_indent_level + 1)
            self._write(f"{NODE_GROUP}.name == {str_to_py_str(node_tree.name)}",
                        self._operator._inner_indent_level + 2)
            self._write(f"and {NODE_GROUP}.bl_idname == {enum_to_py_str(node_tree.bl_idname)}",
                        self._operator._inner_indent_level + 2)
            self._write("):", self._operator._inner_indent_level + 1)
            self._write(f"{node_var}.{attr_name} = {NODE_GROUP}",
                        self._operator._inner_indent_level + 2)
            
            self._write(f"if {node_var}.{attr_name} is None:")
            self._write(f"print(\"Couldn't find node group "
                        f"{node_tree.name}, failing\")",
                        self._operator._inner_indent_level + 1)
            self._write(f"return", self._operator._inner_indent_level + 1)
            return
            
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
            self._operator.report(
                {'WARNING'}, 
                f"{img_str} has no data"
            )
            return False

        # create image dir if one doesn't exist
        img_dir = os.path.join(self._operator._addon_dir, IMAGE_DIR_NAME)
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
    
    def _capture_attribute_items(
        self, 
        capture_attribute_items: bpy.types.NodeGeometryCaptureAttributeItems, 
        capture_attrs_str: str
    ) -> None:
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

    def _menu_switch_items(
        self, 
        menu_switch_items: bpy.types.NodeMenuSwitchItems, 
        menu_switch_items_str: str
    ) -> None:
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
            format_items_str: str
        ) -> None:
            self._write(f"{format_items_str}.clear()")
            for i, item in enumerate(format_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write(f"{format_items_str}.new({socket_type}, {name_str})")

    if bpy.app.version >= (5, 0, 0):
        def _closure_input_items(self,
            closure_input_items : bpy.types.NodeClosureInputItems,
            closure_input_items_str : str
        ) -> None:
            self._write(f"{closure_input_items_str}.clear()")
            for i, item in enumerate(closure_input_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{closure_input_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{closure_input_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")

        def _closure_output_items(self,
            closure_output_items : bpy.types.NodeClosureOutputItems,
            closure_output_items_str : str
        ) -> None:
            self._write(f"{closure_output_items_str}.clear()")
            for i, item in enumerate(closure_output_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{closure_output_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{closure_output_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")

        def _evaluate_closure_input_items(self,
            evaluate_closure_input_items : bpy.types.NodeEvaluateClosureInputItems,
            evaluate_closure_input_items_str : str
        ) -> None:
            self._write(f"{evaluate_closure_input_items_str}.clear()")
            for i, item in enumerate(evaluate_closure_input_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{evaluate_closure_input_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{evaluate_closure_input_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")

        def _evaluate_closure_output_items(self,
            evaluate_closure_output_items : bpy.types.NodeEvaluateClosureOutputItems,
            evaluate_closure_output_items_str : str
        ) -> None:
            self._write(f"{evaluate_closure_output_items_str}.clear()")
            for i, item in enumerate(evaluate_closure_output_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{evaluate_closure_output_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{evaluate_closure_output_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")
        
        def _combine_bundle_items(self,
            combine_bundle_items : bpy.types.NodeCombineBundleItems,
            combine_bundle_items_str : str
        ) -> None:
            self._write(f"{combine_bundle_items_str}.clear()")
            for i, item in enumerate(combine_bundle_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{combine_bundle_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{combine_bundle_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")

        def _separate_bundle_items(self,
            separate_bundle_items: bpy.types.NodeSeparateBundleItems,
            separate_bundle_items_str : str,
        ) -> None:
            self._write(f"{separate_bundle_items_str}.clear()")
            for i, item in enumerate(separate_bundle_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{separate_bundle_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                item_str = f"{separate_bundle_items_str}[{i}]"

                structure_type = enum_to_py_str(item.structure_type)
                self._write(f"{item_str}.structure_type = {structure_type}")

        def _field_to_grid_items(self,
            field_to_grid_items: bpy.types.GeometryNodeFieldToGridItems,
            field_to_grid_items_str : str,
        ) -> None:
            self._write(f"{field_to_grid_items_str}.clear()")
            for i, item in enumerate(field_to_grid_items):
                data_type = enum_to_py_str(item.data_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{field_to_grid_items_str}.new("
                             f"{data_type}, {name_str})"))
                
        def _geometry_viewer_items(self,
            geometry_viewer_items: bpy.types.NodeGeometryViewerItems,
            geometry_viewer_items_str : str,
        ) -> None:
            self._write(f"{geometry_viewer_items_str}.clear()")
            for i, item in enumerate(geometry_viewer_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{geometry_viewer_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                items_str = f"{geometry_viewer_items_str}[{i}]"
                
                # auto remove will automatically remove input if not linked
                # need to initialize after links
                auto_remove_str = f"{items_str}.auto_remove = {item.auto_remove}"
                self._write_after_links.append(
                    lambda _auto_remove_str = auto_remove_str: (
                        self._write(_auto_remove_str)
                    )
                )
        
        def _compositor_file_output_items(self,
            compositor_file_output_items: bpy.types.NodeCompositorFileOutputItems,
            compositor_file_output_items_str : str,
        ) -> None:
            self._write(f"{compositor_file_output_items_str}.clear()")
            for i, item in enumerate(compositor_file_output_items):
                socket_type = enum_to_py_str(item.socket_type)
                name_str = str_to_py_str(item.name)
                self._write((f"{compositor_file_output_items_str}.new("
                             f"{socket_type}, {name_str})"))
                
                items_str = f"{compositor_file_output_items_str}[{i}]"
                
                self._write(f"{items_str}.override_node_format = {item.override_node_format}")
                self._write(f"{items_str}.save_as_render = {item.save_as_render}")
                if item.socket_type == 'VECTOR':
                    self._write(f"{items_str}.vector_socket_dimensions = "
                                f"{item.vector_socket_dimensions}")
                    
        def _color_managed_display_settings(self,
            display_settings : bpy.types.ColorManagedDisplaySettings,
            display_settings_str : str
        ) -> None:
            device_str = enum_to_py_str(display_settings.display_device)
            self._write(f"{display_settings_str}.display_device = {device_str}")
            emulation_str = enum_to_py_str(display_settings.emulation)
            self._write(f"{display_settings_str}.emulation = {emulation_str}")
    
        def _color_managed_view_settings(self,
            view_settings : bpy.types.ColorManagedViewSettings,
            view_settings_str : str
        ) -> None:
            # view transform must go before setting look
            view_transform_str = enum_to_py_str(view_settings.view_transform)
            self._write(f"{view_settings_str}.view_transform = {view_transform_str}")

            look_str = enum_to_py_str(view_settings.look)
            self._write(f"{view_settings_str}.look = {look_str}")

    def _hide_hidden_sockets(self, node: bpy.types.Node) -> None:
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

    def _set_socket_defaults(self, node: bpy.types.Node) -> None:
        """
        Set input and output socket defaults
        """
        self._set_input_defaults(node)
        self._set_output_defaults(node)

    def _set_input_defaults(self, node: bpy.types.Node) -> None:
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
                if (not self._operator._set_unavailable_defaults) and input.is_unavailable:
                    continue
                    
                # TODO: this could be cleaner
                socket_var = f"{node_var}.inputs[{i}]"

                default_val = getattr(input, "default_value")
                # colors
                if input.bl_idname == 'NodeSocketColor':
                    default_val = vec4_to_py_str(default_val)

                # vector types
                elif "Vector" in input.bl_idname:
                    if "2D" in input.bl_idname:
                        default_val = vec2_to_py_str(default_val)
                    elif "4D" in input.bl_idname:
                        default_val = vec4_to_py_str(default_val)
                    else:
                        default_val = vec3_to_py_str(default_val)

                # rotation types
                elif input.bl_idname == 'NodeSocketRotation':
                    default_val = vec3_to_py_str(default_val)

                # strings
                elif input.bl_idname in {
                    'NodeSocketString', 
                    'NodeSocketStringFilePath'
                }:
                    default_val = str_to_py_str(default_val)

                #menu
                elif input.bl_idname == 'NodeSocketMenu':
                    if default_val == '':
                        continue
                    default_val = enum_to_py_str(default_val)

                # images
                elif input.bl_idname == 'NodeSocketImage':
                    if default_val is not None:
                        if self._operator._mode == 'ADDON':
                            if self._save_image(default_val):
                                self._load_image(
                                    default_val, 
                                    f"{socket_var}.default_value"
                                )
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

                elif input.bl_idname == 'NodeSocketFont':
                    self._in_file_inputs(input, socket_var, "fonts")
                    default_val = None

                elif input.bl_idname == 'NodeSocketSound':
                    self._in_file_inputs(input, socket_var, "sounds")
                    default_val = None

                else:
                    default_val = getattr(input, "default_value")

                if default_val is not None:
                    self._write(f"# {input.identifier}")
                    self._write(f"{socket_var}.default_value = {default_val}")
        self._write("", 0)

    def _set_output_defaults(self, node: bpy.types.Node) -> None:
        """
        Some output sockets need default values set. It's rather annoying

        Parameters:
        node (Node): node for the output we're setting
        """
        # TODO: probably should define elsewhere
        OUTPUT_SOCKET_DEFAULT_NODES = {
            'ShaderNodeValue',
            'ShaderNodeRGB',
            'ShaderNodeNormal',
            'CompositorNodeValue',
            'CompositorNodeRGB',
            'CompositorNodeNormal'
        }

        if node.bl_idname not in OUTPUT_SOCKET_DEFAULT_NODES:
            return

        node_var = self._node_vars[node]

        dv = getattr(node.outputs[0], "default_value")
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
        dv = getattr(input, "default_value")
        if dv is None:
            return
        name = str_to_py_str(dv.name)
        self._write(f"if {name} in bpy.data.{type}:")
        self._write(f"{socket_var}.default_value = bpy.data.{type}[{name}]",
                    self._operator._inner_indent_level + 1)

    def _process_zones(self, zone_input_list: list[bpy.types.Node]) -> None:
        """
        Recreates a zone
        zone_input_list (list[bpy.types.Node]): list of zone input 
            nodes
        """
        for input_node in zone_input_list:
            zone_output = getattr(input_node, "paired_output")

            zone_input_var = self._node_vars[input_node]
            zone_output_var = self._node_vars[zone_output]

            self._write(f"# Process zone input {input_node.name}")
            self._write(f"{zone_input_var}.pair_with_output"
                        f"({zone_output_var})")

            #must set defaults after paired with output
            self._set_socket_defaults(input_node)
            self._set_socket_defaults(zone_output)

        if zone_input_list:
            self._write("", 0)

    def _get_node_var(
        self, 
        node_tree: bpy.types.NodeTree, 
        node: bpy.types.Node
    ) -> str:
        nt_var = self._node_tree_vars[node_tree]
        return f"{nt_var}.nodes[{str_to_py_str(node.name)}]"
    
    def _set_parents(self, node_tree: bpy.types.NodeTree) -> None:
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
                node_var = self._get_node_var(node_tree, node)
                parent_var = self._get_node_var(node_tree, node.parent)
                self._write(f"{node_var}.parent = {parent_var}")
        if parent_comment:
            self._write("", 0)

    def _set_locations(self, node_tree: bpy.types.NodeTree) -> None:
        """
        Set locations for all nodes

        Parameters:
        node_tree (NodeTree): node tree we're obtaining nodes from
        """

        self._write(f"# Set locations")
        for node in node_tree.nodes:
            node_var = self._get_node_var(node_tree, node)
            self._write(f"{node_var}.location "
                        f"= ({node.location.x}, {node.location.y})")
        if node_tree.nodes:
            self._write("", 0)

    def _set_dimensions(self, node_tree: bpy.types.NodeTree) -> None:
        """
        Set dimensions for all nodes

        Parameters:
        node_tree (NodeTree): node tree we're obtaining nodes from
        """
        if not self._operator._should_set_dimensions:
            return

        self._write(f"# Set dimensions")
        for node in node_tree.nodes:
            node_var = self._get_node_var(node_tree, node)
            self._write(f"{node_var}.width  = {node.width}")
            self._write(f"{node_var}.height = {node.height}")
            self._write("", 0)
        if node_tree.nodes:
            self._write("", 0)

    def _init_links(self, node_tree: bpy.types.NodeTree) -> None:
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
            if link.from_node is None:
                self._operator.report(
                    {'WARNING'},
                    "Link's from_node was None. This shouldn't happen"
                )
                continue
            if link.to_node is None:
                self._operator.report(
                    {'WARNING'},
                    "Link's to_node was None. This shouldn't happen"
                )
                continue

            in_node_var = self._node_vars[link.from_node]
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

            out_node_var = self._node_vars[link.to_node]
            output_socket = link.to_socket

            for i, item in enumerate(link.to_node.inputs.items()):
                if item[1] == output_socket:
                    output_idx = i
                    break

            self._write(f"# {in_node_var}.{input_socket.name} "
                        f"-> {out_node_var}.{output_socket.name}")
            
            self._write(f"{nt_var}.links.new(")
            self._write(
                f"{self._get_node_var(node_tree, link.from_node)}"
                f".outputs[{input_idx}],",
                self._operator._inner_indent_level + 1
            )
            self._write(
                f"{self._get_node_var(node_tree, link.to_node)}"
                f".inputs[{output_idx}]",
                self._operator._inner_indent_level + 1
            )
            self._write(")")

        for func in self._write_after_links:
            func()
        self._write_after_links = []
        self._write("", 0)

    def _call_node_tree_creation(
        self, 
        node_tree: bpy.types.NodeTree,
        indent_level: int
    ) -> None:
        node_tree_info = self._operator._node_trees[node_tree]
        if node_tree in self._node_tree_vars:
            nt_var = self._node_tree_vars[node_tree]
        else:
            nt_var = self._create_var(f"{node_tree.name}")

        if node_tree_info._module != self._node_tree_info._module:
            func = f"{node_tree_info._module}.{node_tree_info._func}"
        else:
            func = node_tree_info._func
        self._write(
            f"{nt_var} = {func}({NODE_TREE_NAMES})", 
            indent_level
        )
        self._write(
            f"{NODE_TREE_NAMES}[{func}] = {nt_var}.name\n",
            indent_level
        )