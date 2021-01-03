from typing import Union
from abc import abstractmethod, ABC
from fastapi import FastAPI

Numeric = Union[float, int]

class Extension(ABC):
    
    
    def __init__(self, pixels, nLeds, *args, **kwargs):

        if not hasattr(self, "name"):
            raise AttributeError("Object has no attribute name specified")

        self.model = None
        self.pixels = pixels
        self.nLeds = nLeds

        self.parameters = {}
        paramList = self.setupParameters(*args, *kwargs)
        for param in paramList:
            self.parameters[param.parameterName] = param

        self.initialize(*args, *kwargs)
        self.createModel()


    def setupParameters(self, *args, **kwargs):
        return []

    def initialize(self, *args, **kwargs):
        pass

    def getUI(self):
        elements = []
        for p in self.parameters.values():
            elements.append(p.getUI())
        return {"elements": elements}
    
    @abstractmethod
    def display(self):
        pass

    def update(self, params):
        for p in self.parameters:
            newVal = getattr(params, p)
            if newVal:
                self.parameters[p].update(newVal)


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
