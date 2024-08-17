# Node Settings Generator
(Instructions may need adjusted depending on your operating system, especially Windows)
1. To create a node settings file, run
    ```
    python3 node_settings_generator/parse_nodes.py x y
    ```
    where `x.y` is the Blender version you want to generate settings up to.
    * Note that the minimum version is hard-coded to 3.0, as there aren't currently plans to extend NodeToPython compatibility to before that version. 