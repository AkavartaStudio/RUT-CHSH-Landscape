# RUT–CHSH Series

**Classical CHSH Geometry, Memory, and Network Topology**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Paper Status](https://img.shields.io/badge/status-preprint-orange)]()
[![Reproducibility](https://img.shields.io/badge/reproducibility-verified-brightgreen)]()

This repository contains the simulation engine, reproducibility configurations, and experiment data for a three-paper research program on classical CHSH geometry, temporal memory, and network topology.

---

## From CHSH Geometry to Echo Memory to Network Topology

### Paper 1: The CHSH Landscape
**"Continuous-Angle CHSH Correlations in Noisy Coupled Oscillators: A Systematic Parameter-Space Study"**

Maps the CHSH correlation functional across the (K, σ, Δω) parameter space for two coupled oscillators.

- **Location:** `paper1/`
- **Reproducibility:** [paper1/REPRODUCIBILITY.md](paper1/REPRODUCIBILITY.md)
- **Key results:** |S|_max = 2.819, collapse boundary σ_c(K) ≈ 0.60K + 0.22

### Paper 2: CHSH Memory Geometry
**"Echo Geometry of the Classical CHSH Ridge: Memory, Curvature, and Directional Susceptibility"**

Resolves the temporal structure of CHSH correlations, revealing memory collapse at σ_mem ≈ 0.002.

- **Location:** `paper2/`
- **Reproducibility:** [paper2/REPRODUCIBILITY.md](paper2/REPRODUCIBILITY.md)
- **Key results:** Universal σ_mem ≈ 0.002 (~30× below σ_c), three distinct regimes

### Paper 3: Network Topology (In Progress)
**"CHSH Memory in Three-Oscillator Networks"**

Extends the analysis to chain, star, and triangle topologies.

- **Location:** `paper3/`
- **Status:** Experiments in progress

---

## Repository Structure

```
RUT-CHSH-Landscape/
│
├── paper1/                    # Paper 1 manuscript, figures, configs
├── paper2/                    # Paper 2 manuscript, figures
├── paper3/                    # Paper 3 manuscript (in progress)
│
├── experiments/               # Experiment stages for Papers 2 & 3
│   ├── Paper2_Stage1-4/       # Memory threshold, curvature, echo, angle-field
│   └── Paper3_Stage2-4/       # Network topology experiments
│
├── analysis/                  # Shared analysis scripts and Paper 1 data
│   ├── scripts/rut_core.py    # Core simulation engine
│   └── data/paper1/           # Paper 1 raw data
│
├── docs/                      # Documentation
├── CITATION.cff               # Citation metadata
└── LICENSE                    # CC BY 4.0
```

---

## Quick Verification (30 seconds)

**Want to see |S| ≈ 2.82 right now?**

```bash
pip install numpy
python quick_verify_chsh.py
```

Output:
```
RESULTS (10 trials):
  |S| = 2.785 ± 0.001

  ✓ CLASSICAL BOUND VIOLATED by 0.785
  ✓ This is 98.5% of Tsirelson bound
```

This self-contained script demonstrates CHSH violation in coupled oscillators without any setup beyond numpy.

---

## Full Reproducibility

### Paper 1 (complete pipeline, ~5 hours)
```bash
cd analysis/scripts/paper1_runners
bash RUN_ALL_PAPER1.sh
```

### Paper 2
```bash
cd experiments/Paper2_Stage1/scripts
bash RUN_P2_STAGE1_sigma_mem.sh
# ... see paper2/REPRODUCIBILITY.md for full instructions
```

### Generate Figures
```bash
# Paper 1
cd paper1/figures/scripts && for f in generate_fig*.py; do python3 "$f"; done

# Paper 2
cd experiments/Paper2_Stage*/analysis/figs && python3 generate_*.py
```

---

## Key Results Across the Series

| Concept | Result | Source |
|---------|--------|--------|
| Classical CHSH violation exists | \|S\|_max = 2.819 ± 0.003 | Paper 1 |
| Instantaneous collapse boundary | σ_c(K) ≈ 0.60K + 0.22 | Paper 1 |
| Long-lag memory collapses universally | σ_mem ≈ 0.002 (independent of K) | Paper 2 |
| Separation of scales | σ_mem ≪ σ_c (≈1–2 orders of magnitude) | Paper 2 |
| Intermediate regime | |S| > 2 but memory already gone | Paper 2 |
| Angle-field twisting | optimal geometry deforms under noise | Paper 2 |
| Three-oscillator memory | dependent on topology (chain, star, triangle) | Paper 3 (in progress) |

---

## Citation

### Paper 1
**McRae, K.** (2025). *Continuous-Angle CHSH Correlations in Noisy Coupled Oscillators: A Systematic Parameter-Space Study (Paper 1: The CHSH Landscape).* Preprint.

### Paper 2
**McRae, K.** (2025). *Echo Geometry of the Classical CHSH Ridge: Memory, Curvature, and Directional Susceptibility (Paper 2: The Memory Landscape).* Preprint.

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

---

## License

This work is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), permitting reuse with attribution.

---

## Contact

**Kelly McRae**
Akavarta Studio
[studioakavarta@gmail.com](mailto:studioakavarta@gmail.com)

---

*Geometry ↦ Memory ↦ Topology*
