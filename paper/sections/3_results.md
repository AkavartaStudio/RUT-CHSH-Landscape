# Section 3: Results

## Status
**Author**: Kelly/Chase
**Status**: IN PROGRESS
**Target length**: 6-8 pages

---

## 3.1 Noise-Induced Collapse of CHSH Violations (Experiment A1)

We first characterize how CHSH violations degrade as external noise is increased. For each coupling strength K ∈ {0.3, 0.5, 0.7, 0.9}, we sweep the noise amplitude σ ∈ [0, 1] and measure the violation amplitude ⟨|S|⟩ over ten independent trajectories.

### 3.1.1 Violation Regime and Collapse Point

For all coupling strengths tested, the system exhibits a robust violation region at low noise, with maximum values:

```
|S|_max ≈ 2.815 ± 0.005,
```

close to the Tsirelson bound of 2.828. As noise increases, violations degrade smoothly until a sharp collapse point is reached where ⟨|S|⟩ falls below the classical boundary |S| = 2.

We define the collapse threshold σ_c for each K using the operational criterion:

```
σ_c(K) = min{σ : ⟨|S|⟩ ≤ 2.0}.
```

The empirically determined thresholds are:

```
K = 0.3  ⇒  σ_c = 0.384
K = 0.5  ⇒  σ_c = 0.545
K = 0.7  ⇒  σ_c = 0.654
K = 0.9  ⇒  σ_c = 0.749
```

Across all couplings, the collapse region is narrow and well-defined, indicating that the CHSH observable is sensitive to dynamical decoherence in a controlled and repeatable way.

### 3.1.2 Scaling Law for Noise Robustness

A striking linear relationship emerges between the collapse point and coupling strength:

```
σ_c(K) = 0.602 K + 0.222    (R² = 0.984)
```

This scaling captures:

- **Slope (0.602)**: stronger coupling linearly increases resistance to noise
- **Intercept (0.222)**: a nonzero noise tolerance exists even at minimal coupling

This intercept suggests additional dynamical structure beyond pure coupling strength. Possible interpretations are discussed in Section 5.

**Figure 2** shows the linear fit and empirical data points.

### 3.1.3 Collapse Curves and Universal Shape

**Figure 3** displays ⟨|S|⟩ as a function of σ for all four coupling strengths. All curves share a common qualitative structure:

- Violation plateau for σ ≲ σ_c/2
- Smooth degradation as noise increases
- Sharp drop at the collapse threshold
- Classical saturation at ⟨|S|⟩ ≈ 1.6–1.8 for σ ≳ 1.0

The similarity of curve shapes across K indicates a universal collapse mechanism governed primarily by the interplay of coupling-driven alignment and noise-driven phase diffusion.

### 3.1.4 Synchronization and Violation Relationship

Alongside the CHSH observable, we measure the phase-locking index:

```
PLI = |⟨e^{i(θ_A - θ_B)}⟩|
```

PLI decreases more gradually with noise than CHSH violations. Even for σ where |S| < 2, we typically observe:

```
PLI ≈ 0.6 − 0.8,
```

indicating partial synchrony persists after violations have ceased.

This confirms that:

- Violation loss is not identical to loss of phase coherence,
- The CHSH observable is more sensitive to decoherence than PLI, and
- Violation collapse marks a stricter criterion than simple synchrony breakdown.

This distinction becomes important later when comparing memory and violation structure.

### 3.1.5 Summary of Experiment A1

Experiment A1 yields three principal findings:

1. Clean CHSH violations up to |S| ≈ 2.815 across all coupling strengths
2. A linear scaling law for noise robustness
3. A decoupling between simple synchrony (PLI) and violation structure (|S|)

These results establish the foundational dynamical landscape on which the remaining experiments build.

---

## 3.2 Angle Optimization and Ridge Structure (Experiment A2)

The CHSH parameter depends on the choice of measurement angles (a, a′, b, b′). To identify the optimal geometry for this dynamical system, we perform a systematic scan over the angle separations:

```
Δα = a′ - a  ∈ [80°, 110°]
Δβ = b′ - b  ∈ [70°, 100°]
```

with a fixed at 0° and b at 45°.

### 3.2.1 Optimal Measurement Geometry

The global maximum is found at:

