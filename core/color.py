from core.pixel import Pixel
from util.conversions import hexStrToPixelList, pixelListToStrList, strToPixel
from typing import List
import json

colorPalettePath = "resources/colorSchemes.json"

class Colors:

    def __init__(self, path=colorPalettePath):
        self.colorPalettes = {}
        with open(colorPalettePath, "r") as f:
            rawColorPalettes = json.load(f)

            for key, value in rawColorPalettes.items():
                self.colorPalettes[key] = [strToPixel(p) for p in value]

        if "default" in self.colorPalettes:
            self.currentPalette = "default"
        else:
            raise ValueError("No default colorPalette specified in {}".format(path))

    def addPalette(self, name: str, colors: List[Pixel]):
        newPalette = { name: [str(p) for p in colors]}        
        self.colorPalettes.update(newPalette)

        with open(colorPalettePath, "w") as f:
            json.dump(colorPalettes, f, indent=4)        

    @property
    def current(self):
        return self.colorPalettes[self.currentPalette]

    #def registerEndpoints(self, app):
    #     @app.get(f"/colors")
    #     def get_ambi_colors():
    #         return {"colors": pixelListToStrList(self.colors)}

    #     @app.put(f"/{self.name}/colors")
    #     def put_ambi_colors(colors:List[str]):
    #         palette = [strToPixel(c) for c in colors]
    #         self.changeColorPalette(palette)
    #         return {"newPalette" : palette} 

palette = Colors()

#TODO implement endpoints