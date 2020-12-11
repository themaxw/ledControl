from time import sleep
import fastrand

def rand_in_range(start, stop):
    return fastrand.pcg32bounded(stop - start) + start

def display(pixels, nLeds, sleepyTime = 0.05):
    
    r = 255//2
    g = 255//2
    b = 255//2
    while(True):
        randPixel = rand_in_range(0, nLeds)
        pixels[randPixel] = (r,g,b)
        pixels.show()
        sleep(sleepyTime)
        pixels[randPixel] = (0,0,0)


