#!/usr/bin/env python3
"""
Paper 2 - Mission 2: Memory Curvature Surface

Builds the 2D surface (K, σ) → C_mem(τ_mid) mapping how memory curvature
is distributed across short, intermediate, and long lags.

This is the "memory topology heatmap" - the visual heart of Paper 2 (Figure 2).

Outputs:
- E221_memory_curvature_surface.json (full grid data)
- Cmem_short.json (τ_mid = 17.5 surface)
- Cmem_mid.json (τ_mid = 37.5 surface)
- Cmem_long.json (τ_mid = 75.0 surface)
"""

import json
import sys
import uuid
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add warmup scripts to path for reuse
SCRIPT_DIR = Path(__file__).parent
WARMUP_SCRIPTS = SCRIPT_DIR.parent.parent / "Paper2_Warmup" / "scripts"
sys.path.insert(0, str(WARMUP_SCRIPTS))

from rut_core_p2 import run_experiment_with_memory
from memory_metrics import C_mem

# Paths
CONFIG_DIR = SCRIPT_DIR.parent / "config"
DATA_DIR = SCRIPT_DIR.parent / "analysis" / "data"


def load_config() -> dict:
    """Load E221 experiment configuration."""
    with open(CONFIG_DIR / "E221_memory_curvature_surface_config.json") as f:
        return json.load(f)


def run_single_point(K: float, sigma: float, config: dict, seed: int) -> Dict[str, Any]:
    """
    Run simulation at single (K, sigma) point with given seed.
    Returns full memory metrics including curvature.
    """
    cfg = config['parameters']
    tau_vals = cfg['tau_vals']

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
        tau_vals=tau_vals,
        sample_interval=cfg['sample_interval']
    )

    return result


