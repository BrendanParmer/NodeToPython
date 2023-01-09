# Node to Python
<img 
     src="https://github.com/BrendanParmer/NodeToPython/blob/main/img/ntp.jpg" 
     alt="Node To Python" 
     width = "400" 
     height = "400"
    >
    
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/BrendanParmer/NodeToPython)](https://github.com/BrendanParmer/NodeToPython/releases) [![GitHub](https://img.shields.io/github/license/BrendanParmer/NodeToPython)](https://github.com/BrendanParmer/NodeToPython/blob/main/LICENSE) ![](https://visitor-badge.laobi.icu/badge?page_id=BrendanParmer.NodeToPython)
 
## About
A Blender add-on to create add-ons! This script will take your Geometry Node group and convert it into a legible Python script. 

It automatically handles node layout, default values, sub-node groups, naming, and more! 

I think Geometry Nodes is a powerful tool that's fairly accessible to people. I wanted to make scripting node groups easier for add-on creators in cases when Python is needed, as you don't need to recreate the whole node tree from scratch to do things like
* `for` loops
* different node trees for different versions or settings
* interfacing with other parts of the software. 

NodeToPython is compatible with Blender 3.0-3.4

## Supported Versions
Blender 3.0 - 3.4

* Once the 3.5 beta drops, I'll start adding nodes from that release

## Installation and Usage
Download `node_to_python.py`, and install it to Blender like other add-ons. Then, go to `Object > Node to Python`, and type in the name of your node group. It will then save an add-on to where your blend file is stored.

## Future
* Expansion to Shader and Compositing nodes
* Copy over referenced assets in the scene (Collections, Objects, Materials, Textures, etc.)
* Automatically format code to be PEP8 compliant

## Potential Issues
* As of version 1.2.1, the add-on will not set default values for
    * Collections
    * Images
    * Materials
    * Objects
    * Textures

    as they won't exist in every blend file. I plan on implementing these soon.

## Bug Reports and Suggestions

When submitting an issue, please include 

* Your version of Blender
* Your operating system
* A short description of what you were trying to accomplish, or steps to reproduce the issue

If you don't mind sharing a blend file, that helps a lot!

Suggestions for how to improve the add-on are more than welcome!

