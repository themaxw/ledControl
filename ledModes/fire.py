from time import sleep
import fastrand

def rand_in_range(start, stop):
    return fastrand.pcg32bounded(stop - start) + start

def set_heat_pixel( temperature):
        t192 = int((temperature / 255) * 191)
        heatramp = t192 & 0x3F
        heatramp = heatramp << 2

        if t192 > 128:
            return (255, 180, heatramp)
        elif t192 > 0x64:
            return (255, heatramp, 0)
        else:
            return (heatramp, 0, 0)

def display(pixels, nLeds, cooling = 50, sparking = 120, speed_delay = 20):
    heat = [0] * nLeds
    
    while True:
        # Step 1.  Cool down every cell a little
        for i in range(nLeds):
            cooldown = rand_in_range(0, ((cooling * 50) / nLeds) + 2)
            if cooldown > heat[i]:
                heat[i] = 0
            else:
                heat[i] = heat[i] - cooldown

        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(nLeds - 1, 2, -1):
            heat[k] = (
                heat[k - 1] + heat[k - 2] + heat[k - 2]
            ) / 3

        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if rand_in_range(0, 255) < sparking:
            y = rand_in_range(0, 7)
            heat[y] = heat[y] + rand_in_range(160, 255)

        # Step 4.  Convert heat to LED colors
        for j in range(nLeds):
            pixels[j] =  set_heat_pixel(heat[j])
        pixels.show()
        sleep(speed_delay / 1000)