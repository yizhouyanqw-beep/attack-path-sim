from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Optional

from .analysis import rank_paths
from .graph import AttackGraph, Edge
from .risk_model import compute_path_metrics


@dataclass(frozen=True)
class SimulationResult:
    runs: int
    expected_loss: float
    p95_loss: float
    max_loss: float


def _path_loss_base(graph: AttackGraph, base_loss: float) -> float:
    # Impact scaling: sum(asset_value) is treated as a multiplier.
    impact = sum(v for _, v in graph.assets) if graph.assets else 1.0
    return base_loss * impact


def _simulate_one_path(edges: List[Edge]) -> bool:
    # A path is successful if all edges succeed in sequence.
    for e in edges:
        if random.random() > e.prob:
            return False
    return True


def simulate_losses(
    graph: AttackGraph,
    runs: int = 20000,
    base_loss: float = 250_000.0,
    max_depth: int = 6,
    top_paths: int = 10,
    seed: Optional[int] = None,
) -> SimulationResult:
    """Monte Carlo simulate losses.

    Strategy (v0):
    - Rank top candidate paths
    - Each run: sample which (if any) path succeeds
    - If a path succeeds, incur a loss proportional to impact and inversely to cost
    """
    if seed is not None:
        random.seed(seed)

    candidates = rank_paths(graph, max_depth=max_depth, top_k=top_paths)
    if not candidates:
        return SimulationResult(runs=runs, expected_loss=0.0, p95_loss=0.0, max_loss=0.0)

    losses: List[float] = []
    for _ in range(runs):
        run_loss = 0.0
        # In v0 we assume the adversary tries the top paths first.
        for rp in candidates:
            m = compute_path_metrics(graph, rp.edges)
            if _simulate_one_path(rp.edges):
                # Loss scaled by impact and discounted by attacker cost (cheaper attacks tend to be more frequent)
                loss = _path_loss_base(graph, base_loss) * (m.p_success + 1e-9) / (1.0 + m.cost)
                run_loss = max(run_loss, loss)
                break
        losses.append(run_loss)

    losses.sort()
    expected = sum(losses) / len(losses)
    p95 = losses[int(0.95 * (len(losses) - 1))]
    return SimulationResult(runs=runs, expected_loss=expected, p95_loss=p95, max_loss=losses[-1])
