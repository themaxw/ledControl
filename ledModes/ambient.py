from ledModes.pixel import Pixel
from util.random import randInt, randFloat
import math
from util.conversions import hexStrToPixelList
from time import sleep

gryffindorColors = [Pixel(116, 0, 1), Pixel(174,0,1), Pixel(238, 186, 48), Pixel(211, 166, 37)]
aangColors = hexStrToPixelList("#9ECCE0,#F27B44,#904619,#FFDF87,#C48F48,#9ECCE0,#F27B44,#904619")
earthKingdom = hexStrToPixelList("#2E642C,#458643,#4FA24C,#CEBD73,#EDDFA1,#2E642C,#458643,#4FA24C")
adriftInDream = hexStrToPixelList("#CFF09E,#A8DBA8,#79BD9A,#3B8686,#0B486B")
multiBreathing = [  Pixel(12,  120, 210), Pixel(12,  12, 240), Pixel(0, 0, 240),Pixel(30, 12, 230), Pixel(50, 240, 60)]
defaultColors = hexStrToPixelList("#0026E6, #0000B3, #2200CC, #004D99, #0073E6, #00AAFF, #00D5FF, #00FFD5, #00CC44, #006611, #009919, #00FF2A, #33BBFF")


class particleParams:
    def __init__(self, spreadMin = 1, spreadMax = 7, ttlMin = 200, ttlMax=800, gammaMin = 0.1, gammaMax = 0.15):
        self.spreadMin = spreadMin
        self.spreadMax = spreadMax
        self.ttlMin = ttlMin
        self.ttlMax= ttlMax
        self.gammaMin = gammaMin
        self.gammaMax = gammaMax

    def spread(self):
        return randInt(self.spreadMin, self.spreadMax)

    def timeToLive(self):
        return randInt(self.ttlMin, self.ttlMax)

    def gamma(self):
        return randFloat(self.gammaMin, self.gammaMax)
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
    def randomParticle(colors, nLeds, params: particleParams):
        """
        factory to create a random Particle
        """

        center = randInt(0, nLeds)
        spread = params.spread()

        
        #drift = (randFloat(0, 1)-0.5)/100
        drift = 0
        timeToLive = params.timeToLive()
        gamma = params.gamma()

        colorIndex = randInt(0, len(colors))
        color = colors[colorIndex]
        
        return particle(center, spread, drift, timeToLive, color, gamma)
    
    def __repr__(self):
        return f"<particle object: color: {self.color}, age: {self.currentAge}/{self.timeToLive}, center: {self.center}, spread: {self.spread}>"


class ambiLight:
    def __init__(self, pixels, nLeds, colors=defaultColors, maxParticles = 18, initialParticles=4):
        self.pixels = pixels
        self.nLeds = nLeds
        self.colors = colors
        self.maxParticles = maxParticles
        self.timeToNextParticleMax = 80
        self.timeToNextParticle = randInt(0, self.timeToNextParticleMax)
        self.pParams = particleParams()
        self.particles = [particle.randomParticle(self.colors, self.nLeds, self.pParams) for i in range(initialParticles)]

    def changeColorPalette(self, palette):
        self.colors = palette

    def changeParams(self, spreadMin =None, spreadMax =None, ttlMin =None, ttlMax=None, gammaMin =None, gammaMax =None):
        if spreadMin:
            self.pParams.spreadMin = spreadMin
        if spreadMax:
            self.pParams.spreadMax = spreadMax   
        if ttlMin:
            self.pParams.ttlMin = ttlMin  
        if ttlMax:
            self.pParams.ttlMax = ttlMax 
        if gammaMin:
            self.pParams.gammaMin = gammaMin  
        if gammaMax:
            self.pParams.gammaMax = gammaMax 

    def display(self, delay):
        while True:
            self.displaySingleFrame()
            sleep(delay)

    def displaySingleFrame(self):
        newPixels = [Pixel() for n in range(self.nLeds)]

        if self.timeToNextParticle == 0:
            if len(self.particles) < self.maxParticles:
                newParticle = particle.randomParticle(self.colors, self.nLeds, self.pParams)
                
                self.particles.append(newParticle)
                self.timeToNextParticle = randInt(0, self.timeToNextParticleMax)
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
            