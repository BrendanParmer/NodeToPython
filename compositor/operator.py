import bpy
import os

from ..utils import *
from io import StringIO
from .node_settings import compositor_node_settings

SCENE_VAR = "scene"
BASE_NAME_VAR = "base_name"
END_NAME_VAR = "end_name"

ntp_vars = {SCENE_VAR, BASE_NAME_VAR, END_NAME_VAR} 

class NTPCompositorOperator(bpy.types.Operator):
    bl_idname = "node.compositor_to_python"
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
        
        addon_dir = None
        if self.mode == 'ADDON':
            dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
            if not dir or dir == "":
                self.report({'ERROR'},
                            ("NodeToPython: Save your blender file before using "
                            "NodeToPython!"))
                return {'CANCELLED'}

            zip_dir = os.path.join(dir, comp_var)
            addon_dir = os.path.join(zip_dir, comp_var)
            if not os.path.exists(addon_dir):
                os.makedirs(addon_dir)
            file = open(f"{addon_dir}/__init__.py", "w")

            create_header(file, self.compositor_name)
            class_name = clean_string(self.compositor_name, lower=False)
            init_operator(file, class_name, comp_var, self.compositor_name)

            file.write("\tdef execute(self, context):\n")
        else:
            file = StringIO("")

        if self.is_scene:
            def create_scene(indent: str):
                #TODO: wrap in more general unique name util function
                file.write(f"{indent}# Generate unique scene name\n")
                file.write(f"{indent}{BASE_NAME_VAR} = {str_to_py_str(self.compositor_name)}\n")
                file.write(f"{indent}{END_NAME_VAR} = {BASE_NAME_VAR}\n")
                file.write(f"{indent}if bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
                file.write(f"{indent}\ti = 1\n")
                file.write(f"{indent}\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
                file.write(f"{indent}\twhile bpy.data.scenes.get({END_NAME_VAR}) != None:\n")
                file.write(f"{indent}\t\t{END_NAME_VAR} = {BASE_NAME_VAR} + f\".{{i:03d}}\"\n")
                file.write(f"{indent}\t\ti += 1\n\n")

                file.write(f"{indent}{SCENE_VAR} = bpy.context.window.scene.copy()\n\n") 
                file.write(f"{indent}{SCENE_VAR}.name = {END_NAME_VAR}\n")
                file.write(f"{indent}{SCENE_VAR}.use_fake_user = True\n")
                file.write(f"{indent}bpy.context.window.scene = {SCENE_VAR}\n")
            
            if self.mode == 'ADDON':
                create_scene("\t\t")
            elif self.mode == 'SCRIPT':
                create_scene("")
        
        #set to keep track of already created node trees
        node_trees = set()

        #dictionary to keep track of node->variable name pairs
        node_vars = {}

        #keeps track of all used variables
        used_vars = {}

        def is_outermost_node_group(level: int) -> bool:
            if self.mode == 'ADDON' and level == 2:
                return True
            elif self.mode == 'SCRIPT' and level == 0:
                return True
            return False
        
        def process_comp_node_group(node_tree, level, node_vars, used_vars):       
            if is_outermost_node_group(level):
                nt_var = create_var(self.compositor_name, used_vars)
                nt_name = self.compositor_name
            else:
                nt_var = create_var(node_tree.name, used_vars)
                nt_name = node_tree.name

            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {nt_var} node group\n")
            file.write(f"{outer}def {nt_var}_node_group():\n")

            if is_outermost_node_group(level): #outermost node group
                file.write(f"{inner}{nt_var} = {SCENE_VAR}.node_tree\n")
                file.write(f"{inner}#start with a clean node tree\n")
                file.write(f"{inner}for node in {nt_var}.nodes:\n")
                file.write(f"{inner}\t{nt_var}.nodes.remove(node)\n")
            else:
                file.write((f"{inner}{nt_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \'CompositorNodeTree\', "
                        f"name = {str_to_py_str(nt_name)})\n"))
                file.write("\n")
            
            inputs_set = False
            outputs_set = False

            #initialize nodes
            file.write(f"{inner}#initialize {nt_var} nodes\n")

            #dictionary to keep track of node->variable name pairs
            node_vars = {}

            for node in node_tree.nodes:
                if node.bl_idname == 'CompositorNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_comp_node_group(node_nt, level + 1, node_vars, 
                                               used_vars)
                        node_trees.add(node_nt)
                
                node_var = create_node(node, file, inner, nt_var, node_vars, 
                                       used_vars)
                
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

                set_settings_defaults(node, compositor_node_settings, file, 
                                      addon_dir, inner, node_var)
                hide_hidden_sockets(node, file, inner, node_var)

                if node.bl_idname == 'CompositorNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'NodeGroupInput' and not inputs_set:
                    group_io_settings(node, file, inner, "input", nt_var, node_tree)
                    inputs_set = True

                elif node.bl_idname == 'NodeGroupOutput' and not outputs_set:
                    group_io_settings(node, file, inner, "output", nt_var, node_tree)
                    outputs_set = True
                if self.mode == 'ADDON':
                    set_input_defaults(node, file, inner, node_var, addon_dir)
                else:
                    set_input_defaults(node, file, inner, node_var)
                set_output_defaults(node, file, inner, node_var)

            set_parents(node_tree, file, inner, node_vars)
            set_locations(node_tree, file, inner, node_vars)
            set_dimensions(node_tree, file, inner, node_vars)
            
            init_links(node_tree, file, inner, nt_var, node_vars)
            
            file.write(f"\n{outer}{nt_var}_node_group()\n\n")
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0        
        process_comp_node_group(nt, level, node_vars, used_vars)

        if self.mode == 'ADDON':
            file.write("\t\treturn {'FINISHED'}\n\n")

            create_menu_func(file, class_name)
            create_register_func(file, class_name)
            create_unregister_func(file, class_name)
            create_main_func(file)
        else:
            context.window_manager.clipboard = file.getvalue()

        file.close()
        
        if self.mode == 'ADDON':
            zip_addon(zip_dir)
        
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = dir
        self.report({'INFO'}, f"NodeToPython: Saved compositor nodes to {location}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        self.layout.prop(self, "mode")