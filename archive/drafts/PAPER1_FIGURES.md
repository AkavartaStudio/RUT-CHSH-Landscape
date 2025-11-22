# Paper 1: Figure Plan

## Figure Manifest

This document defines exactly what figures Paper 1 will contain and what data feeds each one.

---

## Figure 1: Model Schematic
**Type**: Conceptual diagram
**Content**:
- Two coupled oscillators with antisymmetric coupling
- Phase angles θ_A, θ_B shown on unit circles
- Coupling term K·sin(θ_B - θ_A) illustrated
- Measurement geometry (a, a', b, b') angles shown
- CHSH functional definition

**Data source**: None (schematic only)
**Status**: Needs creation

---

## Figure 2: Noise-Coupling Scaling Law (σ_c vs K)
**Type**: Line plot with error bars
**Content**:
- X-axis: Coupling strength K
- Y-axis: Critical noise σ_c
- Data points at K = {0.3, 0.5, 0.7, 0.9}
- Linear fit: σ_c = 0.602·K + 0.222
- R² = 0.984 shown
- Error bars from interpolation uncertainty

**Data source**: `A1_sigma_c_K_sweep.json`
**Status**: ✓ Data available
**Experiment**: A1

**Key finding**: Clean linear scaling relation between coupling and noise tolerance

---

## Figure 3: |S| vs σ for Representative K Values
**Type**: Multi-line plot
**Content**:
- X-axis: Noise level σ
- Y-axis: Mean |S|
- Multiple curves for different K values
- Horizontal line at |S| = 2.0 (classical bound)
- Horizontal line at |S| = 2.828 (Tsirelson bound)
- Show clear collapse at σ_c for each K

**Data source**: `A1_sigma_c_K_sweep.json`
**Status**: ✓ Data available
**Experiment**: A1

**Key finding**: Smooth violation → collapse transition at σ_c(K)

---

## Figure 4: Angle Ridge Heatmap
**Type**: 2D heatmap
**Content**:
- X-axis: Δα (a' - a)
- Y-axis: Δβ (b' - b)
- Color: Mean |S|
- Contour lines showing ridge structure
- Maximum marked at (98°, 82°)
- E104D point (90°, 75°) marked for comparison

**Data source**: `A2_angle_ridge.json`
**Status**: ⏳ Running (A2)
**Experiment**: A2

**Key finding**: Clear optimal angle geometry for maximal violations

---

## Figure 5: Δω Sweet Spot
**Type**: 1D curve with error bars
**Content**:
- X-axis: Frequency mismatch Δω
- Y-axis: Mean |S|
- Error bars showing standard error
- Peak clearly visible around Δω = 0.2
- Optimal value marked

**Data source**: `A3_delta_omega_sweep.json`
**Status**: ⏳ Running (A3)
**Experiment**: A3

**Key finding**: Moderate mismatch (Δω ≈ 0.2) maximizes violations

---

## Figure 6: Memory Beyond Violations (Minimal Echo Panel)
**Type**: Multi-panel bar chart or line plot
**Content**:
- Three σ values: Ridge (0.2), Boundary (0.7), Classical (1.0)
- Three metrics per σ:
  - |S| (mean ± std)
  - PLI (mean ± std)
  - ρ_S_autocorr (mean ± std)
- Show |S| dropping to classical while PLI and ρ remain elevated

**Data source**: `B1_minimal_echo.json`
**Status**: ⏳ Running (B1)
**Experiment**: B1

**Key finding**: Memory persists after violation collapse

---

## Supplementary Figures (Optional)

### S1: Full (K, σ) Grid Heatmap
**Type**: 2D heatmap
**Content**: Complete K × σ grid showing |S| values
**Data source**: A1
**Status**: Available

### S2: PLI vs σ for Different K
**Type**: Multi-line plot
**Data source**: A1
**Status**: Available

### S3: Additional Angle Slices
**Type**: 1D or 2D slices through angle space
**Data source**: A2
**Status**: Pending

---

## Figure Summary

### Main Text Figures: 6
1. Model schematic (conceptual)
2. σ_c(K) scaling law [A1 ✓]
3. |S| vs σ curves [A1 ✓]
4. Angle ridge heatmap [A2 ⏳]
5. Δω sweet spot [A3 ⏳]
6. Memory panel [B1 ⏳]

### Supplementary Figures: 2-3 (optional)

---

## Production Pipeline

Once experimental data is complete:

1. **Load data** from `/analysis/data/paper1/*.json`
2. **Generate figures** using Python/matplotlib
3. **Save to** `/paper/figures/`
4. **Export formats**:
   - PNG (300 dpi) for preview
   - PDF (vector) for publication
5. **Version control**: Include in git with data provenance

---

## Figure Quality Standards

- **Resolution**: 300 dpi minimum
- **Fonts**: Arial or similar sans-serif, 10-12pt
- **Colors**: Colorblind-safe palette
- **Error bars**: Always show when available
- **Labels**: Clear axis labels with units
- **Legends**: Positioned to not obscure data
- **Size**: Standard column width (~3.5") or full width (~7")
