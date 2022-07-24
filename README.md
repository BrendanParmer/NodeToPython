# Node to Python
## About
A Blender add-on to create add-ons! This script will take your Geometry Node group and convert it into a legible Python script.

It automatically handles node layout, default values, sub-node groups, naming, and more! 

## Installation and Usage
Simply download `node_to_python.py`, and install it to Blender like other add-ons. Then, go to `Object > Node to Python`, and type in the name of your node group. It will then save an add-on to the folder your blend file is stored in.

## Future
* Expansion to Shader and Compositing nodes
* Copy over referenced assets in the scene (Collections, Objects, Materials, Textures, etc.)
* Automatically format code to be PEP8 compliant

## Potential Issues
* This should work on Unix-like systems (macOS, Linux), but I haven't tested it on Windows yet. If you use Windows, please let me know if you encounter any issues. 
* Make sure all your group inputs and outputs have different names, or it won't be able to find the appropriate sockets (this is best practice anyways!)
* As of version 1.0.0, the add-on will not set default values for
    * Collections
    * Images
    * Materials
    * Objects
    * Textures

    These are somewhat messier to deal with, though this may be possible in future versions.