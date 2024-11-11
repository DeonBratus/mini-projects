from pydantic import BaseModel
class Units:


    class Distance:
        units = {  
            "mcm": 10**(-6), 
            "mm": 10**(-3), 
            "cm": 10**(-2),
            "dm":  10**(-1),
            "m":  10**(0),
            "km":  10**(3)
            }

        def __str__(self):
            return "distance"

    class Weight:

        units = { 
            "mg":  10**(-6),
            "g":  10**(-3),
            "kg":  10**(0),
            "t": 10**(3)
        }
    
        def __str__(self):
            return "weight"

    class Time:

        units = { 
            "ms": 10**(-3),
            "s": 1,
            "min": 60,
            "hr": 3600,
            "day": 24 * 3600,
            "week": 7 * 24 * 3600,
            "year": 365 * 24 * 3600
        }
    
        def __str__(self):
            return "time"
    
    class Temperature:
        units = {
            "C": 0,
            "F": 0,
            "K": 273
        }

        def c_to_f(self, c):
            return c * (9/5) + 32
        def f_to_c(self, f):

            return (f-32)*(5/9)
        
        def __str__(self):
            return "temperature"
        
        def handle_temp_convert(self, data):
            if data.unit_from == "C" and data.unit_to == "F":
                result = self.c_to_f(data.value)
            elif data.unit_from == "F" and data.unit_to =="C":
                result = self.f_to_c(data.value)
            elif data.unit_from == "C" and data.unit_to == "K":
                result = data.value + 273
            elif data.unit_from == "K" and data.unit_to == "C":
                result = data.value - 273
            else:
                result = data.value
            return result
    def create_unit_type(cls, type_str):
        for subclass in vars(cls).values():
            if isinstance(subclass, type): 
                if subclass().__str__() == type_str:
                    return subclass
        return None
         

class convertData(BaseModel):
        unit_type: str
        value: float
        unit_from: str
        unit_to : str



unit_options = {
    "distance": [
        {"value": "m", "label": "Meter"},
        {"value": "km", "label": "Kilometer"},
        {"value": "cm", "label": "Centimeter"},
        {"value": "mm", "label": "Millimeter"}
    ],
    "weight": [
        {"value": "g", "label": "Gram"},
        {"value": "kg", "label": "Kilogram"},
        {"value": "mg", "label": "Milligram"},
        {"value": "t", "label": "Ton"}
    ],
    "time": [
        {"value": "ms", "label": "Millisecond"},
        {"value": "s", "label": "Second"},
        {"value": "min", "label": "Minute"},
        {"value": "hr", "label": "Hour"},
        {"value": "day", "label": "Day"},
        {"value": "wk", "label": "Week"},
        {"value": "year", "label": "Year"},
    ],
    "temperature": [
        {"value": "C", "label": "Celsia"},
        {"value": "K", "label": "Kelvin"},
        {"value": "F", "label": "Farengait"}
    ]
}