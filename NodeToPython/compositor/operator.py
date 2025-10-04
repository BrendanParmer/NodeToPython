import bpy

from bpy.types import Node, CompositorNodeColorBalance, CompositorNodeTree

from ..ntp_operator import NTP_Operator, INDEX
from ..ntp_node_tree import NTP_NodeTree
from ..utils import *
from ..node_settings import NTPNodeSetting, ST
from io import StringIO
from ..node_settings import node_settings

SCENE = "scene"
BASE_NAME = "base_name"
END_NAME = "end_name"
NODE = "node"

COMP_OP_RESERVED_NAMES = {SCENE, BASE_NAME, END_NAME, NODE} 

class NTP_OT_Compositor(NTP_Operator):
    bl_idname = "ntp.compositor"
    bl_label =  "Compositor to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    compositor_name: bpy.props.StringProperty(name="Node Group")
    is_scene : bpy.props.BoolProperty(
        name="Is Scene", 
        description="Blender stores compositing node trees differently for scenes and in groups")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node_infos = node_settings
        for name in COMP_OP_RESERVED_NAMES:
            self._used_vars[name] = 0


    def _create_scene(self, indent_level: int):
        #TODO: wrap in more general unique name util function
        self._write(f"# Generate unique scene name", indent_level)
        self._write(f"{BASE_NAME} = {str_to_py_str(self.compositor_name)}",
                    indent_level)
        self._write(f"{END_NAME} = {BASE_NAME}", indent_level)
        self._write(f"if bpy.data.scenes.get({END_NAME}) is not None:", indent_level)

        self._write(f"{INDEX} = 1", indent_level + 1)
        self._write(f"{END_NAME} = {BASE_NAME} + f\".{{i:03d}}\"", 
                    indent_level + 1)
        self._write(f"while bpy.data.scenes.get({END_NAME}) is not None:",
                    indent_level + 1)
        
        self._write(f"{END_NAME} = {BASE_NAME} + f\".{{{INDEX}:03d}}\"", 
                    indent_level + 2)
        self._write(f"{INDEX} += 1\n", indent_level + 2)

        self._write(f"{SCENE} = bpy.context.window.scene.copy()\n", indent_level) 
        self._write(f"{SCENE}.name = {END_NAME}", indent_level)
        self._write(f"{SCENE}.use_fake_user = True", indent_level)
        self._write(f"bpy.context.window.scene = {SCENE}", indent_level)
        self._write("", 0)

    def _initialize_compositor_node_tree(self, ntp_nt, nt_name):
        #initialize node group
        self._write(f"def {ntp_nt.var}_node_group():", self._outer_indent_level)
        self._write(f'"""Initialize {nt_name} node group"""')

        if ntp_nt.node_tree == self._base_node_tree and self.is_scene:
            self._write(f"{ntp_nt.var} = {SCENE}.node_tree")
            self._write("", 0)
            self._write(f"# Start with a clean node tree")
            self._write(f"for {NODE} in {ntp_nt.var}.nodes:")
            self._write(f"{ntp_nt.var}.nodes.remove({NODE})", self._inner_indent_level + 1)
        else:
            self._write((f"{ntp_nt.var} = bpy.data.node_groups.new("
                         f"type = \'CompositorNodeTree\', "
                         f"name = {str_to_py_str(nt_name)})"))
            self._write("", 0)

        # Compositor node tree settings
        #TODO: might be good to make this optional
        enum_settings = ["chunk_size", "edit_quality", "execution_mode",
                         "precision", "render_quality"]
        for enum in enum_settings:
            if not hasattr(ntp_nt.node_tree, enum):
                continue
            setting = getattr(ntp_nt.node_tree, enum)
            if setting != None and setting != "":
                py_str = enum_to_py_str(setting)
                self._write(f"{ntp_nt.var}.{enum} = {py_str}")
        
        bool_settings = ["use_groupnode_buffer", "use_opencl", "use_two_pass",
                         "use_viewer_border"]
        for bool_setting in bool_settings:
            if not hasattr(ntp_nt.node_tree, bool_setting):
                continue
            if getattr(ntp_nt.node_tree, bool_setting) is True:
                self._write(f"{ntp_nt.var}.{bool_setting} = True")
        

    if bpy.app.version < (4, 5, 0):
        def _set_color_balance_settings(self, node: CompositorNodeColorBalance
                                    ) -> None:
            """
            Sets the color balance settings so we only set the active variables,
            preventing conflict

            node (CompositorNodeColorBalance): the color balance node
            """
            if node.correction_method == 'LIFT_GAMMA_GAIN':
                lst = [NTPNodeSetting("correction_method", ST.ENUM),                 
                    NTPNodeSetting("gain",  ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("gain",  ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0)),
                    NTPNodeSetting("gamma", ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("gamma", ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0)),
                    NTPNodeSetting("lift",  ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("lift",  ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0))]
            elif node.correction_method == 'OFFSET_POWER_SLOPE':
                lst = [NTPNodeSetting("correction_method", ST.ENUM),
                    NTPNodeSetting("offset", ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("offset", ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0)),
                    NTPNodeSetting("offset_basis", ST.FLOAT),
                    NTPNodeSetting("power", ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("power", ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0)),
                    NTPNodeSetting("slope", ST.VEC3,  max_version_=(3, 5, 0)),
                    NTPNodeSetting("slope", ST.COLOR, min_version_=(3, 5, 0), max_version_=(4, 5, 0))]
            elif node.correction_method == 'WHITEPOINT':
                lst = [NTPNodeSetting("correction_method", ST.ENUM, max_version_=(4, 5, 0)),
                    NTPNodeSetting("input_temperature", ST.FLOAT, max_version_=(4, 5, 0)),
                    NTPNodeSetting("input_tint", ST.FLOAT, max_version_=(4, 5, 0)),
                    NTPNodeSetting("output_temperature", ST.FLOAT, max_version_=(4, 5, 0)),
                    NTPNodeSetting("output_tint", ST.FLOAT, max_version_=(4, 5, 0))]
            else:
                self.report({'ERROR'},
                            f"Unknown color balance correction method "
                            f"{enum_to_py_str(node.correction_method)}")
                return

            color_balance_info = self._node_infos['CompositorNodeColorBalance']
            self._node_infos['CompositorNodeColorBalance'] = color_balance_info._replace(attributes_ = lst)

    def _process_node(self, node: Node, ntp_nt: NTP_NodeTree):
        """
        Create node and set settings, defaults, and cosmetics

        Parameters:
        node (Node): node to process
        ntp_nt (NTP_NodeTree): the node tree that node belongs to
        """
        node_var: str = self._create_node(node, ntp_nt.var)
        
        if bpy.app.version < (4, 5, 0):
            if node.bl_idname == 'CompositorNodeColorBalance':
                self._set_color_balance_settings(node)

        self._set_settings_defaults(node)
        self._hide_hidden_sockets(node)

        if bpy.app.version < (4, 0, 0):
            if node.bl_idname == 'NodeGroupInput' and not ntp_nt.inputs_set:
                self._group_io_settings(node, "input", ntp_nt)
                ntp_nt.inputs_set = True

            elif node.bl_idname == 'NodeGroupOutput' and not ntp_nt.outputs_set:
                self._group_io_settings(node, "output", ntp_nt)
                ntp_nt.outputs_set = True

        self._set_socket_defaults(node)
    
    def _process_node_tree(self, node_tree: CompositorNodeTree):
        """
        Generates a Python function to recreate a compositor node tree

        Parameters:
        node_tree (CompositorNodeTree): node tree to be recreated
        """  
        if node_tree == self._base_node_tree:
            nt_var = self._create_var(self.compositor_name)
            nt_name = self.compositor_name
        else:
            nt_var = self._create_var(node_tree.name)
            nt_name = node_tree.name

        self._node_tree_vars[node_tree] = nt_var

        ntp_nt = NTP_NodeTree(node_tree, nt_var)
        self._initialize_compositor_node_tree(ntp_nt, nt_name)

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
        
        self._write(f"return {nt_var}\n")
        if self._mode == 'SCRIPT':
            self._write("", 0)

        #create node group
        self._write(f"{nt_var} = {nt_var}_node_group()\n", self._outer_indent_level)
    
    def execute(self, context):
        if not self._setup_options(context.scene.ntp_options):
            return {'CANCELLED'}

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
        
        if self._mode == 'ADDON':
            self._outer_indent_level = 2
            self._inner_indent_level = 3

            if not self._setup_addon_directories(context, comp_var):
                return {'CANCELLED'}

            self._file = open(f"{self._addon_dir}/__init__.py", "w")

            self._create_header(self.compositor_name)
            self._class_name = clean_string(self.compositor_name, lower=False)
            self._init_operator(comp_var, self.compositor_name)

            self._write("def execute(self, context):", 1)
        else:
            self._file = StringIO("")
            if self._include_imports:
                self._file.write("import bpy\nimport mathutils\n\n\n")

        if self.is_scene:
            if self._mode == 'ADDON':
                self._create_scene(2)
            elif self._mode == 'SCRIPT':
                self._create_scene(0)
                self._write("", 0)

        node_trees_to_process = self._topological_sort(self._base_node_tree)

        for node_tree in node_trees_to_process:  
            self._process_node_tree(node_tree)

        if self._mode == 'ADDON':
            self._write("return {'FINISHED'}\n", self._outer_indent_level)

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
        
        self._report_finished("compositor nodes")

        return {'FINISHED'}
    
classes: list[type] = [
    NTP_OT_Compositor
]