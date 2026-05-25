import pathlib
import subprocess

blender_location = "~/Software/blender"

blender_versions = [
    "4.2.9",
    "4.3.2",
    "4.4.3",
    "4.5.9",
    "5.0.1",
    "5.1.1"
]

tests_dir = pathlib.Path(__file__).parent

for version in blender_versions:
    subprocess.run(
        [
            f"{blender_location}/{version}/blender --background "
            f"--factory-startup --python {tests_dir}/__init__.py"
        ],
        shell=True, check=True
    )
    print(f"Done testing version {version}")
    print(f"{"-" * 100}\n")