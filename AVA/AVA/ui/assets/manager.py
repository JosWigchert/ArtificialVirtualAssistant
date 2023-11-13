import os, imghdr
import customtkinter as ctk
from PIL import Image


class AssetManager:
    def __init__(self):
        self.assets = {}

        # loop through assets folder and load images
        dir = self.sanitize_path("AVA/AVA/ui/assets")
        for filename in os.listdir(dir):
            file = self.sanitize_path(os.path.join(dir, filename))
            self.add(".".join(filename.split(".")[0:-1]), file)

    def add(self, name: str, asset: str, dark_asset: str = None):
        try:
            if imghdr.what(asset) is not None:
                loaded_asset = self.load_image(asset)
                loaded_dark_asset = (
                    self.load_image(dark_asset) if dark_asset else loaded_asset
                )

                image = ctk.CTkImage(
                    light_image=loaded_asset, dark_image=loaded_dark_asset
                )

                self.assets[name] = {
                    "type": "image",
                    "data": image,
                }
        except:
            pass

    def load_image(self, path: str) -> Image:
        if os.path.exists(path):
            return Image.open(path)
        else:
            print(f"Image not found at path: {path}")
            return None

    def get(self, name: str):
        if name in self.assets:
            return self.assets[name]["data"]
        else:
            return None

    def sanitize_path(self, path: str) -> str:
        return path.replace("\\", "/").replace("/", os.sep)


assetManager = AssetManager()
