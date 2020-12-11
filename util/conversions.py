from ledModes.pixel import Pixel


def strToPixel(hexStr: str):
    if hexStr.startswith("#"): 
        hexStr = hexStr[1:]
    r = int(hexStr[0:2], base=16)
    g = int(hexStr[2:4], base=16)
    b = int(hexStr[4:6], base=16)
    return Pixel(r, g, b)

def hexStrToPixelList(hexStr: str):
    listOfHexStr = hexStr.split(",")
    pixels = []
    for hexColor in listOfHexStr:
        if not hexColor.startswith("#"):
            continue
        if len(hexColor) < 7:
            continue
        pixels.append(strToPixel(hexColor))

    return pixels
        
