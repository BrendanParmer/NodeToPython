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

#node tree input sockets that have default properties
default_sockets = {'NodeSocketBool', 
                   'NodeSocketColor',
                   'NodeSocketFloat',
                   'NodeSocketInt',
                   'NodeSocketVector'}

#node tree input sockets that have min/max properties           
value_sockets = {'NodeSocketInt',
                 'NodeSocketFloat',
                 'NodeSocketVector'}

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketCollection',
                     'NodeSocketGeometry',
                     'NodeSocketImage',
                     'NodeSocketMaterial'
                     'NodeSocketObject',
                     'NodeSocketTexture',
                     'NodeSocketVirtual'}

node_settings = {
    #attribute
    "GeometryNodeAttributeStatistic" : ["data_type", "domain"],
    "GeometryNodeCaptureAttribute" : ["data_type", "domain"],
    "GeometryNodeAttributeDomainSize" : ["component"],
    "GeometryNodeStoreNamedAttribute" : ["data_type", "domain"],
    "GeometryNodeAttributeTransfer" : ["data_type", "mapping"],

    #color
    "ShaderNodeMixRGB" : ["blend_type", "use_clamp"],

    #curve
    "GeometryNodeCurveToPoints" : ["mode"],
    "GeometryNodeFillCurve" : ["mode"], 
    "GeometryNodeFilletCurve" : ["mode"],
    "GeometryNodeResampleCurve" : ["mode"],
    "GeometryNodeSampleCurve" : ["mode"],
    "GeometryNodeTrimCurve" : ["mode"],
    "GeometryNodeCurveHandleTypeSelection" : ["mode", "handle_type"],
    "GeometryNodeSetCurveHandlePositions" : ["mode"],
    "GeometryNodeCurveSetHandles" : ["mode", "handle_type"],
    "GeometryNodeCurveSplineType" : ["spline_type"],

    #curve primitives
    "GeometryNodeCurveArc" : ["mode"],
    "GeometryNodeCurvePrimitiveBezierSegment" : ["mode"],
    "GeometryNodeCurvePrimitiveCircle" : ["mode"],
    "GeometryNodeCurvePrimitiveLine" : ["mode"],
    "GeometryNodeCurvePrimitiveQuadrilateral" : ["mode"],

    #geometry
    "GeometryNodeDeleteGeometry" : ["domain", "mode"],
    "GeometryNodeDuplicateElements" : ["domain"],
    "GeometryNodeProximity" : ["target_element"],
    "GeometryNodeMergeByDistance" : ["mode"],
    "GeometryNodeRaycast" : ["data_type", "mapping"],
    "GeometryNodeSeparateGeometry" : ["domain"],

    #input
    "GeometryNodeCollectionInfo" : ["transform_space"],
    "GeometryNodeObjectInfo" : ["transform_space"],
    "GeometryNodeInputNamedAttribute" : ["data_type"],

    #mesh
    "GeometryNodeExtrudeMesh" : ["mode"],
    "GeometryNodeMeshBoolean" : ["operation"],
    "GeometryNodeMeshToPoints" : ["mode"],
    "GeometryNodeSubdivisionSurface" : ["uv_smooth", "boundary_smooth"],
    "GeometryNodeTriangulate" : ["quad_method", "ngon_method"],
    "GeometryNodeScaleElements" : ["domain", "scale_mode"],

    #mesh primitives
    "GeometryNodeMeshCone" : ["fill_type"],
    "GeometryNodeMeshCylinder" : ["fill_type"],
    "GeometryNodeMeshCircle" : ["fill_type"],
    "GeometryNodeMeshLine" : ["mode"],

    #point
    "GeometryNodeDistributePointsOnFaces" : ["distribute_method"],
    "GeometryNodePointsToVolume" : ["resolution_mode"],

    #text
    "GeometryNodeStringToCurves" : ["overflow", "align_x", "align_y", 
                                    "pivot_mode"],
    
    #texture
    "ShaderNodeTexBrick" : ["offset", "offset_frequency", "squash", 
                            "squash_frequency"],
    "ShaderNodeTexGradient" : ["gradient_type"],
    "GeometryNodeImageTexture" : ["interpolation", "extension"],
    "ShaderNodeTexMagic" : ["turbulence_depth"],
    "ShaderNodeTexNoise" : ["noise_dimensions"],
    "ShaderNodeTexVoronoi" : ["voronoi_dimensions", "feature", "distance"],
    "ShaderNodeTexWave" : ["wave_type", "bands_direction", "wave_profile"],
    "ShaderNodeTexWhiteNoise" : ["noise_dimensions"],

    #utilities
    "GeometryNodeAccumulateField" : ["data_type", "domain"],
    "FunctionNodeAlignEulerToVector" : ["axis", "pivot_axis"],
    "FunctionNodeBooleanMath" : ["operation"],
    "ShaderNodeClamp" : ["clamp_type"],
    "FunctionNodeCompare" : ["data_type", "operation", "mode"],
    "GeometryNodeFieldAtIndex" : ["data_type", "domain"],
    "FunctionNodeFloatToInt" : ["rounding_mode"],
    "ShaderNodeMapRange" : ["data_type", "interpolation_type", "clamp"], 
    "ShaderNodeMath" : ["operation", "use_clamp"],
    "FunctionNodeRandomValue" : ["data_type"],
    "FunctionNodeRotateEuler" : ["type", "space"],
    "GeometryNodeSwitch" : ["input_type"],

    #vector
    "ShaderNodeVectorMath" : ["operation"],
    "ShaderNodeVectorRotate" : ["rotation_type", "invert"],

    #volume
    "GeometryNodeVolumeToMesh" : ["resolution_mode"]
}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}

