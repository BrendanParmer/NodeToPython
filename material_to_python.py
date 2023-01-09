import bpy
import os

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketCollection',
                     'NodeSocketGeometry',
                     'NodeSocketImage',
                     'NodeSocketMaterial',
                     'NodeSocketObject',
                     'NodeSocketShader',
                     'NodeSocketTexture',
                     'NodeSocketVirtual'}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}   

class MaterialToPython(bpy.types.Operator):
    bl_idname = "node.material_to_python"
    bl_label =  "Material to Python"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(name="Node Group")

    def execute(self, context):
        if self.material_name not in bpy.data.materials:
            return {'FINISHED'}
        
        #set up addon file
        ng = bpy.data.materials[self.material_name].node_tree
        ng_name = ng.name.lower().replace(' ', '_')
        class_name = ng.name.replace(" ", "")
        
        dir = bpy.path.abspath("//")
        if not dir or dir == "":
            self.report({'ERROR'},
                        ("NodeToPython: Save your blender file before using "
                        "NodeToPython!"))
            return {'CANCELLED'}
        addon_dir = os.path.join(dir, "addons")
        if not os.path.exists(addon_dir):
            os.mkdir(addon_dir)
        file = open(f"{addon_dir}/{ng_name}_addon.py", "w")

        """Sets up bl_info and imports Blender"""
        def header():
            file.write("bl_info = {\n")
            file.write(f"\t\"name\" : \"{ng.name}\",\n")
            file.write("\t\"author\" : \"Node To Python\",\n")
            file.write("\t\"version\" : (1, 0, 0),\n")
            file.write(f"\t\"blender\" : {bpy.app.version},\n")
            file.write("\t\"location\" : \"Object\",\n")
            file.write("\t\"category\" : \"Object\"\n")
            file.write("}\n")
            file.write("\n")
            file.write("import bpy\n")
            file.write("\n")
        header()    

        """Creates the class and its variables"""
        def init_class():
            file.write(f"class {class_name}(bpy.types.Operator):\n")
            file.write(f"\tbl_idname = \"object.{ng_name}\"\n")
            file.write(f"\tbl_label = \"{ng.name}\"\n")
            file.write("\tbl_options = {\'REGISTER\', \'UNDO\'}\n")
            file.write("\n")
        init_class()

        file.write("\tdef execute(self, context):\n")

        def process_mat_node_group(node_group, level):
            ng_name = node_group.name.lower().replace(' ', '_')

            outer = "\t"*level
            inner = "\t"*(level + 1)

            #initialize node group
            file.write(f"{outer}#initialize {ng_name} node group\n")
            file.write(f"{outer}def {ng_name}_node_group():\n")
            file.write((f"{inner}{ng_name}"
                    f"= bpy.data.node_groups.new("
                    f"type = \"ShaderNodeGroup\", "
                    f"name = \"{node_group.name}\")\n"))
            file.write("\n")

            #initialize nodes
            file.write(f"{inner}#initialize {ng_name} nodes\n")

            for node in node_group.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    process_mat_node_group(node.node_tree, level + 1)
                #create node
                node_name = node.name.lower()
                node_name = node_name.replace(' ', '_').replace('.', '_')
                file.write(f"{inner}#node {node.name}\n")
                file.write((f"{inner}{node_name} "
                        f"= {ng_name}.nodes.new(\"{node.bl_idname}\")\n"))
                file.write((f"{inner}{node_name}.location "
                        f"= ({node.location.x}, {node.location.y})\n"))
                file.write((f"{inner}{node_name}.width, {node_name}.height "
                        f"= {node.width}, {node.height}\n"))
                if node.label:
                    file.write(f"{inner}{node_name}.label = \"{node.label}\"\n")

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
                            dv = input.default_value
                        if dv is not None:
                            file.write(f"{inner}#{input.identifier}\n")
                            file.write((f"{inner}{node_name}"
                                        f".inputs[{i}]"
                                        f".default_value = {dv}\n"))

            #initialize links
            if node_group.links:
                file.write(f"{inner}#initialize {ng_name} links\n")     
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
                
                file.write((f"{inner}#{input_node}.{input_socket.name} "
                            f"-> {output_node}.{output_socket.name}\n"))
                file.write((f"{inner}{ng_name}.links.new({input_node}"
                            f".outputs[{input_idx}], "
                            f"{output_node}.inputs[{output_idx}])\n"))
            file.write(f"{outer}{ng_name}_node_group()\n")
                
        process_mat_node_group(ng, 2)
        file.write("\t\treturn {'FINISHED'}\n\n")

        """Create the function that adds the addon to the menu"""
        def create_menu_func():
            file.write("def menu_func(self, context):\n")
            file.write(f"\tself.layout.operator({class_name}.bl_idname)\n")
            file.write("\n")
        create_menu_func()

        """Create the register function"""
        def create_register():
            file.write("def register():\n")
            file.write(f"\tbpy.utils.register_class({class_name})\n")
            file.write("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
            file.write("\n")
        create_register()

        """Create the unregister function"""
        def create_unregister():
            file.write("def unregister():\n")
            file.write(f"\tbpy.utils.unregister_class({class_name})\n")
            file.write("\tbpy.types.VIEW3D_MT_objects.remove(menu_func)\n")
            file.write("\n")
        create_unregister()

        """Create the main function"""
        def create_main():
            file.write("if __name__ == \"__main__\":\n")
            file.write("\tregister()")
        create_main()

        file.close()
        return {'FINISHED'}

class NodeToPythonPanel(bpy.types.Panel):
    bl_label = "Node To Python"
    bl_idname = "NODE_PT_node_to_python"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = "NodeToPython"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        
        # Disables menu when len of geometry nodes is 0
        geo_node_groups = [node for node in bpy.data.node_groups if node.type == 'GEOMETRY']
        geo_node_groups_exist = len(geo_node_groups) > 0
        row.enabled = geo_node_groups_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_node_to_python", text="Geometry Node Groups")

classes = [NodeToPythonMenu, NodeToPythonPanel, NodeToPython]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()