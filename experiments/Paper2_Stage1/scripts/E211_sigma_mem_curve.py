#!/usr/bin/env python3
"""
Paper 2 - Mission 1: σ_mem(K) Curve

Maps memory-collapse threshold σ_mem as function of coupling strength K
across the full CHSH ridge.

This produces the central quantitative result for Paper 2:
- Figure 1: σ_mem(K) curve
- Section 3.1 data

Uses same engine and memory metrics as P2 warmups (E201-E203).
"""

import json
import sys
import uuid
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Add warmup scripts to path for reuse
SCRIPT_DIR = Path(__file__).parent
WARMUP_SCRIPTS = SCRIPT_DIR.parent.parent / "Paper2_Warmup" / "scripts"
sys.path.insert(0, str(WARMUP_SCRIPTS))

from rut_core_p2 import run_experiment_with_memory
from memory_metrics import rho_S

# Paths
CONFIG_DIR = SCRIPT_DIR.parent / "config"
DATA_DIR = SCRIPT_DIR.parent / "analysis" / "data"
LAB_DIR = SCRIPT_DIR.parent.parent.parent.parent / "lab"


def load_config() -> dict:
    """Load E211 experiment configuration."""
    with open(CONFIG_DIR / "E211_sigma_mem_config.json") as f:
        return json.load(f)


def run_single_point(K: float, sigma: float, config: dict, seed: int) -> Tuple[float, np.ndarray]:
    """
    Run simulation at single (K, sigma) point with given seed.

    Returns:
        rho_S_50: autocorrelation at lag 50
        S_series: full S(t) time series (empty for memory efficiency)
    """
    cfg = config['parameters']

    # Build params dict in format expected by rut_core_p2
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

    # Get rho_S at the specified tau
    tau = cfg['tau']
    rho_key = f'rho_S_{tau}'
    rho = result.get(rho_key, 0.0)

    return rho, np.array([])


def compute_sigma_mem(
    K: float,
    sigma_values: List[float],
    config: dict,
    rho_det: float,
    threshold_fraction: float
) -> Tuple[Optional[float], List[Dict]]:
    """
    Find σ_mem for given K: smallest σ where ρ_S(τ) < f * ρ_det.

    Returns:
        sigma_mem: threshold value (None if never crossed)
        point_data: list of {sigma, rho_S, rho_S_std} for each σ
    """
    params = config['parameters']
    n_seeds = params['n_seeds']
    target_rho = threshold_fraction * rho_det

    point_data = []
    sigma_mem = None

    for sigma in sigma_values:
        if sigma == 0.0:
            # Already computed rho_det
            point_data.append({
                "sigma": sigma,
                "rho_S": rho_det,
                "rho_S_std": 0.0  # Will update with actual std
            })
            continue

        # Run multiple seeds
        rho_vals = []
        for seed in range(n_seeds):
            rho, _ = run_single_point(K, sigma, config, seed)
            rho_vals.append(rho)

        mean_rho = np.mean(rho_vals)
        std_rho = np.std(rho_vals)

        point_data.append({
            "sigma": sigma,
            "rho_S": float(mean_rho),
            "rho_S_std": float(std_rho)
        })

        # Check threshold crossing
        if sigma_mem is None and mean_rho < target_rho:
            sigma_mem = sigma

    return sigma_mem, point_data


