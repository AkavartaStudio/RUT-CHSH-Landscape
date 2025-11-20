# Paper 1: Experimental Program Status

## Paper Scope
**Title**: "Bell–CHSH Violations from Classical Phase-Coherent Oscillators"
**Scope**: Tier 1 + Tier 1.5 ONLY (CHSH violations, noise, discretization)
**Excludes**: ECR, observer fields, gap metrics, lens dynamics (those go in Paper 2)

---

## Directory Structure

```
RUT-CHSH-Landscape/
├── paper/
│   ├── configs_paper1/          ← Frozen configs for reproducibility
│   │   └── A1_sigma_c_K_sweep.json  [✓ CREATED]
│   ├── figures/                 ← Will update with Paper 1 plots
│   └── main.tex                 ← Will overwrite with tight CHSH paper
│
├── analysis/
│   ├── scripts/
│   │   ├── rut_core.py          ← Core functions (existing)
│   │   └── paper1_runners/      ← Paper 1 experimental runners
│   │       └── A1_sigma_c_K_sweep.py  [✓ CREATED]
│   └── data/
│       └── paper1/              ← Paper 1 results
```

---

## Experimental Program

### Block A: Core Validation (Money Plots)

#### A1: High-Precision σ_c(K) Sweep [✓ READY TO RUN]
- **Purpose**: Nail scaling law σ_c ≈ 0.9 K
- **Config**: `/paper/configs_paper1/A1_sigma_c_K_sweep.json`
- **Runner**: `/analysis/scripts/paper1_runners/A1_sigma_c_K_sweep.py`
- **Parameters**:
  - K ∈ {0.3, 0.5, 0.7, 0.9}
  - σ ∈ {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0}
  - Δω = 0.2
  - Angles = (98°, 82°)
  - Seeds = 20 per point
- **Total runs**: 4 × 9 × 20 = 720 trajectories
- **Estimated time**: ~15-20 minutes
- **Paper figure**: "Figure: σ_c vs K scaling law"

#### A2: Best-Angle Ridge Refinement [PENDING]
- **Purpose**: Confirm optimum and ridge width
- **Parameters**:
  - K = 0.7, Δω = 0.2, σ = 0.0
  - Δα ∈ [94°, 102°] (1° steps)
  - Δβ ∈ [78°, 86°] (1° steps)
  - Seeds = 10 per angle pair
- **Total runs**: 9 × 9 × 10 = 810 trajectories
- **Paper figure**: "Figure: |S| ridge in angle space"

#### A3: Δω vs |S| Curve [PENDING]
- **Purpose**: Show Δω ≈ 0.2 sweet spot
- **Parameters**:
  - K = 0.7, σ = 0.0
  - Angles = (98°, 82°)
  - Δω ∈ {0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5}
  - Seeds = 10
- **Total runs**: 9 × 10 = 90 trajectories
- **Paper figure**: "Figure: |S| vs Δω sweet spot"

#### A4: Dichotomic Collapse Robustness [PENDING]
- **Purpose**: Show collapse is not an artifact
- **Parameters**:
  - K = 0.7, Δω = 0.2, σ = 0.0
  - Two geometries: (98°, 82°) and (90°, 75°)
  - Measurement types: continuous, sign(cos), sign(sin)
  - Seeds = 10
- **Total runs**: 2 × 3 × 10 = 60 trajectories
- **Paper figure**: "Figure/Table: Continuous vs dichotomic |S|"

#### A5: Quantization Threshold Refinement [PENDING]
- **Purpose**: Phase resolution vs violation
- **Parameters**:
  - K = 0.7, Δω = 0.2, σ = 0.0
  - Angles = (98°, 82°)
  - N ∈ {6, 8, 10, 12, 18, 36, 72, 360, ∞}
  - Seeds = 10
- **Total runs**: 9 × 10 = 90 trajectories
- **Paper figure**: "Figure: |S| vs phase resolution N"

---

### Block B: Echo/Forgetfulness (One Clean Panel)

#### B1: Minimal Echo Panel [PENDING]
- **Purpose**: "Violations vanish before all memory vanishes"
- **Parameters**:
  - K = 0.7, Δω = 0.2
  - Angles = (98°, 82°)
  - Three σ values: Ridge (0.2), Boundary (~0.7), Classical (1.0)
  - Seeds = 20
- **Metrics**: |S|, PLI, ρ_S_autocorr (simple)
- **Total runs**: 3 × 20 = 60 trajectories
- **Paper figure**: "Figure: Memory beyond violation boundary"
- **NOTE**: NO ECR taxonomy, NO ρ_violation—keep simple for Paper 1

---

### Block C: Controls & Robustness Checks

#### C1: Time-Window/Integrator Robustness [PENDING]
- **Purpose**: Results not artifacts of simulation parameters
- **Parameters**:
  - Two configs: (K=0.7, Δω=0.2, σ=0.0) and (K=0.7, Δω=0.2, σ=0.7)
  - T ∈ {500, 1000, 2000}
  - dt ∈ {0.01, 0.005}
  - Seeds = 5
- **Total runs**: 2 × 3 × 2 × 5 = 60 trajectories
- **Output**: Appendix table showing stability

#### C2: Initial Condition/N-Oscillator Robustness [PENDING]
- **Purpose**: No fine-tuning required
- **Parameters**:
  - Two configs: good (σ=0.0) and boundary (σ=0.7)
  - Initial distributions: uniform vs narrow
  - N ∈ {20, 50, 100} oscillators
  - Seeds = 5
- **Total runs**: TBD (need to extend to N>2 oscillators)
- **Output**: Appendix table

---

## Total Estimated Workload

- **A1**: 720 runs
- **A2**: 810 runs
- **A3**: 90 runs
- **A4**: 60 runs
- **A5**: 90 runs
- **B1**: 60 runs
- **C1**: 60 runs
- **C2**: TBD

**Total**: ~1,890 trajectories (excluding C2)

With T=6000, dt=0.01, transient=3000:
- Each trajectory: ~60,000 timesteps
- Estimated total time: 1-2 hours on modern hardware

---

## Next Steps

### Option 1: Run A1 First
- Execute A1 to validate the framework
- Check that σ_c(K) scaling looks right
- Then scaffold remaining experiments

### Option 2: Scaffold All, Then Run
- Create all configs and runners (A2-A5, B1, C1-C2)
- Run complete experimental suite in one go
- Process all results together

### Option 3: Incremental
- Run A1-A3 (core violation characterization)
- Run A4-A5 (discretization thresholds)
- Run B1 (echo panel)
- Run C1-C2 (controls)
- Process each block separately

---

## Status

[✓] Directory structure created
[✓] A1 config created
[✓] A1 runner created
[ ] A2-A5, B1, C1-C2 configs
[ ] A2-A5, B1, C1-C2 runners
[ ] Execute experiments
[ ] Generate Paper 1 figures
[ ] Overwrite main.tex with tight CHSH structure

**Awaiting decision on next step.**
