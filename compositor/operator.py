import bpy

from bpy.types import Node

from ..ntp_operator import NTP_Operator
from ..ntp_node_tree import NTP_NodeTree
from ..utils import *
from io import StringIO
from .node_settings import compositor_node_settings

SCENE_VAR = "scene"
BASE_NAME_VAR = "base_name"
END_NAME_VAR = "end_name"

ntp_vars = {SCENE_VAR, BASE_NAME_VAR, END_NAME_VAR} 

class NTPCompositorOperator(NTP_Operator):
    bl_idname = "node.ntp_compositor"
    bl_label =  "Compositor to Python"
    bl_options = {'REGISTER', 'UNDO'}

    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )
    
    compositor_name: bpy.props.StringProperty(name="Node Group")
    is_scene : bpy.props.BoolProperty(name="Is Scene", description="Blender stores compositing node trees differently for scenes and in groups")

    def __init__(self):
        super().__init__()
        self._settings = compositor_node_settings


    def _create_scene(self, indent: str):
        #TODO: wrap in more general unique name util function
        self._write(f"{indent}# Generate unique scene name\n")
        self._write(f"{indent}{BASE_NAME_VAR} = {str_to_py_str(self.compositor_name)}\n")
        self._write(f"{indent}{END_NAME_VAR} = {BASE_NAME_VAR}\n")
        self._write(f"{indent}if bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
        self._write(f"{indent}\ti = 1\n")
        self._write(f"{indent}\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
        self._write(f"{indent}\twhile bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
        self._write(f"{indent}\t\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
        self._write(f"{indent}\t\ti += 1\n\n")

        self._write(f"{indent}{SCENE_VAR} = bpy.context.window.scene.copy()\n\n") 
        self._write(f"{indent}{SCENE_VAR}.name = {END_NAME_VAR}\n")
        self._write(f"{indent}{SCENE_VAR}.use_fake_user = True\n")
        self._write(f"{indent}bpy.context.window.scene = {SCENE_VAR}\n")

    def _initialize_compositor_node_tree(self, outer, ntp_nt, nt_name):
        #initialize node group
        self._write(f"{outer}#initialize {nt_name} node group\n")
        self._write(f"{outer}def {ntp_nt.var}_node_group():\n")

        inner = f"{outer}\t"
        if ntp_nt.node_tree == self._base_node_tree:
            self._write(f"{inner}{ntp_nt.var} = {SCENE_VAR}.node_tree\n")
            self._write(f"{inner}#start with a clean node tree\n")
            self._write(f"{inner}for node in {ntp_nt.var}.nodes:\n")
            self._write(f"{inner}\t{ntp_nt.var}.nodes.remove(node)\n")
        else:
            self._write((f"{inner}{ntp_nt.var}"
                         f"= bpy.data.node_groups.new("
                         f"type = \'CompositorNodeTree\', "
                         f"name = {str_to_py_str(nt_name)})\n"))
            self._write("\n")

    def _process_node(self, node: Node, ntp_nt: NTP_NodeTree, inner: str):
        node_var: str = self._create_node(node, inner, ntp_nt.var)
        
        if node.bl_idname == 'CompositorNodeColorBalance':
            if node.correction_method == 'LIFT_GAMMA_GAIN':
                lst = [("correction_method", ST.ENUM),                 
                        ("gain",              ST.COLOR),
                        ("gamma",             ST.COLOR),
                        ("lift",              ST.COLOR)]
            else:
                lst = [("correction_method", ST.ENUM),
                        ("offset",            ST.COLOR),
                        ("offset_basis",      ST.FLOAT),
                        ("power",             ST.COLOR),
                        ("slope",             ST.COLOR)]

            self._settings['CompositorNodeColorBalance'] = lst

        self._set_settings_defaults(node, inner, node_var)
        self._hide_hidden_sockets(node, inner, node_var)

        if node.bl_idname == 'CompositorNodeGroup':
            self._process_group_node_tree(node, node_var, inner)

        if bpy.app.version < (4, 0, 0):
            if node.bl_idname == 'NodeGroupInput' and not ntp_nt.inputs_set:
                self._group_io_settings(node, inner, "input", ntp_nt)
                ntp_nt.inputs_set = True

            elif node.bl_idname == 'NodeGroupOutput' and not ntp_nt.outputs_set:
                self._group_io_settings(node, inner, "output", ntp_nt)
                ntp_nt.outputs_set = True

        self._set_socket_defaults(node, node_var, inner)
    
    def _process_node_tree(self, node_tree, level):
        """
        Generates a Python function to recreate a compositor node tree

        Parameters:
        node_tree (NodeTree): node tree to be recreated
        level (int): number of tabs to use for each line

        """  
        if node_tree == self._base_node_tree:
            nt_var = self._create_var(self.compositor_name)
            nt_name = self.compositor_name
        else:
            nt_var = self._create_var(node_tree.name)
            nt_name = node_tree.name

        outer, inner = make_indents(level)

        ntp_nt = NTP_NodeTree(node_tree, nt_var)
        self._initialize_compositor_node_tree(outer, ntp_nt, nt_name)

        if bpy.app.version >= (4, 0, 0):
            self._tree_interface_settings(inner, ntp_nt)

        #initialize nodes
        self._write(f"{inner}#initialize {nt_var} nodes\n")

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt, inner)

        self._set_parents(node_tree, inner)
        self._set_locations(node_tree, inner)
        self._set_dimensions(node_tree, inner)
        
        self._init_links(node_tree, inner, nt_var)
        
        self._write(f"{inner}return {nt_var}\n")

        self._write(f"\n{outer}{nt_var} = {nt_var}_node_group()\n\n")
        self._node_trees[node_tree] = nt_var
    
    def execute(self, context):
        #find node group to replicate
        if self.is_scene:
            self._base_node_tree = bpy.data.scenes[self.compositor_name].node_tree
        else:
            self._base_node_tree = bpy.data.node_groups[self.compositor_name]

        if self._base_node_tree is None:
            #shouldn't happen
            self.report({'ERROR'},("NodeToPython: This doesn't seem to be a "
                                   "valid compositor node tree. Is Use Nodes "
                                   "selected?"))
            return {'CANCELLED'}

        #set up names to use in generated addon
        comp_var = clean_string(self.compositor_name)
        
        if self.mode == 'ADDON':
            self._setup_addon_directories(context, comp_var)

            self._file = open(f"{self._addon_dir}/__init__.py", "w")

            self._create_header(self.compositor_name)
            self._class_name = clean_string(self.compositor_name, lower=False)
            self._init_operator(comp_var, self.compositor_name)

            self._write("\tdef execute(self, context):\n")
        else:
            self._file = StringIO("")

        if self.is_scene:
            if self.mode == 'ADDON':
                self._create_scene("\t\t")
            elif self.mode == 'SCRIPT':
                self._create_scene("")
    
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0

        node_trees_to_process = self._topological_sort(self._base_node_tree)

        for node_tree in node_trees_to_process:  
            self._process_node_tree(node_tree, level)

        if self.mode == 'ADDON':
            self._write("\t\treturn {'FINISHED'}\n\n")

            self._create_menu_func()
            self._create_register_func()
            self._create_unregister_func()
            self._create_main_func()
        else:
            context.window_manager.clipboard = self._file.getvalue()

        self._file.close()
        
        if self.mode == 'ADDON':
            self._zip_addon()
        
        self._report_finished("compositor nodes")

        return {'FINISHED'}