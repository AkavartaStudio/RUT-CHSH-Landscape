# Mission 2: Initialization Manifold Sweeps - Design Outline

## Status: PENDING (awaiting resolution of Mission 1B crossover experiments)

## Key Questions to Answer

1. **Does initialization type determine basin selection?**
   - Test: Same K, different init types → same or different attractors?

2. **How many basins exist near K_c?**
   - Test: Large ensemble (100-500 inits) at fixed K values

3. **Is there path dependence?**
   - Test: Sequential vs parallel initialization → same statistics?

## Blocking Issues from Mission 1/1B

Before full Mission 2, need answers from:
- E314B_symmetric_cluster: Does symmetric init collapse multi-basin structure?
- E319B_above_Kc: Does multi-basin persist at K > K_c?
- E320_pilot_init_cluster: Does symmetric_cluster init work correctly?

## Proposed Experiment Blocks

### Block 1: Baseline Multi-Basin Mapping (E321-E325)
- E321: 500 random inits at K=0.1495 (below K_c)
- E322: 500 random inits at K=0.1500 (at K_c)
- E323: 500 random inits at K=0.1505 (above K_c)
- E324: 500 symmetric_cluster inits at K=0.1500
- E325: 500 braid_bait inits at K=0.1500

### Block 2: Init Type Comparison (E326-E330)
At K=0.1501 (where we see 70/30 split):
- E326: clustered_AB init
- E327: opposed_pair_AB init
- E328: biased_phi (phi=+π/2) init
- E329: biased_phi (phi=-π/2) init
- E330: braid_bait (increasing_ABC) init

### Block 3: Basin Boundary Mapping (E331-E335)
Fine K sweep with large ensembles:
- 100 K values from 0.149 to 0.151
- 50 random inits per K
- Goal: Map P(frustrated) vs K curve

### Block 4: History Dependence (E336-E340)
- Sequential restart experiments
- Reset and re-initialize mid-run
- Test for hysteresis effects

## Parameter Choices (Pending Pilot Results)

- T_total: 1000-3000 (based on pilot convergence)
- num_initializations: 50-500 (based on statistics needed)
- K range: 0.148-0.152 (narrow near K_c)

## Timeline

1. ✅ Complete E315-E318 (Mission 1B)
2. ⏳ Run E314B, E319B, E320 crossover experiments
3. 🔜 Analyze crossover results
4. 🔜 Finalize Mission 2 configs based on findings
5. 🔜 Execute Mission 2

## Notes

- The E314/E319 "discrepancy" was resolved: sharp transition at K_c=0.15000
- "Intermittent" classification in E312/E313 detuned is numerical noise, not physical
- Real multi-basin structure exists above K_c (70/30 frustrated/flat split)
