import board
import neopixel
import time
import threading
from ledModes import ambient, fire, sparkle, rainbow, breathing, multiBreathing
from typing import Optional
from fastapi import FastAPI
import uvicorn
from threading import Thread, Event
from api import setupAPI

app = FastAPI()


nLeds = 31
top_right = 9
top_left = 23

pixels = neopixel.NeoPixel(board.D18, nLeds , auto_write = False)


if __name__ == "__main__":
    #ambient.testParticle(pixels, nLeds)
    ambiLight = ambient.ambiLight(pixels, nLeds)
    newThread = Thread(target=ambiLight.display, args = (0.01,), daemon=True)
    newThread.start()
    setupAPI(app, ambiLight)
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
    
    #multiBreathing.display(pixels, nLeds)
    #rainbow.display(pixels, nLeds, 0.01, style="mono")
    #fire.display(pixels, nLeds)
    #sparkle.display(pixels, nLeds)
    #breathing.display(pixels, nLeds, (11,240, 12), 1000, 0.40)
    #TODO so helles grün und blau zum avatar gucken

