from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .graph import Edge, AttackGraph


@dataclass(frozen=True)
class PathMetrics:
    p_success: float
    cost: float
    impact: float
    score: float


def total_impact(graph: AttackGraph) -> float:
    """Compute total impact weight from assets (0..N). Defaults to 1.0."""
    if not graph.assets:
        return 1.0
    return sum(v for _, v in graph.assets)


def path_probability(edges: List[Edge]) -> float:
    p = 1.0
    for e in edges:
        p *= e.prob
    return p


def path_cost(edges: List[Edge]) -> float:
    return sum(e.cost for e in edges)


def risk_score(p_success: float, impact: float, cost: float) -> float:
    """Default scoring: probability × impact discounted by cost."""
    return (p_success * impact) / (1.0 + cost)


def compute_path_metrics(graph: AttackGraph, edges: List[Edge]) -> PathMetrics:
    impact = total_impact(graph)
    p = path_probability(edges)
    c = path_cost(edges)
    s = risk_score(p, impact, c)
    return PathMetrics(p_success=p, cost=c, impact=impact, score=s)
