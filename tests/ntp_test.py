import pathlib
import unittest

class NTPTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo = str(pathlib.Path(__file__).parent.parent)

        import bpy
        bpy.ops.wm.read_factory_settings(
            use_factory_startup_app_template_only = True
        )

        repo_module = "test_repo"
        new_repo = bpy.context.preferences.extensions.repos.new(
            name = "NodeToPython",
            module = repo_module,
            custom_directory = repo,
            source = 'USER'
        )
        cls.module_path = f"bl_ext.{repo_module}.NodeToPython"
        bpy.ops.preferences.addon_enable(module = cls.module_path)

    @classmethod
    def tearDownClass(cls):
        import bpy
        bpy.ops.preferences.addon_disable(module = cls.module_path)