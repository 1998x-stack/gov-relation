"""GEXF graph builder for gov-relation networks.

Usage::

    builder = GEXFBuilder("七里河区领导班子关系图")
    builder.add_person(1, "胡真", current_post="区委书记")
    builder.add_organization(1, "中共七里河区委员会")
    builder.add_relationship(1, 2, "共事", "区委书记—区长")
    builder.write("output.gexf")
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .colors import node_color, node_size, node_shape


class GEXFBuilder:
    """Build a GEXF graph incrementally and write to file."""

    def __init__(self, title: str = "") -> None:
        self._title = title
        self._nodes: dict[int, dict[str, Any]] = {}
        self._edges: list[dict[str, Any]] = []
        self._edge_counter = 0

    def add_person(
        self,
        id: int,
        name: str,
        current_post: str = "",
        current_org: str = "",
        gender: str = "",
        ethnicity: str = "",
        birth: str = "",
        source: str = "",
    ) -> None:
        color = node_color(current_post)
        size = node_size(current_post)
        shape = node_shape(current_post)
        self._nodes[id] = {
            "label": name,
            "type": "person",
            "current_post": current_post,
            "current_org": current_org,
            "gender": gender,
            "ethnicity": ethnicity,
            "birth": birth,
            "source": source,
            "r": color["r"],
            "g": color["g"],
            "b": color["b"],
            "a": color["a"],
            "size": size,
            "shape": shape,
        }

    def add_organization(
        self,
        id: int,
        name: str,
        org_type: str = "",
        level: str = "",
        location: str = "",
    ) -> None:
        self._nodes[id] = {
            "label": name,
            "type": "organization",
            "org_type": org_type,
            "level": level,
            "location": location,
            "r": 220,
            "g": 220,
            "b": 220,
            "a": 0.8,
            "size": 15.0,
            "shape": "hexagon",
        }

    def add_relationship(
        self,
        source: int,
        target: int,
        rel_type: str,
        context: str = "",
        overlap_org: str = "",
        overlap_period: str = "",
    ) -> None:
        self._edge_counter += 1
        self._edges.append({
            "id": self._edge_counter,
            "source": source,
            "target": target,
            "type": rel_type,
            "context": context,
            "overlap_org": overlap_org,
            "overlap_period": overlap_period,
        })

    def write(self, path: Path | str) -> None:
        root = ET.Element(
            "gexf",
            attrib={
                "xmlns": "http://www.gexf.net/1.3",
                "xmlns:viz": "http://www.gexf.net/1.3/viz",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd",
                "version": "1.3",
            },
        )
        graph = ET.SubElement(root, "graph", attrib={
            "mode": "static",
            "defaultedgetype": "directed",
        })

        if self._title:
            meta = ET.SubElement(root, "meta")
            title_el = ET.SubElement(meta, "title")
            title_el.text = self._title

        attributes = ET.SubElement(graph, "attributes", attrib={"class": "node"})
        for attr_id, attr_name, attr_type in [
            ("0", "type", "string"),
            ("1", "current_post", "string"),
            ("2", "current_org", "string"),
            ("3", "gender", "string"),
            ("4", "ethnicity", "string"),
            ("5", "birth", "string"),
            ("6", "source", "string"),
            ("7", "org_type", "string"),
            ("8", "level", "string"),
            ("9", "location", "string"),
        ]:
            ET.SubElement(attributes, "attribute", attrib={"id": attr_id, "title": attr_name, "type": attr_type})

        edge_attrs = ET.SubElement(graph, "attributes", attrib={"class": "edge"})
        for eid, ename, etype in [
            ("0", "type", "string"),
            ("1", "context", "string"),
            ("2", "overlap_org", "string"),
            ("3", "overlap_period", "string"),
        ]:
            ET.SubElement(edge_attrs, "attribute", attrib={"id": eid, "title": ename, "type": etype})

        nodes_el = ET.SubElement(graph, "nodes")
        for nid, data in sorted(self._nodes.items()):
            node_el = ET.SubElement(nodes_el, "node", attrib={"id": str(nid), "label": data["label"]})
            ET.SubElement(node_el, "viz:size", attrib={"value": f"{data['size']:.1f}"})
            ET.SubElement(node_el, "viz:shape", attrib={"value": data["shape"]})
            ET.SubElement(node_el, "viz:color", attrib={
                "r": str(data["r"]),
                "g": str(data["g"]),
                "b": str(data["b"]),
                "a": str(data["a"]),
            })
            for attr_id, key in [
                ("0", "type"),
                ("1", "current_post"),
                ("2", "current_org"),
                ("3", "gender"),
                ("4", "ethnicity"),
                ("5", "birth"),
                ("6", "source"),
                ("7", "org_type"),
                ("8", "level"),
                ("9", "location"),
            ]:
                val = data.get(key, "")
                if val:
                    attvalues = node_el.find("attvalues")
                    if attvalues is None:
                        attvalues = ET.SubElement(node_el, "attvalues")
                    ET.SubElement(attvalues, "attvalue", attrib={"for": attr_id, "value": val})

        edges_el = ET.SubElement(graph, "edges")
        for edge in self._edges:
            edge_el = ET.SubElement(edges_el, "edge", attrib={
                "id": str(edge["id"]),
                "source": str(edge["source"]),
                "target": str(edge["target"]),
            })
            for attr_id, key in [("0", "type"), ("1", "context"), ("2", "overlap_org"), ("3", "overlap_period")]:
                val = edge.get(key, "")
                if val:
                    attvalues = edge_el.find("attvalues")
                    if attvalues is None:
                        attvalues = ET.SubElement(edge_el, "attvalues")
                    ET.SubElement(attvalues, "attvalue", attrib={"for": attr_id, "value": val})

        tree = ET.ElementTree(root)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(path), encoding="utf-8", xml_declaration=True)

    def to_string(self) -> str:
        import io
        buf = io.BytesIO()
        root = ET.Element("gexf", attrib={"xmlns": "http://www.gexf.net/1.3", "version": "1.3"})
        graph = ET.SubElement(root, "graph")
        nodes_el = ET.SubElement(graph, "nodes")
        for nid, data in sorted(self._nodes.items()):
            ET.SubElement(nodes_el, "node", attrib={"id": str(nid), "label": data["label"]})
        edges_el = ET.SubElement(graph, "edges")
        for edge in self._edges:
            ET.SubElement(edges_el, "edge", attrib={
                "id": str(edge["id"]), "source": str(edge["source"]), "target": str(edge["target"]),
            })
        tree = ET.ElementTree(root)
        tree.write(buf, encoding="utf-8", xml_declaration=True)
        return buf.getvalue().decode("utf-8")
