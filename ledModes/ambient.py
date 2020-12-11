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
    def randomParticle(colors, nLeds, spreadMin = 1, spreadMax = 7, ttlMin = 200, ttlMax=800, gammaMin = 0.1, gammaMax = 0.15):
        """
        factory to create a random Particle
        """

        center = randInt(0, nLeds)
        spread = randInt(spreadMin, spreadMax)

        
        drift = (randFloat(0, 1)-0.5)/100
        timeToLive = randInt(ttlMin, ttlMax)
        gamma = randFloat(gammaMin, gammaMax)

        colorIndex = randInt(0, len(colors))
        color = colors[colorIndex]
        
        return particle(center, spread, drift, timeToLive, color, gamma)
    
    def __repr__(self):
        return f"<particle object: color: {self.color}, age: {self.currentAge}/{self.timeToLive}, center: {self.center}, spread: {self.spread}>"

    

def display(pixels, nLeds, delay):
    
    maxParticles = 15
    colors = multiBreathing + gryffindorColors
    particles = [particle.randomParticle(colors, nLeds), particle.randomParticle(colors, nLeds), particle.randomParticle(colors, nLeds)]
    timeToNextParticleMax = 80

    timeToNextParticle = randInt(0, timeToNextParticleMax)
    
    while True:

        newPixels = [Pixel() for n in range(nLeds)]

        if timeToNextParticle == 0:
            if len(particles) < maxParticles:
                newParticle = particle.randomParticle(colors, nLeds)
                
                particles.append(newParticle)
                timeToNextParticle = randInt(0, timeToNextParticleMax)
        else:
            timeToNextParticle -= 1

        deadParticles = []
        for p in particles:
            p.display(newPixels)
            p.age()
            if p.isDed():
                deadParticles.append(p)

        pixels[:] = [p.toTuple() for p in newPixels]
        pixels.show()

        for p in deadParticles:
            particles.remove(p)

        sleep(delay)

def testParticle(pixels, nLeds: int):
    colors = adriftInDream
    particleQueue = [particle.randomParticle(colors, nLeds) for i in range(5)]
    particles = [particle.randomParticle(colors, nLeds)]
    timeToNextParticle = 20

    while len(particles) > 0 or len(particleQueue > 0):
        newPixels = [Pixel() for n in range(nLeds)]
        if timeToNextParticle < 0 and len(particleQueue) > 0:
            particles.append(particleQueue.pop())
            timeToNextParticle = 20
        else:
            timeToNextParticle -= 1

        for p in particles:
            p.display(newPixels)
            p.age()
            if p.isDed():
                particles.remove(p)

        pixels[:] = [p.toTuple() for p in newPixels]
        pixels.show()
        sleep(0.1)

    #for gamma in [0.1, 0.2, 0.3, 0.4]:
    #    delay = 0.01
    #
    #    p = particle(nLeds//2, 5, 0, 400, Pixel(220,1,5), gamma)
    #    print(p)
    #    while not p.isDed():
    #        newPixels = [Pixel() for n in range(nLeds)]
    #        p.display(newPixels)
    #        p.age()
    #        pixels[:] = [p.toTuple() for p in newPixels]
    #        pixels.show()
    #        sleep(delay)
    #    del p
            