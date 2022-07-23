bl_info = {
    "name": "Node to Python", 
    "description": "Convert Geometry Node Groups to a Python add-on",
    "author": "Brendan Parmer",
    "version": (0, 0, 0),
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
        
        """
        NTS: probably should use {ng_name} for node tree variable name,
        replacing spaces with underscores obviously.
        
        Then, for any node groups we encounter, we can just call this same function
        """
        """
        f"node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name={self.ng_name})"
        """
        
        for node in ng.nodes:
            if node.bl_idname == 'NodeGroupInput':
                for input in node.outputs:
                    print("I", input.bl_idname, input.bl_label)
                    """
                    f"node_group.inputs.new({input.bl_idname}, {input.bl_label})"
                    """
                """
                
                """
            if node.bl_idname == 'NodeGroupOutput':
                for output in node.inputs:
                    print("O", output.bl_idname, output.bl_label)
                    """
                    f"node_group.outputs.new({output.bl_idname}, {output.bl_label})"
                    """
                """
                
                """
                        
            print(node.bl_idname) #type of node
            print(node.name) #unique identifier
            print(node.label) #UI label
            print(node.location)
            print(node.width, node.height)
            """
            f"{node.name} = node_group.nodes.new({node.bl_idname})"
            f"{node.name}.location = {node.location}"
            f"{node.name}.width, {node.name}.height = {node.width}, {node.height}"
            f"{node.name}.label = {node.label}"
            
            """
                    
            print("")
                    
        for link in ng.links:
            print(link.from_node.name, "->", link.from_socket.identifier)
            print("to")
            print(link.to_node.name, "->", link.to_socket.identifier)
            print("")
            
            """
                f"node_group.links.new({link.from_node.name}.outputs[\"{link.from_socket.identifier}\"], {link.to_node.name}.outputs[\"{link.to_socket.identifier}\"])
            """
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
