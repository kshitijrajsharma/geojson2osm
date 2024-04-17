import json
import xml.etree.ElementTree as ETree
from typing import TypeVar


T1 = TypeVar("T1", bound="Node")


class Node:
    def __init__(self: T1, coordinates: list, properties: dict) -> None:
        self.lat = coordinates[1]
        self.lon = coordinates[0]
        self.tags = properties


T2 = TypeVar("T2", bound="Way")


class Way:
    def __init__(self: T2, properties: dict) -> None:
        self.tags = properties
        self.nodes: list = []


T3 = TypeVar("T3", bound="Relation")


class Relation:
    def __init__(self: T3, properties: dict) -> None:
        self.tags = properties
        self.members: list = []


def geojson2osm(geojson: dict) -> str:
    features = geojson.get("features", [geojson])

    nodes: list = []
    nodes_index: dict = {}
    ways: list = []
    relations: list = []

    for feature in features:
        properties = feature.get("properties", {})
        for key in properties.keys():
            properties[key] = str(properties[key])
            
        geometry = feature.get("geometry", feature)

        if geometry["type"] == "Point":
            process_point(geometry["coordinates"],
                          properties, nodes, nodes_index)
        elif geometry["type"] == "LineString":
            process_line_string(
                geometry["coordinates"], properties, ways, nodes, nodes_index
            )
        elif geometry["type"] == "Polygon":
            process_multi_polygon(
                [geometry["coordinates"]],
                properties,
                relations,
                ways,
                nodes,
                nodes_index,
            )
        elif geometry["type"] == "MultiPolygon":
            process_multi_polygon(
                geometry["coordinates"], properties,
                relations, ways, nodes, nodes_index
            )
        else:
            print(f"Unknown or unsupported geometry type: {geometry['type']}")

    osm = ETree.Element("osm", {"version": "0.6", "generator": "geojson2osm"})

    last_node_id = -1
    for node in nodes:
        node_el = ETree.SubElement(
            osm,
            "node",
            {
                "id": str(last_node_id),
                "lat": str(node.lat),
                "lon": str(node.lon)
            },
        )

        for k, v in node.tags.items():
            ETree.SubElement(node_el, "tag", {"k": k, "v": v})

        node.id = last_node_id
        last_node_id -= 1

    last_way_id = -1
    for way in ways:
        way_el = ETree.SubElement(osm, "way", {"id": str(last_way_id)})

        for nd in way.nodes:
            ETree.SubElement(way_el, "nd", {"ref": str(nd.id)})

        for k, v in way.tags.items():
            ETree.SubElement(way_el, "tag", {"k": k, "v": v})

        way.id = last_way_id
        last_way_id -= 1

    last_relation_id = -1
    for relation in relations:
        id_dict = {"id": str(last_relation_id)}
        relation_el = ETree.SubElement(osm, "relation", id_dict)

        for member in relation.members:
            ETree.SubElement(
                relation_el,
                "member",
                {
                    "type": member["type"],
                    "ref": str(member["elem"].id),
                    "role": member["role"],
                },
            )

        for k, v in relation.tags.items():
            ETree.SubElement(relation_el, "tag", {"k": k, "v": v})

        relation.id = last_relation_id
        last_relation_id -= 1

    return ETree.tostring(osm, encoding="utf-8", method="xml").decode("utf-8")


def process_point(coordinates: list, properties: dict,
                  nodes: list, nodes_index: dict) -> None:
    node_hash = json.dumps(coordinates)
    if node_hash not in nodes_index:
        node = Node(coordinates, properties)
        nodes.append(node)
        nodes_index[node_hash] = node
    else:
        node = nodes_index[node_hash]
        for k, v in properties.items():
            node.tags[k] = v


def process_line_string(coordinates: list, properties: dict, ways: list,
                        nodes: list, nodes_index: dict) -> None:
    way = Way(properties)
    ways.append(way)

    for point in coordinates:
        node_hash = json.dumps(point)
        if node_hash not in nodes_index:
            node = Node(point, {})
            nodes.append(node)
            nodes_index[node_hash] = node
            way.nodes.append(node)

    # Close the way if it's not already closed
    if coordinates[0] == coordinates[-1]:
        way.nodes.append(way.nodes[0])


def process_multi_polygon(coordinates: list, properties: dict,
                          relations: list, ways: list,
                          nodes: list, nodes_index: dict) -> None:

    if len(coordinates) == 1 and len(coordinates[0]) == 1:
        return process_line_string(
            coordinates[0][0], properties, ways, nodes, nodes_index
        )

    relation = Relation(properties)
    relation.tags["type"] = "multipolygon"
    relations.append(relation)

    for polygon in coordinates:
        for index, ring in enumerate(polygon):
            way = Way({})
            ways.append(way)
            relation.members.append(
                {
                    "elem": way,
                    "type": "way",
                    "role": "outer" if index == 0 else "inner"
                }
            )

            for point in ring:
                node_hash = json.dumps(point)
                if node_hash not in nodes_index:
                    node = Node(point, {})
                    nodes.append(node)
                    nodes_index[node_hash] = node
                    way.nodes.append(node)

            if ring[0] == ring[-1]:
                way.nodes.append(way.nodes[0])
