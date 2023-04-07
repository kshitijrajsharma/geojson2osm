# geojson2osm

A Python package to convert GeoJSON data to OSM XML format.

#### Inspired From [geojsontoosm](https://github.com/tyrasd/geojsontoosm)

## Install 

```
pip install geojson2osm
```

## Usage

```python
import json
from geojson2osm import geojson2osm

# Load your GeoJSON data
geojson_data = json.load(open('your_geojson_file.geojson'))

# Convert the GeoJSON data to OSM XML format
osm_xml = geojson2osm(geojson_data)

# Save the OSM XML data to a file
with open('output.osm', 'w') as output_file:
    output_file.write(osm_xml)

