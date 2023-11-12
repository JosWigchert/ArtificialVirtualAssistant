import os, imghdr
import customtkinter as ctk
from PIL import Image


class AssetManager:
    def __init__(self):
        self.assets = {}

        # loop through assets folder and load images
        dir = "AVA\\AVA\\ui\\assets"
        for filename in os.listdir(dir):
            file = os.path.join(dir, filename)
            self.add(".".join(filename.split(".")[0:-1]), file)

        print(self.assets)

    def add(self, name: str, asset: str, dark_asset: str = None):
        try:
            if imghdr.what(asset) is not None:
                loaded_asset = self.load_image(asset)
                loaded_dark_asset = (
                    self.load_image(dark_asset) if dark_asset else loaded_asset
                )

                image = (
                    ctk.CTkImage(
                        light_image=loaded_asset,
                        dark_image=dark_asset,
                    ),
                )

                self.assets[name] = {
                    "type": "image",
                    "data": image,
                }
            else:
                print(f"{name} not an image: {asset}")
        except Exception as e:
            print(f"Error loading asset: {asset} - {e}")

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


assetManager = AssetManager()
