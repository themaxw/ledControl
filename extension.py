from typing import Union
from abc import abstractmethod, ABC
from fastapi import FastAPI

Numeric = Union[float, int]

class Extension(ABC):
    
    
    def __init__(self, name, pixels, nLeds):
        self.name = name
        self.parameters = {}
        self.model = None
        self.pixels = pixels
        self.nLeds = nLeds

    def getUI(self):
        elements = []
        for p in self.parameters.values():
            elements.append(p.getUI())
        return {"elements": elements}
    
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def update(self, params):
        #TODO Put this here, so the user only has to overwrite it in special scenarios
        pass

    @abstractmethod
    def createModel(self):
        pass
    
    def customEndpoints(self, app):
        pass

    def registerEndpoints(self, app):
        # TODO how to handle multiple modes? remove endpoints
        assert(self.model is not None)

        @app.get(f"/{self.name}/params")
        def get_params():
            params = {}
            for p in self.parameters.values():
                params.update(p.valueDict())
            return params

        @app.put(f"/{self.name}/params")
        def put_params(params: self.model):
            self.update(params)
            return get_params()

        @app.get(f"/{self.name}/ui")
        def get_ui():
            return self.getUI()

        self.customEndpoints(app)
