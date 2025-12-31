# Attack-Path-Sim — README
*A Lightweight Attack Path Simulation Engine for Prototype Device & Supply-Chain Safety*

`attack-path-sim` is a small Python package for simulating **adversarial attack paths** across a process/system graph (e.g., prototype-device lifecycle, internal tooling, shipment handling, warehouse access, privileged APIs).

It focuses on **quantitative, explainable scoring** (probability × impact × cost) and includes a simple **Monte Carlo** engine for estimating expected loss and tail risk.

> **Status:** v0 (MVP). Built to be easy to extend for richer attack graphs, controls, and integrations.

---

## Features
- Build an **attack graph** from YAML (nodes + edges with probability/cost)
- Enumerate candidate paths and compute:
  - Path success probability
  - Path cost
  - Risk score (configurable)
- Run **Monte Carlo simulation** to estimate:
  - Expected loss
  - 95% tail loss (VaR-like)
- Minimal CLI: `attack-path-sim <yaml> --runs 20000`

---

## Install (local dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Quick Start
Run the included example:

```bash
attack-path-sim examples/prototype_device.yaml --runs 20000
```

You’ll see:
- Top critical paths ranked by risk score
- Simulation summary (expected loss, tail loss)

---

## YAML Format
Example: `examples/prototype_device.yaml`

```yaml
assets:
  - name: Prototype Device IP
    value: 0.9          # 0..1 (relative impact weight)
  - name: Shipment Tracking Data
    value: 0.6

nodes:
  warehouse_storage:
    description: Prototype stored in warehouse
  internal_api:
    description: Internal API for prototype tracking
  engineer_workstation:
    description: Engineer accesses device info

edges:
  - from: warehouse_storage
    to: internal_api
    action: badge_spoof
    prob: 0.10          # edge success probability (0..1)
    cost: 0.30          # attacker cost (0..1) lower is easier

  - from: internal_api
    to: engineer_workstation
    action: api_key_leak
    prob: 0.05
    cost: 0.20
```

**Notes**
- Nodes are identifiers; edges are directed.
- `assets[].value` controls impact scaling for loss estimation.

---

## How scoring works (v0)
For a path consisting of k edges:

- The path success probability is the product of all edge probabilities  
  `P_path = ∏ p_i`

- The total attacker cost is the sum of all edge costs  
  `C_path = ∑ c_i`

- The impact term `I` is computed from the aggregated asset value  
  (defaults to `1.0` if no assets are defined)

**Risk score definition:**

`score = (P_path × I) / (1 + C_path)`

You can customize scoring in `risk_model.py`.

---

## Development
Run tests:
```bash
pytest -q
```

---

## Roadmap
- Graph visualization (GraphViz)
- Controls/mitigations layer (reduce probs / increase costs)
- Scenario engine (batch what-if comparisons)
- More realistic loss models (heavy tails, correlated failures)

---

## License
MIT