def main():
    print("=" * 80)
    print("Paper 2 - Mission 1: σ_mem(K) Curve")
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
    print(f"  K values: {len(K_values)} points from {K_values[0]} to {K_values[-1]}")
    print(f"  σ values: {len(sigma_values)} points from {sigma_values[0]} to {sigma_values[-1]}")
    print(f"  τ = {tau}")
    print(f"  Threshold fraction f = {threshold_fraction}")
    print(f"  Seeds per point: {n_seeds}")
    print(f"  Total simulations: {len(K_values) * len(sigma_values) * n_seeds}")
    print()

    # Generate run ID
    run_id = f"E211-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    print(f"Run ID: {run_id}")
    print()

    # Results storage
    sigma_mem_values = []
    grid_data = []

    # Main loop over K
    for i, K in enumerate(K_values):
        print(f"[{i+1}/{len(K_values)}] K = {K:.2f}")

        # First compute ρ_det at σ=0 for this K
        rho_det_vals = []
        for seed in range(n_seeds):
            rho, _ = run_single_point(K, 0.0, config, seed)
            rho_det_vals.append(rho)

        rho_det = np.mean(rho_det_vals)
        rho_det_std = np.std(rho_det_vals)

        print(f"    ρ_det(τ={tau}) = {rho_det:.4f} ± {rho_det_std:.4f}")

        # Add σ=0 point to grid
        grid_data.append({
            "K": K,
            "sigma": 0.0,
            "rho_S": float(rho_det),
            "rho_S_std": float(rho_det_std)
        })

        # Compute σ_mem by sweeping σ > 0
        sigma_mem = None
        target_rho = threshold_fraction * rho_det

        for sigma in sigma_values[1:]:  # Skip σ=0
            rho_vals = []
            for seed in range(n_seeds):
                rho, _ = run_single_point(K, sigma, config, seed)
                rho_vals.append(rho)

            mean_rho = np.mean(rho_vals)
            std_rho = np.std(rho_vals)

            grid_data.append({
                "K": K,
                "sigma": sigma,
                "rho_S": float(mean_rho),
                "rho_S_std": float(std_rho)
            })

            # Check threshold
            if sigma_mem is None and mean_rho < target_rho:
                sigma_mem = sigma
                print(f"    σ_mem = {sigma_mem:.2f} (ρ={mean_rho:.4f} < {target_rho:.4f})")

        if sigma_mem is None:
            print(f"    σ_mem = NULL (threshold never crossed in σ ∈ [0, {sigma_values[-1]}])")

        sigma_mem_values.append(sigma_mem)

    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    # Print σ_mem(K) table
    print("K\t\tσ_mem")
    print("-" * 24)
    for K, sm in zip(K_values, sigma_mem_values):
        sm_str = f"{sm:.2f}" if sm is not None else "NULL"
        print(f"{K:.2f}\t\t{sm_str}")
    print()

    # Build output JSON - Grid
    grid_output = {
        "experiment_id": "E211",
        "run_id": run_id,
        "run_type": "P2_Mission1_sigma_mem_curve",
        "timestamp": datetime.now().isoformat(),
        "tau": tau,
        "threshold_fraction": threshold_fraction,
        "grid": grid_data
    }

    grid_file = DATA_DIR / "E211_sigma_mem_grid.json"
    with open(grid_file, 'w') as f:
        json.dump(grid_output, f, indent=2)
    print(f"Saved grid: {grid_file}")

    # Build output JSON - Curve
    curve_output = {
        "experiment_id": "E211",
        "run_id": run_id,
        "run_type": "P2_Mission1_sigma_mem_curve",
        "timestamp": datetime.now().isoformat(),
        "tau": tau,
        "threshold_fraction": threshold_fraction,
        "K_values": K_values,
        "sigma_mem_values": sigma_mem_values,
        "notes": {
            "description": "Memory-collapse threshold σ_mem(K) based on rho_S(50)",
            "engine": "same as P2 warmups (rut_core_p2)",
            "angles_deg": [
                config['parameters']['angles']['a'],
                config['parameters']['angles']['a_prime'],
                config['parameters']['angles']['b'],
                config['parameters']['angles']['b_prime']
            ],
            "definition": f"σ_mem = smallest σ where ρ_S({tau}) < {threshold_fraction} * ρ_S({tau})|_{{σ=0}}"
        }
    }

    curve_file = DATA_DIR / "memory_threshold_curve.json"
    with open(curve_file, 'w') as f:
        json.dump(curve_output, f, indent=2)
    print(f"Saved curve: {curve_file}")

    # Create run manifest
    runs_dir = LAB_DIR / "runs" / run_id
    runs_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_id,
        "experiment_id": "E211",
        "run_type": "P2_Mission1_sigma_mem_curve",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "operator": "tc",
        "origin_trigger": "manual",
        "status": "COMPLETED",
        "tags": config['tags'],
        "artifacts": [
            str(grid_file.relative_to(SCRIPT_DIR.parent.parent.parent.parent)),
            str(curve_file.relative_to(SCRIPT_DIR.parent.parent.parent.parent))
        ],
        "paper": "Paper 2 - Mission 1",
        "post_analysis": {
            "memory_threshold_curve": str(curve_file.relative_to(SCRIPT_DIR.parent.parent.parent.parent))
        }
    }

    manifest_file = runs_dir / "run_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved manifest: {manifest_file}")

    print()
    print("=" * 80)
    print("Mission 1 COMPLETE")
    print("=" * 80)

    return curve_output


if __name__ == "__main__":
    main()