```
Δα* = 95°,  Δβ* = 84°
```

yielding:

```
|S|_max = 2.819 ± 0.003.
```

This corresponds to the explicit angle configuration:

```
a = 0°,  a′ = 95°,  b = 45°,  b′ = 129°,
```

which we adopt for all subsequent experiments.

The achieved value |S| = 2.819 is close to—but slightly below—the Tsirelson bound of 2.828, suggesting that the continuous-phase measurement model introduces a small but systematic reduction compared to ideal quantum projections.

### 3.2.2 Broad Ridge Structure

**Figure 4** shows the two-dimensional landscape |S|(Δα, Δβ) as a heatmap. The optimal region forms a broad ridge rather than a sharp peak:

- The ridge extends approximately 4° in Δα and 6° in Δβ around the optimum
- Variations of ±2° in either angle reduce |S| by less than 0.005
- The landscape is smooth and well-behaved, with no local optima

This robustness indicates that the CHSH violation structure is not fragile to small misalignments in measurement geometry—a practically important feature for experimental implementations.

### 3.2.3 Comparison to Theoretical Predictions

Standard Bell-CHSH theory predicts optimal angles at:

```
Δα = 90°,  Δβ = 90°  (symmetric case),
```

or slight modifications depending on the observable model. Our empirically determined optimum (95°, 84°) deviates modestly from this, likely reflecting the specific phase-space structure of Kuramoto coupling.

The asymmetry (Δα ≠ Δβ) suggests that the measurement axes do not align perfectly with the principal directions of the correlation tensor for this system—an issue we return to in the Discussion.

### 3.2.4 Summary of Experiment A2

Key findings from angle optimization:

1. Clean global optimum at (95°, 84°) with |S| = 2.819
2. Broad ridge structure ensuring robustness to angle choice
3. Near-Tsirelson violations achievable with continuous-phase measurements

These angles are used for all subsequent experiments to ensure maximum violation amplitude.

---

## 3.3 Frequency Mismatch Sweet Spot (Experiment A3)

In all previous experiments, we set the frequency mismatch to Δω = 0.2. This choice was not arbitrary: we now show that Δω = 0.2 represents an optimal balance between synchronization strength and dynamical tension.

### 3.3.1 The Δω Sweep

We vary Δω ∈ {0.10, 0.20, 0.30, 0.40, 0.50} while holding K = 0.7, σ = 0.2, and measurement angles fixed at the A2 optimum. For each Δω, we measure ⟨|S|⟩ and PLI over 18 independent seeds.

**Figure 5** (top panel) reveals a clear peak structure:

```
Δω* = 0.20  ⇒  |S|_max = 2.815 ± 0.004
```

with degradation on both sides:

```
Δω = 0.10  ⇒  |S| = 2.805
Δω = 0.30  ⇒  |S| = 2.789
Δω = 0.50  ⇒  |S| = 2.734
```

### 3.3.2 Interpretation: Dynamical Tension vs. Lock Strength

The existence of an optimal mismatch is surprising at first glance: why doesn't perfect resonance (Δω = 0) maximize violations?

Two competing effects govern this:

**Too little mismatch (Δω → 0)**:
- The system locks trivially into θ_A ≈ θ_B
- Reduced dynamical diversity in phase-space exploration
- Correlations become overly predictable, limiting violation structure

**Too much mismatch (Δω → K)**:
- Coupling cannot overcome frequency difference
- Phase drift dominates, reducing correlation strength
- PLI decreases (though this happens slowly—see below)

The sweet spot Δω* ≈ 0.2 ≈ 0.29 K provides enough tension to generate rich correlation structure without destabilizing synchrony.

### 3.3.3 PLI Remains Robust Across Δω

**Figure 5** (bottom panel) shows that PLI varies only slightly across the Δω range tested:

```
PLI ∈ [0.997, 0.999]  for all Δω ∈ [0.10, 0.50].
```

This indicates that:

- Phase-locking persists even when |S| decreases by ~3%
- The CHSH observable is more sensitive to Δω than simple synchrony metrics
- Violation amplitude and phase coherence again decouple (cf. Experiment A1)

### 3.3.4 Implications for Experimental Design

The Δω sweet spot has practical consequences:

