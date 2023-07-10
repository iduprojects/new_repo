from ..data.CityInformationModel import CityInformationModel
import os
import networkx as nx
import shapely
import pandas as pd
import geopandas as gpd

def Load_Example_Model():

    path = os.getcwd()

    Example_model = CityInformationModel(city_name = 'saint-petersburg',
                                         city_crs=32636)
### MobilityGraph #####################################################
    MobilityGraph = nx.read_graphml(f"{path}/scr/CityGeoTools/examples/spb_exmpl_MobilityGraph.graphml", 
                        node_type=int)
    MobilityGraph = nx.relabel_nodes(MobilityGraph, (dict(zip(MobilityGraph.nodes,
                                    [int(x) for x in MobilityGraph.nodes]))))
    for i, n in MobilityGraph.nodes(data=True):
        n['geometry'] = shapely.geometry.Point(n['x'], n['y'])

    Example_model.setter(attr_name = 'MobilityGraph',
                         attr_value = MobilityGraph,
                         attr_type = 'graph')
    Example_model.get_supplementary_graphs()
### AdministrativeUnits #####################################################
    AdministrativeUnits = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_AdministrativeUnits.geojson", 
                                        driver = "GeoJSON")
    Example_model.setter(attr_name = 'AdministrativeUnits',
                         attr_value = AdministrativeUnits,
                         attr_type = 'df')
### Blocks #####################################################
    Blocks = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_Blocks.geojson",
                           driver = "GeoJSON")
    Example_model.setter(attr_name = 'Blocks',
                         attr_value = Blocks,
                         attr_type = 'df')
### Buildings #####################################################
    Buildings = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_Buildings.geojson", 
                              driver = "GeoJSON")
    Example_model.setter(attr_name = 'Buildings',
                         attr_value = Buildings,
                         attr_type = 'df')  
### LivingSituations #####################################################
    LivingSituations = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_LivingSituations.xlsx")
    Example_model.setter(attr_name = 'LivingSituations',
                         attr_value = LivingSituations,
                         attr_type = 'df') 
### LivingSituationsCityServiceTypes #####################################################
    LivingSituationsCityServiceTypes = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_LivingSituationsCityServiceTypes.xlsx")
    Example_model.setter(attr_name = 'LivingSituationsCityServiceTypes',
                         attr_value = LivingSituationsCityServiceTypes,
                         attr_type = 'df')
### Municipalities #####################################################
    Municipalities = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_Municipalities.geojson", 
                                   driver = "GeoJSON")
    Example_model.setter(attr_name = 'Municipalities',
                         attr_value = Municipalities,
                         attr_type = 'df')
### PublicTransportStops #####################################################
    PublicTransportStops = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_PublicTransportStops.geojson",
                                         driver = "GeoJSON")
    Example_model.setter(attr_name = 'PublicTransportStops',
                         attr_value = PublicTransportStops,
                         attr_type = 'df')
### Services #####################################################
    Services = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_Services.geojson", 
                                        driver = "GeoJSON")
    Example_model.setter(attr_name = 'Services',
                         attr_value = Services,
                         attr_type = 'df')
### ServiceTypes #####################################################
    ServiceTypes = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_ServiceTypes.xlsx")
    Example_model.setter(attr_name = 'ServiceTypes',
                         attr_value = ServiceTypes,
                         attr_type = 'df')
### RecreationalAreas #####################################################
    RecreationalAreas = gpd.read_file(f"{path}/scr/CityGeoTools/examples/spb_exmpl_RecreationalAreas.geojson", 
                                        driver = "GeoJSON")
    Example_model.setter(attr_name = 'RecreationalAreas',
                         attr_value = RecreationalAreas,
                         attr_type = 'df')
### ValueTypes #####################################################
    ValueTypes = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_ValueTypes.xlsx")
    Example_model.setter(attr_name = 'ValueTypes',
                         attr_value = ValueTypes,
                         attr_type = 'df')
### SocialGroups #####################################################
    SocialGroups = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_SocialGroups.xlsx")
    Example_model.setter(attr_name = 'SocialGroups',
                         attr_value = SocialGroups,
                         attr_type = 'df')    

### SocialGroupsValueTypesLivingSituations #####################################################
    SocialGroupsValueTypesLivingSituations = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_SocialGroupsValueTypesLivingSituations.xlsx")
    Example_model.setter(attr_name = 'SocialGroupsValueTypesLivingSituations',
                         attr_value = SocialGroupsValueTypesLivingSituations,
                         attr_type = 'df')    
### Demands #####################################################
    Demands = pd.read_excel(f"{path}/scr/CityGeoTools/examples/spb_exmpl_Demands.xlsx")
    Example_model.setter(attr_name = 'Demands',
                         attr_value = Demands,
                         attr_type = 'df')    

    return Example_model
