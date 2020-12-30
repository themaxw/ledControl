from extension import Extension
from ui import UIValue, valueModelInt
from neopixel import NeoPixel
from pydantic import BaseModel
from typing import Optional, List
from time import sleep


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, b, g)

class SingleColor(Extension):
    def __init__(self, pixels: NeoPixel, nLeds, initial = 20):
        super().__init__("SingleColor", pixels, nLeds)
        self.parameters["color"] = UIValue("Color", "color", initial, 255)
        self.createModel()
        

    def update(self, params):
        if params.color:
            self.parameters["color"].update(params.color.current)

    def display(self, delay):
        
        self.pixels.fill(wheel(self.parameters["color"].value))
        self.pixels.show()
        sleep(delay)

    def createModel(self):
        class scModel(BaseModel):
            color: Optional[valueModelInt]
        self.model = scModel

    def customEndpoints(self, app):
        @app.get("/test")
        def get_test():
            return "testtest123"