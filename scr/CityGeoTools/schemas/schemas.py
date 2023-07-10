import json
import os 

class Schemas: 
    def __init__(self) -> None:
        self.attrs = ["Blocks", 
                      "Buildings",
                      "Municipalities",
                      "PublicTransportStops",
                      "Services",
                      "ServiceTypes"]
        
        for attr_name in self.attrs:
            self.defaultFactory(attr_name)
    
    def defaultFactory(self, attr_name):
        with open(f"{os.getcwd()}/scr/CityGeoTools/schemas/{attr_name}.json") as schema: 
            return setattr(self, attr_name, json.load(schema))

    