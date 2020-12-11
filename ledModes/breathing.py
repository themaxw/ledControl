from time import sleep
import math

def display(pixels, nLeds, color, duration, gamma):
    currBreath = 0
    
    r, g, b = color
    while True:
        currBreath = (currBreath + 1) % duration
        factor = math.exp(
            -((((currBreath / duration) - 0.5) / gamma) ** 2.0) / 2.0
        )
        pixels.fill((int(r*factor), int(g*factor), int(b*factor)))
        pixels.show()
        sleep(1 / 1000)