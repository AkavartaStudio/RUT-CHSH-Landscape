#!/usr/bin/env python3
"""
Paper 2 - Mission 1b: High-Resolution σ_mem Zoom

High-resolution sweep around the memory collapse threshold σ ∈ [0.00, 0.04]
for representative K values {0.3, 0.6, 0.9}.

Produces:
- E211_sigma_mem_zoom.json with full ρ_S(50) data
- Refined σ_mem estimates
"""

import json
import sys
import uuid
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Add warmup scripts to path for reuse
SCRIPT_DIR = Path(__file__).parent
WARMUP_SCRIPTS = SCRIPT_DIR.parent.parent / "Paper2_Warmup" / "scripts"
sys.path.insert(0, str(WARMUP_SCRIPTS))

from rut_core_p2 import run_experiment_with_memory

# Paths
CONFIG_DIR = SCRIPT_DIR.parent / "config"
DATA_DIR = SCRIPT_DIR.parent / "analysis" / "data"


def load_config() -> dict:
    """Load E211b experiment configuration."""
    with open(CONFIG_DIR / "E211b_sigma_mem_zoom_config.json") as f:
        return json.load(f)


def run_single_point(K: float, sigma: float, config: dict, seed: int) -> float:
    """Run simulation at single (K, sigma) point with given seed."""
    cfg = config['parameters']

    params = {
        'K': K,
        'sigma': sigma,
        'delta_omega': cfg['delta_omega'],
        'angles': cfg['angles'],
        'T': cfg['T_steps'],
        'dt': cfg['dt'],
        'transient': cfg['transient_steps'],
        'omega1': cfg['omega1']
    }

    result = run_experiment_with_memory(
        params=params,
        seed=seed,
        tau_vals=[cfg['tau']],
        sample_interval=cfg['sample_interval']
    )

    tau = cfg['tau']
    rho_key = f'rho_S_{tau}'
    return result.get(rho_key, 0.0)


def main():
    print("=" * 80)
    print("Paper 2 - Mission 1b: High-Resolution σ_mem Zoom")
    print("=" * 80)
    print()

    # Load config
    config = load_config()
    params = config['parameters']

    K_values = params['K_values']
    sigma_values = params['sigma_values']
    tau = params['tau']
    threshold_fraction = params['threshold_fraction']
    n_seeds = params['n_seeds']

    print(f"Configuration:")
    print(f"  K values: {K_values}")
    print(f"  σ range: [{sigma_values[0]}, {sigma_values[-1]}] step {sigma_values[1] - sigma_values[0]:.3f}")
    print(f"  σ points: {len(sigma_values)}")
    print(f"  τ = {tau}")
    print(f"  Threshold fraction f = {threshold_fraction}")
    print(f"  Seeds per point: {n_seeds}")
    print(f"  Total simulations: {len(K_values) * len(sigma_values) * n_seeds}")
    print()

    # Generate run ID
    run_id = f"E211b-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    print(f"Run ID: {run_id}")
    print()

    # Results storage
    results_by_K = {}

    for i, K in enumerate(K_values):
        print(f"[{i+1}/{len(K_values)}] K = {K}")

        K_data = {
            "K": K,
            "sigma_values": [],
            "rho_S_mean": [],
            "rho_S_std": [],
            "sigma_mem": None,
            "rho_det": None
        }

        # First get ρ_det at σ=0
        rho_det_vals = []
        for seed in range(n_seeds):
            rho = run_single_point(K, 0.0, config, seed)
            rho_det_vals.append(rho)

        rho_det = np.mean(rho_det_vals)
        rho_det_std = np.std(rho_det_vals)
        K_data["rho_det"] = float(rho_det)

        print(f"    ρ_det(τ={tau}) = {rho_det:.4f} ± {rho_det_std:.4f}")

        target_rho = threshold_fraction * rho_det
        sigma_mem = None

        # Sweep σ
        for sigma in sigma_values:
            rho_vals = []
            for seed in range(n_seeds):
                rho = run_single_point(K, sigma, config, seed)
                rho_vals.append(rho)

            mean_rho = np.mean(rho_vals)
            std_rho = np.std(rho_vals)

            K_data["sigma_values"].append(sigma)
            K_data["rho_S_mean"].append(float(mean_rho))
            K_data["rho_S_std"].append(float(std_rho))

            # Check threshold
            if sigma_mem is None and mean_rho < target_rho:
                sigma_mem = sigma
                print(f"    σ_mem = {sigma_mem:.3f} (ρ={mean_rho:.4f} < {target_rho:.4f})")

        if sigma_mem is None:
            print(f"    σ_mem = NULL (threshold not crossed in σ ∈ [0, {sigma_values[-1]}])")

        K_data["sigma_mem"] = sigma_mem
        results_by_K[str(K)] = K_data

    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    # Print summary table
    print("K\t\tσ_mem\t\tρ_det")
    print("-" * 40)
    for K in K_values:
        data = results_by_K[str(K)]
        sm = data["sigma_mem"]
        sm_str = f"{sm:.3f}" if sm is not None else "NULL"
        print(f"{K:.1f}\t\t{sm_str}\t\t{data['rho_det']:.4f}")
    print()

    # Build output JSON
    output = {
        "experiment_id": "E211b",
        "run_id": run_id,
        "run_type": "P2_Mission1b_sigma_mem_zoom",
        "timestamp": datetime.now().isoformat(),
        "tau": tau,
        "threshold_fraction": threshold_fraction,
        "K_values": K_values,
        "results_by_K": results_by_K,
        "notes": {
            "description": "High-resolution zoom around σ_mem threshold",
            "sigma_range": [sigma_values[0], sigma_values[-1]],
            "sigma_step": sigma_values[1] - sigma_values[0],
            "definition": f"σ_mem = smallest σ where ρ_S({tau}) < {threshold_fraction} × ρ_det"
        }
    }

    # Save
    zoom_file = DATA_DIR / "E211_sigma_mem_zoom.json"
    with open(zoom_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Saved: {zoom_file}")

    print()
    print("=" * 80)
    print("Mission 1b COMPLETE")
    print("=" * 80)

    return output


if __name__ == "__main__":
    main()
