import bpy
import os

from .utils import *
from io import StringIO

geo_node_settings : dict[str, list[(str, str)]] = {
    # ATTRIBUTE
    'GeometryNodeAttributeStatistic'  : [("data_type", "enum"), 
                                         ("domain", "enum")],
    'GeometryNodeAttributeDomainSize' : [("component", "enum")],
    'GeometryNodeBlurAttribute'       : [("data_type", "enum")],
    'GeometryNodeCaptureAttribute'    : [("data_type", "enum"),
                                         ("domain", "enum")],
    'GeometryNodeRemoveAttribute'     : [],
    'GeometryNodeStoreNamedAttribute' : [("data_type", "enum"),
                                         ("domain", "enum")],
    'GeometryNodeAttributeTransfer'   : [("data_type", "enum"),
                                         ("domain", "enum"),
                                         ("mapping", "enum")],

    # INPUT
    # Input > Constant
    'FunctionNodeInputBool'     : [("boolean", "bool")],
    'FunctionNodeInputColor'    : [("color", "Vec4")],
    'GeometryNodeInputImage'    : [("image", "Image")],
    'FunctionNodeInputInt'      : [("integer", "int")],
    'GeometryNodeInputMaterial' : [("material", "Material")],
    'FunctionNodeInputString'   : [("string", "str")],
    'ShaderNodeValue'           : [],
    'FunctionNodeInputVector'   : [("vector", "Vec3")],

    #Input > Group
    'NodeGroupInput' : [],
    
    # Input > Scene
    'GeometryNodeCollectionInfo' : [("transform_space", "enum")],
    'GeometryNodeImageInfo'      : [],
    'GeometryNodeIsViewport'     : [],
    'GeometryNodeObjectInfo'     : [("transform_space", "enum")],
    'GeometryNodeSelfObject'     : [],
    'GeometryNodeInputSceneTime' : [],


    # OUTPUT
    'GeometryNodeViewer'         : [("data_type", "enum"),
                                    ("domain", "enum")],


    # GEOMETRY
    'GeometryNodeJoinGeometry'       : [],
    'GeometryNodeGeometryToInstance' : [],

    # Geometry > Read
    'GeometryNodeInputID'             : [],
    'GeometryNodeInputIndex'          : [],
    'GeometryNodeInputNamedAttribute' : [("data_type", "enum")],
    'GeometryNodeInputNormal'         : [],
    'GeometryNodeInputPosition'       : [],
    'GeometryNodeInputRadius'         : [],

    # Geometry > Sample
    'GeometryNodeProximity'      : [("target_element", "enum")],
    'GeometryNodeIndexOfNearest' : [],
    'GeometryNodeRaycast'        : [("data_type", "enum"),
                                    ("mapping", "enum")],
    'GeometryNodeSampleIndex'    : [("clamp", "bool"),
                                    ("data_type", "enum"),
                                    ("domain", "enum")],
    'GeometryNodeSampleNearest'  : [("domain", "enum")],

    # Geometry > Write
    'GeometryNodeSetID'       : [],
    'GeometryNodeSetPosition' : [],

    # Geometry > Operations
    'GeometryNodeBoundBox'           : [],
    'GeometryNodeConvexHull'         : [],
    'GeometryNodeDeleteGeometry'     : [("domain", "enum"),
                                        ("mode", "enum")],
    'GeometryNodeDuplicateElements'  : [("domain", "enum")],
    'GeometryNodeMergeByDistance'    : [("mode", "enum")],
    'GeometryNodeTransform'          : [],
    'GeometryNodeSeparateComponents' : [],
    'GeometryNodeSeparateGeometry'   : [("domain", "enum")],


    # CURVE
    # Curve > Read
    'GeometryNodeInputCurveHandlePositions' : [],
    'GeometryNodeCurveLength'               : [],
    'GeometryNodeInputTangent'              : [],
    'GeometryNodeInputCurveTilt'            : [],
    'GeometryNodeCurveEndpointSelection'    : [],
    'GeometryNodeCurveHandleTypeSelection'  : [("handle_type", "enum"),
                                               ("mode", "enum")],
    'GeometryNodeInputSplineCyclic'         : [],
    'GeometryNodeSplineLength'              : [],
    'GeometryNodeSplineParameter'           : [],
    'GeometryNodeInputSplineResolution'     : [],

    # Curve > Sample
    'GeometryNodeSampleCurve' : [("data_type", "enum"),
                                 ("mode", "enum"),
                                 ("use_all_curves", "bool")],

    # Curve > Write
    'GeometryNodeSetCurveNormal'          : [("mode", "enum")],
    'GeometryNodeSetCurveRadius'          : [],
    'GeometryNodeSetCurveTilt'            : [],
    'GeometryNodeSetCurveHandlePositions' : [("mode", "enum")],
    'GeometryNodeCurveSetHandles'         : [("handle_type", "enum"),
                                             ("mode", "enum")],
    'GeometryNodeSetSplineCyclic'         : [],
    'GeometryNodeSetSplineResolution'     : [],
    'GeometryNodeCurveSplineType'         : [("spline_type", "enum")],

    # Curve > Operations
    'GeometryNodeCurveToMesh'           : [],
    'GeometryNodeCurveToPoints'         : [("mode", "enum")],
    'GeometryNodeDeformCurvesOnSurface' : [],
    'GeometryNodeFillCurve'             : [("mode", "enum")], 
    'GeometryNodeFilletCurve'           : [("mode", "enum")],
    'GeometryNodeInterpolateCurves'     : [],
    'GeometryNodeResampleCurve'         : [("mode", "enum")],
    'GeometryNodeReverseCurve'          : [],
    'GeometryNodeSubdivideCurve'        : [],
    'GeometryNodeTrimCurve'             : [("mode", "enum")],

    # Curve > Primitives
    'GeometryNodeCurveArc'                    : [("mode", "enum")],
    'GeometryNodeCurvePrimitiveBezierSegment' : [("mode", "enum")],
    'GeometryNodeCurvePrimitiveCircle'        : [("mode", "enum")],
    'GeometryNodeCurvePrimitiveLine'          : [("mode", "enum")],
    'GeometryNodeCurveSpiral'                 : [],
    'GeometryNodeCurveQuadraticBezier'        : [],
    'GeometryNodeCurvePrimitiveQuadrilateral' : [("mode", "enum")],
    'GeometryNodeCurveStar'                   : [],

    # Curve > Topology
    'GeometryNodeOffsetPointInCurve' : [],
    'GeometryNodeCurveOfPoint'       : [],
    'GeometryNodePointsOfCurve'      : [],


    # INSTANCES
    'GeometryNodeInstanceOnPoints'      : [],
    'GeometryNodeInstancesToPoints'     : [],
    'GeometryNodeRealizeInstances'      : [("legacy_behavior", "bool")],
    'GeometryNodeRotateInstances'       : [],
    'GeometryNodeScaleInstances'        : [],
    'GeometryNodeTranslateInstances'    : [],
    'GeometryNodeInputInstanceRotation' : [],
    'GeometryNodeInputInstanceScale'    : [],


    # MESH
    # Mesh > Read
    'GeometryNodeInputMeshEdgeAngle'       : [],
    'GeometryNodeInputMeshEdgeNeighbors'   : [],
    'GeometryNodeInputMeshEdgeVertices'    : [],
    'GeometryNodeEdgesToFaceGroups'        : [],
    'GeometryNodeInputMeshFaceArea'        : [],
    'GeometryNodeInputMeshFaceNeighbors'   : [],
    'GeometryNodeMeshFaceSetBoundaries'    : [],
    'GeometryNodeInputMeshFaceIsPlanar'    : [],
    'GeometryNodeInputShadeSmooth'         : [],
    'GeometryNodeInputMeshIsland'          : [],
    'GeometryNodeInputShortestEdgePaths'   : [],
    'GeometryNodeInputMeshVertexNeighbors' : [],

    # Mesh > Sample
    'GeometryNodeSampleNearestSurface' : [("data_type", "enum")],
    'GeometryNodeSampleUVSurface'      : [("data_type", "enum")],

    # Mesh > Write
    'GeometryNodeSetShadeSmooth' : [],

    # Mesh > Operations
    'GeometryNodeDualMesh'             : [],
    'GeometryNodeEdgePathsToCurves'    : [],
    'GeometryNodeEdgePathsToSelection' : [],
    'GeometryNodeExtrudeMesh'          : [("mode", "enum")],
    'GeometryNodeFlipFaces'            : [],
    'GeometryNodeMeshBoolean'          : [("operation", "enum")],
    'GeometryNodeMeshToCurve'          : [],
    'GeometryNodeMeshToPoints'         : [("mode", "enum")],
    'GeometryNodeMeshToVolume'         : [("resolution_mode", "enum")],
    'GeometryNodeScaleElements'        : [("domain", "enum"),
                                          ("scale_mode", "enum")],
    'GeometryNodeSplitEdges'           : [],
    'GeometryNodeSubdivideMesh'        : [],
    'GeometryNodeSubdivisionSurface'   : [("boundary_smooth", "enum"),
                                          ("uv_smooth", "enum")],
    'GeometryNodeTriangulate'          : [("ngon_method", "enum"),
                                          ("quad_method", "enum")],

    # Mesh > Primitives
    'GeometryNodeMeshCone'      : [("fill_type", "enum")],
    'GeometryNodeMeshCube'      : [],
    'GeometryNodeMeshCylinder'  : [("fill_type", "enum")],
    'GeometryNodeMeshGrid'      : [],
    'GeometryNodeMeshIcoSphere' : [],
    'GeometryNodeMeshCircle'    : [("fill_type", "enum")],
    'GeometryNodeMeshLine'      : [("count_mode", "enum"),
                                   ("mode", "enum")],
    'GeometryNodeMeshUVSphere'  : [],

    # Mesh > Topology
    'GeometryNodeCornersOfFace'      : [],
    'GeometryNodeCornersOfVertex'    : [],
    'GeometryNodeEdgesOfCorner'      : [],
    'GeometryNodeEdgesOfVertex'      : [],
    'GeometryNodeFaceOfCorner'       : [],
    'GeometryNodeOffsetCornerInFace' : [],
    'GeometryNodeVertexOfCorner'     : [],

    # Mesh > UV
    'GeometryNodeUVPackIslands' : [],
    'GeometryNodeUVUnwrap'      : [("method", "enum")],


    # POINT
    'GeometryNodeDistributePointsInVolume' : [("mode", "enum")],
    'GeometryNodeDistributePointsOnFaces'  : [("distribute_method", "enum"),
                                              ("use_legacy_normal", "bool")],
    'GeometryNodePoints'                   : [],
    'GeometryNodePointsToVertices'         : [],
    'GeometryNodePointsToVolume'           : [("resolution_mode", "enum")],
    'GeometryNodeSetPointRadius'           : [],


    # VOLUME
    'GeometryNodeVolumeCube'   : [],
    'GeometryNodeVolumeToMesh' : [("resolution_mode", "enum")],

    
    # SIMULATION
    'GeometryNodeSimulationInput'  : [],
    'GeometryNodeSimulationOutput' : [],


    # MATERIAL
    'GeometryNodeReplaceMaterial'    : [],
    'GeometryNodeInputMaterialIndex' : [],
    'GeometryNodeMaterialSelection'  : [],
    'GeometryNodeSetMaterial'        : [],
    'GeometryNodeSetMaterialIndex'   : [],


    # TEXTURE
    'ShaderNodeTexBrick'       : [("offset", "float"),
                                  ("offset_frequency", "int"),
                                  ("squash", "float"), 
                                  ("squash_frequency", "int")],
    'ShaderNodeTexChecker'     : [],
    'ShaderNodeTexGradient'    : [("gradient_type", "enum")],
    'GeometryNodeImageTexture' : [("extension", "enum"),
                                  ("interpolation", "enum")],
    'ShaderNodeTexMagic'       : [("turbulence_depth", "int")],
    'ShaderNodeTexMusgrave'    : [("musgrave_dimensions", "enum"),
                                  ("musgrave_type", "enum")],
    'ShaderNodeTexNoise'       : [("noise_dimensions", "enum")],
    'ShaderNodeTexVoronoi'     : [("distance", "enum"),
                                  ("feature", "enum"),
                                  ("voronoi_dimensions", "enum")],
    'ShaderNodeTexWave'        : [("bands_direction", "enum"),
                                  ("rings_direction", "enum"),
                                  ("wave_profile", "enum"),
                                  ("wave_type", "enum")],
    'ShaderNodeTexWhiteNoise'  : [("noise_dimensions", "enum")],


    # UTILITIES
    'ShaderNodeMix'           : [("blend_type", "enum"),
                                 ("clamp_factor", "bool"),
                                 ("clamp_result", "bool"),
                                 ("data_type", "enum"),
                                 ("factor_mode", "enum")],
    'FunctionNodeRandomValue' : [("data_type", "enum")],
    'GeometryNodeSwitch'      : [("input_type", "enum")],
    
    # Utilities > Color
    'ShaderNodeValToRGB'        : [("color_ramp", "ColorRamp")],
    'ShaderNodeRGBCurve'        : [("mapping", "CurveMapping")],
    'FunctionNodeCombineColor'  : [("mode", "enum")],
    'ShaderNodeMixRGB'          : [("blend_type", "enum"),
                                   ("use_alpha", "bool"),
                                   ("use_clamp", "bool")], #legacy
    'FunctionNodeSeparateColor' : [("mode", "enum")],
    
    # Utilities > Text
    'GeometryNodeStringJoin'             : [],
    'FunctionNodeReplaceString'          : [],
    'FunctionNodeSliceString'            : [],
    'FunctionNodeStringLength'           : [],
    'GeometryNodeStringToCurves'         : [("align_x", "enum"),
                                            ("align_y", "enum"),
                                            ("font", "Font"), #TODO: font
                                            ("overflow", "enum"),
                                            ("pivot_mode", "enum")],
    'FunctionNodeValueToString'          : [],
    'FunctionNodeInputSpecialCharacters' : [],

    # Utilities > Vector
    'ShaderNodeVectorCurve'  : [("mapping", "CurveMapping")],
    'ShaderNodeVectorMath'   : [("operation", "enum")],
    'ShaderNodeVectorRotate' : [("invert", "bool"),
                                ("rotation_type", "enum")],
    'ShaderNodeCombineXYZ'   : [],
    'ShaderNodeSeparateXYZ'  : [],

    # Utilities > Field
    'GeometryNodeAccumulateField' : [("data_type", "enum"),
                                     ("domain", "enum")],
    'GeometryNodeFieldAtIndex'    : [("data_type", "enum"),
                                     ("domain", "enum")],
    'GeometryNodeFieldOnDomain'   : [("data_type", "enum"),
                                     ("domain", "enum")],

    # Utilities > Math
    'FunctionNodeBooleanMath' : [("operation", "enum")],
    'ShaderNodeClamp'         : [("clamp_type", "enum")],
    'FunctionNodeCompare'     : [("data_type", "enum"),
                                 ("mode", "enum"),
                                 ("operation", "enum")],
    'ShaderNodeFloatCurve'    : [("mapping", "CurveMapping")],
    'FunctionNodeFloatToInt'  : [("rounding_mode", "enum")],
    'ShaderNodeMapRange'      : [("clamp", "bool"),
                                 ("data_type", "enum"),
                                 ("interpolation_type", "enum")], 
    'ShaderNodeMath'          : [("operation", "enum"),
                                 ("use_clamp", "bool")],

    # Utilities > Rotation
    'FunctionNodeAlignEulerToVector' : [("axis", "enum"),
                                        ("pivot_axis", "enum")],
    'FunctionNodeRotateEuler'        : [("space", "enum"),
                                        ("type", "enum")]
}

