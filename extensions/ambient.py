from core.pixel import Pixel
from util.random import randInt, randFloat
import math
from util.conversions import hexStrToPixelList, pixelListToStrList, strToPixel
from time import sleep
from pydantic import BaseModel
from typing import Optional, List
from core.ui import UIRange, UIValue, rangeModelFloat, rangeModelInt, valueModelInt

from core.extension import Extension
from core.color import palette


class particle:
    def __init__(self, center, spread, drift, timeToLive, color, gamma=0.1):
        self.color = color
        self.center = center
        self.spread = spread
        self.drift = drift
        self.timeToLive = timeToLive
        self.gamma = gamma
        self.currentAge = 0
        self.pixel = self.color * self.calculateBreath()

    def calculateBreath(self):
        return math.exp(
            -((((self.currentAge / self.timeToLive) - 0.5) / self.gamma) ** 2.0) / 2.0
        )

    def age(self):
        self.currentAge += 1
        self.center += self.drift
        # TODO make drift smoother. Maybe toss a coin with the chance in drift, and if it lands move in either direction
        # prevPixel = self.pixel
        self.pixel = self.color * self.calculateBreath()

    def display(self, pixelArray):
        currentCenter = int(round(self.center))
        currentCenter = max(currentCenter, 0)
        currentCenter = min(currentCenter, len(pixelArray))
        lower = max(currentCenter - (self.spread - 1), 0)
        upper = min(currentCenter + self.spread, len(pixelArray))

        for i in range(lower, upper):
            dimm = 1 - abs((i - currentCenter) / self.spread)
            pixelArray[i] += self.pixel * dimm

    def isDed(self):
        return self.currentAge >= self.timeToLive

    @staticmethod
    def randomParticle(colors, nLeds, parameters):
        """
        factory to create a random Particle
        """

        center = randInt(0, nLeds)
        spread = randInt(*parameters["spread"].value)

        # drift = (randFloat(0, 1)-0.5)/100
        drift = 0
        ttl = randInt(*parameters["ttl"].value)
        gamma = randFloat(*parameters["gamma"].value)

        colorIndex = randInt(0, len(colors))
        color = colors[colorIndex]
        return particle(center, spread, drift, ttl, color, gamma)

    def __repr__(self):
        return f"<particle object: color: {self.color}, age: {self.currentAge}/{self.timeToLive}, center: {self.center}, spread: {self.spread}>"


class ambiLight(Extension):

    name = "ambilight"

    def setupParameters(self, maxParticles=18, initialParticles=4):
        return [
            UIValue(
                "Max amount of Particles",
                "maxParticles",
                current=maxParticles,
                maxValue=30,
            ),
            UIValue(
                "Max Wait time for next particle spawn",
                "maxTimeToNextParticle",
                current=80,
                maxValue=1000,
            ),
            UIRange("Spread", "spread", 1, 7, 31),
            UIRange("Time to Live", "ttl", 200, 800, 1000),
            UIRange("Gamma", "gamma", 0.1, 0.15, maxValue=0.6, stepSize=0.01),
        ]

    def initialize(self, maxParticles=18, initialParticles=4):
        self.timeToNextParticle = randInt(
            0, self.parameters["maxTimeToNextParticle"].value
        )
        self.particles = [
            particle.randomParticle(palette.current, self.nLeds, self.parameters)
            for i in range(initialParticles)
        ]

    def display(self, delay):

        self.displaySingleFrame()
        sleep(delay)

    def displaySingleFrame(self):
        newPixels = [Pixel() for n in range(self.nLeds)]

        if self.timeToNextParticle == 0:
            if len(self.particles) < self.parameters["maxParticles"].value:
                newParticle = particle.randomParticle(
                    palette.current, self.nLeds, self.parameters
                )

                self.particles.append(newParticle)
                self.timeToNextParticle = randInt(
                    0, self.parameters["maxTimeToNextParticle"].value
                )
        else:
            self.timeToNextParticle -= 1

        deadParticles = []
        for p in self.particles:
            p.display(newPixels)
            p.age()
            if p.isDed():
                deadParticles.append(p)

        self.pixels[:] = [p.toTuple() for p in newPixels]
        self.pixels.show()

        for p in deadParticles:
            self.particles.remove(p)

    def createModel(self):
        class ambiModel(BaseModel):
            spread: Optional[rangeModelInt] = None
            ttl: Optional[rangeModelInt] = None
            gamma: Optional[rangeModelFloat] = None
            maxParticles: Optional[valueModelInt] = None
            maxTimeToNextParticle: Optional[valueModelInt] = None

        self.model = ambiModel

    def testParticle(self):
        particleQueue = [
            particle.randomParticle(self.colors, self.nLeds) for i in range(5)
        ]
        particles = [particle.randomParticle(self.colors, self.nLeds)]
        timeToNextParticle = 20

        for gamma in [0.1, 0.2, 0.3, 0.4]:
            delay = 0.01

            p = particle(self.nLeds // 2, 5, 0, 400, Pixel(220, 1, 5), gamma)
            print(p)
            while not p.isDed():
                newPixels = [Pixel() for n in range(self.nLeds)]
                p.display(newPixels)
                p.age()
                self.pixels[:] = [p.toTuple() for p in newPixels]
                self.pixels.show()
                sleep(delay)
            del p
