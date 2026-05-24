from ntp_test import NTPTest

class TestExtension(NTPTest):
    """
    @classmethod
    def setUpClass(cls):
        repo = str(Path(__file__).parent.parent)

        import bpy
        bpy.ops.wm.read_factory_settings(use_factory_startup_app_template_only=True)

        repo_module = "test_repo"
        new_repo = bpy.context.preferences.extensions.repos.new(
            name="NodeToPython",
            module=repo_module,
            custom_directory=repo,
            source='USER'
        )
        cls.module_path = f"bl_ext.{repo_module}.NodeToPython"
        bpy.ops.preferences.addon_enable(module=cls.module_path)
    """
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
    """
    @classmethod
    def tearDownClass(cls):
        import bpy
        bpy.ops.preferences.addon_disable(module=cls.module_path)
    """