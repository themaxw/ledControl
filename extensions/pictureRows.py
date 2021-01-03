from core.extension import Extension
from core.ui import UIValue, valueModelInt, UIUrl, urlModel
from time import sleep
from PIL import Image
from pydantic import BaseModel
from core.pixel import Pixel
from typing import Optional
import requests
from io import BytesIO

class pictureRows(Extension):
    
    name = "picturerows"

    def setupParameters(self):
        return [
            UIValue("Time per Row", "time", 3, 1000),
            UIValue("Smoothing of Steps", "smooth", 0, 100),
            UIUrl("URL of image", "url", "")
        ]

    def initialize(self):
        self.timeToNextCol = 0
        self.currentRow = -1
        self.loadImageLocal("resources/vibrant.jpg")

    def imageRowToPixels(self, row: int):
        newPixels = []
        for i in range(self.nLeds):
            p = self.image.getpixel((row, i))
            newPixels.append(Pixel(p[0], p[1], p[2]))
        return newPixels

    def display(self, delay):

        if self.parameters["url"].changed:
            self.loadImageFromUrl()
            self.timeToNextCol = 0
            self.currentRow = -1

        if self.timeToNextCol == 0:

            self.currentRow = (self.currentRow + 1)% self.image.size[0]
            newPixels = self.imageRowToPixels(self.currentRow)
            
            self.pixels[:] = [p.toTuple() for p in newPixels]
            self.pixels.show()
            self.timeToNextCol = self.parameters["time"].value
        else:
            self.timeToNextCol -= 1
        sleep(delay)
    
    def loadImageFromUrl(self):
        #TODO error handling hier
        response = requests.get(self.parameters["url"].value)
        image = Image.open(BytesIO(response.content))
        self.image = image.resize((image.size[0], self.nLeds))
    
    def loadImageLocal(self, path):
        image = Image.open(path)
        self.image = image.resize((image.size[0], self.nLeds))

    def createModel(self):
        class pictureRowModel(BaseModel):
            time: Optional[valueModelInt] = None
            smooth: Optional[valueModelInt] = None
            url: Optional[urlModel] = None

        self.model = pictureRowModel

if __name__ == "__main__":
    image = Image.open("resources/default.jpg")
    image = image.resize((image.size[0], 31))
    print(image[0])