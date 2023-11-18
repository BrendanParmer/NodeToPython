import bpy
import os

from bpy.types import Node

from ..NTP_Operator import NTP_Operator
from .node_tree import NTP_CompositorNodeTree
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
        self._file.write(f"{indent}# Generate unique scene name\n")
        self._file.write(f"{indent}{BASE_NAME_VAR} = {str_to_py_str(self.compositor_name)}\n")
        self._file.write(f"{indent}{END_NAME_VAR} = {BASE_NAME_VAR}\n")
        self._file.write(f"{indent}if bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
        self._file.write(f"{indent}\ti = 1\n")
        self._file.write(f"{indent}\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
        self._file.write(f"{indent}\twhile bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
        self._file.write(f"{indent}\t\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
        self._file.write(f"{indent}\t\ti += 1\n\n")

        self._file.write(f"{indent}{SCENE_VAR} = bpy.context.window.scene.copy()\n\n") 
        self._file.write(f"{indent}{SCENE_VAR}.name = {END_NAME_VAR}\n")
        self._file.write(f"{indent}{SCENE_VAR}.use_fake_user = True\n")
        self._file.write(f"{indent}bpy.context.window.scene = {SCENE_VAR}\n")

    def _initialize_compositor_node_tree(self, outer, nt_var, level, inner, nt_name):
                #initialize node group
        self._file.write(f"{outer}#initialize {nt_var} node group\n")
        self._file.write(f"{outer}def {nt_var}_node_group():\n")

        if self._is_outermost_node_group(level): #outermost node group
            self._file.write(f"{inner}{nt_var} = {SCENE_VAR}.node_tree\n")
            self._file.write(f"{inner}#start with a clean node tree\n")
            self._file.write(f"{inner}for node in {nt_var}.nodes:\n")
            self._file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
        else:
            self._file.write((f"{inner}{nt_var}"
                    f"= bpy.data.node_groups.new("
                    f"type = \'CompositorNodeTree\', "
                    f"name = {str_to_py_str(nt_name)})\n"))
            self._file.write("\n")

    def _process_node(self, node: Node, ntp_nt: NTP_CompositorNodeTree, inner: str, level: int):
        if node.bl_idname == 'CompositorNodeGroup':
            node_nt = node.node_tree
            if node_nt is not None and node_nt not in self._node_trees:
                self._process_comp_node_group(node_nt, level + 1, self._node_vars, 
                                        self._used_vars)
                self._node_trees.add(node_nt)
        
        node_var: str = create_node(node, self._file, inner, ntp_nt.var, self._node_vars, 
                                self._used_vars)
        
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

            compositor_node_settings['CompositorNodeColorBalance'] = lst

        set_settings_defaults(node, compositor_node_settings, self._file, 
                                self._addon_dir, inner, node_var)
        hide_hidden_sockets(node, self._file, inner, node_var)

        if node.bl_idname == 'CompositorNodeGroup':
            if node.node_tree is not None:
                self._file.write((f"{inner}{node_var}.node_tree = "
                            f"bpy.data.node_groups"
                            f"[\"{node.node_tree.name}\"]\n"))
        elif node.bl_idname == 'NodeGroupInput' and not inputs_set:
            group_io_settings(node, self._file, inner, "input", ntp_nt.var, ntp_nt.node_tree)
            inputs_set = True

        elif node.bl_idname == 'NodeGroupOutput' and not outputs_set:
            group_io_settings(node, self._file, inner, "output", ntp_nt.var, ntp_nt.node_tree)
            outputs_set = True

        self._set_socket_defaults(node, node_var, inner)
    
    def _process_node_tree(self, node_tree, level):
        """
        Generates a Python function to recreate a compositor node tree

        Parameters:
        node_tree (NodeTree): node tree to be recreated
        level (int): number of tabs to use for each line

        """  
        if self._is_outermost_node_group(level):
            nt_var = create_var(self.compositor_name, self._used_vars)
            nt_name = self.compositor_name
        else:
            nt_var = create_var(node_tree.name, self._used_vars)
            nt_name = node_tree.name

        outer, inner = make_indents(level)

        self._initialize_compositor_node_tree(outer, nt_var, level, inner, nt_name)
        
        ntp_nt = NTP_CompositorNodeTree(node_tree, nt_var)

        #initialize nodes
        self._file.write(f"{inner}#initialize {nt_var} nodes\n")

        for node in node_tree.nodes:
            self._process_node(node, ntp_nt, inner, level)

        set_parents(node_tree, self._file, inner, self._node_vars)
        set_locations(node_tree, self._file, inner, self._node_vars)
        set_dimensions(node_tree, self._file, inner, self._node_vars)
        
        init_links(node_tree, self._file, inner, nt_var, self._node_vars)
        
        self._file.write(f"\n{outer}{nt_var}_node_group()\n\n")
    
    def execute(self, context):
        #find node group to replicate
        if self.is_scene:
            nt = bpy.data.scenes[self.compositor_name].node_tree
        else:
            nt = bpy.data.node_groups[self.compositor_name]

        if nt is None:
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

            create_header(self._file, self.compositor_name)
            class_name = clean_string(self.compositor_name, lower=False)
            init_operator(self._file, class_name, comp_var, self.compositor_name)

            self._file.write("\tdef execute(self, context):\n")
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
        self._process_node_tree(nt, level)

        if self.mode == 'ADDON':
            self._file.write("\t\treturn {'FINISHED'}\n\n")

            create_menu_func(self._file, class_name)
            create_register_func(self._file, class_name)
            create_unregister_func(self._file, class_name)
            create_main_func(self._file)
        else:
            context.window_manager.clipboard = self._file.getvalue()

        self._file.close()
        
        if self.mode == 'ADDON':
            zip_addon(self._zip_dir)
        
        self._report_finished("compositor nodes")

        return {'FINISHED'}