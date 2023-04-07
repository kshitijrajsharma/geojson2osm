import re
from geojson2osm import geojson2osm

def test_basic_conversion():
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"building": "yes"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [36.77125867456199, 37.2584759589531],
                            [36.77126068621875, 37.2584759589531],
                            [36.77126102149488, 37.258475158401765],
                            [36.771257668733604, 37.25847489155132],
                            [36.77125867456199, 37.2584759589531],
                        ]
                    ],
                },
            }
        ],
    }

    osm_xml = geojson2osm(geojson_data)
    assert '<osm version="0.6" generator="geojson2osm">' in osm_xml
    assert '<tag k="building" v="yes" />' in osm_xml

    # Check for the presence of a way element with a closed loop
    way_pattern = re.compile(r'<way id="-\d+">.*?</way>', re.DOTALL)
    assert re.search(way_pattern, osm_xml)

    # Check if the first and last node reference in the way are the same
    way_match = re.search(way_pattern, osm_xml)
    way_content = way_match.group()
    nd_pattern = re.compile(r'<nd ref="(-\d+)" />')
    nd_matches = nd_pattern.findall(way_content)
    assert nd_matches[0] == nd_matches[-1]