- Fixed-frequency implementations should target Δω ≈ 0.3 K for maximum violations
- Systems with slight natural detuning may outperform perfectly matched oscillators
- The peak is broad (FWHM ~ 0.2), so exact tuning is not critical

### 3.3.5 Summary of Experiment A3

Three principal findings:

1. Optimal frequency mismatch at Δω* = 0.20 with |S| = 2.815
2. Dynamical tension enhances violation amplitude compared to perfect resonance
3. PLI robustness across Δω confirms decoupling from CHSH structure

This completes the characterization of the violation-supporting parameter regime.

---

## 3.4 Memory Beyond Violations (Experiment B1)

A central conceptual question is whether the loss of CHSH violations coincides with the complete loss of dynamical memory. Experiment B1 provides a clear answer: **memory persists well into the classical regime.**

### 3.4.1 Experimental Design

We select three noise levels representing qualitatively different regimes:

1. **Ridge** (σ = 0.2): Deep in the violation region
2. **Boundary** (σ = 0.7): Near the collapse threshold σ_c ≈ 0.65 for K = 0.7
3. **Classical** (σ = 1.0): Well beyond the classical bound

For each regime, we measure:

- CHSH amplitude ⟨|S|⟩
- Phase-locking index PLI
- Temporal coherence ρ_S(τ = 10)

using K = 0.7, Δω = 0.2, and optimal angles.

### 3.4.2 Key Findings

**Figure 6** displays the results as a three-panel bar chart. The data show:

**Ridge regime (σ = 0.2)**:
```
|S| = 2.774 ± 0.001
PLI = 0.985 ± 0.0003
ρ_S = 0.762 ± 0.005
```
Strong violations, high synchrony, moderate temporal coherence.

**Boundary regime (σ = 0.7)**:
```
|S| = 2.228 ± 0.018
PLI = 0.792 ± 0.006
ρ_S = 0.858 ± 0.011
```
Violations reduced but still present (|S| > 2). Synchrony partially degraded. **Temporal coherence increases.**

**Classical regime (σ = 1.0)**:
```
|S| = 1.594 ± 0.036
PLI = 0.567 ± 0.013
ρ_S = 0.860 ± 0.005
```
**No violations** (|S| < 2). Synchrony weak. **Temporal coherence remains high.**

### 3.4.3 The Persistence of Temporal Coherence

The most striking result is that ρ_S remains elevated (≈ 0.86) even when |S| has collapsed to 1.59, far below the classical bound.

This means:

- The CHSH time series retains autocorrelation structure
- Past values of S(t) predict future values with high fidelity
- Memory persists even though instantaneous violation amplitude is classical

This is not a trivial statement. One might expect that noise sufficient to destroy violations would also destroy all temporal structure. Instead, we observe a **decoupling** between:

- **Violation amplitude** (sensitive to noise, collapses at σ_c)
- **Temporal memory** (robust to noise, persists beyond σ_c)

### 3.4.4 Why Does ρ_S Increase at the Boundary?

Curiously, ρ_S reaches its maximum value (0.858) at the boundary regime (σ = 0.7), higher than in the ridge (0.762). This non-monotonic behavior suggests:

- At low noise, the system exhibits transient fluctuations that reduce autocorrelation
- At intermediate noise, fluctuations are smoothed while structure persists
- At high noise, memory is maintained through a different mechanism (slower phase diffusion?)

This effect warrants further investigation and will be revisited in the Discussion.

### 3.4.5 Implications for Interpretation

The persistence of memory beyond violations challenges a strict identification of CHSH structure with dynamical coherence. Specifically:

- **Violations do not require perfect memory**: ρ_S can be moderate (0.76) while |S| is large (2.77)
- **Memory does not imply violations**: ρ_S can be high (0.86) while |S| is classical (1.59)
- **The two structures are distinct**: Loss of one does not immediately imply loss of the other

This motivates a more nuanced taxonomy of dynamical regimes—but such exploration is deferred to future work (see Section 5).

### 3.4.6 Summary of Experiment B1

Key findings:

1. Temporal coherence ρ_S ≈ 0.86 persists well into the classical regime (σ = 1.0)
2. CHSH violations and temporal memory are distinct dynamical structures
3. Non-monotonic ρ_S behavior suggests phase-space reorganization at intermediate noise

This completes the experimental results section.
