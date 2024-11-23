import argparse
from bs4 import BeautifulSoup
from threading import Thread, Lock
from io import TextIOWrapper
import os
import re
import time
from typing import NamedTuple
import urllib.request

import types_utils

class NTPNodeSetting(NamedTuple):
    name_: str
    type_: types_utils.ST

    def __lt__(self, other):
        return self.name_ < other.name_

class Version(NamedTuple):
    major_: int
    minor_: int

    def tuple_str(self) -> str:
        return f"({self.major_}, {self.minor_})"

    def point_str(self) -> str:
        return f"{self.major_}.{self.minor_}"

class NodeInfo(NamedTuple):
    versions_: list[Version]
    attributes_: dict[NTPNodeSetting, list[Version]]

mutex = Lock()
log_mutex = Lock()
nodes_dict : dict[str, NodeInfo] = {}
types_dict : dict[str, set[str]] = {}
log_file = None

NTP_MIN_VERSION = (3, 0)

def process_attr(attr, section, node: str, version: Version) -> None:
    name_section = attr.find(["code", "span"], class_="sig-name descname")
    
    if not name_section:
        raise ValueError(f"{version.tuple_str()} {node}: Couldn't find name section in\n\t{section}")
    name = name_section.text
    
    type_section = attr.find("dd", class_="field-odd")
    if not type_section:
        raise ValueError(f"{version.tuple_str()} {node}.{name}: Couldn't find type section in\n\t{section}")
    type_text = type_section.text

    with mutex:
        first_word = type_text.split()[0]
        if first_word not in types_dict:
            types_dict[first_word] = {type_text}
        else:
            types_dict[first_word].add(type_text)

    ntp_type = types_utils.get_NTP_type(type_text)
    if ntp_type is None:
        # Read-only attribute, don't add to attribute list
        with log_mutex:
            log_file.write(f"WARNING: {version.tuple_str()} {node}.{name}'s type is being ignored:\n\t{type_text.strip()}\n")
        return

    ntp_setting = NTPNodeSetting(name, ntp_type)
    with mutex:
        if ntp_setting not in nodes_dict[node].attributes_:
            nodes_dict[node].attributes_[ntp_setting] = []
        nodes_dict[node].attributes_[ntp_setting].append(version)

def process_node(node: str, section, version: Version):
    global nodes_dict
    with mutex:
        if node not in nodes_dict:
            nodes_dict[node] = NodeInfo([], {})
        nodes_dict[node].versions_.append(version)

    attrs = section.find_all("dl", class_="py attribute")

    for attr in attrs:
        process_attr(attr, section, node, version)

    datas = section.find_all("dl", class_="py data")
    for data in datas:
        process_attr(data, section, node, version)

def download_file(filepath: str, version: Version, local_path: str) -> bool:
    file_url = f"https://docs.blender.org/api/{version.point_str()}/{filepath}"

    headers_ = {'User-Agent': 'Mozilla/5.0'}

    req = urllib.request.Request(file_url, headers=headers_)

    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))

    NUM_TRIES = 10
    for i in range(NUM_TRIES):
        try:
            with urllib.request.urlopen(req) as response:
                with open(local_path, 'wb') as file:
                    file.write(response.read())
                    break
        except Exception as e:
            if i == NUM_TRIES - 1:
                raise e
            time.sleep(1.0)

    print(f"Downloaded {file_url} to {local_path}")
    return True


