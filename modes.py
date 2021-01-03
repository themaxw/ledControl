from extensions import ambient, singleColor, pictureRows
from threading import Event

__activeMode = None # Type: Extension
modes = {}



def setupModes(pixels, nLeds, app):
    modelist = [
        ambient.ambiLight(pixels, nLeds), 
        singleColor.SingleColor(pixels, nLeds),
        pictureRows.pictureRows(pixels, nLeds)
    ]
    for m in modelist:
        modes[m.name] = m
        m.registerEndpoints(app)

    global __activeMode
    #TODO find a better way for choosing defaults
    __activeMode = modes["Ambilight"]
    

def getModes():
    return [mode.name for mode in modes.values()]

def activeMode():
    return __activeMode

def changeMode(mode: str):
    global __activeMode

    if mode not in modes:
        raise KeyError


    if __activeMode != modes[mode]:
        __activeMode = modes[mode]

def activeModeDisplay(delay: float):
    if __activeMode:
        __activeMode.display(0.01)