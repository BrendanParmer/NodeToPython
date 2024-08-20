import bpy
from bpy.types import Panel
from bpy.types import Menu
from .operator import NTPCompositorOperator

class NTPCompositorPanel(Panel):
    bl_label = "Compositor to Python"
    bl_idname = "NODE_PT_ntp_compositor"
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
        scenes_row = layout.row()
        
        # Disables menu when there are no compositing node groups
        scenes = [scene for scene in bpy.data.scenes if scene.node_tree]
        scenes_exist = len(scenes) > 0
        scenes_row.enabled = scenes_exist
        
        scenes_row.alignment = 'EXPAND'
        scenes_row.operator_context = 'INVOKE_DEFAULT'
        scenes_row.menu("NODE_MT_ntp_comp_scenes", 
                        text="Scene Compositor Nodes")

        groups_row = layout.row()
        groups = [node_tree for node_tree in bpy.data.node_groups 
                  if node_tree.bl_idname == 'CompositorNodeTree']
        groups_exist = len(groups) > 0
        groups_row.enabled = groups_exist

        groups_row.alignment = 'EXPAND'
        groups_row.operator_context = 'INVOKE_DEFAULT'
        groups_row.menu("NODE_MT_ntp_comp_groups", 
                        text="Group Compositor Nodes")

class NTPCompositorScenesMenu(Menu):
    bl_idname = "NODE_MT_ntp_comp_scenes"
    bl_label = "Select "
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for scene in bpy.data.scenes:
            if scene.node_tree:
                op = layout.operator(NTPCompositorOperator.bl_idname, 
                                     text=scene.name)
                op.compositor_name = scene.name
                op.is_scene = True

class NTPCompositorGroupsMenu(Menu):
    bl_idname = "NODE_MT_ntp_comp_groups"
    bl_label = "Select "
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = 'INVOKE_DEFAULT'
        for node_group in bpy.data.node_groups:
            if node_group.bl_idname == 'CompositorNodeTree':
                op = layout.operator(NTPCompositorOperator.bl_idname, 
                                     text=node_group.name)
                op.compositor_name = node_group.name
                op.is_scene = False