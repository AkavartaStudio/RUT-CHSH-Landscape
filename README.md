# RUT-CHSH-Landscape

**Continuous-Angle CHSH Correlations in Noisy Coupled Oscillators**
**Paper 1: The CHSH Landscape**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Paper Status](https://img.shields.io/badge/status-preprint-orange)]()
[![Reproducibility](https://img.shields.io/badge/reproducibility-verified-brightgreen)]()

This repository contains the complete simulation code, data, and figure-generation tools supporting the manuscript *"Continuous-Angle CHSH Correlations in Noisy Coupled Oscillators: A Systematic Parameter-Space Study."* All results are fully reproducible using the scripts provided.

---

## Overview

We study how the CHSH correlation functional behaves in a classical two-oscillator system with noise, detuning, and variable measurement geometry. Although the CHSH test originates in quantum information, here it is used strictly as a correlation geometry diagnostic for classical dynamics.

Key observations include:

- **Maximum CHSH value:** |S|<sub>max</sub> = 2.819 ± 0.003
- **Noise–coupling collapse boundary:** σ<sub>c</sub>(K) ≈ 0.60K + 0.22
- **Optimal angles:** (Δα, Δβ) ≈ (95°, 84°)
- **Detuning optimum:** Δω* ≈ 0.14K
- **Temporal memory:** ρ<sub>S</sub>(τ=10) ≈ 0.86 even past collapse

These results reveal structured classical dynamics and a narrow, tune-dependent high-correlation regime.

---

## Reproducibility

**Run all experiments (A1, A2, A3, B1):**
```bash
cd analysis/scripts/paper1_runners
bash RUN_ALL_PAPER1.sh
```

**Generate all manuscript figures:**
```bash
cd paper/figures/scripts
for f in generate_fig*.py; do python3 "$f"; done
```

All figure names, output files, and corresponding scripts follow a one-to-one mapping (see [REPRODUCIBILITY.md](REPRODUCIBILITY.md)).

A complete verification workflow, determinism tests, and manifest metadata are included in `docs/reproducibility/`.

---

## Repository Structure

```
RUT-CHSH-Landscape/
│
├── analysis/
│   ├── scripts/
│   │   ├── rut_core.py
│   │   ├── paper1_runners/
│   │   ├── control_random_params.py
│   │   └── run_extended_sigma_sweep.py
│   └── data/paper1/
│
├── paper/
│   ├── PAPER1_COMPLETE_DRAFT.tex
│   ├── PAPER1_COMPLETE_DRAFT.pdf
│   ├── figures/
│   ├── figures/scripts/
│   └── configs_paper1/
│
├── docs/reproducibility/
├── REPRODUCIBILITY.md
├── CITATION.md
├── CITATION.cff
├── CLEANROOM_TEST_PROCEDURE.md
└── LICENSE
```

---

## Experiments

- **A1 — Noise–Coupling Collapse:** Determines σ<sub>c</sub>(K) across the parameter range.
- **A2 — Angle Optimization:** Maps CHSH values across measurement geometries (Δα, Δβ).
- **A3 — Detuning Sweep:** Identifies optimal frequency mismatch Δω*.
- **B1 — Temporal Memory:** Evaluates persistence of ρ<sub>S</sub>(τ) beyond the instantaneous collapse point.

All configurations are in `paper/configs_paper1/`.

---

## Figures

Twelve manuscript figures (7 main + 5 supplementary) are fully script-generated.
Each script is named by figure number (e.g., `generate_fig5_delta_omega.py` → `fig5_delta_omega.png`).

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the complete figure-to-script mapping.

---

## Citation

**McRae, K.** (2025). *Continuous-Angle CHSH Correlations in Noisy Coupled Oscillators: A Systematic Parameter-Space Study (Paper 1: The CHSH Landscape).* Preprint.

See [CITATION.md](CITATION.md) and [CITATION.cff](CITATION.cff) for formatted entries.

---

## License

This work is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), permitting reuse with attribution.

---

## Contact

**Kelly McRae**
Akavarta Studio
[studioakavarta@gmail.com](mailto:studioakavarta@gmail.com)
