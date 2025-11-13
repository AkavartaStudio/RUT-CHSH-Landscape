# Analysis Code and Data

This directory contains all scripts, data, and notebooks used to generate the results in the manuscript.

## Directory Structure

```
analysis/
├── scripts/          # Python scripts for experiments and plotting
├── data/             # Experimental results (JSON format)
└── notebooks/        # Optional Jupyter notebooks for exploration
```

## Scripts

### Experimental Code

**`run_experiment.py`** — Main simulation code
- Runs coupled Kuramoto oscillators with configurable parameters
- Implements proper Wiener process noise scaling (σ√dt)
- Computes CHSH violations using phase-difference method
- Calculates Phase Lock Index (PLI) and cross-echo density
- Outputs results to JSON

**Usage:**
```bash
python run_experiment.py
```

### Visualization Scripts

**`plot_3d_landscape.py`** — Generates 3D surface plots
- Creates PLI × |S| × σ landscape visualization
- Produces regime diagram showing three regimes
- Outputs: `rut_chsh_landscape_3d.png`, `rut_chsh_regime_diagram.png`

**`plot_goldilocks_ridge.py`** — Multi-panel heatmaps (filename retained for compatibility)
- Shows RUT Plateau robustness across noise spectrum
- Outputs: `rut_plateau_multipanel.png`, `rut_plateau_persistence.png`

**Usage:**
```bash
cd scripts
python plot_3d_landscape.py
python plot_goldilocks_ridge.py
```

## Data

**`e107n_rut_plateau_results.json`** — Complete E107N dataset
- 220 experimental runs
- Parameter sweep: K ∈ [0.2, 0.7], Δω ∈ [0.1, 0.5], σ ∈ [0.0, 0.2]
- Each entry contains:
  - Input parameters (K, Δω, σ)
  - Output metrics (|S|, PLI, violation status)
  - Time series statistics

**Data format:**
```json
{
  "experiment_id": "E107N",
  "description": "RUT Plateau noise robustness study",
  "results": [
    {
      "K": 0.7,
      "delta_omega": 0.3,
      "sigma": 0.1,
      "PLI": 0.996,
      "S": 2.441,
      "violation": true,
      "regime": "rut_plateau"
    },
    ...
  ]
}
```

## Key Experiments Referenced

- **E103C**: Time-varying coupling experiment (|S|≈2.42, PLI≈0.95)
- **E104D**: Asymmetric angle optimization (|S|=2.794, PLI=1.0)
- **E107N**: Systematic noise sweep (this dataset)

## Reproducing Results

1. **Generate new data:**
   ```bash
   cd scripts
   python run_experiment.py
   ```

2. **Regenerate all figures:**
   ```bash
   python plot_3d_landscape.py
   python plot_goldilocks_ridge.py
   ```

3. **Check output:**
   - Figures saved to `../figures/`
   - Data saved to `../data/`

## Dependencies

- Python 3.8+
- NumPy
- Matplotlib
- SciPy
- Seaborn (for heatmaps)

Install with:
```bash
pip install numpy matplotlib scipy seaborn
```

## Notes

- All experiments use dt=0.01 integration timestep
- Transient period: 3000 steps discarded
- Measurement window: 3000 steps after transient
- CHSH angles follow E104B convention (0°, 45°, 22.5°, 67.5°)
