from ntp_test import NTPTest

class TestExtension(NTPTest):
    def test_disable_enable(self):
        try:
            import bpy
            bpy.ops.preferences.addon_disable(module=self.module_path)
            bpy.ops.preferences.addon_enable(module=self.module_path)
        except Exception as e:
            self.fail(str(e))

    def test_has_ntp_props(self):
        import bpy

        self.assertTrue(hasattr(bpy.context.scene, "ntp_options"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_compositor_node_group_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_scene_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_geometry_node_group_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_light_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_line_style_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_material_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_shader_node_group_slots"))
        self.assertTrue(hasattr(bpy.context.scene, "ntp_world_slots"))