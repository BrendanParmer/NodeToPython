import bpy
import os

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketCollection',
                     'NodeSocketGeometry',
                     'NodeSocketImage',
                     'NodeSocketMaterial',
                     'NodeSocketObject',
                     'NodeSocketTexture',
                     'NodeSocketVirtual'}
        
def execute(self, material_name):
    #validate material name
    if material_name not in bpy.data.materials:
        return {'FINISHED'}
    
    print("_________________________________")
    #set up addon file
    ng = bpy.data.materials[material_name].node_tree
    ng_name = ng.name.lower().replace(' ', '_')
    class_name = ng.name.replace(" ", "")
    """
    dir = bpy.path.abspath("//")
    if not dir or dir == "":
        self.report({'ERROR'},
                    ("NodeToPython: Save your blender file before using "
                     "NodeToPython!"))
        return {'CANCELLED'}
    addon_dir = os.path.join(dir, "addons")
    if not os.path.exists(addon_dir):
        os.mkdir(addon_dir)
    file = open(f"{addon_dir}/{mat_ng_name}_addon.py", "w")
    """
    #file = open("/home/Documents/Repos/NodeToPython/test.py", "w")

    """Sets up bl_info and imports Blender"""
    def header():
        print("bl_info = {\n")
        print(f"\t\"name\" : \"{ng.name}\",\n")
        print("\t\"author\" : \"Node To Python\",\n")
        print("\t\"version\" : (1, 0, 0),\n")
        print(f"\t\"blender\" : {bpy.app.version},\n")
        print("\t\"location\" : \"Object\",\n")
        print("\t\"category\" : \"Object\"\n")
        print("}\n")
        print("\n")
        print("import bpy\n")
        print("\n")
    header()    

    """Creates the class and its variables"""
    def init_class():
        print(f"class {class_name}(bpy.types.Operator):\n")
        print(f"\tbl_idname = \"object.{ng_name}\"\n")
        print(f"\tbl_label = \"{ng.name}\"\n")
        print("\tbl_options = {\'REGISTER\', \'UNDO\'}\n")
        print("\n")
    init_class()

    print("\tdef execute(self, context):\n")

    def process_mat_node_group(node_group, level):
        ng_name = node_group.name.lower().replace(' ', '_')

        outer = "\t"*level
        inner = "\t"*(level + 1)

        #initialize node group
        print(f"{outer}#initialize {ng_name} node group\n")
        print(f"{outer}def {ng_name}_node_group():\n")
        print((f"{inner}{ng_name}"
                f"= bpy.data.node_groups.new("
                f"type = \"ShaderNodeGroup\", "
                f"name = \"{node_group.name}\")\n"))
        print("\n")

        #initialize nodes
        print(f"{inner}#initialize {ng_name} nodes\n")

        for node in node_group.nodes:
            if node.bl_idname == 'ShaderNodeGroup':
                process_mat_node_group(node.node_tree, level + 1)
            #create node
            node_name = node.name.lower()
            node_name = node_name.replace(' ', '_').replace('.', '_')
            print(f"{inner}#node {node.name}\n")
            print((f"{inner}{node_name} "
                    f"= {ng_name}.nodes.new(\"{node.bl_idname}\")\n"))
            print((f"{inner}{node_name}.location "
                    f"= ({node.location.x}, {node.location.y})\n"))
            print((f"{inner}{node_name}.width, {node_name}.height "
                    f"= {node.width}, {node.height}\n"))
            if node.label:
                print(f"{inner}{node_name}.label = \"{node.label}\"\n")

            for i, input in enumerate(node.inputs):
                if input.bl_idname not in dont_set_defaults:
                    dv = None
                    if input.bl_idname == 'NodeSocketColor':
                        col = input.default_value
                        dv = f"({col[0]}, {col[1]}, {col[2]}, {col[3]})"
                    elif "Vector" in input.bl_idname:
                        vector = input.default_value
                        dv = f"({vector[0]}, {vector[1]}, {vector[2]})"
                    elif input.bl_idname == 'NodeSocketString':
                        dv = f"\"\""
                    else:
                        #TODO: fix this later
                        if input.bl_idname != 'NodeSocketShader':
                            dv = input.default_value
                    if dv is not None:
                        print(f"{inner}#{input.identifier}\n")
                        print((f"{inner}{node_name}"
                                    f".inputs[{i}]"
                                    f".default_value = {dv}\n"))

        #initialize links
        if node_group.links:
            print(f"{inner}#initialize {ng_name} links\n")     
        for link in node_group.links:
            input_node = link.from_node.name.lower()
            input_node = input_node.replace(' ', '_').replace('.', '_')
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
            
            output_node = link.to_node.name.lower()
            output_node = output_node.replace(' ', '_').replace('.', '_')
            output_socket = link.to_socket
            
            for i, item in enumerate(link.to_node.inputs.items()):
                if item[1] == output_socket:
                    output_idx = i
                    break
            
            print((f"{inner}#{input_node}.{input_socket.name} "
                        f"-> {output_node}.{output_socket.name}\n"))
            print((f"{inner}{ng_name}.links.new({input_node}"
                        f".outputs[{input_idx}], "
                        f"{output_node}.inputs[{output_idx}])\n"))
        print(f"{outer}{ng_name}_node_group()\n")
              
    process_mat_node_group(ng, 2)
    print("\t\treturn {'FINISHED'}\n\n")

    """Create the function that adds the addon to the menu"""
    def create_menu_func():
        print("def menu_func(self, context):\n")
        print(f"\tself.layout.operator({class_name}.bl_idname)\n")
        print("\n")
    create_menu_func()

    """Create the register function"""
    def create_register():
        print("def register():\n")
        print(f"\tbpy.utils.register_class({class_name})\n")
        print("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
        print("\n")
    create_register()

    """Create the unregister function"""
    def create_unregister():
        print("def unregister():\n")
        print(f"\tbpy.utils.unregister_class({class_name})\n")
        print("\tbpy.types.VIEW3D_MT_objects.remove(menu_func)\n")
        print("\n")
    create_unregister()

    """Create the main function"""
    def create_main():
        print("if __name__ == \"__main__\":\n")
        print("\tregister()")
    create_main()

execute(None, "Material")