# Paper 3 — Master README

### *Three-Oscillator Topography & Classical Contextuality*

### *Experiments E301–E399 • Missions 1–4*

---

## Overview

Paper 3 completes **Arc 1** (Paper 1 → Paper 2 → Paper 3) by moving from:

* **Pairs (2 oscillators)** → geometry
* **Landscapes (parameter sweeps)** → structure
* **Triangles (3 oscillators)** → *irreducible topography*

This paper demonstrates, for the first time in a classical system:

* circulating loop-charge regimes,
* nontransitive coherence (A→B→C→A),
* braided phase dynamics,
* path-order–dependent S-metrics, and
* **classical contextuality** arising from topology, not nonlocality.

The experimental arc is divided into four Missions, each with its own config set, scripts, analysis folder, and paper outputs.

---

## Mission Suite

| Mission       | Experiments | Focus                                                         |
| ------------- | ----------- | ------------------------------------------------------------- |
| **Mission 1** | E301–E320   | **K-Matrix Sweeps** — frustration, sign structure, K-grids    |
| **Mission 2** | E321–E340   | **Initialization Manifolds** — basins, history dependence     |
| **Mission 3** | E341–E380   | **Loop Charge & Braiding** — Φ modes, braid index, chaos edge |
| **Mission 4** | E381–E399   | **Path-Order & Contextuality** — ΔS(order), 2-body vs 3-body  |

All 99 experiments together form the empirical foundation of Paper 3.

> **Note on Scientific Structure**
>
> Mission 3 contains **two distinct scientific regimes**:
> - **3A. Loop-Charge (Φ) Dynamics**
> - **3B. Braiding & Phase-Order Dynamics**
>
> These remain **separate analytical sections in the paper**, even though they
> share computational infrastructure and therefore live in the same Mission
> directory. Loop-charge and braiding represent different dynamical signatures
> of the three-oscillator system and are treated independently in the final
> results narrative.
>
> Missions are execution units for TC; scientific regimes remain five-part:
> 1. K-Matrix Geometry
> 2. Initialization Manifolds
> 3A. Loop-Charge Modes
> 3B. Braiding Modes
> 4. Path-Order & Contextuality

---

## Directory Layout

```
Paper3/
│
├── README.md                <-- Master README (this file)
│
├── Paper3_Mission1/
│   ├── README.md
│   ├── config/
│   │   ├── base_M1_E3xx.json
│   │   ├── overrides_M1_E3xx.json
│   │   └── E301.json ... E320.json
│   ├── scripts/
│   ├── analysis/
│   └── paper/
│
├── Paper3_Mission2/
│   ├── README.md
│   ├── config/
│   │   ├── base_M2_E3xx.json
│   │   ├── overrides_M2_E3xx.json
│   │   └── E321.json ... E340.json
│   ├── scripts/
│   ├── analysis/
│   └── paper/
│
├── Paper3_Mission3/
│   ├── README.md
│   ├── config/
│   │   ├── base_M3_E3xx.json
│   │   ├── overrides_M3_E3xx.json
│   │   └── E341.json ... E380.json
│   ├── scripts/
│   ├── analysis/
│   └── paper/
│
└── Paper3_Mission4/
    ├── README.md
    ├── config/
    │   ├── base_M4_E3xx.json
    │   ├── overrides_M4_E3xx.json
    │   └── E381.json ... E399.json
    ├── scripts/
    ├── analysis/
    └── paper/
```

---

## Scientific Goals

### 1. Establish 3-oscillator dynamics as the minimal classical topological system

Unlike 2-node systems, the triangle cannot be collapsed into a single phase difference.

It creates:

* loop charge (Φ)
* circulation
* frustration
* path-dependence
* braid classes
* attractor multiplicity

These cannot exist in a two-oscillator world.

---

### 2. Build the first topographic map of Φ, braids, and S-like surfaces

Mission 1 & 3 produce:

* Φ(K) / Φ(Δω) curves
* regime boundaries
* braid class partitions
* chaos-edge transitions

These form Figure panels F30–F39.

---

### 3. Demonstrate classical contextuality

Mission 4 shows that:

```
S_ABC ≠ S_ACB ≠ S_CBA
```

even though it's a *classical*, *local*, *deterministic* system.

Order matters because topology matters.

This is the climax of Arc 1.

---

## How to Run Experiments

TC should:

1. Enter any Mission directory.
2. Use `generate_configs.py` to emit individual configs:

   ```
   python generate_configs.py
   ```
3. Run scripts in `scripts/`, which load one config at a time.
4. Save results to each experiment's folder under `results/MissionX`.
5. Use `analysis/` notebooks to produce:

   * attractor maps
   * Φ timeseries
   * braid sequences
   * ΔS(order) surfaces
6. Export publication figures into `paper/`.

Each experiment is fully deterministic given its seed.

---

## Figure Anchors (for Paper)

* **F30** Triangle Topology + Loop Charge
* **F31** Phase Portraits
* **F32** K-Matrix Topography
* **F33** Circulating Φ State
* **F34** Nontransitive Coherence Map
* **F35** Braiding Diagram
* **F36** CHSH-like Surface in Triangle System
* **F37** Multi-Basin Map
* **F38** Chaos-Edge Behavior
* **F39** Contextuality Summary ΔS(order)

---

## Experiment Groups Summary

### E301–E320 → K-Matrix Geometry

### E321–E340 → Initialization Manifolds

### E341–E360 → Loop Charge Modes (static, circulating, intermittent, reversal)

### E361–E380 → Braiding Modes (permutations, braid index, chaos-edge)

### E381–E399 → Contextuality Modes (path order, ΔS, 2-body vs 3-body)

---

## Purpose of Paper 3 in Arc 1

Paper 3 answers the question:
**"What actually causes CHSH-like structure in classical systems?"**

Answer:
Not quantum rules.
Not randomness.
**Topology.**

The three-oscillator triangle is the first classical system with enough structure to produce:

* degeneracy lifting,
* phase memory,
* irreducible loops,
* order-sensitive readouts.

This closes Arc 1 and opens the door to RUT Proper.

---

## Status

* Mission folders created: ✅
* All config templates generated (base + overrides): ✅
* E301–E399 configs ready for execution: ✅
* Analysis pipelines and figure generation: next step
* Paper drafting begins after first-run sweeps

---

## Next Steps

Available on request:

* **Notion-ready table** for all E301–E399 (Experiment ID, Mission, Purpose, Script Name, Status)
* **Master `run_all.sh` script** to execute all Missions sequentially
* **Figure manifest** for TC to use when populating `/paper/`

---

*Paper 3 • Arc 1 Finale • Three-Oscillator Topography & Classical Contextuality*
