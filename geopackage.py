import geopandas as gpd


class GeoPackage:
    driver = 'GPKG'
    crs = 'EPSG:4326'

    def __init__(self, path, layer):
        self.path = path
        self.layer = layer

    def add_locations_to_layer(self, data):
        frame = gpd.GeoDataFrame(data, crs=self.crs)
        frame.to_file(self.path,
                      layer=self.layer,
                      driver=self.driver,
                      mode='a')

    def count_locations(self):  # method not used
        layer = gpd.read_file(self.path, layer=self.layer)
        return len(layer)
