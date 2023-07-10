import geopandas as gpd

from jsonschema.exceptions import ValidationError


class BaseMethod():

    def __init__(self, city_model):
        self.city_model = city_model
        self.city_crs = city_model.city_crs

    @staticmethod
    def _get_territorial_select(area_type, area_id, *args):
        return tuple(df.loc[df[area_type + "_id"] == area_id].copy() for df in args)

    @staticmethod
    def _get_custom_polygon_select(geojson: dict, set_crs, *args):
        geojson_crs = geojson["crs"]["properties"]["name"]
        geojson = gpd.GeoDataFrame.from_features(geojson['features'])
        geojson = geojson.set_crs(geojson_crs).to_crs(set_crs)
        custom_polygon = geojson['geometry'][0]
        return tuple(df.loc[df.within(custom_polygon)].copy() for df in args)