class NTPGeoNodesOperator(bpy.types.Operator):
    bl_idname = "node.ntp_geo_nodes"
    bl_label = "Geo Nodes to Python"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode : bpy.props.EnumProperty(
        name = "Mode",
        items = [
            ('SCRIPT', "Script", "Copy just the node group to the Blender clipboard"),
            ('ADDON', "Addon", "Create a full addon")
        ]
    )

    geo_nodes_group_name: bpy.props.StringProperty(name="Node Group")
    
    def execute(self, context):
        #find node group to replicate
        nt = bpy.data.node_groups[self.geo_nodes_group_name]

        #set up names to use in generated addon
        nt_var = clean_string(nt.name)

        if self.mode == 'ADDON':
            #find base directory to save new addon
            dir = bpy.path.abspath(context.scene.ntp_options.dir_path)
            if not dir or dir == "":
                self.report({'ERROR'}, 
                            ("NodeToPython: Save your blend file before using "
                            "NodeToPython!"))
                return {'CANCELLED'}

            #save in addons/ subdirectory
            zip_dir = os.path.join(dir, nt_var)
            addon_dir = os.path.join(zip_dir, nt_var)

            if not os.path.exists(addon_dir):
                os.makedirs(addon_dir)
            file = open(f"{addon_dir}/__init__.py", "w")
            
            create_header(file, nt.name)
            class_name = clean_string(nt.name.replace(" ", "").replace('.', ""), 
                                    lower = False)
            init_operator(file, class_name, nt_var, nt.name)
            file.write("\tdef execute(self, context):\n")
        else:
            file = StringIO("")

        #set to keep track of already created node trees
        node_trees = set()

        #dictionary to keep track of node->variable name pairs
        node_vars = {}

        #dictionary to keep track of variables->usage count pairs
        used_vars = {}
        
        def process_geo_nodes_group(node_tree, level, node_vars, used_vars):
            nt_var = create_var(node_tree.name, used_vars)
                
            outer, inner = make_indents(level)

            #initialize node group
            file.write(f"{outer}#initialize {nt_var} node group\n")
            file.write(f"{outer}def {nt_var}_node_group():\n")
            file.write((f"{inner}{nt_var}"
                        f"= bpy.data.node_groups.new("
                        f"type = \'GeometryNodeTree\', "
                        f"name = {str_to_py_str(node_tree.name)})\n"))
            file.write("\n")

            inputs_set = False
            outputs_set = False

            #initialize nodes
            file.write(f"{inner}#initialize {nt_var} nodes\n")
            
            sim_inputs = []

            for node in node_tree.nodes:
                if node.bl_idname == 'GeometryNodeGroup':
                    node_nt = node.node_tree
                    if node_nt is not None and node_nt not in node_trees:
                        process_geo_nodes_group(node_nt, level + 1, node_vars, 
                                                used_vars)
                        node_trees.add(node_nt)
                elif node.bl_idname == 'NodeGroupInput' and not inputs_set:
                    group_io_settings(node, file, inner, "input", nt_var, 
                                      node_tree)
                    inputs_set = True

                elif node.bl_idname == 'NodeGroupOutput' and not outputs_set:
                    group_io_settings(node, file, inner, "output", nt_var, 
                                      node_tree)
                    outputs_set = True

                #create node
                node_var = create_node(node, file, inner, nt_var, 
                                       node_vars, used_vars)
                set_settings_defaults(node, geo_node_settings, file, inner, 
                                      node_var)
                hide_sockets(node, file, inner, node_var)

                if node.bl_idname == 'GeometryNodeGroup':
                    if node.node_tree is not None:
                        file.write((f"{inner}{node_var}.node_tree = "
                                    f"bpy.data.node_groups"
                                    f"[{str_to_py_str(node.node_tree.name)}]\n"))

                elif node.bl_idname == 'ShaderNodeValToRGB':
                    color_ramp_settings(node, file, inner, node_var)

                elif node.bl_idname in curve_nodes:
                    curve_node_settings(node, file, inner, node_var)

                elif node.bl_idname in image_nodes and self.mode == 'ADDON':
                    img = node.image
                    if img is not None and img.source in {'FILE', 'GENERATED', 'TILED'}:
                        save_image(img, addon_dir)
                        load_image(img, file, inner, f"{node_var}.image")

                elif node.bl_idname == 'GeometryNodeSimulationInput':
                    sim_inputs.append(node)

                elif node.bl_idname == 'GeometryNodeSimulationOutput':
                    file.write(f"{inner}#remove generated sim state items\n")
                    file.write(f"{inner}for item in {node_var}.state_items:\n")
                    file.write(f"{inner}\t{node_var}.state_items.remove(item)\n")

                    for i, si in enumerate(node.state_items):
                        socket_type = enum_to_py_str(si.socket_type)
                        name = str_to_py_str(si.name)
                        file.write(f"{inner}#create SSI {name}\n")
                        file.write((f"{inner}{node_var}.state_items.new"
                                    f"({socket_type}, {name})\n"))
                        si_var = f"{node_var}.state_items[{i}]"
                        attr_domain = enum_to_py_str(si.attribute_domain)
                        file.write((f"{inner}{si_var}.attribute_domain = "
                                    f"{attr_domain}\n"))

                if node.bl_idname != 'GeometryNodeSimulationInput':
                    if self.mode == 'ADDON':
                        set_input_defaults(node, file, inner, node_var, addon_dir)
                    else:
                        set_input_defaults(node, file, inner, node_var)
                    set_output_defaults(node, file, inner, node_var)

            #create simulation zones
            for sim_input in sim_inputs:
                sim_input_var = node_vars[sim_input]
                sim_output_var = node_vars[sim_input.paired_output]
                file.write((f"{inner}{sim_input_var}.pair_with_output"
                            f"({sim_output_var})\n"))

                #must set defaults after paired with output
                if self.mode == 'ADDON':
                    set_input_defaults(node, file, inner, node_var, addon_dir)
                else:
                    set_input_defaults(node, file, inner, node_var)
                set_output_defaults(sim_input, file, inner, sim_input_var)
            
            #set look of nodes
            set_parents(node_tree, file, inner, node_vars)
            set_locations(node_tree, file, inner, node_vars)
            set_dimensions(node_tree, file, inner, node_vars)

            #create connections
            init_links(node_tree, file, inner, nt_var, node_vars)
            
            file.write(f"{inner}return {nt_var}\n")

            #create node group
            file.write((f"\n{outer}{nt_var} = "
                        f"{nt_var}_node_group()\n\n"))
            return used_vars
        
        if self.mode == 'ADDON':
            level = 2
        else:
            level = 0
        process_geo_nodes_group(nt, level, node_vars, used_vars)

        def apply_modifier():
            #get object
            file.write(f"\t\tname = bpy.context.object.name\n")
            file.write(f"\t\tobj = bpy.data.objects[name]\n")

            #set modifier to the one we just created
            mod_name = str_to_py_str(nt.name)
            file.write((f"\t\tmod = obj.modifiers.new(name = {mod_name}, "
                        f"type = 'NODES')\n"))
            file.write(f"\t\tmod.node_group = {nt_var}\n")
        if self.mode == 'ADDON':
            apply_modifier()

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

        #alert user that NTP is finished
        if self.mode == 'SCRIPT':
            location = "clipboard"
        else:
            location = dir
        self.report({'INFO'}, 
                    f"NodeToPython: Saved geometry nodes group to {location}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "mode")
    
class NTPGeoNodesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_geo_nodes"
    bl_label = "Select Geo Nodes"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'

        geo_node_groups = [node for node in bpy.data.node_groups 
                           if node.type == 'GEOMETRY']

        for geo_ng in geo_node_groups:
            op = layout.operator(NTPGeoNodesOperator.bl_idname, text=geo_ng.name)
            op.geo_nodes_group_name = geo_ng.name
            
class NTPGeoNodesPanel(bpy.types.Panel):
    bl_label = "Geometry Nodes to Python"
    bl_idname = "NODE_PT_geo_nodes"
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
        row.menu("NODE_MT_ntp_geo_nodes", text="Geometry Nodes")