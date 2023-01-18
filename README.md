# Node to Python
<img 
     src="https://github.com/BrendanParmer/NodeToPython/blob/main/img/ntp.jpg" 
     alt="Node To Python" 
     width = "400" 
     height = "400"
    >
    
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/BrendanParmer/NodeToPython)](https://github.com/BrendanParmer/NodeToPython/releases) [![GitHub](https://img.shields.io/github/license/BrendanParmer/NodeToPython)](https://github.com/BrendanParmer/NodeToPython/blob/main/LICENSE) ![](https://visitor-badge.laobi.icu/badge?page_id=BrendanParmer.NodeToPython)
 
## About
A Blender add-on to create add-ons! This addo-on will take your Geometry Nodes or Materials and convert them into legible Python add-ons!

It automatically handles node layout, default values, sub-node groups, naming, and more! 

I think Blender's node-based editors are powerful, yet accessible tools, and I wanted to make scripting them easier for add-on creators. Combining Python with node based setups allows you to do things that would otherwise be tedious or impossible, such as
* `for` loops
* creating different node trees for different versions or settings
* interfacing with other parts of the software or properties of an object

NodeToPython recreates the node networks for you, so you can focus on the good stuff. 

## Supported Versions
NodeToPython v2.0 is compatible with Blender 3.0 - 3.4 on Windows, macOS, and Linux. I generally try to update the addon to handle new nodes around the beta release of each update.

## Installation
1. Download the .zip file from the [latest release](https://github.com/BrendanParmer/NodeToPython/releases)
2. In Blender, navigate to `Edit > Preferences > Add-ons`
3. Click Install, and find where you downloaded the zip file. Then hit the `Install Add-on` button, and you're done!

## Usage
Once you've installed the add-on, you'll see a new tab to the side of a Node Editor. 

In the tab, there's panels to create add-ons for Geometry Nodes and Materials, each with a drop-down menu. 

Just select the one you want, and soon a python file will be created in an `addons` folder located in the folder where your blend file is.

From here, you can install it like a regular add-on.

## Future
* Expansion to Compositing nodes
* Copy over referenced assets in the scene (Collections, Objects, Materials, Textures, etc.)
* Automatically format code to be PEP8 compliant

## Potential Issues
* As of version 2.0.0, the add-on will not set default values for
    * Collections
    * Materials
    * Objects
    * Textures
    * Scripts
    * IES files
    * Filepaths

    as they won't exist in every blend file. I'm expecting to support some of these in the future.

    There are a few nodes that don't set their default values like other ones, though these should also soon be supported. 

## Bug Reports and Suggestions

When submitting an issue, please include 

* Your version of Blender
* Your operating system
* A short description of what you were trying to accomplish, or steps to reproduce the issue.
* Sample blend files are more than welcome!

Suggestions for how to improve the add-on are more than welcome!