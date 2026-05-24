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

        ntp_props = [
            "ntp_options",
            "ntp_compositor_node_group_slots",
            "ntp_scene_slots",
            "ntp_geometry_node_group_slots",
            "ntp_light_slots",
            "ntp_line_style_slots",
            "ntp_material_slots",
            "ntp_shader_node_group_slots",
            "ntp_world_slots"
        ]

        for prop in ntp_props:
            self.assertTrue(hasattr(bpy.context.scene, prop))