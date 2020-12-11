from time import sleep
import math

def interpolatePixels(segments, nLeds):
    nSegments = len(segments)
    segmentSize = nLeds//nSegments
    interpolated = [(0,0,0)] * nLeds
    #print("\n start interpolate\n")
    # TODO positionen graduell verändern
    # TODO smooth überblenden
    for i, s in enumerate(segments):
        r, g, b = s
        indexStart = i*segmentSize
        indexEnd = (i+1)*segmentSize
        indexEnd = indexEnd if indexEnd < nLeds else nLeds -1
        interpolated[indexStart:indexEnd] = [(r, b, g)] * (indexEnd-indexStart)
        #print(f"segment {i}: {indexStart}-{indexEnd}")
    return interpolated
        


def display(pixels, nLeds):
    gamma = 0.33
    segments = [  (12,  120, 210,450), (12,  12, 240, 600), (0, 0, 240, 800),(30, 12, 230, 700), (50, 240, 60, 640)]
    currBreath = [0] * len(segments)
    #TODO farben graduell anpassen, vllt mit so was ähnlichem wie wheel 
    while True:
        dimmedSegments = []
        for i, s in enumerate(segments): 
            r, g, b, duration = s
            currBreath[i] = (currBreath[i] + 1) % duration
            factor = math.exp(-((((currBreath[i] / duration) - 0.5) / gamma) ** 2.0) / 2.0)
            dimmedSegments.append((int(r*factor), int(g*factor), int(b*factor)))

        pixels[:] = interpolatePixels(dimmedSegments, nLeds)
        pixels.show()
        sleep(1 / 1000)