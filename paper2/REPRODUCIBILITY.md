# Reproducibility Guide - Paper 2

This document provides instructions for reproducing all results presented in:

**"Echo Geometry of the Classical CHSH Ridge: Memory, Curvature, and Directional Susceptibility"**
*Paper 2: The Memory Landscape*

## System Requirements

- **Python:** 3.8 or higher
- **Required packages:** `numpy`, `scipy`, `matplotlib`, `json`
- **Compute time:** ~2-3 hours for full reproduction (single core)
- **Storage:** ~50 MB for all output data

## Quick Start

Paper 2 experiments are organized into four stages, each in `experiments/Paper2_Stage*/`:

```bash
# Run all stages sequentially
cd experiments/Paper2_Stage1/scripts && bash RUN_P2_STAGE1_sigma_mem.sh
cd ../../Paper2_Stage2/scripts && python3 E221_memory_curvature_surface.py
cd ../../Paper2_Stage3/analysis && python3 build_echo_and_chi_surfaces.py
cd ../../Paper2_Stage4/scripts && python3 E231_angle_resolved_field_scan.py
```

## Individual Experiments

### Stage 1: Memory Threshold (σ_mem)

**Purpose:** Identify the universal memory-collapse threshold σ_mem ≈ 0.002

```bash
cd experiments/Paper2_Stage1/scripts
python3 E211_sigma_mem_curve.py
python3 E211b_sigma_mem_zoom.py
```

**Configs:** `experiments/Paper2_Stage1/config/E211*.json`
**Output:** `experiments/Paper2_Stage1/analysis/data/E211*.json`
**Figures:** Fig. 1a, Fig. 1b
**Runtime:** ~45 minutes

### Stage 2: Memory Curvature Surface

**Purpose:** Map C_mem(K, σ) curvature across parameter space

```bash
cd experiments/Paper2_Stage2/scripts
python3 E221_memory_curvature_surface.py
```

**Config:** `experiments/Paper2_Stage2/config/E221_memory_curvature_surface_config.json`
**Output:** `experiments/Paper2_Stage2/analysis/data/Cmem_*.json`
**Figures:** Fig. 2
**Runtime:** ~30 minutes

### Stage 3: Echo and χ Surfaces

**Purpose:** Compute echo strength ρ_S(τ=50) and directional susceptibility χ_mid

```bash
cd experiments/Paper2_Stage3/analysis
python3 build_echo_and_chi_surfaces.py
```

**Output:** `experiments/Paper2_Stage3/analysis/data/P2_*.json`
**Figures:** Fig. 3, Fig. 4
**Runtime:** ~30 minutes

### Stage 4: Angle-Resolved Field

**Purpose:** Map CHSH functional across measurement geometries under noise

```bash
cd experiments/Paper2_Stage4/scripts
python3 E231_angle_resolved_field_scan.py
```

**Config:** `experiments/Paper2_Stage4/config/E231_angle_resolved_field_scan.json`
**Output:** `experiments/Paper2_Stage4/analysis/data/E231*.json`
**Figures:** Fig. 5
**Runtime:** ~45 minutes

## Figure Regeneration

After running experiments, regenerate all manuscript figures:

### Main Figures

| Paper Figure | Script Location | Output |
|--------------|-----------------|--------|
| Figure 1a | `experiments/Paper2_Stage1/analysis/figs/generate_fig1_sigma_mem_vs_sigma_c.py` | `fig1_sigma_mem_comparison.pdf` |
| Figure 1b | `experiments/Paper2_Stage1/analysis/figs/generate_fig_sigma_mem_zoom.py` | `fig1b_sigma_mem_zoom.pdf` |
| Figure 2 | `experiments/Paper2_Stage2/analysis/figs/generate_Fig2_memory_curvature_surface.py` | `fig2_memory_curvature.pdf` |
| Figure 3 | `experiments/Paper2_Stage3/analysis/figs/generate_Fig3_echo_and_chi.py` | `fig3_echo_surface.pdf` |
| Figure 4 | `experiments/Paper2_Stage3/analysis/figs/generate_Fig3_echo_and_chi.py` | `fig4_chi_surface.pdf` |
| Figure 5 | `experiments/Paper2_Stage4/analysis/figs/generate_Fig5_angle_field.py` | `fig5_angle_field_panel.pdf` |

### Regenerate All Figures

```bash
# Stage 1 figures
cd experiments/Paper2_Stage1/analysis/figs
python3 generate_fig1_sigma_mem_vs_sigma_c.py
python3 generate_fig_sigma_mem_zoom.py

# Stage 2 figure
cd ../../Paper2_Stage2/analysis/figs
python3 generate_Fig2_memory_curvature_surface.py

# Stage 3 figures (generates both Fig 3 and Fig 4)
cd ../../Paper2_Stage3/analysis/figs
python3 generate_Fig3_echo_and_chi.py

# Stage 4 figure
cd ../../Paper2_Stage4/analysis/figs
python3 generate_Fig5_angle_field.py

# Copy to paper2/figs/
cp experiments/Paper2_Stage1/analysis/figs/Fig1_sigma_mem_vs_sigma_c.pdf paper2/figs/fig1_sigma_mem_comparison.pdf
cp experiments/Paper2_Stage1/analysis/figs/Fig_sigma_mem_zoom.pdf paper2/figs/fig1b_sigma_mem_zoom.pdf
cp experiments/Paper2_Stage2/analysis/figs/Fig2_memory_curvature_surface.pdf paper2/figs/fig2_memory_curvature.pdf
cp experiments/Paper2_Stage3/analysis/figs/Fig3_echo_surface.pdf paper2/figs/fig3_echo_surface.pdf
cp experiments/Paper2_Stage3/analysis/figs/Fig4_chi_mid_surface.pdf paper2/figs/fig4_chi_surface.pdf
cp experiments/Paper2_Stage4/analysis/figs/fig5_angle_field_panel.pdf paper2/figs/fig5_angle_field_panel.pdf
```

## Data Dependencies

Paper 2 builds on Paper 1's σ_c(K) collapse curve:

- **Input:** `analysis/data/paper1/A1_sigma_c_K_sweep.json`
- **Used in:** Stage 1 comparison plots (σ_mem vs σ_c)

Ensure Paper 1 data exists before running Stage 1 figure generation.

## Expected Results

| Quantity | Paper Value | Expected Range |
|----------|-------------|----------------|
| σ_mem | 0.002 | 0.0015 - 0.0025 |
| Fragility ratio (σ_mem/σ_c) | ~0.03-0.08 | 0.02 - 0.10 |
| C_mem range | [-0.005, +0.007] | ±0.01 |
| χ_mid sign | ~85% positive | 80-90% |
| Echo ρ_S(50) max | ~1.0 at σ=0 | 0.95 - 1.0 |

## Troubleshooting

**Issue:** Missing Paper 1 data for σ_c comparison
**Solution:** Run Paper 1's A1 experiment first, or use the provided data in `analysis/data/paper1/`

**Issue:** Figure colors don't match paper
**Solution:** Ensure matplotlib version ≥3.5 for consistent colormap rendering

**Issue:** χ contour missing from Fig 4
**Solution:** If all χ values have same sign, contour at χ=0 won't appear (check data range)

## Questions?

For reproducibility issues, please open an issue at:
https://github.com/AkavartaStudio/RUT-CHSH-Landscape/issues

## License

All code and data are available under the CC BY 4.0 license.
See LICENSE file for details.
