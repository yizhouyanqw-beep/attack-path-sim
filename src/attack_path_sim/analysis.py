from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .graph import AttackGraph, Edge
from .risk_model import PathMetrics, compute_path_metrics


@dataclass(frozen=True)
class RankedPath:
    edges: List[Edge]
    metrics: PathMetrics


def rank_paths(
    graph: AttackGraph,
    start: Optional[str] = None,
    end: Optional[str] = None,
    max_depth: int = 6,
    top_k: int = 10,
) -> List[RankedPath]:
    """Enumerate and rank paths by risk score."""
    paths = graph.paths(start=start, end=end, max_depth=max_depth)
    ranked: List[RankedPath] = []
    for p in paths:
        m = compute_path_metrics(graph, p)
        ranked.append(RankedPath(edges=p, metrics=m))

    ranked.sort(key=lambda rp: rp.metrics.score, reverse=True)
    return ranked[:top_k]


def format_path(edges: List[Edge]) -> str:
    if not edges:
        return "<empty>"
    nodes = [edges[0].src] + [e.dst for e in edges]
    return " → ".join(nodes)