class NodeToPython(bpy.types.Operator):
    bl_idname = "object.node_to_python"
    bl_label = "Node to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    node_group_name: bpy.props.StringProperty(name="Node Group")
    
    def execute(self, context):
        ng = bpy.data.node_groups[self.node_group_name]
        ng_name = ng.name.lower().replace(' ', '_')
        class_name = ng.name.replace(" ", "")
        dir = bpy.path.abspath("//")
        
        file = open(f"{dir}{ng_name}_addon.py", "w")
        
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

        """Construct the execute function"""
        file.write("\tdef execute(self, context):\n")

        def process_node_group(node_group, level):
            ng_name = node_group.name.lower().replace(' ', '_')
                
            outer = "\t"*level       #outer indentation
            inner = "\t"*(level + 1) #inner indentation

            #initialize node group
            file.write(f"{outer}#initialize {ng_name} node group\n")
            file.write(f"{outer}def {ng_name}_node_group():\n")
            file.write((f"{inner}{ng_name}"
                        f"= bpy.data.node_groups.new("
                        f"type = \"GeometryNodeTree\", "
                        f"name = \"{node_group.name}\")\n"))
            file.write("\n")

            #initialize nodes
            file.write(f"{inner}#initialize {ng_name} nodes\n")
            for node in node_group.nodes:
                if node.bl_idname == 'GeometryNodeGroup':
                    process_node_group(node.node_tree, level + 1)
                elif node.bl_idname == 'NodeGroupInput':
                    file.write(f"{inner}#{ng_name} inputs\n")
                    for input in node.outputs:
                        if input.bl_idname != "NodeSocketVirtual":
                            file.write(f"{inner}#input {input.name}\n")
                            file.write((f"{inner}{ng_name}.inputs.new"
                                        f"(\"{input.bl_idname}\", "
                                        f"\"{input.name}\")\n"))
                            if input.bl_idname in default_sockets:
                                socket = node_group.inputs[input.name]
                                if input.bl_idname == 'NodeSocketColor':
                                    col = socket.default_value
                                    r, g, b, a = col[0], col[1], col[2], col[3]
                                    dv = f"({r}, {g}, {b}, {a})"
                                elif input.bl_idname == 'NodeSocketVector':
                                    vec = socket.default_value
                                    dv = f"({vec[0]}, {vec[1]}, {vec[2]})"
                                else:
                                    dv = socket.default_value
                                
                                #default value
                                file.write((f"{inner}{ng_name}"
                                            f".inputs[\"{input.name}\"]"
                                            f".default_value = {dv}\n"))
                                if input.bl_idname in value_sockets:
                                    #min value
                                    file.write((f"{inner}{ng_name}"
                                                f".inputs[\"{input.name}\"]"
                                                f".min_value = "
                                                f"{socket.min_value}\n"))
                                    #max value
                                    file.write((f"{inner}{ng_name}"
                                                f".inputs[\"{input.name}\"]"
                                                f".max_value = "
                                                f"{socket.max_value}\n"))
                            file.write("\n")
                    file.write("\n")
                elif node.bl_idname == 'NodeGroupOutput':
                    file.write(f"{inner}#{ng_name} outputs\n")
                    for output in node.inputs:
                        if output.bl_idname != 'NodeSocketVirtual':
                            file.write((f"{inner}{ng_name}.outputs"
                                        f".new(\"{output.bl_idname}\", "
                                        f"\"{output.name}\")\n"))
                    file.write("\n")

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

                #special nodes
                if node.bl_idname in node_settings:
                    for setting in node_settings[node.bl_idname]:
                        attr = getattr(node, setting)
                        if type(attr) == str:
                            attr = f"\'{attr}\'"
                        file.write((f"{inner}{node_name}.{setting} = "
                                    f"{attr}\n"))
                elif node.bl_idname == 'GeometryNodeGroup':
                    file.write((f"{inner}{node_name}.node_tree = "
                                f"bpy.data.node_groups"
                                f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'ShaderNodeValToRGB':
                    color_ramp = node.color_ramp
                    file.write("\n")
                    file.write((f"{inner}{node_name}.color_ramp.color_mode = "
                                f"\'{color_ramp.color_mode}\'\n"))
                    file.write((f"{inner}{node_name}.color_ramp"
                                f".hue_interpolation = "
                                f"\'{color_ramp.hue_interpolation}\'\n"))
                    file.write((f"{inner}{node_name}.color_ramp.interpolation "
                                f"= '{color_ramp.interpolation}'\n"))
                    file.write("\n")
                    for i, element in enumerate(color_ramp.elements):
                        file.write((f"{inner}{node_name}_cre_{i} = "
                                    f"{node_name}.color_ramp.elements"
                                    f".new({element.position})\n"))
                        file.write((f"{inner}{node_name}_cre_{i}.alpha = "
                                    f"{element.alpha}\n"))
                        col = element.color
                        r, g, b, a = col[0], col[1], col[2], col[3]
                        file.write((f"{inner}{node_name}_cre_{i}.color = "
                                    f"({r}, {g}, {b}, {a})\n\n"))
                elif node.bl_idname in curve_nodes:
                    file.write(f"{inner}#mapping settings")
                    mapping = f"{inner}{node_name}.mapping"

                    extend = f"\'{node.mapping.extend}\'"
                    file.write(f"{mapping}.extend = {extend}\n")
                    tone = f"\'{node.mapping.tone}\'"
                    file.write(f"{mapping}.tone = {tone}\n")

                    b_lvl = node.mapping.black_level
                    b_lvl_str = f"({b_lvl[0]}, {b_lvl[1]}, {b_lvl[2]})"
                    file.write((f"{mapping}.black_level = {b_lvl_str}\n"))
                    w_lvl = node.mapping.white_level
                    w_lvl_str = f"({w_lvl[0]}, {w_lvl[1]}, {w_lvl[2]})"
                    file.write((f"{mapping}.white_level = {w_lvl_str}\n"))

                    min_x = node.mapping.clip_min_x
                    file.write(f"{mapping}.clip_min_x = {min_x}\n")
                    min_y = node.mapping.clip_min_y
                    file.write(f"{mapping}.clip_min_y = {min_y}\n")
                    max_x = node.mapping.clip_max_x
                    file.write(f"{mapping}.clip_max_x = {max_x}\n")
                    max_y = node.mapping.clip_max_y
                    file.write(f"{mapping}.clip_max_y = {max_y}\n")

                    use_clip = node.mapping.use_clip
                    file.write(f"{mapping}.use_clip = {use_clip}\n")

                    for i, curve in enumerate(node.mapping.curves):
                        file.write(f"{inner}#curve {i}")
                        curve_i = f"{node_name}_curve_{i}"
                        file.write((f"{inner}{curve_i} = "
                                    f"{node_name}.mapping.curves[{i}]\n"))
                        for j, point in enumerate(curve.points):
                            point_j = f"{inner}{curve_i}_point_{j}"

                            loc = point.location
                            file.write((f"{point_j} = "
                                        f"{curve_i}.points.new"
                                        f"({loc[0]}, {loc[1]})\n"))

                            handle = f"\'{point.handle_type}\'"
                            file.write(f"{point_j}.handle_type = {handle}\n")
                    file.write(f"{inner}#update curve after changes")
                    file.write(f"{mapping}.update()\n")
                
                for i, input in enumerate(node.inputs):
                    if input.bl_idname not in dont_set_defaults:
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
                file.write("\n")
            
            #initialize links
            if node_group.links:
                file.write(f"{inner}#initialize {ng_name} links\n")     
            for link in node_group.links:
                input_node = link.from_node.name.lower().replace(' ', '_')
                input_socket = link.from_socket.name
                
                output_node = link.to_node.name.lower().replace(' ', '_')
                output_socket = link.to_socket.name
                
                file.write((f"{inner}{ng_name}.links.new({input_node}"
                            f".outputs[\"{input_socket}\"], "
                            f"{output_node}.inputs[\"{output_socket}\"])\n"))
            
            #create node group
            file.write("\n")
            file.write(f"{outer}{ng_name}_node_group()\n")
            file.write("\n")    
        
        process_node_group(ng, 2)

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

def menu_func(self, context):
    self.layout.operator(NodeToPython.bl_idname, text=NodeToPython.bl_label)
    
def register():
    bpy.utils.register_class(NodeToPython)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(NodeToPython)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()