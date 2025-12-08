# Paper 2 Figures

Place final publication-quality figures here.

## Figure Placeholders

Copy actual figures from stage analysis directories:

- **Fig 1** (σ_mem vs σ_c): `Paper2_Stage1/analysis/figs/Fig1_sigma_mem_vs_sigma_c.pdf`
- **Fig 1b** (zoom): `Paper2_Stage1/analysis/figs/Fig_sigma_mem_zoom.pdf`
- **Fig 2** (C_mem surface): `Paper2_Stage2/analysis/figs/Fig2_memory_curvature_surface.pdf`
- **Fig 3** (echo surface): `Paper2_Stage3/analysis/figs/Fig3_echo_surface.pdf`
- **Fig 4** (χ surface): `Paper2_Stage3/analysis/figs/Fig4_chi_mid_surface.pdf`

## Naming Convention

- `fig1_sigma_mem_comparison.pdf` - σ_mem vs σ_c comparison
- `fig1b_sigma_mem_zoom.pdf` - High-resolution zoom
- `fig2_memory_curvature.pdf` - C_mem(K, σ) heatmap
- `fig3_echo_surface.pdf` - ρ_S(50) heatmap
- `fig4_chi_surface.pdf` - χ_mid heatmap with boundary

## To copy figures after stages complete:

```bash
cp ../Paper2_Stage1/analysis/figs/Fig1_sigma_mem_vs_sigma_c.pdf fig1_sigma_mem_comparison.pdf
cp ../Paper2_Stage1/analysis/figs/Fig_sigma_mem_zoom.pdf fig1b_sigma_mem_zoom.pdf
cp ../Paper2_Stage2/analysis/figs/Fig2_memory_curvature_surface.pdf fig2_memory_curvature.pdf
cp ../Paper2_Stage3/analysis/figs/Fig3_echo_surface.pdf fig3_echo_surface.pdf
cp ../Paper2_Stage3/analysis/figs/Fig4_chi_mid_surface.pdf fig4_chi_surface.pdf
```
