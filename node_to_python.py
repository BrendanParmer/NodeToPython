bl_info = {
    "name": "Node to Python", 
    "description": "Convert Geometry Node Groups to a Python add-on",
    "author": "Brendan Parmer",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Object", 
    "category": "Object",
}

import bpy

class NodeToPython(bpy.types.Operator):
    bl_idname = "object.node_to_python"
    bl_label = "Node to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    ng_name: bpy.props.StringProperty(name="Node Group", default = "Poop", description="Name of the node group to convert into an add-on")
    
    def execute(self, context):
        if self.ng_name not in bpy.data.node_groups:
            print(f"Node group {self.ng_name} does not exist!")
            return {'CANCELLED'}
        ng = bpy.data.node_groups[self.ng_name]
        ng_name = ng.name.lower().replace(' ', '_')
        class_name = ng.name.replace(" ", "")
        dir = bpy.path.abspath("//")
        
        file = open(f"{dir}{ng_name}_addon.py", "w")
        
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
        file.write(f"class {class_name}(bpy.types.Operator):\n")
        file.write(f"\tbl_idname = \"object.{ng_name}\"\n")
        file.write(f"\tbl_label = \"{ng.name}\"\n")
        file.write("\tbl_options = {\'REGISTER\', \'UNDO\'}\n")
        file.write("\n")
        
        file.write("\tdef execute(self, context):\n")
        
        def process_node_group(node_group, level):
            ng_name = node_group.name.lower().replace(' ', '_')
                
            file.write("\t"*level + f"#initialize {ng_name} node group\n")
            file.write("\t"*level + f"def {ng_name}_node_group():\n")
            file.write("\t"*(level + 1) + f"{ng_name} = bpy.data.node_groups.new(type = \"GeometryNodeTree\", name = \"{node_group.name}\")\n")
            
            file.write("\n")
            file.write("\t"*(level + 1) + f"#initialize {ng_name} nodes\n")
            for node in node_group.nodes:
                if node.bl_idname == 'GeometryNodeGroup':
                    process_node_group(node.node_tree, level + 1)
                if node.bl_idname == 'NodeGroupInput':
                    file.write("\t"*(level+1) + f"#{ng_name} inputs\n")
                    for input in node.outputs:
                        if input.bl_idname != "NodeSocketVirtual":
                            file.write("\t"*(level+1) + f"{ng_name}.inputs.new(\"{input.bl_idname}\", \"{input.name}\")\n")
                    file.write("\n")
                if node.bl_idname == 'NodeGroupOutput':
                    file.write("\t"*(level+1) + f"#{ng_name} outputs\n")
                    for output in node.inputs:
                        if output.bl_idname != "NodeSocketVirtual":
                            file.write("\t"*(level+1) + f"{ng_name}.outputs.new(\"{output.bl_idname}\", \"{output.name}\")\n")
                    file.write("\n")
    
                node_name = node.name.lower().replace(' ', '_')
                file.write("\t"*(level+1) + f"{node_name} = {ng_name}.nodes.new(\"{node.bl_idname}\")\n")
                file.write("\t"*(level+1) + f"{node_name}.location = ({node.location.x}, {node.location.y})\n")
                file.write("\t"*(level+1) + f"{node_name}.width, {node_name}.height = {node.width}, {node.height}\n")
                if node.label:
                    file.write("\t"*(level+1) + f"{node_name}.label = \"{node.label}\"\n")
                if node.bl_idname == 'GeometryNodeGroup':
                    file.write("\t"*(level+1) + f"{node_name}.node_tree = bpy.data.node_groups[\"{node.node_tree.name}\"]\n")
                file.write("\n")
            
            file.write("\t"*(level + 1) + f"#initialize {ng_name} links\n")          
            for link in node_group.links:
                input_node = link.from_node.name.lower().replace(' ', '_')
                input_socket = link.from_socket.name
                #input_idx = link.from_node.outputs.find(input_socket)
                
                output_node = link.to_node.name.lower().replace(' ', '_')
                output_socket = link.to_socket.name
                #output_idx = link.from_node.inputs.find(output_socket)
                
                file.write("\t"*(level+1) + f"{ng_name}.links.new({input_node}.outputs[\"{input_socket}\"], {output_node}.inputs[\"{output_socket}\"])\n")
            file.write("\n")
            file.write("\t"*level + f"{ng_name}_node_group()\n")
            file.write("\n")    
        
        process_node_group(ng, 2)
        
        file.write("\t\treturn {'FINISHED'}\n\n")
        
        file.write("def menu_func(self, context):\n")
        file.write(f"\tself.layout.operator({class_name}.bl_idname)\n")
        file.write("\n")
        file.write("def register():\n")
        file.write(f"\tbpy.utils.register_class({class_name})\n")
        file.write("\tbpy.types.VIEW3D_MT_object.append(menu_func)\n")
        file.write("\n")
        file.write("def unregister():\n")
        file.write(f"\tbpy.utils.unregister_class({class_name})\n")
        file.write("\tbpy.types.VIEW3D_MT_objects.remove(menu_func)\n")
        file.write("\n")
        file.write("if __name__ == \"__main__\":\n")
        file.write("\tregister()")
        
        file.close()
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(NodeToPython.bl_idname)
    
def register():
    bpy.utils.register_class(NodeToPython)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(NodeToPython)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()