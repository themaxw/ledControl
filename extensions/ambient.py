from ledModes.pixel import Pixel
from util.random import randInt, randFloat
import math
from util.conversions import hexStrToPixelList, pixelListToStrList, strToPixel
from time import sleep
from pydantic import BaseModel
from typing import Optional, List
from ui import UIRange, UIValue, rangeModelFloat, rangeModelInt, valueModelInt

from extension import Extension

gryffindorColors = [Pixel(116, 0, 1), Pixel(174,0,1), Pixel(238, 186, 48), Pixel(211, 166, 37)]
aangColors = hexStrToPixelList("#9ECCE0,#F27B44,#904619,#FFDF87,#C48F48,#9ECCE0,#F27B44,#904619")
earthKingdom = hexStrToPixelList("#2E642C,#458643,#4FA24C,#CEBD73,#EDDFA1,#2E642C,#458643,#4FA24C")
adriftInDream = hexStrToPixelList("#CFF09E,#A8DBA8,#79BD9A,#3B8686,#0B486B")
multiBreathing = [  Pixel(12,  120, 210), Pixel(12,  12, 240), Pixel(0, 0, 240),Pixel(30, 12, 230), Pixel(50, 240, 60)]
defaultColors = hexStrToPixelList("#0026E6, #0000B3, #2200CC, #004D99, #0073E6, #00AAFF, #00D5FF, #00FFD5, #00CC44, #006611, #009919, #00FF2A, #33BBFF")


class particle:

    def __init__(self, center, spread, drift, timeToLive, color, gamma = 0.1):   
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
        prevPixel = self.pixel
        self.pixel = self.color * self.calculateBreath()
        

    def display(self, pixelArray):
        currentCenter = int(round(self.center))
        currentCenter = max(currentCenter, 0)
        currentCenter = min(currentCenter, len(pixelArray))
        lower = max( currentCenter - (self.spread -1), 0)
        upper = min( currentCenter + self.spread, len(pixelArray))
    
        
        for i in range(lower, upper):
            dimm = (1-abs((i-currentCenter)/self.spread))
            pixelArray[i] += (self.pixel * dimm)
        


    def isDed(self):
        return self.currentAge >= self.timeToLive

    @staticmethod
    def randomParticle(colors, nLeds, parameters):
        """
        factory to create a random Particle
        """

        center = randInt(0, nLeds)
        spread = randInt(*parameters["spread"].value)

        
        #drift = (randFloat(0, 1)-0.5)/100
        drift = 0
        ttl = randInt(*parameters["ttl"].value)
        gamma = randFloat(*parameters["gamma"].value)


        colorIndex = randInt(0, len(colors))
        color = colors[colorIndex]
        
        return particle(center, spread, drift, ttl, color, gamma)
    
    def __repr__(self):
        return f"<particle object: color: {self.color}, age: {self.currentAge}/{self.timeToLive}, center: {self.center}, spread: {self.spread}>"


class ambiLight(Extension):
    def __init__(self, pixels, nLeds, colors=defaultColors, maxParticles = 18, initialParticles=4):
        super().__init__("Ambilight", pixels, nLeds)
        
        self.colors = colors
        self.parameters["maxParticles"] = UIValue("Max amount of Particles", "maxParticles", current=maxParticles, maxValue=30)
        self.parameters["timeToNextParticleMax"] = UIValue("Max Wait time for next particle spawn", "timeToNextParticleMax", current=80, maxValue=1000)
        self.timeToNextParticle = randInt(0, self.parameters["timeToNextParticleMax"].value)
        
        self.parameters["spread"] = UIRange("Spread", "spread", 1, 7, 31)
        self.parameters["ttl"] = UIRange("Time to Live", "ttl", 200, 800, 1000)
        self.parameters["gamma"] = UIRange("Gamma", "gamma", 0.1, 0.15, maxValue=0.6, stepSize=0.01)
        
        self.particles = [particle.randomParticle(self.colors, self.nLeds, self.parameters) for i in range(initialParticles)]
        self.createModel()

    def changeColorPalette(self, palette):
        self.colors = palette

    def update(self, params):
        if params.spread:
            self.parameters["spread"].update(params.spread.lower, params.spread.upper)
        if params.ttl:
            self.parameters["ttl"].update(params.ttl.lower, params.ttl.upper)
        if params.gamma:
            self.parameters["gamma"].update(params.gamma.lower, params.gamma.upper)
        if params.maxParticles:
            self.parameters["maxParticles"].update(params.maxParticles.current)
        if params.maxTimeToNextParticle:
            self.parameters["maxTimeToNextParticle"].update(params.maxTimeToNextParticle.current)
        

    def display(self, delay):
        
        self.displaySingleFrame()
        sleep(delay)

    def displaySingleFrame(self):
        newPixels = [Pixel() for n in range(self.nLeds)]

        if self.timeToNextParticle == 0:
            if len(self.particles) < self.parameters["maxParticles"].value:
                newParticle = particle.randomParticle(self.colors, self.nLeds, self.parameters)
                
                self.particles.append(newParticle)
                self.timeToNextParticle = randInt(0, self.parameters["timeToNextParticleMax"].value)
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


    def customEndpoints(self, app):
        
        @app.get(f"/{self.name}/colors")
        def get_ambi_colors():
            return {"colors": pixelListToStrList(self.colors)}

        @app.put(f"/{self.name}/colors")
        def put_ambi_colors(colors:List[str]):
            palette = [strToPixel(c) for c in colors]
            self.changeColorPalette(palette)
            return {"newPalette" : palette} 

    def createModel(self):
        
        class ambiModel(BaseModel):
            spread: Optional[rangeModelInt] = None
            ttl: Optional[rangeModelInt] = None
            gamma: Optional[rangeModelFloat] = None
            maxParticles: Optional[valueModelInt] = None
            maxTimeToNextParticle: Optional[valueModelInt] = None
        self.model = ambiModel

    def testParticle(self):
        particleQueue = [particle.randomParticle(self.colors, self.nLeds) for i in range(5)]
        particles = [particle.randomParticle(self.colors, self.nLeds)]
        timeToNextParticle = 20

        for gamma in [0.1, 0.2, 0.3, 0.4]:
            delay = 0.01
        
            p = particle(self.nLeds//2, 5, 0, 400, Pixel(220,1,5), gamma)
            print(p)
            while not p.isDed():
                newPixels = [Pixel() for n in range(self.nLeds)]
                p.display(newPixels)
                p.age()
                self.pixels[:] = [p.toTuple() for p in newPixels]
                self.pixels.show()
                sleep(delay)
            del p
            