# TC CHECKLIST — EXPERIMENT LAUNCH (Paper 3)

### *For Missions 1–4 (E301–E399)*

### *TC execution must follow this order unless otherwise instructed.*

---

## 0. Pre-Flight System Checks

### 0.1 Activate the correct environment

```
conda activate akavarta
```

(or TC's equivalent container environment)

### 0.2 Confirm directory exists

```
cd /Users/kellymcrae/Akavarta/research/phys/Paper3/
```

### 0.3 Confirm Mission directories present

TC should check:

```
Paper3_Mission1/
Paper3_Mission2/
Paper3_Mission3/
Paper3_Mission4/
```

If anything is missing → **STOP and notify Kelly.**

---

## 1. Config Generation (per Mission)

For each Mission:

### 1.1 Enter Mission config folder

Example:

```
cd Paper3_Mission1/config
```

### 1.2 Run generator script

```
python generate_configs.py
```

### 1.3 Verify output

TC must confirm:

* All expected config files exist
  * e.g., Mission 1 → `E301.json` … `E320.json`
* `base_MX_E3xx.json` remains unchanged
* `overrides_MX_E3xx.json` merges correctly
* Seeds match experiment ID
* No null or missing values in model blocks

If errors arise → **STOP and report.**

---

## 2. Experiment Execution

### 2.1 Move into Mission scripts folder

```
cd ../scripts
```

### 2.2 Run the first experiment as a smoke test

Example:

```
python run_experiment.py --config ../config/E301.json
```

### 2.3 Verify results directory

TC must check:

```
../analysis/
../paper/
../../results/Mission1/E301/
```

Inside each results folder ensure at minimum:

* `summary.json`
* `classification.json`
* `phi_series.npy` (if enabled)
* `braid_sequence.npy` (if enabled)

If missing → **STOP.**

---

## 3. Batch Execution

Once the single experiment passes:

### 3.1 Run all configs in the Mission

```
python run_all.py
```

TC must verify:

* All config files were processed
* No suppressed exceptions
* Output counts match config counts
* Log sequence is monotonic and complete

If any experiment fails → report experiment ID and stack trace.

---

## 4. Post-Processing & Validation

### 4.1 Generate standard analysis artifacts

TC should run any analysis script inside:

```
Paper3_MissionX/analysis/
```

Examples:

* `analyze_phi.py`
* `analyze_braids.py`
* `plot_K_grid.py`
* `compute_path_order_deltaS.py`

### 4.2 Confirm expected scientific signatures

TC should automatically check (where applicable):

#### Mission 1

* presence of frustrated regions
* presence of circulating Φ in some K bands
* continuity of K-grid

#### Mission 3

* nonzero braid index in some experiments
* permutation sequences nontrivial
* loop-charge modes detected (static / circulating / intermittent)

#### Mission 2

* multi-basin structure
* initialization-dependent attractor divergence

#### Mission 4

* ΔS(order) ≠ 0 in at least some experiments
* 2-body vs 3-body differences detectable

If anomalies are present (flat data everywhere, no variation) → **STOP and notify Kelly.**

---

## 5. Logging & Reporting

TC must create a short `launch_report.md` in each Mission folder, containing:

* completion timestamp
* number of successful runs
* failures with error logs
* quick summary of observed regimes
* any warnings or anomalies

Example:

```
Mission 1 completed.
20/20 experiments ran successfully.
Frustration present at K ≈ 1.3–1.7.
Circulating Φ detected in E306 and E308.
No anomalies.
```

---

## 6. Safety & Determinism Checks

Before moving to next Mission:

TC must verify determinism:

1. Re-run one config with the same seed
2. Confirm identical output hashes
3. Re-run one config with a different seed
4. Confirm output divergence (where expected)

If determinism fails → **STOP immediately** (paper invalid without this).

---

## 7. Proceed to Next Mission

### Recommended sequence:

1. Mission 1 → (K-topography works)
2. Mission 3 → (Φ + braids appear)
3. Mission 2 → (basins explain Mission 3)
4. Mission 4 → (contextuality climax)

TC must not skip Missions unless Kelly instructs.

---

## Summary for TC

**You must:**

* Generate configs
* Run smoke test
* Batch run
* Validate scientific signatures
* Report anomalies
* Verify determinism
* Produce `launch_report.md`

Then move to the next Mission.

---

*Paper 3 • TC Launch Checklist v1.0*
