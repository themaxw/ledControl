from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ledModes.ambient import ambiLight
from util.conversions import hexStrToPixelList, pixelListToStrList, strToPixel
from typing import List

class particleParams(BaseModel):
    spreadMin: Optional[int] = None
    spreadMax: Optional[int] = None
    ttlMin: Optional[int] = None
    ttlMax: Optional[int] = None
    gammaMin: Optional[float] = None
    gammaMax: Optional[float] = None
    maxParticles: Optional[int] = None
    maxTimeToNextParticle: Optional[int] = None

origins = ["http://localhost", "http://localhost:3000", "http://192.168.178.21:3000", "http://192.168.178.21", "http://det.lef"]

def setupAPI(app: FastAPI, ambi: ambiLight):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/colors")
    def get_ambi_colors():
        return {"colors": pixelListToStrList(ambi.colors)}

    @app.put("/colors")
    def put_ambi_colors(colors:List[str]):
        palette = [strToPixel(c) for c in colors]
        ambi.changeColorPalette(palette)
        return {"newPalette" : palette}

    @app.put("/params")
    def change_particle_params(params: particleParams):
        ambi.changeParams(spreadMin=params.spreadMin, spreadMax=params.spreadMax, ttlMin=params.ttlMin, ttlMax=params.ttlMax, gammaMin=params.gammaMin, gammaMax=params.gammaMax)
        if params.maxParticles:
            ambi.maxParticles = params.maxParticles
        if params.maxTimeToNextParticle:
            ambi.timeToNextParticleMax = params.maxTimeToNextParticle

        return {"params" : ambi.pParams,
                "maxParticles": ambi.maxParticles,
                "maxTimeToNextParticle": ambi.timeToNextParticleMax
                }

    @app.get("/params")
    def get_params():
        return {"params" : ambi.pParams,
                "maxParticles": ambi.maxParticles,
                "maxTimeToNextParticle": ambi.timeToNextParticleMax
                }

    
    @app.get("/ui")
    def get_ui():
        # TODO put this in the extension class
        return {"elements":[
            {
                "displayName": "Spread",
                "parameterName": "spread",
                "type": "range",
                "lower": ambi.pParams.spreadMin,
                "upper": ambi.pParams.spreadMax,
                "max": 31,
            },
            {
                "displayName": "Time to Live",
                "parameterName": "ttl",
                "type": "range",
                "lower": ambi.pParams.ttlMin,
                "upper": ambi.pParams.ttlMax,
                "max": 1000,
            },
            {
                "displayName": "Gamma",
                "parameterName": "gamma",
                "type": "range",
                "lower": ambi.pParams.gammaMin,
                "upper": ambi.pParams.gammaMax,
                "stepSize": 0.01,
                "max": 0.6,
            },
            {
                "displayName": "Max amount of Particles",
                "parameterName": "maxParticles",
                "type": "value",
                "current": ambi.maxParticles,
                "max": 30,
            },
            {
                "displayName": "Max Wait time for next particle spawn",
                "parameterName": "timeToNextParticleMax",
                "type": "value",
                "current": ambi.timeToNextParticleMax,
                "max": 1000,
            },
        ]}
