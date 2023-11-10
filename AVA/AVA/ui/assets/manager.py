

class AssetManager:
    def __init__(self):
        self.assets = {}


    def add(self, name, asset, dark_asset = None):
        self.assets[name] = {'light' : asset, 'dark' : dark_asset if dark_asset else asset}

    def load_asset(path)
        
    def get(self, name, theme="light"):
        return self.assets[name][theme]