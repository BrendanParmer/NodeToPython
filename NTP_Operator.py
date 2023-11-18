import bpy
from bpy.types import Context, Operator
from bpy.types import Node, NodeTree

from io import StringIO
import os
from typing import TextIO

from .NTP_NodeTree import NTP_NodeTree
from .utils import *

class NTP_Operator(Operator):
    """
    "Abstract" base class for all NTP operators. Blender types and abstraction
    don't seem to mix well, but this should only be inherited from
    """
    
    bl_idname = ""
    bl_label = ""

    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )

    def __init__(self):
        super().__init__()

        # File (TextIO) or string (StringIO) the add-on/script is generated into
        self._file : TextIO = None

        # Path to the current directory
        self._dir: str = None

        # Path to the directory of the zip file
        self._zip_dir: str = None

        # Path to the directory for the generated addon
        self._addon_dir: str = None

        # Class named for the generated operator
        self._class_name: str = None

        # Set to keep track of already created node trees
        self._node_trees: set[NodeTree] = set()

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}

        # Dictionary used for setting node properties
        self._settings: dict[str, list[(str, ST)]] = {}

    def _setup_addon_directories(self, context: Context, nt_var: str) -> None:
        """
        Finds/creates directories to save add-on to
        """
        #find base directory to save new addon
        self._dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
        if not self._dir or self._dir == "":
            self.report({'ERROR'}, 
                        ("NodeToPython: Save your blend file before using "
                         "NodeToPython!")) #TODO: Still valid??
            return {'CANCELLED'} #TODO

        self._zip_dir = os.path.join(self._dir, nt_var)
        self._addon_dir = os.path.join(self._zip_dir, nt_var)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)

    def _is_outermost_node_group(self, level: int) -> bool:
        if self.mode == 'ADDON' and level == 2:
            return True
        elif self.mode == 'SCRIPT' and level == 0:
            return True
        return False

    def _process_group_node_tree(self, node: Node, node_var: str, level: int, inner: str) -> None:
        """
        Processes node tree of group node if one is present
        """
        node_tree = node.node_tree
        if node_tree is not None:
            if node_tree not in self._node_trees:
                self._process_node_tree(node_tree, level + 1)
                self._node_trees.add(node_tree)
            self._file.write((f"{inner}{node_var}.node_tree = "
                              f"bpy.data.node_groups"
                              f"[\"{node.node_tree.name}\"]\n"))

    def _set_socket_defaults(self, node: Node, node_var: str, inner: str):
        if self.mode == 'ADDON':
            set_input_defaults(node, self._file, inner, node_var, self._addon_dir)
        elif self.mode == 'SCRIPT':
            set_input_defaults(node, self._file, inner, node_var)
        set_output_defaults(node, self._file, inner, node_var)

    # ABSTRACT
    def _process_node(self, node: Node, ntp_node_tree: NTP_NodeTree, inner: str, 
                      level: int) -> None:
        return

    # ABSTRACT
    def _process_node_tree(self, node_tree: NodeTree, level: int) -> None:
        return 

    def _report_finished(self, object: str):
        """
        Alert user that NTP is finished

        Parameters:
        object (str): the copied node tree or encapsulating structure
            (geometry node modifier, material, scene, etc.)
        """
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = self._dir
        self.report({'INFO'}, 
                    f"NodeToPython: Saved {object} to {location}")
    
    # ABSTRACT
    def execute(self):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")