def get_subclasses(current: str, parent: str, root_path: str, 
                   version: Version) -> list[str]:
    relative_path = f"bpy.types.{current}.html"
    current_path = os.path.join(root_path, relative_path)

    if not os.path.exists(current_path):
        download_file(relative_path, version, current_path)

    if os.path.getsize(current_path) == 0:
        download_file(relative_path, version, current_path)

    with open(current_path, "r") as current_file:
        current_html = current_file.read()

    soup = BeautifulSoup(current_html, "html.parser")

    main_id = f"{current.lower()}-{parent.lower()}"
    sections = soup.find_all(id=main_id)
    if not sections:
        raise ValueError(f"{version.tuple_str()} {current}: Couldn't find main section with id {main_id}")

    section = sections[0]
    paragraphs = section.find_all("p")
    if len(paragraphs) < 2:
        raise ValueError(f"{version.tuple_str()} {current}: Couldn't find subclass section")

    subclasses_paragraph = paragraphs[1]
    if not subclasses_paragraph.text.strip().startswith("subclasses —"):
        # No subclasses for this type
        process_node(current, section, version)
        return

    subclass_anchors = subclasses_paragraph.find_all("a")
    if not subclass_anchors:
        raise ValueError(f"{version.tuple_str()} {current} No anchors in subclasses paragraph")

    subclass_types = [anchor.get("title") for anchor in subclass_anchors]
    threads: list[Thread] = []
    for type in subclass_types:
        if not type:
            raise ValueError(f"{version.tuple_str()} {current} Type was invalid")
        is_matching = re.match(r"bpy\.types\.(.*)", type)
        if not is_matching:
            raise ValueError(f"{version.tuple_str()} {current}: Type {type} was not of the form \"bpy.types.x\"")
        pure_type = is_matching.group(1)
        if (pure_type == "TextureNode"):
            # unsupported
            continue

        thread = Thread(target=get_subclasses, args=(pure_type, current, root_path, version))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def process_bpy_version(version: Version) -> None:
    print(f"Processing version {version.point_str()}")

    current = "NodeInternal"
    parent = "Node"

    root_path = os.path.join(bpy_docs_path, f"{version.point_str()}/")

    get_subclasses(current, parent, root_path, version)

def generate_versions(max_version_inc: Version) -> list[Version]:
    BLENDER_3_MAX_VERSION = 6

    versions = [Version(3, i) for i in range(0, BLENDER_3_MAX_VERSION + 1)]
    versions += [Version(4, i) for i in range(0, max_version_inc[1] + 1)]
    
    #lazy max version check
    for version in versions[::-1]:
        if version > max_version_inc:
            versions.remove(version)

    return versions

def subminor(version: Version) -> tuple:
    return (version[0], version[1], 0)

def get_min_version(versions: list[Version]) -> Version:
    min_version = min(versions)

    if min_version != NTP_MIN_VERSION:
        return min_version
    else:
        return None

def get_max_version(versions: list[Version], blender_versions: list[Version]
                   ) -> Version:
    max_v_inclusive = max(versions)
    max_v_inclusive_index = blender_versions.index(max_v_inclusive)
    max_v_exclusive = blender_versions[max_v_inclusive_index + 1]

    if max_v_exclusive != blender_versions[-1]:
        return max_v_exclusive
    else:
        return None

def write_imports(file: TextIOWrapper):
    file.write("from enum import Enum, auto\n")
    file.write("from typing import NamedTuple\n")
    file.write("\n")

def write_st_enum(file: TextIOWrapper):
    file.write("class ST(Enum):\n")
    file.write("\t\"\"\"\n\tSettings Types\n\t\"\"\"\n")

    for setting_type in types_utils.ST:
        file.write(f"\t{setting_type.name} = auto()\n")
    
    file.write("\n")

def write_ntp_node_setting_class(file: TextIOWrapper):
    file.write("class NTPNodeSetting(NamedTuple):\n")
    file.write("\tname_: str\n")
    file.write("\tst_: ST\n")
    file.write(f"\tmin_version_: tuple = {subminor(NTP_MIN_VERSION)}\n")
    file.write(f"\tmax_version_: tuple = {subminor(NTP_MAX_VERSION_EXC)}\n")
    file.write("\n")

