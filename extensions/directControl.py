from core.extension import Extension
from time import sleep

from pydantic import BaseModel
from typing import List
from core.pixel import Pixel

class pixelModel(BaseModel):
    r: int
    g: int
    b: int

class newPixelsModel(BaseModel):
    pixels: List[pixelModel]

class directControl(Extension):
    name = "direct"

    def display(self, delay):
        sleep(delay)

    def customEndpoints(self, app):
        @app.get(f"/{self.name}/leds")
        def getPixels():
            return self.pixels

        @app.put(f"/{self.name}/leds")
        def putPixels(newPixels: newPixelsModel):
            if len(newPixels.pixels) > self.nLeds:
                newPixels = [Pixel(p.r, p.g, p.b).toTuple() for p in newPixels.pixels[:self.nLeds]]
            else:
                fillUp = self.nLeds - len(newPixels.pixels)
                newPixels = [Pixel(p.r, p.g, p.b).toTuple() for p in newPixels.pixels] + [(0,0,0)]*fillUp

            self.pixels[:] = newPixels

            