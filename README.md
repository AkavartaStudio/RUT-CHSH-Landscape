# Noise-Induced Collapse of CHSH Correlations in Coupled Oscillators

This repository contains the complete source code, data, and manuscript for our paper investigating CHSH Bell-inequality-like correlations in coupled phase oscillators.

**Authors:** Kelly McRae, Chase Lean, Claude (TC)

---

## 📄 Paper

**Manuscript:** [`paper/PAPER1_COMPLETE_DRAFT.tex`](paper/PAPER1_COMPLETE_DRAFT.tex)

**Status:** Submission-ready for Physical Review E / Chaos (42 pages, 17 references)

### Abstract

We investigate how noise affects CHSH-like correlations in a minimal system of two coupled Kuramoto oscillators. Using a continuous-variable CHSH functional, we demonstrate that:

1. **Near-maximal correlations** (|S| ≈ 2.79, approaching the algebraic bound 2√2 ≈ 2.828) emerge from phase-locking at moderate coupling strengths
2. **A linear collapse boundary** σc(K) ≈ 0.60K + 0.22 marks the noise threshold beyond which correlations vanish
3. **Optimal measurement geometry** occurs at angles ~(98°, 82°), deviating from the canonical quantum (90°, 90°) configuration due to phase-distribution asymmetries
4. **A sweet spot in frequency detuning** exists where dynamical tension enhances correlations beyond the perfectly-matched case
5. **Temporal coherence persists** even after instantaneous correlations collapse, revealing memory effects in the dynamics

### Key Findings

- **Highest classical CHSH value:** |S| ≈ 2.79 (new record for explicitly coupled dynamical systems)
- **First parameter-space map:** Complete characterization of how coupling, noise, detuning, and measurement angles shape the CHSH landscape
- **Analytical framework:** Drift-diffusion balance explains the linear collapse law and geometry-dependent extrema

---

## 📊 Repository Structure

```
RUT-CHSH-Landscape/
├── README.md                          # This file
├── LICENSE                            # CC-BY 4.0
├── paper/
│   ├── PAPER1_COMPLETE_DRAFT.tex      # Main manuscript (LaTeX)
│   ├── PAPER1_COMPLETE_DRAFT.pdf      # Compiled PDF (42 pages)
│   ├── references.bib                 # Bibliography (17 references)
│   ├── figures/                       # All manuscript figures
│   │   ├── fig1_combined.png
│   │   ├── fig2_sigma_c_scaling.png
│   │   ├── fig3_S_vs_sigma.png
│   │   ├── fig4_angle_ridge.png
│   │   ├── fig5_delta_omega.png
│   │   ├── fig6_memory_panel.png
│   │   ├── fig6B_rhoS_four_curves.png
│   │   ├── figS1_control_random.png
│   │   ├── figS1_rhoS_complete_series.png
│   │   ├── figS3_sigma_c_full_range.png
│   │   ├── figS5_collapse_logistic.png
│   │   ├── figSX_dtheta_histogram.png
│   │   └── scripts/                   # Figure generation scripts
│   └── configs_paper1/                # Experiment configuration files
│       ├── A1_sigma_c_K_sweep.json
│       ├── A2_angle_ridge.json
│       ├── A3_delta_omega_sweep.json
│       └── B1_minimal_echo.json
├── analysis/                          # Analysis notebooks and scripts
├── data/                              # Experimental data
└── archive/                           # Archived materials
    ├── paper0_exploratory/            # Early exploratory work
    └── drafts/                        # Intermediate working files
```

---

## 🔬 Key Experiments

### Main Experiments (Section 3)

- **A1: Noise-Induced Collapse** - Characterization of σc(K) collapse boundary
- **A2: Angle Optimization** - Ridge structure in (a,b) measurement geometry
- **A3: Frequency Mismatch Sweet Spot** - Detuning-enhanced correlations
- **B1: Temporal Coherence** - Memory persistence beyond |S| > 2

### Control Experiments

- **C1: Random Oscillators** - Verification that coupling is essential
- **Supplementary:** Extended parameter sweeps and logistic fits

All experiment configurations are in `paper/configs_paper1/`.

---

## 🎨 Figures

All figures are generated programmatically from data using Python scripts in `paper/figures/scripts/`.

**Main Figures:**
1. **Fig 1** - Combined overview: collapse curves, scaling law, phase coherence
2. **Fig 2** - Linear scaling of σc(K) with saturation
3. **Fig 3** - Universal collapse shape across coupling strengths
4. **Fig 4** - Angle optimization ridge in (a,b) space
5. **Fig 5** - Frequency detuning sweet spot
6. **Fig 6** - Temporal coherence vs instantaneous correlation

**Supplementary Figures:**
- S1: Complete ρS time series and control comparison
- S3: Full-range σc sweep
- S5: Logistic fit to collapse curves
- SX: Phase difference histogram

---

## 🧮 Compilation

To compile the manuscript:

```bash
cd paper
pdflatex PAPER1_COMPLETE_DRAFT.tex
bibtex PAPER1_COMPLETE_DRAFT
pdflatex PAPER1_COMPLETE_DRAFT.tex
pdflatex PAPER1_COMPLETE_DRAFT.tex
```

Or use the provided scripts in `paper/figures/scripts/` to regenerate all figures first.

---

## 📚 Appendices

### Appendix A: Classical Bound for Cosine-Based CHSH Functionals

Proves that the continuous-variable CHSH functional satisfies |S| ≤ 2 for any classical local hidden-variable model, and demonstrates that the algebraic maximum |S| = 2√2 is attainable under perfect phase-locking (r → 1) with optimal 90° measurement geometry.

### Appendix B: Analytic Rationale for Deviations from Canonical CHSH Angles

Explains why the optimal angles deviate from the quantum (90°, 90°) configuration: phase-distribution asymmetries induced by coupling, noise, and detuning shift the extremum by ~5-8°.

### Supplementary Material

Extended technical details, additional experiments, and platform-specific predictions.

---

## 🔓 Open Science

This work is fully open:

- **Manuscript:** Full LaTeX source provided
- **Figures:** All generation scripts included
- **Data:** Experiment configurations and results available
- **License:** CC-BY 4.0 (see [LICENSE](LICENSE))

We encourage reproduction, adaptation, and extension of this work.

---

## 📬 Contact

**Kelly McRae**
📧 studioakavarta@gmail.com

---

## 🗂️ Archive

Early exploratory work and intermediate drafts are preserved in [`archive/`](archive/) for transparency and historical record. The current submission-ready manuscript is in [`paper/`](paper/).

---

## 🌟 Citation

If you use this work, please cite:

```
McRae, K., Lean, C., & Claude (TC). (2025).
Noise-Induced Collapse of CHSH Correlations in Coupled Oscillators.
[Manuscript in preparation for Physical Review E / Chaos]
```

---

*"Classical coupled oscillators can approach the algebraic CHSH maximum through phase-locking dynamics."*
