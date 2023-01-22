import bpy
import os

from .utils import *

#node tree input sockets that have default properties
default_sockets = {'NodeSocketBool', 
                   'NodeSocketColor',
                   'NodeSocketFloat',
                   'NodeSocketInt',
                   'NodeSocketVector'}

geo_node_settings = {
    #attribute
    "GeometryNodeAttributeStatistic" : ["data_type", "domain"],
    "GeometryNodeCaptureAttribute" : ["data_type", "domain"],
    "GeometryNodeAttributeDomainSize" : ["component"],
    "GeometryNodeStoreNamedAttribute" : ["data_type", "domain"],
    "GeometryNodeAttributeTransfer" : ["data_type", "mapping"],

    #color
    "ShaderNodeMixRGB"          : ["blend_type", "use_clamp"],
    "FunctionNodeCombineColor"  : ["mode"],
    "FunctionNodeSeparateColor" : ["mode"],

    #curve
    "GeometryNodeCurveToPoints" : ["mode"],
    "GeometryNodeFillCurve" : ["mode"], 
    "GeometryNodeFilletCurve" : ["mode"],
    "GeometryNodeResampleCurve" : ["mode"],
    "GeometryNodeSampleCurve" : ["data_type", "mode", "use_all_curves"],
    "GeometryNodeTrimCurve" : ["mode"],
    "GeometryNodeSetCurveNormal" : ["mode"],
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
    "GeometryNodeSampleIndex" : ["data_type", "domain", "clamp"],
    "GeometryNodeSampleNearest" : ["domain"],
    "GeometryNodeSeparateGeometry" : ["domain"],

    #input
    "FunctionNodeInputBool" : ["boolean"],
    "GeometryNodeCollectionInfo" : ["transform_space"],
    "FunctionNodeInputColor" : ["color"],
    "FunctionNodeInputInt" : ["integer"],
    "GeometryNodeInputMaterial" : ["material"],
    "GeometryNodeObjectInfo" : ["transform_space"],
    "FunctionNodeInputString" : ["string"],
    "FunctionNodeInputVector" : ["vector"],
    "GeometryNodeInputNamedAttribute" : ["data_type"],

    #mesh
    "GeometryNodeExtrudeMesh" : ["mode"],
    "GeometryNodeMeshBoolean" : ["operation"],
    "GeometryNodeMeshToPoints" : ["mode"],
    "GeometryNodeMeshToVolume" : ["resolution_mode"],
    "GeometryNodeSampleNearestSurface" : ["data_type"],
    "GeometryNodeSampleUVSurface" : ["data_type"],
    "GeometryNodeSubdivisionSurface" : ["uv_smooth", "boundary_smooth"],
    "GeometryNodeTriangulate" : ["quad_method", "ngon_method"],
    "GeometryNodeScaleElements" : ["domain", "scale_mode"],

    #mesh primitives
    "GeometryNodeMeshCone" : ["fill_type"],
    "GeometryNodeMeshCylinder" : ["fill_type"],
    "GeometryNodeMeshCircle" : ["fill_type"],
    "GeometryNodeMeshLine" : ["mode"],

    #output
    "GeometryNodeViewer" : ["domain"],
    
    #point
    "GeometryNodeDistributePointsInVolume" : ["mode"],
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
    "GeometryNodeFieldOnDomain" : ["data_type", "domain" ],
    "ShaderNodeMapRange" : ["data_type", "interpolation_type", "clamp"], 
    "ShaderNodeMath" : ["operation", "use_clamp"],
    "FunctionNodeRandomValue" : ["data_type"],
    "FunctionNodeRotateEuler" : ["type", "space"],
    "GeometryNodeSwitch" : ["input_type"],

    #uv
    "GeometryNodeUVUnwrap" : ["method"],

    #vector
    "ShaderNodeVectorMath" : ["operation"],
    "ShaderNodeVectorRotate" : ["rotation_type", "invert"],

    #volume
    "GeometryNodeVolumeToMesh" : ["resolution_mode"]
}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}

