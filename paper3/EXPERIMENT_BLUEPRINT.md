# Paper 3 — Experiment Blueprint (E301–E399)

This document defines the full experiment plan for Paper 3 (Three-Oscillator Topography). It is structured so TC can file it locally under the Akavarta repo and generate the corresponding experiment scripts.

---

## Overview

Paper 3 explores the irreducible topography of a three-oscillator coupled phase system. The experiments are grouped into five blocks:

* **E301–E320:** K-matrix sweeps
* **E321–E340:** Initialization manifold sweeps
* **E341–E360:** Loop charge Φ detection
* **E361–E380:** Braiding and ordering
* **E381–E399:** Path-order and contextuality tests

Each block includes experiment purpose, core configuration, output requirements, and metrics.

---

# E301–E320 — K-Matrix Sweep Experiments

## Purpose

To map system behavior under variations in coupling strength and edge asymmetry, revealing the onset of frustration, circulating echo states, and braiding.

## Shared Inputs

* Oscillators: A, B, C
* Natural frequencies: ω_i ∈ {0, Δω}
* Initial phases: θ_i(0) uniform or structured (per experiment)
* Simulation length: T = 2000–5000 time units
* Time step: dt = 0.01

## Experiments

### **E301 — Symmetric Triangle (Baseline K)**

* K_AB = K_BC = K_CA = K
* Sweep K from 0.1 → 3.0
* Output: attractor type, Φ, braid index, S-like metric

### **E302–E305 — Edge-Weighted Triangles**

Vary one edge at a time:

* E302: K_AB = K + δ
* E303: K_BC = K + δ
* E304: K_CA = K + δ
* E305: anti-symmetric perturbations (K_AB = K + δ, K_BC = K, K_CA = K - δ)

### **E306–E310 — Strong vs Weak Frustration**

* Hold two edges fixed
* Sweep the third across strong/weak modes
* Detect transitions: flat → frustrated → circulating → braided

### **E311–E315 — Sign-Flipped Triangles**

* K_ij taking mixed signs
* Detect negative-coupling-induced braids

### **E316–E320 — Full K-Matrix Grid**

* 2D grid over (K_AB, K_BC)
* K_CA fixed
* Produce topographic surfaces

---

# E321–E340 — Initialization Manifold Sweeps

## Purpose

To show that 3-body systems have multiple basins of attraction, path dependence, and history-encoded structure.

### **E321 — Uniform Random θ_i**

* 100–500 random initializations per (K, Δω)

### **E322 — Clustered Initial Phases**

* θ_A ≈ θ_B ≠ θ_C

### **E323 — Opposed Pair**

* θ_A = 0, θ_B = π, θ_C random

### **E324–E327 — Biased Loop-Charge Initialization**

* Impose Φ(0) = ±π/2, ±π
* Track stability of initial Φ

### **E328–E330 — "Braid-Bait" Structured Starts**

* Phase ordering A < B < C < A

### **E331–E340 — Random-Reset Sweeps**

* Repeated random restarts under identical K
* Detect multi-basin coexistence

---

# E341–E360 — Loop Charge Φ Detection

## Purpose

To classify regimes by loop charge and identify circulating echo states.

### Loop Charge Definition

Φ = (θ_B − θ_A) + (θ_C − θ_B) + (θ_A − θ_C)

### **E341 — Static Φ Detection**

* Determine if Φ converges to fixed value

### **E342 — Circulating Φ Detection**

* Detect monotonic or periodic drift in Φ(t)

### **E343 — Intermittent Loop Charge**

* Identify switching between static and circulating modes

### **E344–E348 — Φ Reversal Events**

* Track sign changes of Φ drift

### **E349–E355 — Loop-Charge Basin Mapping**

* Measure Φ stability across initializations

### **E356–E360 — Loop-Charge vs K-Gradient**

* Construct Φ(K) curve

---

# E361–E380 — Braiding & Phase Order Dynamics

## Purpose

To detect braid-like permutations in the ordering of (θ_A, θ_B, θ_C).

### **E361 — Permutation Tracking**

* Track ordering of phases at each timestep

### **E362 — Braid Index Computation**

* Convert permutation sequences into braid words

### **E363–E370 — Braid Transitions**

* Detect regime boundaries where braid words change class

### **E371–E375 — Braid Frequency vs K Map**

* Compute rate of permutation changes

### **E376–E380 — Chaotic Braid Boundary**

* Detect intermittency, partial braids, near-chaos

---

# E381–E399 — Path-Order & Contextuality Tests

## Purpose

To demonstrate classical contextuality-like effects where measurement order changes observed metrics.

### **E381 — A→B→C Sampling**

* Compute S-like metric under one path

### **E382 — A→C→B Sampling**

* Compare S-like metric after reordering

### **E383 — C-First Contextual Shift**

* Test impact of C-first ordering

### **E384–E390 — Multi-Angle Path Order Tests**

* Use 6–9 angle sampling sets

### **E391–E395 — 2-Body Reduction Comparison**

* Compute S_AB as if C did not exist
* Compare to full 3-body S under same conditions

### **E396–E399 — Classical Contextuality Benchmark**

* Define regimes where ordering changes S
* Equivalent to contextuality without QM assumptions

---

# Output Requirements for All Experiments

* Time series θ_i(t)
* Orderings and braid words
* Loop charge Φ(t)
* Attractor classification
* S-like metrics
* Diagnostic flags:

  * static
  * frustrated
  * circulating
  * braided
  * chaotic edge

---

# Storage Plan

* Each experiment → folder under `/experiments/E3xx/`
* Each folder contains:

  * config.json
  * run_manifest.json
  * results.npz or parquet
  * metadata.json (Akavarta standard)
  * optional: preview plot PNGs
