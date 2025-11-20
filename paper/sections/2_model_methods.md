# Section 2: Model and Methods

## Status
**Author**: Kelly/Chase
**Status**: DRAFT COMPLETE
**Target length**: 3-4 pages

---

## 2.1 Dynamical Model

We adopt the minimal two-oscillator Kuramoto model with symmetric coupling to isolate phase-correlation structure without higher-order interactions or network effects. This choice enables systematic parameter sweeps while retaining the essential features of nonlinear synchronization.

We study a pair of coupled phase oscillators evolving according to a noisy Kuramoto-type dynamic:

```
θ̇_A = ω_A + K·sin(θ_B - θ_A) + η_A(t),
θ̇_B = ω_B + K·sin(θ_A - θ_B) + η_B(t).
```

Here:

- θ_A(t), θ_B(t) ∈ [0, 2π) are oscillator phases
- ω_A, ω_B are intrinsic frequencies
- Δω = ω_B - ω_A is the frequency mismatch parameter
- K is the symmetric coupling strength
- η_A(t), η_B(t) are independent Gaussian noise increments applied at each integration step, drawn from N(0, σ²·dt). This implements discrete additive noise with amplitude σ, not a continuous Wiener process formulation.

The model exhibits expected features of nonlinear synchronization: deterministic drift toward phase locking for K ≳ Δω, degradation of synchrony with increasing noise σ, and full desynchronization in the high-noise regime.

---

## 2.2 Numerical Integration

All simulations use explicit Euler integration:

```
θ(t+dt) = θ(t) + dt·θ̇(t),
```

with:

- **time step**: dt = 0.01
- **total time**: T = 1000 (100,000 integration steps)
- **transient discarded**: first 20% of samples
- **phases wrapped** mod 2π after every update

**Integration method justification:** Explicit Euler integration is sufficient for this system because: (i) phase increments remain small (|dθ/dt| ≪ 1/dt in the synchronized regime), (ii) the dynamics are not stiff except at very high K (not explored here), and (iii) convergence tests (see below) confirm numerical error is negligible compared to measurement uncertainty.

**Transient removal:** The first 20% of each trajectory is discarded to remove transient dynamics. This corresponds to approximately 200 time units, sufficient for the system to reach steady-state phase-locking (PLI convergence occurs within 50-100 time units for K > 0.5).

For each experimental condition, we generate 10-20 independent trajectories using different random seeds to estimate mean and variance. **Sample size justification:** Ten independent trajectories per condition provide adequate statistical power: variance in |S| across seeds is low in synchronized regimes (coefficient of variation < 5%), and error bars (SEM) are smaller than symbol size in most figures. For high-noise regimes where variance increases, N=10 yields error estimates consistent with the reported precision.

**Error Reporting Convention**: Unless otherwise specified, all error bars and ± values reported in this paper represent the **standard error of the mean (SEM)** across independent random seeds, computed as SEM = σ/√N, where σ is the sample standard deviation and N is the number of seeds. This quantifies uncertainty in the mean estimate, not the intrinsic variability of individual trajectories.

All code is included in the supplementary repository and is fully reproducible via `RUN_ALL_PAPER1.sh`.

---

## 2.3 Measurement Model: Continuous CHSH

**Continuous-Outcome CHSH Extension.** The standard CHSH inequality applies to dichotomic outcomes (±1) in tests of local hidden-variable theories. Here we adopt a continuous generalization valid for phase variables, where the correlation function E(a,b) naturally captures angle-dependent phase coherence between oscillators. This continuous-variable CHSH formulation has been used in optical phase-space Bell tests [Banaszek & Wódkiewicz 1999], classical entanglement studies in multimode optics [Spreeuw 1998; Ghose & Mukherjee 1994], and quantum continuous-variable systems [Braunstein & Mann 1995].

As in these continuous-variable analyses, the numerical value of |S| depends on the chosen observable and averaging procedure; therefore, |S| > 2 in this setting should be interpreted as a feature of the resulting correlation geometry rather than as a violation of Bell's theorem. Our system exhibits explicit coupling (violating the locality assumption), and we treat S as a correlation diagnostic probing phase-space geometry, not as a constraint derived from local realism.

We evaluate a continuous-outcome CHSH correlator of the form:

```
E(a,b) = ⟨cos[(θ_A(t) + a) - (θ_B(t) + b)]⟩_t,
```

where:

- a, a′, b, b′ are static measurement angles
- angles are defined in degrees but converted to radians in computation
- expectations are taken over the post-transient segment of each trajectory

