import json
import bpy
import requests
from bpy.props import StringProperty, PointerProperty
from . import asset_exporter
from . import asset_loader
from . import os_handler

bl_info = {
    "name": "assetto",
    "author": "peq.Muro",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar > assetto",
    "description": "Export and save your 3D models as assets to the Cloud.",
    "category": "Asset Creation",
}


class AssetCreator(bpy.types.Panel):
    """Creates a panel on the sidebar.
    """
    bl_label = "assetto"
    bl_idname = "OBJECT_PT_asset-to-cloud"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "assetto"

    def draw_header(self, context):
        """Title
        """
        layout = self.layout
        layout.label(text="peqMuro's")

    def draw(self, context):
        """Buttons and search bar.
        """
        layout = self.layout
        row = layout.row()
        row.operator("asset_loader.asset_get_items_operator")
        layout.label(text="Export Tools:")
        row = layout.row()
        row.operator("asset_creator.asset_exporter_operator")
        row = layout.row()
        row.operator("asset_creator.asset_post_operator")
        row = layout.row()
        row.prop(self, "filepath")
        row = layout.row()
        row.label(text="Import Tools:")
        props = context.scene.my_addon_props
        layout.prop(props, "my_text")
        layout.operator("asset_creator.asset_get_item_operator")
        layout.operator("asset_creator.asset_delete_item_operator")


class DeleteItem(bpy.types.Operator):
    """Send data to the delete method.
    """
    bl_label = "Delete Asset"
    bl_idname = "asset_creator.asset_delete_item_operator"

    def execute(self, context):
        props = context.scene.my_addon_props
        text = props.my_text
        result = asset_loader.delete_item(text)
        if result == 200:
            self.report({'INFO'}, "Document deleted.")
            return {'FINISHED'}
        elif result == 404:
            self.report({'INFO'}, "Document not found.")
            return {'FINISHED'}


class GetAsset(bpy.types.Operator):
    """Send data to the get method.
    """
    # Uses data passed in the search bar
    bl_label = "Get Asset"
    bl_idname = "asset_creator.asset_get_item_operator"

    def execute(self, context):
        try:
            props = context.scene.my_addon_props
            text = props.my_text

            asset_loader.load_item(text)

            self.report({'INFO'}, f"Document loaded: {text}")
            print(f"User entered: {text}")
            return {'FINISHED'}
        except json.decoder.JSONDecodeError:
            self.report({'INFO'}, "Asset not found.")
            return {'CANCELLED'}


class GetAllAssets(bpy.types.Operator):
    """Send data to the get method.
    """
    bl_label = "Get Assets List"
    bl_idname = "asset_loader.asset_get_items_operator"

    def execute(self, context):
        try:
            items_list = asset_loader.get_items()
            if not items_list:
                self.report({'INFO'}, "No documents in Cloudant.")
            else:
                self.report({"INFO"}, f"Cloudant documents: {items_list}")
            return {'FINISHED'}
        except requests.exceptions.JSONDecodeError:
            self.report({'INFO'}, "No database in Cloudant.")
            return {'CANCELLED'}


class MyAddonProperties(bpy.types.PropertyGroup):
    """Create a search bar in the Panel.
    """
    my_text: StringProperty(name="Asset_Name", default="")

    def execute():
        item = bpy.context.scene.my_addon_props.my_text
        report({"INFO"}, item)


class ExportAsset(bpy.types.Operator):
    """Export 3D model to your local drive.
    """
    bl_label = "Export Asset"
    bl_idname = "asset_creator.asset_exporter_operator"

    def execute(self, context):
        try:
            asset_exporter.asset_export()
            self.report({"INFO"}, "Asset exported with success.")
            return {"FINISHED"}
        except IndexError:
            self.report({"INFO"}, "Error: No object selected.")
            return {"CANCELLED"}


class PostAsset(bpy.types.Operator):
    """Export 3D model to the Cloud.
    """
    bl_label = "Post Asset"
    bl_idname = "asset_creator.asset_post_operator"

    def execute(self, context):
        try:
            response = asset_exporter.post_item()
            self.report({"INFO"}, response.text)
            return {"FINISHED"}
        except IndexError:
            self.report({"INFO"}, "Error: No object selected.")
            return {"CANCELLED"}
        except FileNotFoundError:
            self.report({"INFO"}, "Error: Export asset before post.")
            return {"CANCELLED"}


def register():
    bpy.utils.register_class(AssetCreator)
    bpy.utils.register_class(GetAllAssets)
    bpy.utils.register_class(ExportAsset)
    bpy.utils.register_class(PostAsset)
    bpy.utils.register_class(GetAsset)
    bpy.utils.register_class(DeleteItem)
    bpy.utils.register_class(MyAddonProperties)
    bpy.types.Scene.my_addon_props = PointerProperty(type=MyAddonProperties)


def unregister():
    bpy.utils.unregister_class(AssetCreator)
    bpy.utils.unregister_class(GetAllAssets)
    bpy.utils.unregister_class(ExportAsset)
    bpy.utils.unregister_class(PostAsset)
    bpy.utils.unregister_class(GetAsset)
    bpy.utils.unregister_class(DeleteItem)
    bpy.utils.unregister_class(MyAddonProperties)
    del bpy.types.Scene.my_addon_props


if __name__ == "__main__":
    register()
