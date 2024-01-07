import bpy
from bpy.types import Context, Operator
from bpy.types import Node, NodeTree

if bpy.app.version < (4, 0, 0):
    from bpy.types import NodeSocketInterface

import os
from typing import TextIO

from .ntp_node_tree import NTP_NodeTree
from .utils import *


class NTP_Operator(Operator):
    """
    "Abstract" base class for all NTP operators. Blender types and abstraction
    don't seem to mix well, but this should only be inherited from
    """

    bl_idname = ""
    bl_label = ""

    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )

    #node tree input sockets that have default properties
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

    def __init__(self):
        super().__init__()

        # File (TextIO) or string (StringIO) the add-on/script is generated into
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
        self._node_trees: set[NodeTree] = set()

        # Dictionary to keep track of node->variable name pairs
        self._node_vars: dict[Node, str] = {}

        # Dictionary to keep track of variables->usage count pairs
        self._used_vars: dict[str, int] = {}

        # Dictionary used for setting node properties
        self._settings: dict[str, list[(str, ST)]] = {}

    def _write(self, string: str):
        self._file.write(string)

    def _setup_addon_directories(self, context: Context, nt_var: str) -> None:
        """
        Finds/creates directories to save add-on to
        """
        # find base directory to save new addon
        self._dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
        if not self._dir or self._dir == "":
            self.report({'ERROR'},
                        ("NodeToPython: Save your blend file before using "
                         "NodeToPython!"))  # TODO: Still valid??
            return {'CANCELLED'}  # TODO

        self._zip_dir = os.path.join(self._dir, nt_var)
        self._addon_dir = os.path.join(self._zip_dir, nt_var)

        if not os.path.exists(self._addon_dir):
            os.makedirs(self._addon_dir)

    def _create_header(self, name: str) -> None:
        """
        Sets up the bl_info and imports the Blender API

        Parameters:
        file (TextIO): the file for the generated add-on
        name (str): name of the add-on
        """

        self._write("bl_info = {\n")
        self._write(f"\t\"name\" : \"{name}\",\n")
        self._write("\t\"author\" : \"Node To Python\",\n")
        self._write("\t\"version\" : (1, 0, 0),\n")
        self._write(f"\t\"blender\" : {bpy.app.version},\n")
        self._write("\t\"location\" : \"Object\",\n")  # TODO
        self._write("\t\"category\" : \"Node\"\n")
        self._write("}\n")
        self._write("\n")
        self._write("import bpy\n")
        self._write("import mathutils\n")
        self._write("import os\n")
        self._write("\n")

    def _init_operator(self, idname: str, label: str) -> None:
        """
        Initializes the add-on's operator 

        Parameters:
        file (TextIO): the file for the generated add-on
        name (str): name for the class
        idname (str): name for the operator
        label (str): appearence inside Blender
        """
        self._write(f"class {self._class_name}(bpy.types.Operator):\n")
        self._write(f"\tbl_idname = \"object.{idname}\"\n")
        self._write(f"\tbl_label = \"{label}\"\n")
        self._write("\tbl_options = {\'REGISTER\', \'UNDO\'}\n")
        self._write("\n")

    def _is_outermost_node_group(self, level: int) -> bool:
        if self.mode == 'ADDON' and level == 2:
            return True
        elif self.mode == 'SCRIPT' and level == 0:
            return True
        return False

    def _process_group_node_tree(self, node: Node, node_var: str, level: int,
                                 inner: str) -> None:
        """
        Processes node tree of group node if one is present
        """
        node_tree = node.node_tree
        if node_tree is not None:
            if node_tree not in self._node_trees:
                self._process_node_tree(node_tree, level + 1)
                self._node_trees.add(node_tree)
            self._write((f"{inner}{node_var}.node_tree = bpy.data.node_groups"
                         f"[\"{node.node_tree.name}\"]\n"))

    def _create_var(self, name: str) -> str:
        """
        Creates a unique variable name for a node tree

        Parameters:
        name (str): basic string we'd like to create the variable name out of
        used_vars (dict[str, int]): dictionary containing variable names and usage counts

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

    def _create_node(self, node: Node, inner: str, node_tree_var: str) -> str:
        """
        Initializes a new node with location, dimension, and label info

        Parameters:
        node (bpy.types.Node): node to be copied
        inner (str): indentation level for this logic
        node_tree_var (str): variable name for the node tree
        Returns:
        node_var (str): variable name for the node
        """

        self._write(f"{inner}#node {node.name}\n")

        node_var = self._create_var(node.name)
        self._node_vars[node] = node_var

        self._write((f"{inner}{node_var} "
                    f"= {node_tree_var}.nodes.new(\"{node.bl_idname}\")\n"))
        # label
        if node.label:
            self._write(f"{inner}{node_var}.label = \"{node.label}\"\n")

        # name
        self._write(f"{inner}{node_var}.name = \"{node.name}\"\n")

        # color
        if node.use_custom_color:
            self._write(f"{inner}{node_var}.use_custom_color = True\n")
            self._write(
                f"{inner}{node_var}.color = {vec3_to_py_str(node.color)}\n")

        # mute
        if node.mute:
            self._write(f"{inner}{node_var}.mute = True\n")

        return node_var

    def _set_settings_defaults(self, node: Node, inner: str, node_var: str
                               ) -> None:
        """
        Sets the defaults for any settings a node may have

        Parameters:
        node (bpy.types.Node): the node object we're copying settings from
        inner (str): indentation
        node_var (str): name of the variable we're using for the node in our add-on
        """
        if node.bl_idname not in self._settings:
            print((f"NodeToPython: couldn't find {node.bl_idname} in settings."
                   f"Your Blender version may not be supported"))
            return

        for (attr_name, type) in self._settings[node.bl_idname]:
            attr = getattr(node, attr_name, None)
            if attr is None:
                print(f"\"{node_var}.{attr_name}\" not found")
                continue
            setting_str = f"{inner}{node_var}.{attr_name}"
            if type == ST.ENUM:
                if attr != '':
                    self._write(f"{setting_str} = {enum_to_py_str(attr)}\n")
            elif type == ST.ENUM_SET:
                self._write(f"{setting_str} = {attr}\n")
            elif type == ST.STRING:
                self._write(f"{setting_str} = {str_to_py_str(attr)}\n")
            elif type == ST.BOOL or type == ST.INT or type == ST.FLOAT:
                self._write(f"{setting_str} = {attr}\n")
            elif type == ST.VEC1:
                self._write(f"{setting_str} = {vec1_to_py_str(attr)}\n")
            elif type == ST.VEC2:
                self._write(f"{setting_str} = {vec2_to_py_str(attr)}\n")
            elif type == ST.VEC3:
                self._write(f"{setting_str} = {vec3_to_py_str(attr)}\n")
            elif type == ST.VEC4:
                self._write(f"{setting_str} = {vec4_to_py_str(attr)}\n")
            elif type == ST.COLOR:
                self._write(f"{setting_str} = {color_to_py_str(attr)}\n")
            elif type == ST.MATERIAL:
                name = str_to_py_str(attr.name)
                self._write((f"{inner}if {name} in bpy.data.materials:\n"))
                self._write((f"{inner}\t{node_var}.{attr_name} = "
                             f"bpy.data.materials[{name}]\n"))
            elif type == ST.OBJECT:
                name = str_to_py_str(attr.name)
                self._write((f"{inner}if {name} in bpy.data.objects:\n"))
                self._write((f"{inner}\t{node_var}.{attr_name} = "
                             f"bpy.data.objects[{name}]\n"))
            elif type == ST.COLOR_RAMP:
                self._color_ramp_settings(node, inner, node_var, attr_name)
            elif type == ST.CURVE_MAPPING:
                self._curve_mapping_settings(node, inner, node_var, attr_name)
            elif type == ST.IMAGE:
                if self._addon_dir is not None and attr is not None:
                    if attr.source in {'FILE', 'GENERATED', 'TILED'}:
                        self._save_image(attr)
                        self._load_image(
                            attr, inner, f"{node_var}.{attr_name}")
            elif type == ST.IMAGE_USER:
                self._image_user_settings(
                    attr, inner, f"{node_var}.{attr_name}")

    if bpy.app.version < (4, 0, 0):
        def _set_group_socket_default_v3(self, socket_interface: NodeSocketInterface,
                                         inner: str, socket_var: str) -> None:
            """
            Set a node group input/output's default properties if they exist

            Parameters:
            socket_interface (NodeSocketInterface): socket interface associated
                with the input/output
            inner (str): indentation string
            socket_var (str): variable name for the socket
            """
            if socket_interface.type not in self.default_sockets_v3:
                return

            if socket_interface.type == 'RGBA':
                dv = vec4_to_py_str(socket_interface.default_value)
            elif socket_interface.type == 'VECTOR':
                dv = vec3_to_py_str(socket_interface.default_value)
            else:
                dv = socket_interface.default_value
            self._write(f"{inner}{socket_var}.default_value = {dv}\n")

            # min value
            if hasattr(socket_interface, "min_value"):
                min_val = socket_interface.min_value
                self._write(f"{inner}{socket_var}.min_value = {min_val}\n")
            # max value
            if hasattr(socket_interface, "min_value"):
                max_val = socket_interface.max_value
                self._write((f"{inner}{socket_var}.max_value = {max_val}\n"))

        def _group_io_settings_v3(self, node: bpy.types.Node, inner: str,
                            io: str,  # TODO: convert to enum
                            ntp_node_tree: NTP_NodeTree) -> None:
            """
            Set the settings for group input and output sockets

            Parameters:
            node (bpy.types.Node) : group input/output node
            inner (str): indentation string
            io (str): whether we're generating the input or output settings
            node_tree_var (str): variable name of the generated node tree
            node_tree (bpy.types.NodeTree): node tree that we're generating 
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

            self._write(f"{inner}#{node_tree_var} {io}s\n")
            for i, inout in enumerate(io_sockets):
                if inout.bl_idname == 'NodeSocketVirtual':
                    continue
                self._write(f"{inner}#{io} {inout.name}\n")
                idname = enum_to_py_str(inout.bl_idname)
                name = str_to_py_str(inout.name)
                self._write(
                    f"{inner}{node_tree_var}.{io}s.new({idname}, {name})\n")
                socket_interface = io_socket_interfaces[i]
                socket_var = f"{node_tree_var}.{io}s[{i}]"

                self._set_group_socket_default_v3(socket_interface, inner, 
                                                  socket_var)

                # default attribute name
                if hasattr(socket_interface, "default_attribute_name"):
                    if socket_interface.default_attribute_name != "":
                        dan = str_to_py_str(
                            socket_interface.default_attribute_name)
                        self._write((f"{inner}{socket_var}"
                                    f".default_attribute_name = {dan}\n"))

                # attribute domain
                if hasattr(socket_interface, "attribute_domain"):
                    ad = enum_to_py_str(socket_interface.attribute_domain)
                    self._write(f"{inner}{socket_var}.attribute_domain = {ad}\n")

                # tooltip
                if socket_interface.description != "":
                    description = str_to_py_str(socket_interface.description)
                    self._write(
                        (f"{inner}{socket_var}.description = {description}\n"))

                # hide_value
                if socket_interface.hide_value is True:
                    self._write(f"{inner}{socket_var}.hide_value = True\n")

                # hide in modifier
                if hasattr(socket_interface, "hide_in_modifier"):
                    if socket_interface.hide_in_modifier is True:
                        self._write(
                            f"{inner}{socket_var}.hide_in_modifier = True\n")

                self._write("\n")
            self._write("\n")
    
    elif bpy.app.version >= (4, 0, 0):
        def _set_group_socket_default_v4(self, socket_interface: bpy.types.NodeTreeInterfaceSocket,
                                         inner: str, socket_var: str) -> None:
            """
            Set a node group input/output's default properties if they exist

            Parameters:
            socket_interface (NodeTreeInterfaceSocket): socket interface associated
                with the input/output
            inner (str): indentation string
            socket_var (str): variable name for the socket
            """
            if type(socket_interface) in self.nondefault_sockets_v4:
                return

            dv = socket_interface.default_value

            if type(socket_interface) == bpy.types.NodeTreeInterfaceSocketColor:
                dv = vec4_to_py_str(dv)
            elif type(dv) in {mathutils.Vector, mathutils.Euler}:
                dv = vec3_to_py_str(dv)
            elif type(dv) == str:
                dv = str_to_py_str(dv)
            self._write(f"{inner}{socket_var}.default_value = {dv}\n")

            # min value
            if hasattr(socket_interface, "min_value"):
                min_val = socket_interface.min_value
                self._write(f"{inner}{socket_var}.min_value = {min_val}\n")
            # max value
            if hasattr(socket_interface, "min_value"):
                max_val = socket_interface.max_value
                self._write((f"{inner}{socket_var}.max_value = {max_val}\n"))

        def _group_io_settings_v4(self, node: bpy.types.Node, inner: str,
                            io: str,  # TODO: convert to enum
                            ntp_node_tree: NTP_NodeTree) -> None:
            """
            Set the settings for group input and output sockets

            Parameters:
            node (bpy.types.Node) : group input/output node
            inner (str): indentation string
            io (str): whether we're generating the input or output settings
            node_tree_var (str): variable name of the generated node tree
            node_tree (bpy.types.NodeTree): node tree that we're generating 
                input and output settings for
            """
            node_tree_var = ntp_node_tree.var
            node_tree = ntp_node_tree.node_tree

            if io == "input":
                io_sockets = node.outputs # Might be removeable,
                # think we can get all the info from the inouts
                # from the socket interfaces, need to double check.
                # If so, then we can just run these at the initialization
                # of the node tree, meaning we can clean up the clunky
                # Group Input/Group Output node reliance, two calls
                # Should be pretty easy to add in panels afterwards,
                # looks like those are tied fairly close to the new socket
                # system
                items_tree = node_tree.interface.items_tree
                io_socket_interfaces = [item for item in items_tree 
                                        if item.item_type == 'SOCKET' 
                                        and item.in_out == 'INPUT']
            else:
                io_sockets = node.inputs
                items_tree = node_tree.interface.items_tree
                io_socket_interfaces = [item for item in items_tree 
                                        if item.item_type == 'SOCKET' 
                                        and item.in_out == 'OUTPUT']

            self._write(f"{inner}#{node_tree_var} {io}s\n")
            for i, socket_interface in enumerate(io_socket_interfaces):
                self._write(f"{inner}#{io} {socket_interface.name}\n")
            
                socket_interface: bpy.types.NodeTreeInterfaceSocket = io_socket_interfaces[i]

                #initialization
                socket_var = clean_string(socket_interface.name) + "_socket"
                name = str_to_py_str(socket_interface.name)
                in_out_enum = enum_to_py_str(socket_interface.in_out)

                socket_type = enum_to_py_str(socket_interface.bl_socket_idname)
                """
                I might be missing something, but the Python API's set up a bit 
                weird here now. The new socket initialization only accepts types
                from a list of basic ones, but there doesn't seem to be a way of
                retrieving just this basic typewithout the subtype information.
                """
                if 'Float' in socket_type:
                    socket_type = enum_to_py_str('NodeSocketFloat')
                elif 'Int' in socket_type:
                    socket_type = enum_to_py_str('NodeSocketInt')
                elif 'Vector' in socket_type:
                    socket_type = enum_to_py_str('NodeSocketVector')
                

                self._write(f"{inner}{socket_var} = "
                            f"{node_tree_var}.interface.new_socket("
                            f"name = {name}, in_out={in_out_enum}, "
                            f"socket_type = {socket_type})\n")

                #subtype
                if hasattr(socket_interface, "subtype"):
                    subtype = enum_to_py_str(socket_interface.subtype)
                    self._write(f"{inner}{socket_var}.subtype = {subtype}\n")

                    self._set_group_socket_default_v4(socket_interface, inner, 
                                                      socket_var)

                # default attribute name
                if socket_interface.default_attribute_name != "":
                    dan = str_to_py_str(socket_interface.default_attribute_name)
                    self._write((f"{inner}{socket_var}.default_attribute_name = {dan}\n"))

                # attribute domain
                ad = enum_to_py_str(socket_interface.attribute_domain)
                self._write(f"{inner}{socket_var}.attribute_domain = {ad}\n")

                # tooltip
                if socket_interface.description != "":
                    description = str_to_py_str(socket_interface.description)
                    self._write(
                        (f"{inner}{socket_var}.description = {description}\n"))

                # hide_value
                if socket_interface.hide_value is True:
                    self._write(f"{inner}{socket_var}.hide_value = True\n")

                # hide in modifier
                if socket_interface.hide_in_modifier is True:
                    self._write(f"{inner}{socket_var}.hide_in_modifier = True\n")

                #force non field
                if socket_interface.force_non_field is True:
                    self._write(f"{inner}{socket_var}.force_non_field = True\n")

                self._write("\n")
            self._write("\n")

    def _group_io_settings(self, node: bpy.types.Node, inner: str, 
                            io: str,  # TODO: convert to enum
                            ntp_node_tree: NTP_NodeTree) -> None:
        """
        Set the settings for group input and output sockets

        Parameters:
        node (bpy.types.Node) : group input/output node
        inner (str): indentation string
        io (str): whether we're generating the input or output settings
        node_tree_var (str): variable name of the generated node tree
        node_tree (bpy.types.NodeTree): node tree that we're generating 
            input and output settings for
        """
        if bpy.app.version < (4, 0, 0):
            self._group_io_settings_v3(node, inner, io, ntp_node_tree)
        else:
            self._group_io_settings_v4(node, inner, io, ntp_node_tree)

    def _set_input_defaults(self, node: bpy.types.Node, inner: str,
                            node_var: str) -> None:
        """
        Sets defaults for input sockets

        Parameters:
        node (bpy.types.Node): node we're setting inputs for
        inner (str): indentation
        node_var (str): variable name we're using for the copied node
        addon_dir (str): directory of the add-on, for if we need to save other
            objects for the add-on
        """
        if node.bl_idname == 'NodeReroute':
            return

        for i, input in enumerate(node.inputs):
            if input.bl_idname not in dont_set_defaults and not input.is_linked:
                # TODO: this could be cleaner
                socket_var = f"{node_var}.inputs[{i}]"

                # colors
                if input.bl_idname == 'NodeSocketColor':
                    default_val = vec4_to_py_str(input.default_value)

                # vector types
                elif "Vector" in input.bl_idname:
                    default_val = vec3_to_py_str(input.default_value)

                #rotation types
                elif input.bl_idname == 'NodeSocketRotation':
                    default_val = vec3_to_py_str(input.default_value)
                    
                # strings
                elif input.bl_idname == 'NodeSocketString':
                    default_val = str_to_py_str(input.default_value)

                # images
                elif input.bl_idname == 'NodeSocketImage':
                    img = input.default_value
                    if img is not None and self._addon_dir != None:  # write in a better way
                        self._save_image(img)
                        self._load_image(
                            img, inner, f"{socket_var}.default_value")
                    default_val = None

                # materials
                elif input.bl_idname == 'NodeSocketMaterial':
                    self._in_file_inputs(input, inner, socket_var, "materials")
                    default_val = None

                # collections
                elif input.bl_idname == 'NodeSocketCollection':
                    self._in_file_inputs(
                        input, inner, socket_var, "collections")
                    default_val = None

                # objects
                elif input.bl_idname == 'NodeSocketObject':
                    self._in_file_inputs(input, inner, socket_var, "objects")
                    default_val = None

                # textures
                elif input.bl_idname == 'NodeSocketTexture':
                    self._in_file_inputs(input, inner, socket_var, "textures")
                    default_val = None

                else:
                    default_val = input.default_value
                if default_val is not None:
                    self._write(f"{inner}#{input.identifier}\n")
                    self._write((f"{inner}{socket_var}.default_value"
                                f" = {default_val}\n"))
        self._write("\n")

    def _set_output_defaults(self, node: bpy.types.Node,
                             inner: str, node_var: str) -> None:
        """
        Some output sockets need default values set. It's rather annoying

        Parameters:
        node (bpy.types.Node): node for the output we're setting
        inner (str): indentation string
        node_var (str): variable name for the node we're setting output defaults for
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

        dv = node.outputs[0].default_value
        if node.bl_idname in {'ShaderNodeRGB', 'CompositorNodeRGB'}:
            dv = vec4_to_py_str(list(dv))
        if node.bl_idname in {'ShaderNodeNormal', 'CompositorNodeNormal'}:
            dv = vec3_to_py_str(dv)
        self._write((f"{inner}{node_var}.outputs[0].default_value = {dv}\n"))

    def _in_file_inputs(self, input: bpy.types.NodeSocket,
                        inner: str,
                        socket_var: str,
                        type: str
                        ) -> None:
        """
        Sets inputs for a node input if one already exists in the blend file

        Parameters:
        input (bpy.types.NodeSocket): input socket we're setting the value for
        inner (str): indentation string
        socket_var (str): variable name we're using for the socket
        type (str): from what section of bpy.data to pull the default value from
        """

        if input.default_value is None:
            return
        name = str_to_py_str(input.default_value.name)
        self._write(f"{inner}if {name} in bpy.data.{type}:\n")
        self._write((f"{inner}\t{socket_var}.default_value = "
                     f"bpy.data.{type}[{name}]\n"))

    def _color_ramp_settings(self, node: bpy.types.Node,
                             inner: str,
                             node_var: str,
                             color_ramp_name: str) -> None:
        """
        Replicate a color ramp node

        Parameters
        node (bpy.types.Node): node object we're copying settings from
        inner (str): indentation
        node_var (str): name of the variable we're using for the color ramp
        color_ramp_name (str): name of the color ramp to be copied
        """

        color_ramp: bpy.types.ColorRamp = getattr(node, color_ramp_name)
        if not color_ramp:
            raise ValueError(
                f"No color ramp named \"{color_ramp_name}\" found")

        # settings
        ramp_str = f"{inner}{node_var}.{color_ramp_name}"

        color_mode = enum_to_py_str(color_ramp.color_mode)
        self._write(f"{ramp_str}.color_mode = {color_mode}\n")

        hue_interpolation = enum_to_py_str(color_ramp.hue_interpolation)
        self._write((f"{ramp_str}.hue_interpolation = "
                     f"{hue_interpolation}\n"))
        interpolation = enum_to_py_str(color_ramp.interpolation)
        self._write((f"{ramp_str}.interpolation "
                     f"= {interpolation}\n"))
        self._write("\n")

        # key points
        self._write(f"{inner}#initialize color ramp elements\n")
        self._write((f"{ramp_str}.elements.remove"
                    f"({ramp_str}.elements[0])\n"))
        for i, element in enumerate(color_ramp.elements):
            element_var = f"{node_var}_cre_{i}"
            if i == 0:
                self._write(f"{inner}{element_var} = "
                            f"{ramp_str}.elements[{i}]\n")
                self._write(
                    f"{inner}{element_var}.position = {element.position}\n")
            else:
                self._write((f"{inner}{element_var} = "
                             f"{ramp_str}.elements"
                             f".new({element.position})\n"))

            self._write((f"{inner}{element_var}.alpha = "
                         f"{element.alpha}\n"))
            color_str = vec4_to_py_str(element.color)
            self._write((f"{inner}{element_var}.color = {color_str}\n\n"))

    def _curve_mapping_settings(self, node: bpy.types.Node, inner: str,
                                node_var: str, curve_mapping_name: str
                                ) -> None:
        """
        Sets defaults for Float, Vector, and Color curves

        Parameters:
        node (bpy.types.Node): curve node we're copying settings from
        file (TextIO): file we're generating the add-on into
        inner (str): indentation
        node_var (str): variable name for the add-on's curve node
        curve_mapping_name (str): name of the curve mapping to be set
        """

        mapping = getattr(node, curve_mapping_name)
        if not mapping:
            raise ValueError((f"Curve mapping \"{curve_mapping_name}\" not found "
                              f"in node \"{node.bl_idname}\""))

        # mapping settings
        self._write(f"{inner}#mapping settings\n")
        mapping_var = f"{inner}{node_var}.{curve_mapping_name}"

        # extend
        extend = enum_to_py_str(mapping.extend)
        self._write(f"{mapping_var}.extend = {extend}\n")
        # tone
        tone = enum_to_py_str(mapping.tone)
        self._write(f"{mapping_var}.tone = {tone}\n")

        # black level
        b_lvl_str = vec3_to_py_str(mapping.black_level)
        self._write((f"{mapping_var}.black_level = {b_lvl_str}\n"))
        # white level
        w_lvl_str = vec3_to_py_str(mapping.white_level)
        self._write((f"{mapping_var}.white_level = {w_lvl_str}\n"))

        # minima and maxima
        min_x = mapping.clip_min_x
        self._write(f"{mapping_var}.clip_min_x = {min_x}\n")
        min_y = mapping.clip_min_y
        self._write(f"{mapping_var}.clip_min_y = {min_y}\n")
        max_x = mapping.clip_max_x
        self._write(f"{mapping_var}.clip_max_x = {max_x}\n")
        max_y = mapping.clip_max_y
        self._write(f"{mapping_var}.clip_max_y = {max_y}\n")

        # use_clip
        use_clip = mapping.use_clip
        self._write(f"{mapping_var}.use_clip = {use_clip}\n")

        # create curves
        for i, curve in enumerate(mapping.curves):
            # TODO: curve function
            self._write(f"{inner}#curve {i}\n")
            curve_i = f"{node_var}_curve_{i}"
            self._write((f"{inner}{curve_i} = "
                         f"{node_var}.{curve_mapping_name}.curves[{i}]\n"))

            # Remove default points when CurveMap is initialized with more than
            # two points (just CompositorNodeHueCorrect)
            if (node.bl_idname == 'CompositorNodeHueCorrect'):
                self._write((f"{inner}for i in range"
                             f"(len({curve_i}.points.values()) - 1, 1, -1):\n"))
                self._write(
                    f"{inner}\t{curve_i}.points.remove({curve_i}.points[i])\n")

            for j, point in enumerate(curve.points):
                # TODO: point function
                point_j = f"{inner}{curve_i}_point_{j}"

                loc = point.location
                loc_str = f"{loc[0]}, {loc[1]}"
                if j < 2:
                    self._write(f"{point_j} = {curve_i}.points[{j}]\n")
                    self._write(f"{point_j}.location = ({loc_str})\n")
                else:
                    self._write(
                        (f"{point_j} = {curve_i}.points.new({loc_str})\n"))

                handle = enum_to_py_str(point.handle_type)
                self._write(f"{point_j}.handle_type = {handle}\n")

        # update curve
        self._write(f"{inner}#update curve after changes\n")
        self._write(f"{mapping_var}.update()\n")

    def _save_image(self, img: bpy.types.Image) -> None:
        """
        Saves an image to an image directory of the add-on

        Parameters:
        img (bpy.types.Image): image to be saved
        """

        if img is None:
            return

        # create image dir if one doesn't exist
        img_dir = os.path.join(self._addon_dir, IMAGE_DIR_NAME)
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        # save the image
        img_str = img_to_py_str(img)
        img_path = f"{img_dir}/{img_str}"
        if not os.path.exists(img_path):
            img.save_render(img_path)

    def _load_image(self, img: bpy.types.Image,
                    inner: str,
                    img_var: str
                    ) -> None:
        """
        Loads an image from the add-on into a blend file and assigns it

        Parameters:
        img (bpy.types.Image): Blender image from the original node group
        inner (str): indentation string
        img_var (str): variable name to be used for the image
        """

        if img is None:
            return

        img_str = img_to_py_str(img)

        # TODO: convert to special variables
        self._write(f"{inner}#load image {img_str}\n")
        self._write((f"{inner}base_dir = "
                     f"os.path.dirname(os.path.abspath(__file__))\n"))
        self._write((f"{inner}image_path = "
                     f"os.path.join(base_dir, \"{IMAGE_DIR_NAME}\", "
                     f"\"{img_str}\")\n"))
        self._write((f"{inner}{img_var} = bpy.data.images.load"
                     f"(image_path, check_existing = True)\n"))

        # copy image settings
        self._write(f"{inner}#set image settings\n")

        # source
        source = enum_to_py_str(img.source)
        self._write(f"{inner}{img_var}.source = {source}\n")

        # color space settings
        color_space = enum_to_py_str(img.colorspace_settings.name)
        self._write(
            f"{inner}{img_var}.colorspace_settings.name = {color_space}\n")

        # alpha mode
        alpha_mode = enum_to_py_str(img.alpha_mode)
        self._write(f"{inner}{img_var}.alpha_mode = {alpha_mode}\n")

    def _image_user_settings(self, img_user: bpy.types.ImageUser,
                             inner: str,
                             img_user_var: str) -> None:
        """
        Replicate the image user of an image node

        Parameters
        img_usr (bpy.types.ImageUser): image user to be copied
        inner (str): indentation
        img_usr_var (str): variable name for the generated image user
        """

        img_usr_attrs = ["frame_current", "frame_duration", "frame_offset",
                         "frame_start", "tile", "use_auto_refresh", "use_cyclic"]

        for img_usr_attr in img_usr_attrs:
            self._write((f"{inner}{img_user_var}.{img_usr_attr} = "
                         f"{getattr(img_user, img_usr_attr)}\n"))

    def _set_parents(self, node_tree: bpy.types.NodeTree,
                     inner: str) -> None:
        """
        Sets parents for all nodes, mostly used to put nodes in frames

        Parameters:
        node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
        inner (str): indentation string
        """
        parent_comment = False
        for node in node_tree.nodes:
            if node is not None and node.parent is not None:
                if not parent_comment:
                    self._write(f"{inner}#Set parents\n")
                    parent_comment = True
                node_var = self._node_vars[node]
                parent_var = self._node_vars[node.parent]
                self._write(f"{inner}{node_var}.parent = {parent_var}\n")
        self._write("\n")

    def _set_locations(self, node_tree: bpy.types.NodeTree, inner: str) -> None:
        """
        Set locations for all nodes

        Parameters:
        node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
        inner (str): indentation string
        """

        self._write(f"{inner}#Set locations\n")
        for node in node_tree.nodes:
            node_var = self._node_vars[node]
            self._write((f"{inner}{node_var}.location "
                        f"= ({node.location.x}, {node.location.y})\n"))
        self._write("\n")

    def _set_dimensions(self, node_tree: bpy.types.NodeTree, inner: str,
                        ) -> None:
        """
        Set dimensions for all nodes

        Parameters:
        node_tree (bpy.types.NodeTree): node tree we're obtaining nodes from
        inner (str): indentation string
        """
        self._write(f"{inner}#Set dimensions\n")
        for node in node_tree.nodes:
            node_var = self._node_vars[node]
            self._write((f"{inner}{node_var}.width, {node_var}.height "
                         f"= {node.width}, {node.height}\n"))
        self._write("\n")

    def _init_links(self, node_tree: bpy.types.NodeTree,
                    inner: str,
                    node_tree_var: str) -> None:
        """
        Create all the links between nodes

        Parameters:
        node_tree (bpy.types.NodeTree): node tree we're copying
        inner (str): indentation
        node_tree_var (str): variable name we're using for the copied node tree
        """

        if node_tree.links:
            self._write(f"{inner}#initialize {node_tree_var} links\n")
        for link in node_tree.links:
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

            self._write((f"{inner}#{in_node_var}.{input_socket.name} "
                         f"-> {out_node_var}.{output_socket.name}\n"))
            self._write((f"{inner}{node_tree_var}.links.new({in_node_var}"
                         f".outputs[{input_idx}], "
                         f"{out_node_var}.inputs[{output_idx}])\n"))

    def _hide_hidden_sockets(self, node: bpy.types.Node, inner: str,
                             node_var: str) -> None:
        """
        Hide hidden sockets

        Parameters:
        node (bpy.types.Node): node object we're copying socket settings from
        inner (str): indentation string
        node_var (str): name of the variable we're using for this node
        """
        for i, socket in enumerate(node.inputs):
            if socket.hide is True:
                self._write(f"{inner}{node_var}.inputs[{i}].hide = True\n")
        for i, socket in enumerate(node.outputs):
            if socket.hide is True:
                self._write(f"{inner}{node_var}.outputs[{i}].hide = True\n")

    def _set_socket_defaults(self, node: Node, node_var: str, inner: str):
        self._set_input_defaults(node, inner, node_var)
        self._set_output_defaults(node, inner, node_var)

    def _create_menu_func(self) -> None:
        """
        Creates the menu function
        """

        self._write("def menu_func(self, context):\n")
        self._write(f"\tself.layout.operator({self._class_name}.bl_idname)\n")
        self._write("\n")

    def _create_register_func(self) -> None:
        """
        Creates the register function
        """
        self._write("def register():\n")
        self._write(f"\tbpy.utils.register_class({self._class_name})\n")
        self._write("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
        self._write("\n")

    def _create_unregister_func(self) -> None:
        """
        Creates the unregister function
        """
        self._write("def unregister():\n")
        self._write(f"\tbpy.utils.unregister_class({self._class_name})\n")
        self._write("\tbpy.types.VIEW3D_MT_object.remove(menu_func)\n")
        self._write("\n")

    def _create_main_func(self) -> None:
        """
        Creates the main function
        """
        self._write("if __name__ == \"__main__\":\n")
        self._write("\tregister()")

    def _zip_addon(self) -> None:
        """
        Zips up the addon and removes the directory
        """
        shutil.make_archive(self._zip_dir, "zip", self._zip_dir)
        shutil.rmtree(self._zip_dir)

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
        self.report({'INFO'}, f"NodeToPython: Saved {object} to {location}")

    # ABSTRACT
    def execute(self):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")
