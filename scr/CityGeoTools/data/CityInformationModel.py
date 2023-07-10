from typing import Any
import numpy as np
import jsonschema
import json
#np.finfo(np.dtype("float32"))
#np.finfo(np.dtype("float64"))

import pandas as pd
import geopandas as gpd
import networkx as nx

from .data_transform import load_graph_geometry, convert_nx2nk, get_nx2nk_idmap, get_nk_attrs, get_subgraph
from ..schemas import schemas

Schemas = schemas.Schemas()

class CityInformationModel:
    
    def __init__(self,
                 city_name: str, 
                 city_crs: int) -> None:

        self.city_name = city_name
        self.city_crs = city_crs

        self.default_attrs = {'MobilityGraph': None,       
                              'Buildings': None,
                              'Services': None,
                              'PublicTransportStops': None,
                              'ServiceTypes': None,
                              'RecreationalAreas': None,
                              'Blocks': None,
                              'Municipalities': None,
                              'AdministrativeUnits': None,
                              'ValueTypes': None,
                              'SocialGroups': None,
                              'SocialGroupsValueTypesLivingSituations': None,
                              'LivingSituationsCityServiceTypes': None,
                              'LivingSituations': None}
    
    @staticmethod
    def validate_df(layer_name: str,
                    city_name: str,
                    df: Any):

        if layer_name in Schemas.attrs:
            if isinstance(df, gpd.GeoDataFrame):
                json_obj = json.loads(df.to_json())
                json_obj["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}} 
            else:
                json_obj = json.loads(df.to_json(orient="records"))
            try:
                validator = jsonschema.Draft7Validator(getattr(Schemas,
                                                            layer_name))
                if validator.is_valid(json_obj):
                    print(f"{city_name} - {layer_name} matches specification.")
                    return df
                else: 
                    errors = validator.iter_errors(json_obj)
                    messages = set([f"{e.relative_path[-1]}: {e.message}" if e.relative_path[-1] != "features"
                                    else "Some property in 'features' contain only NaN. Or there is no objects in 'features' at all." 
                                    for e in errors])
                    for message in messages:
                        print(f"{city_name} - {layer_name} DO NOT match specification. {message}.")
                    return None
            except Exception as e:
                print(f"{e}, No schema for {city_name} - {layer_name}, risk procceed allowed")
                return df
        else:
            print(f"No schema for {city_name} - {layer_name}, risk procceed allowed")
            return df

    @staticmethod
    def validate_graphml(layer_name, 
                         city_name,
                         G):
        message = []
        edge_validity = {}
        node_validity = {}
        public_transport = ["subway", "tram", "trolleybus", "bus"]

        graph_size = len(G.edges()) > 1
        types = set([e[-1]["type"] for e in G.edges(data=True)])
        edge_validity["type"] = len(types) > 0
        edge_validity["walk value in type"] = 'walk' in types
        edge_validity["public transport in type"] = any([t in types for t in public_transport])
        edge_validity["length_meter"] = all(["length_meter" in e[-1] for e in G.edges(data=True)])
        edge_validity["time_min"] = all(["time_min" in e[-1] for e in G.edges(data=True)])

        node_validity["x"] = all(["x" in n[-1] for n in G.nodes(data=True)])
        node_validity["y"] = all(["y" in n[-1] for n in G.nodes(data=True)])
        node_validity["stop"] = all(["stop" in n[-1] for n in G.nodes(data=True)])

        validity = graph_size & all(node_validity.values()) & all(edge_validity.values())
        if validity:
            print(f"{city_name} - {layer_name} matches specification.")
            return G
        else: 
            edge_error = ", ".join([k for k, v in edge_validity.items() if not v])
            node_error = ", ".join([k for k, v in node_validity.items() if not v])
            message = "Layer matches specification" if validity else ""
            message += f"Graph has too little edges." if not graph_size else ""
            message += f"Edges do not have {edge_error} attributes. " if len(edge_error) > 0 else ""
            message += f"Nodes do not have {node_error} attributes." if len(node_error) > 0 else ""
            print(f"{city_name} - {layer_name} DO NOT match specification. {message}")
            return None
        
    def get_supplementary_graphs(self) -> None:

        sub_edges = ["subway", "bus", "tram", "trolleybus", "walk"] # exclude drive
        MobilitySubGraph = get_subgraph(self.MobilityGraph, "type", sub_edges)
        self.nk_idmap = get_nx2nk_idmap(MobilitySubGraph)
        self.nk_attrs = get_nk_attrs(MobilitySubGraph)
        self.graph_nk_length = convert_nx2nk(MobilitySubGraph, idmap=self.nk_idmap, weight="length_meter")
        self.graph_nk_time = convert_nx2nk(MobilitySubGraph, idmap=self.nk_idmap, weight="time_min")
        self.MobilitySubGraph = load_graph_geometry(MobilitySubGraph)
        print("supplementary graphs created")
        return self

    def setter(self,
               attr_name, 
               attr_value,
               attr_type,
               validate = True) -> None:
          
          if validate == True:
              if attr_type == 'df':
                  attr_value = self.validate_df(attr_name, 
                                                self.city_name, 
                                                df = attr_value)
              elif attr_type =='graph':
                  attr_value = self.validate_graphml(attr_name, 
                                                     self.city_name, 
                                                     G = attr_value)
          try:
              return setattr(self, 
                             attr_name,
                             attr_value)
          except Exception as e:
              print(f"{e} - sth went wrong")

