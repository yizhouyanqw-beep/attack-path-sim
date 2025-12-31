from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .graph import AttackGraph, Edge


@dataclass(frozen=True)
class EdgeUpdate:
    action: str
    prob: Optional[float] = None
    cost: Optional[float] = None


def apply_edge_updates(graph: AttackGraph, updates: List[EdgeUpdate]) -> AttackGraph:
    """Return a modified copy of graph with updates applied by matching edge.action."""
    g2 = AttackGraph()
    g2.nodes = dict(graph.nodes)
    g2.adj = {k: list(v) for k, v in graph.adj.items()}
    g2.assets = list(graph.assets)

    update_map: Dict[str, EdgeUpdate] = {u.action: u for u in updates}

    new_adj: Dict[str, List[Edge]] = {}
    for src, edges in g2.adj.items():
        out: List[Edge] = []
        for e in edges:
            u = update_map.get(e.action)
            if u is None:
                out.append(e)
                continue
            out.append(
                Edge(
                    src=e.src,
                    dst=e.dst,
                    action=e.action,
                    prob=float(u.prob) if u.prob is not None else e.prob,
                    cost=float(u.cost) if u.cost is not None else e.cost,
                )
            )
        new_adj[src] = out
    g2.adj = new_adj
    return g2
