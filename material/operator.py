import bpy
from bpy.types import Context
from bpy.types import Operator
from bpy.types import Node
from bpy.types import ShaderNodeTree

import os
from io import StringIO

from ..utils import *
from .node_settings import shader_node_settings
from .node_tree import NTP_ShaderNodeTree

MAT_VAR = "mat"

class NTPMaterialOperator(Operator):
    bl_idname = "node.ntp_material"
    bl_label =  "Material to Python"
    bl_options = {'REGISTER', 'UNDO'}

    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )
    
    #TODO: add option for general shader node groups
    material_name: bpy.props.StringProperty(name="Node Group")

    def __init__(self):
        # File/string the add-on/script is generated into
        self._file: TextIO = None

        # Path to the current directory
        self._dir: str = None

        # Path to the directory of the zip file
        self._zip_dir: str = None

        # Path to the directory for the generated addon
        self._addon_dir: str = None

        # Class named for the generated operator
        self._class_name: str = None

        # Set to keep track of already created node trees
        self._node_trees: set[ShaderNodeTree] = set()

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}

    def _setup_addon_directories(self, context: Context, mat_var: str):
        self._dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
        if not self._dir or self._dir == "":
            self.report({'ERROR'},
                        ("NodeToPython: Save your blender file before using "
                        "NodeToPython!"))
            return {'CANCELLED'} #TODO: check this doesn't make sad

        self._zip_dir = os.path.join(self._dir, mat_var)
        self._addon_dir = os.path.join(self._zip_dir, mat_var)
        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)
        self._file = open(f"{self._addon_dir}/__init__.py", "w")

        create_header(self._file, self.material_name)
        self._class_name = clean_string(self.material_name, lower=False)
        init_operator(self._file, self._class_name, mat_var, self.material_name)

        self._file.write("\tdef execute(self, context):\n")

    def _create_material(self, indent: str):
        self._file.write((f"{indent}{MAT_VAR} = bpy.data.materials.new("
                    f"name = {str_to_py_str(self.material_name)})\n"))
        self._file.write(f"{indent}{MAT_VAR}.use_nodes = True\n")
    
    def _is_outermost_node_group(self, level: int) -> bool:
        if self.mode == 'ADDON' and level == 2:
            return True
        elif self.mode == 'SCRIPT' and level == 0:
            return True
        return False

    def _initialize_shader_node_tree(self, outer, nt_var, level, inner, nt_name):
         #initialize node group
        self._file.write(f"{outer}#initialize {nt_var} node group\n")
        self._file.write(f"{outer}def {nt_var}_node_group():\n")

        if self._is_outermost_node_group(level):
            self._file.write(f"{inner}{nt_var} = {MAT_VAR}.node_tree\n")
            self._file.write(f"{inner}#start with a clean node tree\n")
            self._file.write(f"{inner}for node in {nt_var}.nodes:\n")
            self._file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
        else:
            self._file.write((f"{inner}{nt_var}"
                    f"= bpy.data.node_groups.new("
                    f"type = \'ShaderNodeTree\', "
                    f"name = {str_to_py_str(nt_name)})\n"))
            self._file.write("\n")

    def _process_shader_group_node(self, node, level, inner, node_var):
        node_nt = node.node_tree
        if node_nt is not None:
            if node_nt not in self._node_trees:
                self._process_shader_node_tree(node_nt, level + 1)
                self._node_trees.add(node_nt)

            self._file.write((f"{inner}{node_var}.node_tree = "
                                f"bpy.data.node_groups"
                                f"[\"{node.node_tree.name}\"]\n"))

    def _set_socket_defaults(self, node, inner, node_var):
        if self.mode == 'ADDON':
            set_input_defaults(node, self._file, inner, node_var, self._addon_dir)
        else:
            set_input_defaults(node, self._file, inner, node_var)
        set_output_defaults(node, self._file, inner, node_var)

    def _process_shader_node(self, node: Node, ntp_node_tree: NTP_ShaderNodeTree, inner: str, level: int) -> None:
        node_var = create_node(node, self._file, inner, ntp_node_tree.var_name, self._node_vars, 
                                self._used_vars)
        set_settings_defaults(node, shader_node_settings, self._file, 
                                self._addon_dir, inner, node_var)

        if node.bl_idname == 'ShaderNodeGroup':
            self._process_shader_group_node(node, level, inner, node_var)

        elif node.bl_idname == 'NodeGroupInput' and not ntp_node_tree.inputs_set:
            group_io_settings(node, self._file, inner, "input", ntp_node_tree.var_name, ntp_node_tree.node_tree)
            ntp_node_tree.inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not ntp_node_tree.outputs_set:
            group_io_settings(node, self._file, inner, "output", ntp_node_tree.var_name, ntp_node_tree.node_tree)
            ntp_node_tree.outputs_set = True

        hide_hidden_sockets(node, self._file, inner, node_var)
        self._set_socket_defaults(node, inner, node_var)
        
    def _process_shader_node_tree(self, node_tree: bpy.types.NodeTree, 
                            level: int
                            ) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (bpy.types.NodeTree): node tree to be recreated
        level (int): number of tabs to use for each line, used with
            node groups within node groups and script/add-on differences
        """

        if self._is_outermost_node_group(level):
            nt_var = create_var(self.material_name, self._used_vars)
            nt_name = self.material_name #TODO: this is probably overcomplicating things if we move to a harder material vs shader node tree difference
        else:
            nt_var = create_var(node_tree.name, self._used_vars)
            nt_name = node_tree.name

        outer, inner = make_indents(level)

        self._initialize_shader_node_tree(outer, nt_var, level, inner, nt_name)

        ntp_nt = NTP_ShaderNodeTree(node_tree, nt_var)

        #initialize nodes
        self._file.write(f"{inner}#initialize {nt_var} nodes\n")

        for node in node_tree.nodes:
            self._process_shader_node(node, ntp_nt, inner, level)

        set_parents(node_tree, self._file, inner, self._node_vars)
        set_locations(node_tree, self._file, inner, self._node_vars)
        set_dimensions(node_tree, self._file, inner, self._node_vars)

        init_links(node_tree, self._file, inner, nt_var, self._node_vars)

        self._file.write(f"\n{outer}{nt_var}_node_group()\n\n")

    def _report_finished(self):
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = self._dir

        self.report({'INFO'}, f"NodeToPython: Saved material to {location}")

    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.materials[self.material_name].node_tree
        if nt is None:
            self.report({'ERROR'}, ("NodeToPython: This doesn't seem to be a "
                                    "valid material. Is Use Nodes selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        mat_var = clean_string(self.material_name)
        
        if self.mode == 'ADDON':
            self._setup_addon_directories(context, mat_var)
        else:
            self._file = StringIO("")

        if self.mode == 'ADDON':
            self._create_material("\t\t")
        elif self.mode == 'SCRIPT':
            self._create_material("")


        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0        
        self._process_shader_node_tree(nt, level)

        if self.mode == 'ADDON':
            self._file.write("\t\treturn {'FINISHED'}\n\n")
            create_menu_func(self._file, self._class_name)
            create_register_func(self._file, self._class_name)
            create_unregister_func(self._file, self._class_name)
            create_main_func(self._file)
        else:
            context.window_manager.clipboard = self._file.getvalue()

        self._file.close()
        
        if self.mode == 'ADDON':
            zip_addon(self._zip_dir)

        self._report_finished()

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")