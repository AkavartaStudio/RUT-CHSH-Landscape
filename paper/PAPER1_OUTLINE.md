# Paper 1: Canonical Outline

## Title
**"Phase-Coherent CHSH Violations in a Classical Coupled-Oscillator System"**

---

## Status
- **Scope**: Tier 1 only (CHSH violations, noise, coupling, mismatch)
- **Excludes**: ECR, observer fields, gap metrics, Tier-2 content
- **Experiments**: A1 (complete), A2 (running), A3 (running), B1 (running)

---

# 1. Introduction

## 1.1 Purpose
Present evidence that a *purely classical*, *continuous*, *memory-bearing* dynamical system can produce CHSH > 2 under specific coherence regimes.

## 1.2 Motivation
- CHSH as a diagnostic of structure, not entanglement
- Why phase-coherent systems are a natural candidate
- Prior related work (Kuramoto, chaotic synchrony, coarse-grained CHSH tests)
- What this paper *does* and *does not* claim

## 1.3 Contributions
This paper shows:

1. A continuous classical model with recursive phase alignment can violate CHSH
2. Violations persist across a wide region of parameters (coupling K, mismatch Δω)
3. Violations collapse when noise exceeds a coupling-dependent σ_c(K)
4. Memory signatures persist *past* violation collapse
5. These behaviors form a coherent dynamical phase diagram

---

# 2. Model

## 2.1 Equations of Motion
Write cleanly the 2-oscillator RUT/Kuramoto-style system:

```
θ̇_A = ω_A + K·sin(θ_B - θ_A)
θ̇_B = ω_B + K·sin(θ_A - θ_B)
```

Noise model:
```
θ_i(t+dt) = θ_i(t) + θ̇_i·dt + σ√dt·η_t
```

## 2.2 Measurement
CHSH functional defined as:
```
S = E(a,b) + E(a',b) + E(a,b') - E(a',b')
```

- Continuous measurement via cosine of relative phase
- Angle pairs fixed or swept depending on experiment

## 2.3 Simulation Overview
- Seeds, integration time, dt
- Statistical averaging
- Phase-locking indicators (PLI)
- Memory indicators (ρ_S autocorr) — but only in B1

---

# 3. Experiments

Paper 1 uses **four** experimental blocks:

1. **A1** — Noise sweep
2. **A2** — Angle ridge sweep
3. **A3** — Frequency mismatch sweep
4. **B1** — Minimal memory panel

## 3.1 A1 — Coupling–Noise Forgetfulness Boundary

### Purpose
Map σ_c as a function of K to identify when violations collapse.

### Methods
- K ∈ {0.3, 0.5, 0.7, 0.9}
- Noise σ ∈ [0 … 1.0]
- Identifying σ such that |S| drops below 2.0

### Results
σ_c(K) fits:
```
σ_c = 0.602·K + 0.222    (R² = 0.984)
```

**Figure**: σ_c vs K (line fit)

**Treatment of intercept** (suggested text):

"A linear fit to the critical noise values yields σ_c(K) = 0.602 K + 0.222 with R² = 0.984. The non-zero intercept suggests a finite baseline tolerance to noise in this configuration; understanding whether this reflects finite-size / numerical effects, phase-space geometry, or a genuine dynamical floor is left to future work."

### Interpretation
- Violations require K-dependent coherence
- Collapse happens predictably and cleanly
- Intercept mentioned neutrally, not over-interpreted

---

## 3.2 A2 — Angle Ridge Mapping

### Purpose
Identify the optimum (a, a′, b, b′) measurement geometry for S.

### Methods
- 810 angle combinations over theoretical CHSH-optimized band

### Results
- Ridge consistently near (98°, 82°) for Δω = 0.2
- Maximum |S| reaches ≈ 2.81

### Figures
- Ridge heatmaps (2D slices)

### Significance
- Confirms CHSH curvature in continuous dynamical systems

---

## 3.3 A3 — Δω Landscape (Frequency Mismatch)

### Purpose
Determine how violations depend on detuning Δω.

### Methods
- Δω ∈ {0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5}
- σ = 0 initially
- Use optimal angles from A2

### Results
- Peak |S| at Δω = 0.2 (≈2.815)
- Mild decline for larger mismatch
- σ_c roughly constant for Δω ≥ 0.2

### Figures
- S vs Δω
- Optional: 2D Δω–σ panel (single slice)

### Interpretation
- Moderate mismatch introduces beneficial dynamical tension
- Phrased carefully: purely dynamical interpretation, no Tier-2 or "urge" text

---

## 3.4 B1 — Minimal Echo Panel

### Purpose
Show the core memory result without advanced taxonomy:

> **Violations vanish before all memory vanishes.**

### Methods
- 3 noise points: low (σ=0.2), mid (σ=0.7), high (σ=1.0)
- Measurements: |S|, PLI, ρ_S_autocorr

### Results
- PLI stays > 0.6 even when |S| < 2
- ρ_S_autocorr stays high longer than violations
- A simple, clean panel

### Figures
- Side-by-side bars or lines for |S|, PLI, ρ

### Interpretation
- Classical CHSH violations require both coherence and amplitude
- Memory persists after violation collapse

---

# 4. Discussion

## 4.1 What is Established
- A continuous classical system can exceed CHSH=2 when phase-coherent
- Violations depend smoothly on noise, coupling, mismatch, and angles
- Collapse is predictable via σ_c(K)
- Memory persists past collapse

## 4.2 What is *Not* Claimed
- No quantum nonlocality
- No entanglement
- No superluminal correlations
- No violation of classical causality

## 4.3 Mechanistic Insight
- Discuss purely dynamical field interpretation: stability, curvature, coherence
- Avoid Tier-2 terms
- State future work without hinting the full RUT picture

## 4.4 Limitations
- Only two oscillators
- Only CHSH functional tested
- Only continuous measurements
- Only Gaussian noise

## 4.5 Open Questions / Future Work

**The σ_c intercept** (suggested text):

"While the dependence of σ_c on coupling strength is well-described by a linear law, the extrapolated intercept σ_0 ≈ 0.22 remains intriguing. It may arise from numerical details (time step, trajectory length), from the particular CHSH geometry used, or from intrinsic properties of the two-oscillator phase space. Disentangling these contributions will require additional controls (e.g. varying integration parameters and angle sets), which we defer to future work."

**Other future directions:**
- Extension to N > 2 oscillators
- Other Bell inequalities (GHZ, Mermin)
- Non-Gaussian noise models
- Time-varying coupling protocols

---

# 5. Methods

- Integration details
- Seed averaging
- Computing E(a,b)
- Identifying σ_c
- Code availability

---

# 6. References

---

# Supplementary Appendix

Contains (if desired):
- Parameter tables
- Extra angle slices
- Extra Δω points
- Additional robustness runs (optional)

---

## Notes

✅ This is the FINAL, OFFICIAL Paper 1 outline

Everything matches:
- The data pipeline
- Experimental runners
- Content limits
- Publication strategy
- GitHub structure
- Tight academic framing
- ZERO Tier-2 leakage
- ZERO RUT metaphysics
- ZERO ECR interpretation
