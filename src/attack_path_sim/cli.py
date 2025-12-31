from __future__ import annotations

import argparse
from typing import Optional

from .analysis import format_path, rank_paths
from .io import load_graph_from_yaml
from .simulator import simulate_losses


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="attack-path-sim", description="Attack path simulation (v0)")
    parser.add_argument("yaml", help="Path to YAML file defining attack graph")
    parser.add_argument("--runs", type=int, default=20000, help="Monte Carlo runs")
    parser.add_argument("--top", type=int, default=5, help="Top paths to display")
    parser.add_argument("--max-depth", type=int, default=6, help="Max path length")
    parser.add_argument("--base-loss", type=float, default=250000.0, help="Base loss amount ($) for scaling")
    args = parser.parse_args(argv)

    g = load_graph_from_yaml(args.yaml)

    ranked = rank_paths(g, max_depth=args.max_depth, top_k=max(args.top, 10))
    print("\nTop critical paths (ranked):")
    for i, rp in enumerate(ranked[: args.top], start=1):
        m = rp.metrics
        print(
            f"{i:>2}. {format_path(rp.edges)} | "
            f"P={m.p_success:.6f} Cost={m.cost:.2f} Impact={m.impact:.2f} Score={m.score:.6f}"
        )

    res = simulate_losses(
        g,
        runs=args.runs,
        base_loss=args.base_loss,
        max_depth=args.max_depth,
        top_paths=max(args.top, 10),
    )
    print("\nMonte Carlo summary:")
    print(f"  runs:          {res.runs}")
    print(f"  expected loss: ${res.expected_loss:,.2f}")
    print(f"  p95 loss:      ${res.p95_loss:,.2f}")
    print(f"  max loss:      ${res.max_loss:,.2f}")
    print()
    return 0
