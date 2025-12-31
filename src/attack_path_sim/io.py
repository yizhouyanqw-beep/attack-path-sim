from __future__ import annotations

from typing import Any, Dict, List, Tuple

import yaml

from .graph import AttackGraph


def load_graph_from_yaml(path: str) -> AttackGraph:
    """Load an AttackGraph from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}

    g = AttackGraph()

    # assets
    assets_raw = data.get("assets", []) or []
    assets: List[Tuple[str, float]] = []
    for a in assets_raw:
        if not isinstance(a, dict):
            continue
        name = str(a.get("name", "asset"))
        value = float(a.get("value", 1.0))
        assets.append((name, value))
    if assets:
        g.set_assets(assets)

    # nodes
    nodes_raw = data.get("nodes", {}) or {}
    if isinstance(nodes_raw, dict):
        for nid, meta in nodes_raw.items():
            desc = ""
            if isinstance(meta, dict):
                desc = str(meta.get("description", ""))
            g.add_node(str(nid), desc)

    # edges
    edges_raw = data.get("edges", []) or []
    for e in edges_raw:
        if not isinstance(e, dict):
            continue
        src = str(e["from"])
        dst = str(e["to"])
        action = str(e.get("action", "transition"))
        prob = float(e.get("prob", 0.0))
        cost = float(e.get("cost", 0.5))
        g.add_edge(src, dst, action, prob, cost)

    return g
