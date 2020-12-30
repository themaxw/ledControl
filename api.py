from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from extensions.ambient import ambiLight
from util.conversions import hexStrToPixelList, pixelListToStrList, strToPixel
from typing import List
from modes import getModes, activeMode, changeMode
origins = ["http://localhost", "http://localhost:3000", "http://192.168.178.21:3000", "http://192.168.178.21", "http://det.lef"]

def setupAPI(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/mode")
    def get_mode():
        curr = activeMode()
        if curr:
            return {"activeMode":curr.name}
        else:
            return {"activeMode":""}

    @app.put("/mode")
    def change_mode(mode: str):
        try:
            changeMode(mode)
        except KeyError:
            raise HTTPException(status_code=404, detail="Mode not found")

        #TODO semaphore here
        

    
    @app.get("/modes")
    def get_modes():
        
        return {"modes": getModes()}

    
