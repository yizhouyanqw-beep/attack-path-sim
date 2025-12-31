from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Node:
    id: str
    description: str = ""


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    action: str
    prob: float  # success probability (0..1)
    cost: float  # attacker cost (0..1), lower = easier


class AttackGraph:
    """A minimal directed graph for attack-path modeling."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.adj: Dict[str, List[Edge]] = {}
        self.assets: List[Tuple[str, float]] = []  # (name, value 0..1)

    def add_node(self, node_id: str, description: str = "") -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(id=node_id, description=description)
        self.adj.setdefault(node_id, [])

    def add_edge(self, src: str, dst: str, action: str, prob: float, cost: float) -> None:
        if not (0.0 <= prob <= 1.0):
            raise ValueError(f"edge prob must be in [0,1], got {prob}")
        if not (0.0 <= cost <= 1.0):
            raise ValueError(f"edge cost must be in [0,1], got {cost}")
        self.add_node(src)
        self.add_node(dst)
        self.adj[src].append(Edge(src=src, dst=dst, action=action, prob=prob, cost=cost))

    def set_assets(self, assets: List[Tuple[str, float]]) -> None:
        for name, v in assets:
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"asset value must be in [0,1], got {v} for {name}")
        self.assets = assets

    def iter_edges(self) -> List[Edge]:
        out: List[Edge] = []
        for edges in self.adj.values():
            out.extend(edges)
        return out

    def paths(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        max_depth: int = 6,
    ) -> List[List[Edge]]:
        """Enumerate simple paths of edges up to max_depth.

        If start/end are None, paths are generated from all nodes to all nodes.
        """
        starts = [start] if start else list(self.nodes.keys())
        ends = {end} if end else set(self.nodes.keys())

        results: List[List[Edge]] = []

        def dfs(cur: str, path_edges: List[Edge], visited: set) -> None:
            if len(path_edges) > max_depth:
                return
            if cur in ends and path_edges:
                results.append(list(path_edges))
            for e in self.adj.get(cur, []):
                if e.dst in visited:
                    continue
                visited.add(e.dst)
                path_edges.append(e)
                dfs(e.dst, path_edges, visited)
                path_edges.pop()
                visited.remove(e.dst)

        for s in starts:
            if s not in self.nodes:
                continue
            dfs(s, [], {s})

        return results
