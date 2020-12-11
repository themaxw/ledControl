from time import sleep

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, b, g)

def rainbow_cycle(pixels, nLeds, wait):
    for j in range(255):
        for i in range(nLeds):
            pixel_index = (i * 256 // nLeds) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        sleep(wait)

def rainbowVertical(pixels, nLeds, wait, direction):
    minimum = 0
    maximum = 256
    stepsize = 3
    r = range(minimum, maximum, stepsize) if direction else range(maximum, minimum, -stepsize)
    print("up" if direction else "down")
    for i in r:
        for j in range(16):
            pixel_index = (j * 256 // nLeds) + i
            val = wheel(pixel_index & 255)
            pixels[j]  = val
            pixels[nLeds-1-j] = val
        pixels.show()
        sleep(wait)

def rainbowMono(pixels, nLeds, wait):
    for j in range(255):
        color = wheel(j)
        pixels[:] = [color]*nLeds
        pixels.show()
        sleep(wait)


def display(pixels, nLeds, wait, style = "mono"):
    """[summary]

    Args:
        pixels ([type]): [description]
        nLeds ([type]): [description]
        wait ([type]): [description]
        style (str, optional): one of "mono", "double" or "single". Defaults to "mono".
    """
    if style == "mono":
        while True:
            rainbowMono(pixels, nLeds, wait)
    elif style == "double":
        direction = True
        while True:
            rainbowVertical(pixels, nLeds, wait, direction)
            direction = not direction
    elif style == "single":
        while True:
            rainbow_cycle(pixels, nLeds, wait)
