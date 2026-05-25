import pathlib
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    path = str(pathlib.Path(__file__).parent)
    suite = loader.discover(path)
    runner = unittest.TextTestRunner(buffer=True)
    runner.run(suite)

    import bpy
    bpy.ops.wm.quit_blender()