def main():
    print("=" * 80)
    print("Paper 2 - Mission 2: Memory Curvature Surface")
    print("=" * 80)
    print()

    # Load config
    config = load_config()
    params = config['parameters']

    K_values = params['K_values']
    sigma_values = params['sigma_values']
    tau_vals = params['tau_vals']
    tau_mid_vals = params['tau_mid_vals']
    n_seeds = params['n_seeds']

    total_sims = len(K_values) * len(sigma_values) * n_seeds

    print(f"Configuration:")
    print(f"  K values: {len(K_values)} points [{K_values[0]}, {K_values[-1]}]")
    print(f"  σ values: {len(sigma_values)} points [{sigma_values[0]}, {sigma_values[-1]}]")
    print(f"  τ values: {tau_vals}")
    print(f"  τ_mid values: {tau_mid_vals}")
    print(f"  Seeds per point: {n_seeds}")
    print(f"  Total simulations: {total_sims}")
    print()

    # Generate run ID
    run_id = f"E221-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    print(f"Run ID: {run_id}")
    print()

    # Initialize storage for surfaces
    # Shape: [K_idx, sigma_idx]
    n_K = len(K_values)
    n_sigma = len(sigma_values)

    Cmem_short = np.zeros((n_K, n_sigma))
    Cmem_mid = np.zeros((n_K, n_sigma))
    Cmem_long = np.zeros((n_K, n_sigma))

    # Full grid entries
    entries = []

    sim_count = 0
    start_time = datetime.now()

    for i, K in enumerate(K_values):
        print(f"[{i+1}/{len(K_values)}] K = {K:.2f}")

        for j, sigma in enumerate(sigma_values):
            # Collect metrics over seeds
            S_instant_means = []
            pli_vals = []

            rho_by_tau = {str(tau): [] for tau in tau_vals}
            curvature_by_tau_mid = {str(tm): [] for tm in tau_mid_vals}

            for seed in range(n_seeds):
                result = run_single_point(K, sigma, config, seed)
                sim_count += 1

                S_instant_means.append(result['S_instant_mean'])
                pli_vals.append(result['PLI'])

                # Collect rho values
                for tau in tau_vals:
                    rho_key = f'rho_S_{tau}'
                    rho_by_tau[str(tau)].append(result.get(rho_key, 0.0))

                # Compute curvature from rho values
                rho_vals_for_curv = [result.get(f'rho_S_{tau}', 0.0) for tau in tau_vals]
                tau_mids, C_vals = C_mem(rho_vals_for_curv, tau_vals)

                for tm, cv in zip(tau_mids, C_vals):
                    curvature_by_tau_mid[str(tm)].append(cv)

            # Average over seeds
            entry = {
                "K": K,
                "sigma": sigma,
                "S_instant_mean": float(np.mean(S_instant_means)),
                "S_instant_std": float(np.std(S_instant_means)),
                "PLI": float(np.mean(pli_vals)),
                "rho_by_tau": {},
                "curvature": []
            }

            # Add rho stats
            for tau in tau_vals:
                vals = rho_by_tau[str(tau)]
                entry["rho_by_tau"][str(tau)] = {
                    "mean": float(np.mean(vals)),
                    "std": float(np.std(vals))
                }

            # Add curvature stats and store in surfaces
            for k, tm in enumerate(tau_mid_vals):
                vals = curvature_by_tau_mid[str(tm)]
                mean_curv = float(np.mean(vals))
                entry["curvature"].append({
                    "tau_mid": tm,
                    "C_mem": mean_curv,
                    "C_mem_std": float(np.std(vals))
                })

                # Store in surface arrays
                if k == 0:  # short (17.5)
                    Cmem_short[i, j] = mean_curv
                elif k == 1:  # mid (37.5)
                    Cmem_mid[i, j] = mean_curv
                elif k == 2:  # long (75.0)
                    Cmem_long[i, j] = mean_curv

            entries.append(entry)

            # Progress update every 10 sigma points
            if (j + 1) % 5 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = sim_count / elapsed if elapsed > 0 else 0
                remaining = (total_sims - sim_count) / rate if rate > 0 else 0
                print(f"    σ = {sigma:.2f} | {sim_count}/{total_sims} sims | "
                      f"~{remaining/60:.1f} min remaining")

    print()
    print("=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    print()

    # Build main output JSON
    output = {
        "experiment_id": "E221",
        "run_id": run_id,
        "run_type": "P2_Mission2_memory_curvature_surface",
        "timestamp": datetime.now().isoformat(),
        "tau_vals": tau_vals,
        "tau_mid_vals": tau_mid_vals,
        "K_values": K_values,
        "sigma_values": sigma_values,
        "n_seeds": n_seeds,
        "entries": entries
    }

    # Save main grid file
    main_file = DATA_DIR / "E221_memory_curvature_surface.json"
    with open(main_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Saved: {main_file}")

    # Save condensed surface files
    for name, tau_mid, data in [
        ("Cmem_short", 17.5, Cmem_short),
        ("Cmem_mid", 37.5, Cmem_mid),
        ("Cmem_long", 75.0, Cmem_long)
    ]:
        surface_output = {
            "experiment_id": "E221",
            "run_id": run_id,
            "tau_mid": tau_mid,
            "K_values": K_values,
            "sigma_values": sigma_values,
            "C_mem": data.tolist()
        }

        surface_file = DATA_DIR / f"{name}.json"
        with open(surface_file, 'w') as f:
            json.dump(surface_output, f, indent=2)
        print(f"Saved: {surface_file}")

    print()
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()

    # Print surface statistics
    for name, tau_mid, data in [
        ("Short-lag (τ_mid=17.5)", 17.5, Cmem_short),
        ("Mid-lag (τ_mid=37.5)", 37.5, Cmem_mid),
        ("Long-lag (τ_mid=75.0)", 75.0, Cmem_long)
    ]:
        print(f"{name}:")
        print(f"  C_mem range: [{data.min():.6f}, {data.max():.6f}]")
        print(f"  Mean: {data.mean():.6f}")
        print(f"  Std: {data.std():.6f}")
        # Count sign changes
        pos_count = np.sum(data > 0)
        neg_count = np.sum(data < 0)
        zero_count = np.sum(data == 0)
        print(f"  Sign distribution: {pos_count} positive, {neg_count} negative, {zero_count} zero")
        print()

    elapsed_total = (datetime.now() - start_time).total_seconds() / 60
    print(f"Total runtime: {elapsed_total:.1f} minutes")
    print()
    print("=" * 80)
    print("Mission 2 COMPLETE")
    print("=" * 80)

    return output


if __name__ == "__main__":
    main()
