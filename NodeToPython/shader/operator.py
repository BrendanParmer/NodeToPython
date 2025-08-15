import bpy
from bpy.types import Node
from bpy.types import ShaderNodeTree

from io import StringIO

from ..utils import *
from ..ntp_operator import NTP_Operator
from ..ntp_node_tree import NTP_NodeTree
from ..node_settings import node_settings

MAT_VAR = "mat"
NODE = "node"
SHADER_OP_RESERVED_NAMES = {MAT_VAR, NODE}

class NTPShaderOperator(NTP_Operator):
    bl_idname = "node.ntp_material"
    bl_label =  "Material to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    #TODO: add option for general shader node groups
    material_name: bpy.props.StringProperty(name="Node Group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node_infos = node_settings
        for name in SHADER_OP_RESERVED_NAMES:
            self._used_vars[name] = 0
    
    def _create_material(self, indent_level: int):
        self._write(f"{MAT_VAR} = bpy.data.materials.new("
                    f"name = {str_to_py_str(self.material_name)})", indent_level)
        self._write(f"{MAT_VAR}.use_nodes = True\n\n", indent_level)

    def _initialize_shader_node_tree(self, ntp_node_tree: NTP_NodeTree, 
                                    nt_name: str) -> None:
        """
        Initialize the shader node group

        Parameters:
        ntp_node_tree (NTP_NodeTree): node tree to be generated and 
            variable to use
        nt_name (str): name to use for the node tree
        """
        self._write(f"def {ntp_node_tree.var}_node_group():", self._outer_indent_level)
        self._write(f'"""Initialize {nt_name} node group"""')

        if ntp_node_tree.node_tree == self._base_node_tree:
            self._write(f"{ntp_node_tree.var} = {MAT_VAR}.node_tree\n")
            self._write(f"# Start with a clean node tree")
            self._write(f"for {NODE} in {ntp_node_tree.var}.nodes:")
            self._write(f"{ntp_node_tree.var}.nodes.remove({NODE})", self._inner_indent_level + 1)
        else:
            self._write((f"{ntp_node_tree.var} = bpy.data.node_groups.new("
                         f"type = \'ShaderNodeTree\', "
                         f"name = {str_to_py_str(nt_name)})"))
            self._write("", 0)

    def _process_node(self, node: Node, ntp_nt: NTP_NodeTree) -> None:
        """
        Create node and set settings, defaults, and cosmetics

        Parameters:
        node (Node): node to process
        ntp_nt (NTP_NodeTree): the node tree that node belongs to
        """
        node_var: str = self._create_node(node, ntp_nt.var)
        self._set_settings_defaults(node)
        
        if bpy.app.version < (4, 0, 0):
            if node.bl_idname == 'NodeGroupInput' and not ntp_nt.inputs_set:
                self._group_io_settings(node, "input", ntp_nt)
                ntp_nt.inputs_set = True

            elif node.bl_idname == 'NodeGroupOutput' and not ntp_nt.outputs_set:
                self._group_io_settings(node, "output", ntp_nt)
                ntp_nt.outputs_set = True

        self._hide_hidden_sockets(node)
        self._set_socket_defaults(node)

    def _process_node_tree(self, node_tree: ShaderNodeTree) -> None:
        """
        Generates a Python function to recreate a node tree

        Parameters:
        node_tree (NodeTree): node tree to be recreated
        level (int): number of tabs to use for each line, used with
            node groups within node groups and script/add-on differences
        """

        if node_tree == self._base_node_tree:
            nt_var = self._create_var(self.material_name)
            nt_name = self.material_name #TODO: this is probably overcomplicating things if we move to a harder material vs shader node tree difference
        else:
            nt_var = self._create_var(node_tree.name)
            nt_name = node_tree.name

        self._node_tree_vars[node_tree] = nt_var

        ntp_nt = NTP_NodeTree(node_tree, nt_var)

        self._initialize_shader_node_tree(ntp_nt, nt_name)

        self._set_node_tree_properties(node_tree)
        
        if bpy.app.version >= (4, 0, 0):
            self._tree_interface_settings(ntp_nt)

        #initialize nodes
        self._write(f"# Initialize {nt_var} nodes\n")

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt)

        #set look of nodes
        self._set_parents(node_tree)
        self._set_locations(node_tree)
        self._set_dimensions(node_tree)

        #create connections
        self._init_links(node_tree)
        
        self._write(f"return {nt_var}\n\n")

        #create node group
        self._write(f"{nt_var} = {nt_var}_node_group()\n", self._outer_indent_level)
        

    def execute(self, context):
        if not self._setup_options(context.scene.ntp_options):
            return {'CANCELLED'}
        
        #find node group to replicate
        self._base_node_tree = bpy.data.materials[self.material_name].node_tree
        if self._base_node_tree is None:
            self.report({'ERROR'}, ("NodeToPython: This doesn't seem to be a "
                                    "valid material. Is Use Nodes selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        mat_var = clean_string(self.material_name)
        
        if self._mode == 'ADDON':
            self._outer_indent_level = 2
            self._inner_indent_level = 3

            if not self._setup_addon_directories(context, mat_var):
                return {'CANCELLED'}

            self._file = open(f"{self._addon_dir}/__init__.py", "w")

            self._create_header(self.material_name)
            self._class_name = clean_string(self.material_name, lower=False)
            self._init_operator(mat_var, self.material_name)

            self._write("def execute(self, context):", 1)
        else:
            self._file = StringIO("")
            if self._include_imports:
                self._file.write("import bpy\nimport mathutils\n\n\n")

        if self._mode == 'ADDON':
            self._create_material(2)
        elif self._mode == 'SCRIPT':
            self._create_material(0)   
        
        node_trees_to_process = self._topological_sort(self._base_node_tree)

        for node_tree in node_trees_to_process:
            self._process_node_tree(node_tree)

        if self._mode == 'ADDON':
            self._write("return {'FINISHED'}", self._outer_indent_level)
            self._create_menu_func()
            self._create_register_func()
            self._create_unregister_func()
            self._create_main_func()
            self._create_license()
            if bpy.app.version >= (4, 2, 0):
                self._create_manifest()
        else:
            context.window_manager.clipboard = self._file.getvalue()

        self._file.close()
        
        if self._mode == 'ADDON':
            self._zip_addon()

        self._report_finished("material")

        return {'FINISHED'}