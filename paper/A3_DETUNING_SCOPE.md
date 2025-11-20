# A3 Detuning Sweep: Scoped Instructions for Paper 1

## Objective

Demonstrate that **Δω = 0 is not optimal** at the ridge point, while reserving full Δω–K landscape exploration for Paper 2.

---

## Experimental Parameters

**Fixed parameters (ridge point):**
- K = 0.7
- σ = 0.2
- Measurement angles: optimal from A2 (a=0°, a'=95°, b=45°, b'=129°)

**Sweep variable:**
- Δω ∈ {0, 0.05, 0.10, 0.20, 0.30}

**Ensemble:**
- N seeds = [10 or 18, whichever is used in existing A3 runs for consistency]

---

## What to Compute

For each Δω value:
- Run N independent trajectories
- Compute mean |S| and SEM
- (Optional: compute phase coherence r for consistency with other experiments)

**Output:**
- Single curve: |S|(Δω) at K=0.7, σ=0.2

---

## What to Claim (Paper 1)

**One sentence interpretation:**

> "At K = 0.7 in the ridge regime, we observe a maximum near Δω ≈ 0.2K; Δω = 0 yields a slightly smaller |S|, confirming that imperfect frequency matching is optimal in this parameter regime."

**Reservation clause for Paper 2:**

> "Broader exploration of the Δω–K landscape is left for future work."

---

## What NOT to Do

❌ Do **not** extend to multiple K values
❌ Do **not** create a 2D Δω–K heatmap
❌ Do **not** claim "Δω ≈ 0.2K is a general rule"
❌ Do **not** explore Δω > 0.30 or negative detuning

**Why:** The full Δω–K landscape, including bifurcations, phase diagrams, and generalization across coupling strengths, belongs to **Paper 2**. This focused sweep establishes the phenomenon at one representative point without constraining future exploration.

---

## Implementation Notes

**Consistency with existing A3:**
- Use identical integration parameters (Δt, T, transient discard)
- Use same CHSH functional definition
- Use same random seed generation method
- Match existing A3 data format for easy plotting

**Figure placement:**
- Fig 5: |S|(Δω) curve at K=0.7, σ=0.2
- Caption: emphasize this is a single-K slice, not a general landscape

---

## Expected Result

Peak |S| near Δω ≈ 0.14–0.20 (based on exploratory runs), with:
- Δω = 0: slightly lower |S| (rigid locking, less flexible)
- Δω > 0.3: declining |S| (too much detuning, weakened sync)

This demonstrates the "Goldilocks zone" exists without mapping its full structure.

---

## Timeline Suggestion

- **Run time:** ~15 minutes (5 Δω values × 10–18 seeds × fast integration)
- **Analysis:** <10 minutes (single curve + error bars)
- **Figure generation:** <5 minutes (reuse existing plotting scripts)

Total: **under 30 minutes** for focused, publication-ready data.

---

**Status:** Ready to implement
**Approval:** Kelly (scoping confirmed)
**Next step:** Execute sweep and generate Fig 5