def write_node_info_class(file: TextIOWrapper):
    file.write("class NodeInfo(NamedTuple):\n")
    file.write("\tattributes_: list[NTPNodeSetting]\n")
    file.write(f"\tmin_version_: tuple = {subminor(NTP_MIN_VERSION)}\n")
    file.write(f"\tmax_version_: tuple = {subminor(NTP_MAX_VERSION_EXC)}\n")
    file.write("\n")

def write_ntp_node_settings(node_info: NodeInfo, file: TextIOWrapper,
                            node_min_v: Version, node_max_v: Version):
    attr_dict = node_info.attributes_
    file.write("\n\t\t[")
    attrs_exist = len(attr_dict.items()) > 0
    if attrs_exist:
        file.write("\n")
    sorted_attrs = dict(sorted(attr_dict.items()))
    for attr, attr_versions in sorted_attrs.items():
        min_version_str = ""
        attr_min_version = get_min_version(attr_versions)
        if attr_min_version != None and attr_min_version != node_min_v:
            min_version_str = f", min_version_={subminor(attr_min_version)}"

        max_version_str = ""
        attr_max_version = get_max_version(attr_versions, versions)
        if attr_max_version != None and attr_max_version != node_max_v:
            max_version_str = f", max_version_={subminor(attr_max_version)}"

        file.write(f"\t\t\tNTPNodeSetting(\"{attr.name_}\", ST.{attr.type_.name}"
                    f"{min_version_str}{max_version_str}),\n")

    if attrs_exist:
        file.write("\t\t")
    file.write("]")

def write_node(name: str, node_info: NodeInfo, file: TextIOWrapper):
    file.write(f"\t\'{name}\' : NodeInfo(")

    node_min_v = get_min_version(node_info.versions_)
    node_max_v = get_max_version(node_info.versions_, versions)

    write_ntp_node_settings(node_info, file, node_min_v, node_max_v)

    if node_min_v != None:
        file.write(f",\n\t\tmin_version_ = {subminor(node_min_v)}")
    if node_max_v != None:
        file.write(f",\n\t\tmax_version_ = {subminor(node_max_v)}")

    file.write("\n\t),\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('max_major_version', type=int, 
                        help="Max major version (inclusive) of Blender to generate node settings for")
    parser.add_argument('max_minor_version', type=int, 
                        help="Max minor version (inclusive) of Blender to generate node settings for")
    args = parser.parse_args()

    current_path = os.path.dirname(os.path.realpath(__file__))
    bpy_docs_path = os.path.join(current_path, "bpy_docs")

    NTP_MAX_VERSION_INC = Version(args.max_major_version, args.max_minor_version)
    max_version_path = os.path.join(bpy_docs_path, f"{NTP_MAX_VERSION_INC.point_str()}")

    versions = generate_versions(NTP_MAX_VERSION_INC)

    output_dir_path = os.path.join(current_path, "output")
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    log_filepath = os.path.join(output_dir_path, "log.txt")
    log_file = open(log_filepath, 'w')

    for version in versions:
        process_bpy_version(version)

    NTP_MAX_VERSION_EXC = (NTP_MAX_VERSION_INC[0], NTP_MAX_VERSION_INC[1] + 1)
    versions.append(NTP_MAX_VERSION_EXC)

    sorted_nodes = dict(sorted(nodes_dict.items()))

    output_filepath = os.path.join(output_dir_path, "node_settings.py")

    with open(output_filepath, 'w') as file:
        print(f"Writing settings to {output_filepath}")

        write_imports(file)

        write_st_enum(file)

        write_ntp_node_setting_class(file)
       
        write_node_info_class(file)

        file.write("node_settings : dict[str, NodeInfo] = {\n")
        
        for name, node_info in sorted_nodes.items():
            write_node(name, node_info, file)

        file.write("}")

        print("Successfully finished")

    sorted_types = dict(sorted(types_dict.items()))
    log_file.write("\nTypes encountered:\n")
    for key, value in types_dict.items():
        log_file.write(f"{key}\n")
        for string in value:
            log_file.write(f"\t{string}\n")