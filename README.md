# Overcloud

Overcloud is a backend for [Overland](https://overland.p3k.app/). Overland is a GPS logger for iOS devices, written by Aaron Parecki. It logs your location in the background and sends them to a backend. There are [various backends](https://overland.p3k.app/#:~:text=Servers) available, some offering detailed visualizations and analyses. Overcloud takes a different approach. Instead of complex features, Overcloud focuses on simplicity. It stores your location history in a single file. That's its sole function. No visualizations, no analytics, just a single [GeoPackage](https://www.geopackage.org/) you can inspect with other GIS tools.

To recap:

- **Overcloud**: A backend for Overland, storing location data in a single GeoPackage.
- **Overland**: An iOS app that logs location data and sends it to a chosen server.
- **GeoPackage**: An open, standard format for geographic information.

## Install & Run

Overcloud is written in Python and uses the excellent [GeoPandas](https://geopandas.org/) library. If you have [Nix](https://nixos.org/) installed and [flakes enabled](https://nixos.wiki/wiki/flakes) you can run it in one go:

```sh
nix run github:cimm/overcloud -- --host 127.0.0.1 --token sEcretPasswOrd
```

> [!WARNING]  
> Overcloud does not utilize HTTPS, which means that all requests can be seen by anyone on the network. I personally run Overcloud on a server in my home that is not exposed to the internet.

## Development

The development environment is easily configured via Nix as well, simply run:

```sh
git clone https://github.com/cimm/overcloud.git
cd overcloud
nix develop
```

## GDAL

[GDAL](https://gdal.org) is a powerful library for working with raster and vector geospatial data, including GeoPackages. Here are some usefull examples for manipulating GeoPackages.

### Count Records

These two commands count the number of records in the `locations` layer (which Overcloud creates) and displays the results. Both give the same result but are formatted differently.

```sh
ogr2ogr /vsistdout/ input.gpkg -f CSV -sql "SELECT count(*) FROM locations"
ogrinfo input.gpkg -sql "SELECT count(*) FROM locations"
```

### Spit GeoPackage by Attribute

Creates a new GeoPackage, output.gpkg, containing only records with a "wifi" value. The filtered results will be stored in the `locations` layer. (Without the `-nln` parameter, the data would be placed directly in the GeoPackage's root.)

```sh
ogr2ogr output.gpkg input.gpkg -f GPKG -nln locations -sql "SELECT * FROM locations WHERE wifi IS NOT NULL" 
```

### Filter by Timestamp

Creates a new GeoPackage with a `locations` layer containing only records from April 2025.

```sh
ogr2ogr output.gpkg input.gpkg -f GPKG -nln locations -sql "SELECT * FROM locations WHERE timestamp >= '2025-03-01' AND timestamp < '2025-04-01'" 
```

### Combine GeoPackages

Append all data from the input.gpkg to the output.gpkg, leaving the input.gpkg GeoPackage untouched.

```sh
ogr2ogr -append input.gpkg output.gpkg
```

### Update Values

To clean up scattered location data recorded around my home Wi-Fi, I use this command. It updates all points where the "wifi" attribute is "MyHomeWiFi" to a single set of coordinates, effectively stacking them.

```sh
ogrinfo input.gpkg -sql "UPDATE locations SET geom = ST_GeomFromText('POINT(4.3499932 50.8449861)', 4326) WHERE wifi = 'MyHomeWiFi'"
```

### GeoPackage to GeoJSON

Convert the GeoPackage to GeoJSON.

```sh
ogr2ogr -f GeoJSON output.json input.gpkg
```
