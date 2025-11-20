#!/usr/bin/env python3
"""
Extended σ_c(K) Sweep
====================
Run additional K values for full-range σ_c(K) curve: K ∈ [0.1, 2.5]
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Add rut_core to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from rut_core import run_single_experiment

def run_sigma_sweep_for_K(K_val, sigma_values, n_seeds=10):
    """Run σ sweep for a single K value"""

    # Parameters from A1 config
    params_template = {
        'K': K_val,
        'delta_omega': 0.2,
        'angles': {
            'a': 0.0,
            'a_prime': 95.0,
            'b': 45.0,
            'b_prime': 129.0
        },
        'T': 100000,
        'dt': 0.01,
        'transient': 20000,
        'omega1': 1.0,
        'K_modulation': None
    }

    results = []

    for sigma in sigma_values:
        print(f"  σ={sigma:.2f}...", end='', flush=True)

        params = params_template.copy()
        params['sigma'] = sigma

        # Run seeds
        seed_results = []
        for seed in range(1, n_seeds + 1):
            result = run_single_experiment(params, seed=seed)
            seed_results.append(result)

        # Compute statistics
        abs_S_vals = [r['abs_S'] for r in seed_results]

        results.append({
            'K': K_val,
            'sigma': sigma,
            'abs_S_mean': float(np.mean(abs_S_vals)),
            'abs_S_std': float(np.std(abs_S_vals, ddof=1)),
            'abs_S_sem': float(np.std(abs_S_vals, ddof=1) / np.sqrt(n_seeds))
        })

        print(f" |S|={results[-1]['abs_S_mean']:.3f}")

    return results

def main():
    print("="*80)
    print("Extended σ_c(K) Sweep: K ∈ {1.8, 2.0, 2.2, 2.5}")
    print("="*80)

    # K values to add (we already have 0.1-1.5)
    new_K_values = [1.8, 2.0, 2.2, 2.5]

    # σ values (broad range to capture crossing)
    sigma_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5]

    n_seeds = 10

    print(f"\nNew K values: {new_K_values}")
    print(f"σ sweep: {sigma_values}")
    print(f"Seeds per point: {n_seeds}")
    print(f"Total runs: {len(new_K_values) * len(sigma_values) * n_seeds} = {len(new_K_values)}×{len(sigma_values)}×{n_seeds}")
    print()

    # Run sweeps
    all_results = []

    for i, K_val in enumerate(new_K_values, 1):
        print(f"\n[{i}/{len(new_K_values)}] K = {K_val}")
        K_results = run_sigma_sweep_for_K(K_val, sigma_values, n_seeds)
        all_results.extend(K_results)

    # Save results
    output_dir = SCRIPT_DIR.parent / "data" / "paper1"
    output_file = output_dir / "A1_extended_sigma_sweep.json"

    output_data = {
        'experiment_id': 'A1-EXTENDED-SIGMA-SWEEP',
        'description': 'Extended K range for full σ_c(K) curve',
        'timestamp': datetime.now().isoformat(),
        'K_values': new_K_values,
        'sigma_values': sigma_values,
        'n_seeds': n_seeds,
        'results': all_results
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ Extended sweep complete")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
