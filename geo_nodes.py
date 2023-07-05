import bpy
import os

from .utils import *
from io import StringIO

geo_node_settings = {
    # Attribute nodes
    "GeometryNodeAttributeStatistic" : ["data_type", "domain"],
    "GeometryNodeAttributeDomainSize" : ["component"],

    "GeometryNodeBlurAttribute" : ["data_type"],
    "GeometryNodeCaptureAttribute" : ["data_type", "domain"],
    "GeometryNodeStoreNamedAttribute" : ["data_type", "domain"],
    "GeometryNodeAttributeTransfer" : ["data_type", "mapping"],

    # Input Nodes
    # Input > Constant
    "FunctionNodeInputBool" : ["boolean"],
    "FunctionNodeInputColor" : ["color"],
    "FunctionNodeInputInt" : ["integer"],
    "GeometryNodeInputMaterial" : ["material"],
    "FunctionNodeInputString" : ["string"],
    "FunctionNodeInputVector" : ["vector"],

    # Input > Scene
    "GeometryNodeCollectionInfo" : ["transform_space"],
    "GeometryNodeObjectInfo" : ["transform_space"],

    # Output Nodes
    "GeometryNodeViewer" : ["domain"],

    # Geometry Nodes
    # Geometry > Read
    "GeometryNodeInputNamedAttribute" : ["data_type"],

    # Geometry > Sample
    "GeometryNodeProximity" : ["target_element"],
    "GeometryNodeRaycast" : ["data_type", "mapping"],
    "GeometryNodeSampleIndex" : ["data_type", "domain", "clamp"],
    "GeometryNodeSampleNearest" : ["domain"],

    # Geometry > Operations
    "GeometryNodeDeleteGeometry" : ["domain", "mode"],
    "GeometryNodeDuplicateElements" : ["domain"],
    "GeometryNodeMergeByDistance" : ["mode"],
    "GeometryNodeSeparateGeometry" : ["domain"],


    # Curve
    # Curve > Read
    "GeometryNodeCurveHandleTypeSelection" : ["mode", "handle_type"],

    # Curve > Sample
    "GeometryNodeSampleCurve" : ["data_type", "mode", "use_all_curves"],

    # Curve > Write
    "GeometryNodeSetCurveNormal" : ["mode"],
    "GeometryNodeSetCurveHandlePositions" : ["mode"],
    "GeometryNodeCurveSetHandles" : ["mode", "handle_type"],
    "GeometryNodeCurveSplineType" : ["spline_type"],

    # Curve > Operations
    "GeometryNodeCurveToPoints" : ["mode"],
    "GeometryNodeFillCurve" : ["mode"], 
    "GeometryNodeFilletCurve" : ["mode"],
    "GeometryNodeResampleCurve" : ["mode"],
    "GeometryNodeTrimCurve" : ["mode"],

    # Curve > Primitives
    "GeometryNodeCurveArc" : ["mode"],
    "GeometryNodeCurvePrimitiveBezierSegment" : ["mode"],
    "GeometryNodeCurvePrimitiveCircle" : ["mode"],
    "GeometryNodeCurvePrimitiveLine" : ["mode"],
    "GeometryNodeCurvePrimitiveQuadrilateral" : ["mode"],


    # Mesh Nodes
    # Mesh > Sample
    "GeometryNodeSampleNearestSurface" : ["data_type"],
    "GeometryNodeSampleUVSurface" : ["data_type"],

    # Mesh > Operations
    "GeometryNodeExtrudeMesh" : ["mode"],
    "GeometryNodeMeshBoolean" : ["operation"],
    "GeometryNodeMeshToPoints" : ["mode"],
    "GeometryNodeMeshToVolume" : ["resolution_mode"],
    "GeometryNodeScaleElements" : ["domain", "scale_mode"],
    "GeometryNodeSubdivisionSurface" : ["uv_smooth", "boundary_smooth"],
    "GeometryNodeTriangulate" : ["quad_method", "ngon_method"],

    # Mesh > Primitives
    "GeometryNodeMeshCone" : ["fill_type"],
    "GeometryNodeMeshCylinder" : ["fill_type"],
    "GeometryNodeMeshCircle" : ["fill_type"],
    "GeometryNodeMeshLine" : ["mode"],

    # Mesh > UV
    "GeometryNodeUVUnwrap" : ["method"],


    # Point Nodes
    "GeometryNodeDistributePointsInVolume" : ["mode"],
    "GeometryNodeDistributePointsOnFaces" : ["distribute_method"],
    "GeometryNodePointsToVolume" : ["resolution_mode"],

    # Volume Nodes
    "GeometryNodeVolumeToMesh" : ["resolution_mode"],


    # Texture Nodes
    "ShaderNodeTexBrick" : ["offset", "offset_frequency", "squash", 
                            "squash_frequency"],
    "ShaderNodeTexGradient" : ["gradient_type"],
    "GeometryNodeImageTexture" : ["interpolation", "extension"],
    "ShaderNodeTexMagic" : ["turbulence_depth"],
    "ShaderNodeTexNoise" : ["noise_dimensions"],
    "ShaderNodeTexVoronoi" : ["voronoi_dimensions", "feature", "distance"],
    "ShaderNodeTexWave" : ["wave_type", "bands_direction", "wave_profile"],
    "ShaderNodeTexWhiteNoise" : ["noise_dimensions"],


    # Utilities
    # Utilities > Color
    "FunctionNodeCombineColor" : ["mode"],
    "ShaderNodeMixRGB" : ["blend_type", "use_clamp"], #legacy
    "FunctionNodeSeparateColor" : ["mode"],
    
    # Utilities > Text
    "GeometryNodeStringToCurves" : ["overflow", "align_x", "align_y", 
                                    "pivot_mode"],

    # Utilities > Vector
    "ShaderNodeVectorMath" : ["operation"],
    "ShaderNodeVectorRotate" : ["rotation_type", "invert"],

    # Utilities > Field
    "GeometryNodeAccumulateField" : ["data_type", "domain"],
    "GeometryNodeFieldAtIndex" : ["data_type", "domain"],
    "GeometryNodeFieldOnDomain" : ["data_type", "domain" ],

    # Utilities > Math
    "FunctionNodeBooleanMath" : ["operation"],
    "ShaderNodeClamp" : ["clamp_type"],
    "FunctionNodeCompare" : ["data_type", "operation", "mode"],
    "FunctionNodeFloatToInt" : ["rounding_mode"],
    "ShaderNodeMapRange" : ["data_type", "interpolation_type", "clamp"], 
    "ShaderNodeMath" : ["operation", "use_clamp"],

    # Utilities > Rotate
    "FunctionNodeAlignEulerToVector" : ["axis", "pivot_axis"],
    "FunctionNodeRotateEuler" : ["type", "space"],

    # Utilities > General
    "ShaderNodeMix" : ["data_type", "blend_type", "clamp_result", 
                       "clamp_factor", "factor_mode"],
    "FunctionNodeRandomValue" : ["data_type"],
    "GeometryNodeSwitch" : ["input_type"]
}

curve_nodes = {'ShaderNodeFloatCurve', 
               'ShaderNodeVectorCurve', 
               'ShaderNodeRGBCurve'}

image_nodes = {'GeometryNodeInputImage'}

class GeoNodesToPython(bpy.types.Operator):
    bl_idname = "node.geo_nodes_to_python"
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
    
class SelectGeoNodesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_ntp_geo_nodes_selection"
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