import os
import re
import json
import requests
import bpy
from . os_handler import file_path

url = "http://127.0.0.1:5000/item"


def data_extractor():
    """ Opens the original file and returns it's data.
    """
    file_name = bpy.context.selected_objects[0].name

    if os.name == "nt":
        sep = "\\"
    else:
        sep = "/"

    _file_path = file_path + sep + file_name

    with open(file=_file_path, mode="r") as file:
        data = file.read()
        return data


def extract_name(file):
    """Extract the object name from the obj file.
    """
    name = re.findall("o\s(\w+)", file)
    name = name[0]
    return name


def extract_vertices(file):
    """Extract the position of vertices from a obj file
    """
    vertices = re.findall(
        "[n-nv-vs-st]+\s[-?\d\.\d{0,6}\s]*[-?\d\.\d{1,6}\s]*[-?\d{0,1}\.\d{0,6}]*", file)
    return vertices


def extract_faces(file):
    """Extract the position of faces from a obj file.
    """
    faces = re.findall("f\s(?:\d{1,3}/\d{1,3}/\d{1,3}\s)+", file)
    return faces


def conv_obj_to_json():
    """Use data extracted from the original file and writes a json file from it.
    """
    content = data_extractor()
    name = extract_name(content)
    vertices = extract_vertices(content)
    faces = extract_faces(content)

    data = {name: [*vertices, *faces]}

    file = json.dumps(data)
    print(type(file))
    return json.loads(file)


def post_item():
    """Post method the send a json file containing all data extracted from the obj file.
    """
    asset_export()
    json_object = conv_obj_to_json()
    response = requests.post(url, json=json_object)
    return response


def asset_export():
    """Export selected 3D Model to a obj file.
    """
    # Save the scene to a Wavefront OBJ file.
    file_name = bpy.context.selected_objects[0].name

    if os.name == "nt":
        sep = "\\"
    else:
        sep = "/"

    _file_path = file_path + sep + file_name

    bpy.ops.wm.obj_export(filepath=_file_path,
                          apply_modifiers=True, export_selected_objects=True)
