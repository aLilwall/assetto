import bpy
import requests
from . os_handler import file_path

url = "http://68.211.58.117:5000/item/"


def get_items():
    """Get method to retrieve a list of all items saved in the API.
    """
    url = "http://68.211.58.117:5000/items"
    response = requests.get(url)
    item_data = response.json()
    return item_data


def get_item(item_name):
    """Get method to retrieve a 3D model from the API.
    """
    _url = url + item_name
    response = requests.get(_url)
    item_data = response.json()
    return item_data


def delete_item(item_name):
    """Delete method that excludes a 3D model in the API.
    """
    _url = url + item_name
    response = requests.delete(_url)
    status_code = response.status_code
    return status_code


def load_item(item_name):
    """Converts json data retrieved from the API to a .obj file. 
    """
    data = get_item(item_name)
    _data = {**data}
    key_data = _data.keys()
    unpacked_key = [key for key in key_data]
    values_data = _data.values()
    _file_path = file_path + str(*key_data) + ".obj"
    title = f"# Blender 4.4.3\n# www.blender.org\nmtllib {unpacked_key[0]}.mtl\n"

    with open(file=_file_path, mode="w+") as file:
        file.writelines(title)
        file.writelines(f"o {unpacked_key[0]}\n")
        file.writelines(*values_data)

    asset_import(_file_path)


def asset_import(file_path):
    """Export selected object to local drive in a obj file format. 
    """
    bpy.ops.wm.obj_import(filepath=file_path)
