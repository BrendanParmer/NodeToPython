# Node to Python
<img 
     src="https://github.com/BrendanParmer/NodeToPython/blob/main/img/ntp.jpg" 
     alt="Node To Python" 
     width = "400" 
     height = "400"
    >
## About
A Blender add-on to create add-ons! This script will take your Geometry Node group and convert it into a legible Python script. 

It automatically handles node layout, default values, sub-node groups, naming, and more! 

I think Geometry Nodes is a powerful tool that's fairly accessible to people, and I wanted to create a lightweight, faster way of distributing them than just passing around blend files. It also makes scripting Geometry Nodes easier for add-on creators in cases when Python is needed, as you don't need to recreate the whole node tree from scratch just to add in functionality like a `for` loop or interfacing with other parts of the software. 

NodeToPython is compatible with Blender 3.0-3.3

## Installation and Usage
Download `node_to_python.py`, and install it to Blender like other add-ons. Then, go to `Object > Node to Python`, and type in the name of your node group. It will then save an add-on to where your blend file is stored.

## Future
* Expansion to Shader and Compositing nodes
* Copy over referenced assets in the scene (Collections, Objects, Materials, Textures, etc.)
* Automatically format code to be PEP8 compliant

## Potential Issues
* This should work on Unix-like systems (macOS, Linux), but I haven't tested it on Windows yet. If you use Windows, please let me know or create an issue.
* Make sure all your group inputs and outputs have different names, or it won't be able to find the appropriate sockets (this is best practice anyways!)
* As of version 1.0.0, the add-on will not set default values for
    * Collections
    * Images
    * Materials
    * Objects
    * Textures

    as they won't exist in every blend file. In the future, I may have the script automatically recreate these assets, espcially with materials. 
