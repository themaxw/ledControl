from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Union

Numeric = Union[float, int]


class rangeModelFloat(BaseModel):
    lower: float
    upper: float
class rangeModelInt(BaseModel):
    lower: int
    upper: int
class valueModelFloat(BaseModel):
    current: float
class valueModelInt(BaseModel):
    current: int

class UIElement(ABC):

    """Abstract Base Class for UI Elements
    """

    def __init__(self, displayName: str, parameterName: str, elementType: str):
        self.displayName = displayName
        self.parameterName = parameterName
        self.type = elementType

    def getGeneralFields(self):
        return {
            "displayName": self.displayName,
            "parameterName": self.parameterName,
            "type": self.type,
        }

    @abstractmethod
    def getSpecificFields(self):
        """returns the custom fields of this UI element as a dict
        """
        pass

    def getUI(self):
        """
        returns the UI element as a dict so a user interface can be created
        """
        uiDict = self.getGeneralFields()
        uiDict.update(self.getSpecificFields())
        return uiDict

    @abstractmethod 
    def update(self, *args):
        pass

    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def valueDict(self):
        pass

class UIRange(UIElement):

    def __init__(self, displayName: str, parameterName: str, lower: Numeric, upper: Numeric, maxValue: Numeric, stepSize:Numeric = 1): 
        super().__init__(displayName, parameterName, "range")
        assert(lower <= upper <= maxValue)
        self.lower = lower
        self.upper = upper
        self.max = maxValue  
        self.stepSize = stepSize

    def getSpecificFields(self):
        fields = {
            "lower": self.lower,
            "upper": self.upper,
            "max": self.max,
        }
        if self.stepSize != 1:
            fields["stepSize"] = self.stepSize

        return fields

    def update(self, lower=None, upper=None):
        if lower:
            self.lower = lower if lower < self.upper else self.upper
        if upper:
            self.upper = upper if upper < self.max else self.max

    @property
    def value(self):
        return (self.lower, self.upper)

    def valueDict(self):
        return {self.parameterName: {"lower": self.lower, "upper": self.upper}}

class UIValue(UIElement):

    def __init__(self, displayName: str, parameterName: str, current: Numeric, maxValue: Numeric, stepSize:Numeric = 1 ):
        super().__init__(displayName, parameterName, "value")
        assert(current <= maxValue)
        self.current = current
        self.max = maxValue
        self.stepSize = stepSize

    def getSpecificFields(self):
        fields = {
            "current": self.current,
            "max": self.max,
        }
        if self.stepSize != 1:
            fields["stepSize"] = self.stepSize
        return fields
    
    def update(self, current=None):
        if current:
            self.current = current if current < self.max else self.max

    @property
    def value(self):
        return self.current

    def valueDict(self):
        return {self.parameterName: {"current": self.current}}
