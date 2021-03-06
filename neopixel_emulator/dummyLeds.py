import numpy as np
from neopixel_emulator.emulator_backend import Adafruit_NeoPixel
from threading import Lock, Thread, Event


class Neopixel:
    def __init__(self, nLeds, stopEvent):
        self.nLeds = nLeds

        self.pixels = Adafruit_NeoPixel(self.nLeds, 6, "NEO_GRB")
        self.stopEvent = stopEvent
        self.showEvent = Event()
        self.setupFinished = Event()
        self.lock = Lock()

        self.thread = Thread(target=self.emulatorLoop)
        self.thread.start()
        self.setupFinished.wait()

    def show(self):
        self.showEvent.set()

    def newArray(self, rgbarray):
        with self.lock:
            for i, (r, g, b) in enumerate(rgbarray):
                if i >= self.nLeds:
                    break
                self.pixels.setPixelColor(i, (r, b, g))

    def __setitem__(self, key, value):
        self.newArray(value)

    def fill(self, rgb):
        r, g, b = rgb
        with self.lock:
            self.pixels.fill((r, b, g), 0, self.nLeds)

    def emulatorLoop(self):

        self.pixels.begin(window_w=1100, window_h=12)
        self.pixels.setBrightness(100)
        self.setupFinished.set()
        while not self.stopEvent.is_set():
            no_timeout = self.showEvent.wait(1)
            if no_timeout:
                with self.lock:
                    self.pixels.show()
