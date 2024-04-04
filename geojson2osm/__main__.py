import json
import sys
from geojson2osm import geojson2osm


def main() -> None:
    # Load your GeoJSON data
    input = sys.argv[1]
    geojson_data = json.load(open(input))

    # Convert the GeoJSON data to OSM XML format
    osm_xml = geojson2osm(geojson_data)

    # Save the OSM XML data to a file
    output = sys.argv[2]
    with open(output, 'w') as output_file:
        output_file.write(osm_xml)
    

if __name__ == '__main__':
    main()
