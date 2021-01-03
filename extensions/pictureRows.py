from extension import Extension
from ui import UIValue, valueModelInt
from time import sleep
from PIL import Image
from pydantic import BaseModel
from ledModes.pixel import Pixel
from typing import Optional

class pictureRows(Extension):
    def __init__(self, pixels, nLeds):
        super().__init__("pictureRows", pixels, nLeds)

        self.parameters["time"] = UIValue("Time per Row", "time", 3, 1000)
        self.parameters["smooth"] = UIValue("Smoothing of Steps", "smooth", 0, 100)
        image = Image.open("resources/default.jpg")
        self.image = image.resize((image.size[0], nLeds))
        self.timeToNextCol = 0
        self.currentRow = -1
        self.createModel()


    def imageRowToPixels(self, row: int):
        newPixels = []
        for i in range(self.nLeds):
            p = self.image.getpixel((row, i))
            newPixels.append(Pixel(p[0], p[1], p[2]))
        return newPixels

    def display(self, delay):
        if self.timeToNextCol == 0:
            self.currentRow = (self.currentRow + 1)% self.image.size[0]
            newPixels = self.imageRowToPixels(self.currentRow)
            print(len(newPixels), self.currentRow)
            self.pixels[:] = [p.toTuple() for p in newPixels]
            self.pixels.show()
            self.timeToNextCol = self.parameters["time"].value
        else:
            self.timeToNextCol -= 1
        sleep(delay)

    def createModel(self):
        class pictureRowModel(BaseModel):
            time: Optional[valueModelInt] = None
            smooth: Optional[valueModelInt] = None

        self.model = pictureRowModel

if __name__ == "__main__":
    image = Image.open("resources/default.jpg")
    image = image.resize((image.size[0], 31))
    print(image[0])