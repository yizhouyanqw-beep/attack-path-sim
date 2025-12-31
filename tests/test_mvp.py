from attack_path_sim.io import load_graph_from_yaml
from attack_path_sim.analysis import rank_paths
from attack_path_sim.simulator import simulate_losses


def test_rank_paths(tmp_path):
    yaml_path = tmp_path / "g.yaml"
    yaml_path.write_text(
        """assets:
  - name: A
    value: 1.0
nodes:
  s: {description: start}
  m: {description: mid}
  e: {description: end}
edges:
  - from: s
    to: m
    action: a1
    prob: 0.5
    cost: 0.1
  - from: m
    to: e
    action: a2
    prob: 0.5
    cost: 0.2
""",
        encoding="utf-8",
    )
    g = load_graph_from_yaml(str(yaml_path))
    ranked = rank_paths(g, start="s", end="e", max_depth=4, top_k=5)
    assert ranked, "should find at least one path"
    assert ranked[0].metrics.p_success == 0.25


def test_simulate_losses(tmp_path):
    yaml_path = tmp_path / "g.yaml"
    yaml_path.write_text(
        """assets:
  - name: A
    value: 1.0
nodes:
  s: {}
  e: {}
edges:
  - from: s
    to: e
    action: direct
    prob: 1.0
    cost: 0.0
""",
        encoding="utf-8",
    )
    g = load_graph_from_yaml(str(yaml_path))
    res = simulate_losses(g, runs=200, seed=42)
    assert res.expected_loss > 0