class GeoNodesToPython(bpy.types.Operator):
    bl_idname = "node.geo_nodes_to_python"
    bl_label = "Geo Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    geo_nodes_group_name: bpy.props.StringProperty(name="Node Group")
    
    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)
        class_name = clean_string(nt.name.replace(" ", "").replace('.', ""), 
                                  lower = False)

        #find base directory to save new addon
        base_dir = bpy.path.abspath("//")
        if not base_dir or base_dir == "":
            self.report({'ERROR'}, 
                        ("NodeToPython: Save your blend file before using "
                        "NodeToPython!"))
            return {'CANCELLED'}

        #save in /addons/ subdirectory
        zip_dir = os.path.join(base_dir, "addons", nt_var)
        addon_dir = os.path.join(zip_dir, nt_var)
        if not os.path.exists(addon_dir):
            os.makedirs(addon_dir)
        file = open(f"{addon_dir}/__init__.py", "w")
        
        create_header(file, nt.name)
        init_operator(file, class_name, nt_var, nt.name)

        file.write("\tdef execute(self, context):\n")

        #set to keep track of already created node trees
        node_trees = set()

        #dictionary to keep track of node->variable name pairs
        node_vars = {}

        #keeps track of all used variables
        used_vars = set()
        
        def process_geo_nodes_group(node_tree, level, node_vars, used_vars):
            node_tree_var = create_var(node_tree.name, used_vars)
                
            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {node_tree_var} node group\n")
            file.write(f"{outer}def {node_tree_var}_node_group():\n")
            file.write((f"{inner}{node_tree_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \"GeometryNodeTree\", "
                        f"name = \"{node_tree.name}\")\n"))
            file.write("\n")

            inputs_set = False
            outputs_set = False

            #initialize nodes
            file.write(f"{inner}#initialize {node_tree_var} nodes\n")
            
            for node in node_tree.nodes:
                if node.bl_idname == 'GeometryNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_geo_nodes_group(node_nt, level + 1, node_vars, 
                                                used_vars)
                        node_trees.add(node_nt)
                elif node.bl_idname == 'NodeGroupInput' and not inputs_set:
                    file.write(f"{inner}#{node_tree_var} inputs\n")
                    for i, input in enumerate(node.outputs):
                        if input.bl_idname != "NodeSocketVirtual":
                            file.write(f"{inner}#input {input.name}\n")
                            file.write((f"{inner}{node_tree_var}.inputs.new"
                                        f"(\"{input.bl_idname}\", "
                                        f"\"{input.name}\")\n"))
                            socket = node_tree.inputs[i]
                            if input.bl_idname in default_sockets:  
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
                                file.write((f"{inner}{node_tree_var}"
                                            f".inputs[{i}]"
                                            f".default_value = {dv}\n"))

                                #min value
                                if hasattr(socket, "min_value"):
                                    file.write((f"{inner}{node_tree_var}"
                                                f".inputs[{i}]"
                                                f".min_value = "
                                                f"{socket.min_value}\n"))
                                #max value
                                if hasattr(socket, "max_value"):
                                    file.write((f"{inner}{node_tree_var}"
                                                f".inputs[{i}]"
                                                f".max_value = "
                                                f"{socket.max_value}\n"))
                            #default attribute name
                            if hasattr(socket, "default_attribute_name"):
                                if socket.default_attribute_name != "":
                                    file.write((f"{inner}{node_tree_var}"
                                                f".inputs[{i}]"
                                                f".default_attribute_name = \""
                                                f"{socket.default_attribute_name}"
                                                f"\"\n"))
                            #description
                            if socket.description != "":
                                file.write((f"{inner}{node_tree_var}"
                                            f".inputs[{i}]"
                                            f".description = "
                                            f"\"{socket.description}\"\n"))
                            #hide value
                            if socket.hide_value is True:
                                file.write((f"{inner}{node_tree_var}"
                                            f".inputs[{i}]"
                                            f".hide_value = "
                                            f"{socket.hide_value}\n"))
                            file.write("\n")
                    file.write("\n")
                    inputs_set = True

                elif node.bl_idname == 'NodeGroupOutput' and not outputs_set:
                    file.write(f"{inner}#{node_tree_var} outputs\n")
                    for i, output in enumerate(node.inputs):
                        if output.bl_idname != 'NodeSocketVirtual':
                            file.write((f"{inner}{node_tree_var}.outputs"
                                        f".new(\"{output.bl_idname}\", "
                                        f"\"{output.name}\")\n"))
                            
                            socket = node_tree.outputs[i]
                            #description
                            if socket.description != "":
                                file.write((f"{inner}{node_tree_var}"
                                            f".outputs[{i}]"
                                            f".description = "
                                            f"\"{socket.description}\"\n"))
                            #hide value
                            if socket.hide_value is True:
                                file.write((f"{inner}{node_tree_var}"
                                            f".outputs[{i}]"
                                            f".hide_value = "
                                            f"{socket.hide_value}\n"))

                            #default attribute name
                            if hasattr(socket, "default_attribute_name"):
                                if socket.default_attribute_name != "":
                                    file.write((f"{inner}{node_tree_var}"
                                                f".outputs[{i}]"
                                                f".default_attribute_name = \""
                                                f"{socket.default_attribute_name}"
                                                f"\"\n"))
                            #attribute domain
                            if hasattr(socket, "attribute_domain"):
                                file.write((f"{inner}{node_tree_var}"
                                            f".outputs[{i}]"
                                            f".attribute_domain = "
                                            f"\'{socket.attribute_domain}\'\n"))             
                    file.write("\n")
                    outputs_set = True

                #create node
                node_var = create_node(node, file, inner, node_tree_var, 
                                      node_vars, used_vars)
                set_settings_defaults(node, geo_node_settings, file, inner, 
                                        node_var)
                hide_sockets(node, file, inner, node_var)

                if node.bl_idname == 'GeometryNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[\"{node.node_tree.name}\"]\n"))
                elif node.bl_idname == 'ShaderNodeValToRGB':
                    color_ramp_settings(node, file, inner, node_var)
                elif node.bl_idname in curve_nodes:
                    curve_node_settings(node, file, inner, node_var)
                
                set_input_defaults(node, file, inner, node_var, addon_dir)
                set_output_defaults(node, file, inner, node_var)
            set_parents(node_tree, file, inner, node_vars)
            set_locations(node_tree, file, inner, node_vars)
            set_dimensions(node_tree, file, inner, node_vars)

            init_links(node_tree, file, inner, node_tree_var, node_vars)
            
            file.write(f"{inner}return {node_tree_var}\n")

            #create node group
            file.write((f"\n{outer}{node_tree_var} = "
                        f"{node_tree_var}_node_group()\n\n"))
            return used_vars
        
        process_geo_nodes_group(nt, 2, node_vars, used_vars)

        def apply_modifier():
            #get object
            file.write(f"\t\tname = bpy.context.object.name\n")
            file.write(f"\t\tobj = bpy.data.objects[name]\n")

            #set modifier to the one we just created
            mod_name = str_to_py_str(nt.name)
            file.write((f"\t\tmod = obj.modifiers.new(name = {mod_name}, "
                        f"type = 'NODES')\n"))
            file.write(f"\t\tmod.node_group = {nt_var}\n")
        apply_modifier()

        file.write("\t\treturn {'FINISHED'}\n\n")
        
        create_menu_func(file, class_name)
        create_register_func(file, class_name)
        create_unregister_func(file, class_name)
        create_main_func(file)

        file.close()

        zip_addon(zip_dir)

        return {'FINISHED'}

class SelectGeoNodesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_geo_nodes_selection"
    bl_label = "Select Geo Nodes"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'

        geo_node_groups = [node for node in bpy.data.node_groups if node.type == 'GEOMETRY']

        for geo_ng in geo_node_groups:
            op = layout.operator(GeoNodesToPython.bl_idname, text=geo_ng.name)
            op.geo_nodes_group_name = geo_ng.name
            
class GeoNodesToPythonPanel(bpy.types.Panel):
    bl_label = "Geometry Nodes to Python"
    bl_idname = "NODE_PT_geo_nodes_to_python"
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
        geo_node_groups = [node 
                            for node in bpy.data.node_groups 
                            if node.type == 'GEOMETRY']
        geo_node_groups_exist = len(geo_node_groups) > 0
        row.enabled = geo_node_groups_exist
        
        row.alignment = 'EXPAND'
        row.operator_context = 'INVOKE_DEFAULT'
        row.menu("NODE_MT_ntp_geo_nodes_selection", text="Geometry Nodes")