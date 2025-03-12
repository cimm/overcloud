from shapely.geometry import Point
import geopandas as gpd
import pandas as pd


class GeoPackage:
    driver = 'GPKG'
    crs = 'EPSG:4326'

    def __init__(self, path, layer):
        self.path = path
        self.layer = layer

    def json_to_frame(self, json):
        data = {}
        data['geometry'] = [Point(json['geometry']['coordinates'])]
        for key, value in json['properties'].items():
            match key:
                case 'timestamp':
                    value = pd.to_datetime(value)
                case 'altitude':
                    value = int(value)
                case 'speed':
                    value = int(value)
                case 'course':
                    value = int(value)
                case 'horizontal_accuracy':
                    value = int(value)
                case 'vertical_accuracy':
                    value = int(value)
                case 'speed_accuracy':
                    value = int(value)
                case 'course_accuracy':
                    value = int(value)
                case 'battery_level':
                    value = int(value)
            data[key] = [value]
        return gpd.GeoDataFrame(data, crs=self.crs)

    def save_frames_to_file(self, frames):
        combined = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True),
                                    crs=self.crs)
        combined.to_file(self.path,
                         layer=self.layer,
                         driver=self.driver,
                         mode='a')