The CHSH parameter is:

```
S = E(a,b) - E(a,b′) + E(a′,b) + E(a′,b′).
```

The measurement conventions match standard continuous-angle Bell-type analyses used in synchronization studies, optical phase-space CHSH tests, and analog correlation experiments. This continuous-variable CHSH formulation has precedent in quantum optics [Banaszek & Wódkiewicz 1999], where phase-space measurements naturally yield continuous outcomes rather than dichotomic ±1 values. Our classical implementation extends this framework to deterministic coupled oscillator dynamics.

**Measurement geometry:** Unless otherwise specified, experiments use the optimal angle configuration identified via systematic sweep in Section III.A2. Specific angle values are reported in the Results section.

---

## 2.4 Parameter Sweeps and Experimental Conditions

Across the four experiments of Paper 1, we systematically vary the following parameters. **Parameter grids** balance coverage and computational cost: K spacing captures the transition from weak to strong coupling, σ spacing resolves the collapse boundary, and Δω spacing spans the synchronization-to-detuning transition.

### Coupling strength K
```
K ∈ {0.3, 0.5, 0.7, 0.9}
```
Used in A1 (scaling law) and B1 (memory panel).

### Noise amplitude σ
```
σ ∈ {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0}
```
Used in A1 (collapse curves) and B1.

### Frequency mismatch Δω
```
Δω ∈ {0.10, 0.20, 0.30, 0.40, 0.50}
```
Used in A3 (detuning sweep).

### Measurement geometry
```
(a, a′, b, b′) ∈ [0°, 180°]
```
Sampled on a 181×181 grid in A2 (global angle ridge).

---

## 2.5 Derived Metrics

In addition to the CHSH parameter S, we compute:

### Phase Coherence (Order Parameter)
```
r = |⟨e^{i(θ_A(t) - θ_B(t))}⟩_t|
```
This is the Kuramoto order parameter [Acebrón et al., Rev. Mod. Phys. 2005], measuring phase synchronization strength between oscillators. Values near r = 1 indicate strong phase-locking, while r → 0 indicates incoherent dynamics. (Note: This differs from the Phase Lag Index of Stam et al. 2007, which measures phase distribution asymmetry in EEG/MEG signals.)

### Autocorrelation of CHSH Time Series ρ_S(τ)

We compute ρ_S(τ) to quantify temporal coherence in the CHSH observable itself, testing whether correlation structure persists beyond instantaneous phase synchronization (as measured by r). This metric provides a novel diagnostic for memory in the correlation observable, distinct from phase-locking strength.

For each trajectory, we compute the CHSH instantaneous value:

```
S_inst(t) = cos(θ_A + a - θ_B - b)
          - cos(θ_A + a - θ_B - b′)
          + cos(θ_A + a′ - θ_B - b)
          + cos(θ_A + a′ - θ_B - b′).
```

Then compute:

```
ρ_S(τ) = corr(S_inst(t), S_inst(t+τ)),
```

with lag τ = 10 steps.

This provides a measure of temporal coherence of the CHSH observable.

### Violation Amplitude
```
⟨|S|⟩
```
used to track approach to the classical bound |S| = 2.

---

## 2.6 Reproducibility

All runners for Paper 1 are provided in the repository under:

```
analysis/scripts/paper1_runners/
```

The entire study — 1,680 trajectories — can be reproduced with:

```bash
bash RUN_ALL_PAPER1.sh
```

which executes A1 → A2 → A3 → B1 → C1 sequentially and produces all figures used in the paper.

**Computational environment:** All simulations use Python 3.10 with NumPy 1.24, employing the default Mersenne Twister PRNG (numpy.random.default_rng). Random seeds are set deterministically per trajectory and logged. The complete environment specification is provided in `requirements.txt` in the supplementary repository.

---

## Notes

- All numerical values reported in Results use post-transient statistics
- Error bars represent standard error across independent seeds
- **Critical noise threshold σ_c:** We operationally define the noise-induced 'collapse' line σ_c(K) as the locus where the time-averaged CHSH functional crosses |S| = 2.3. This choice lies midway between the classical Bell value 2.0 and the maximal values |S| ≈ 2.8 observed along the high-correlation ridge, providing a robust threshold that is insensitive to small statistical fluctuations yet still clearly marks the transition out of the strongly correlated regime. Using |S| = 2.0 as a threshold would blur this transition, because finite-time sampling and continuous outcomes allow |S| to wander around 2 even in clearly decohered regimes.
- Angle optimization (A2) uses fine 1° grid near expected optimum
