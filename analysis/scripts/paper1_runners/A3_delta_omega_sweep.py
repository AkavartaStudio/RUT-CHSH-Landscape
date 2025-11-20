#!/usr/bin/env python3
"""
Paper 1 - Experiment A3: Δω vs |S| Curve at Optimal Geometry

Purpose:
--------
Show clearly that Δω ≈ 0.2 is the sweet spot for maximal violations

Outputs:
--------
- |S| vs Δω curve with error bars
- Identification of Δω* (optimal mismatch)

Expected Result:
----------------
Clear peak in |S| around Δω ≈ 0.2
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Add rut_core to path
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
from rut_core import run_single_experiment

def load_config():
    """Load A3 configuration"""
    config_path = Path(__file__).parent.parent.parent.parent / "paper" / "configs_paper1" / "A3_delta_omega_sweep.json"
    with open(config_path) as f:
        return json.load(f)

def run_delta_omega_point(delta_omega, config):
    """Run all seeds for a single Δω value"""
    params = {
        'K': config['parameters']['K'],
        'delta_omega': delta_omega,
        'sigma': config['parameters']['sigma'],
        'angles': config['parameters']['angles'],
        'T': config['parameters']['T_steps'],
        'dt': config['parameters']['dt'],
        'transient': config['parameters']['transient_steps'],
        'omega1': config['parameters']['omega1'],
        'K_modulation': None
    }

    n_seeds = config['parameters']['n_seeds']
    results = []

    for seed in range(1, n_seeds + 1):
        result = run_single_experiment(params, seed=seed)
        results.append(result)

    # Compute statistics
    abs_S_vals = [r['abs_S'] for r in results]
    PLI_vals = [r['PLI'] for r in results]

    return {
        'delta_omega': delta_omega,
        'n_seeds': n_seeds,
        'abs_S_mean': float(np.mean(abs_S_vals)),
        'abs_S_std': float(np.std(abs_S_vals, ddof=1)),
        'abs_S_sem': float(np.std(abs_S_vals, ddof=1) / np.sqrt(n_seeds)),
        'PLI_mean': float(np.mean(PLI_vals)),
        'PLI_std': float(np.std(PLI_vals, ddof=1)),
        'individual_results': results
    }

def main():
    """Run A3: Δω sweep"""
    print("=" * 80)
    print("Paper 1 - Experiment A3: Δω vs |S| Curve")
    print("=" * 80)
    print()

    config = load_config()
    print(f"Configuration: {config['experiment_id']}")
    print(f"Purpose: {config['purpose']}")
    print()

    delta_omega_values = config['parameters']['delta_omega_values']

    print(f"Δω values: {delta_omega_values}")
    print(f"Seeds per point: {config['parameters']['n_seeds']}")
    print(f"Total runs: {len(delta_omega_values) * config['parameters']['n_seeds']}")
    print()
    print("=" * 80)

    # Run sweep
    all_results = []

    for i, delta_omega in enumerate(delta_omega_values, 1):
        print(f"\n[{i}/{len(delta_omega_values)}] Running Δω = {delta_omega:.2f}...")

        result = run_delta_omega_point(delta_omega, config)
        all_results.append(result)

        abs_S = result['abs_S_mean']
        abs_S_sem = result['abs_S_sem']
        PLI = result['PLI_mean']

        print(f"  |S| = {abs_S:.3f}±{abs_S_sem:.3f}, PLI = {PLI:.3f}")

    # Find optimal Δω
    best = max(all_results, key=lambda r: r['abs_S_mean'])

    print("\n" + "=" * 80)
    print("SWEET SPOT ANALYSIS")
    print("=" * 80)
    print(f"\nOptimal Δω* = {best['delta_omega']:.2f}")
    print(f"Maximum |S| = {best['abs_S_mean']:.3f}±{best['abs_S_sem']:.3f}")
    print(f"PLI = {best['PLI_mean']:.3f}")

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "data" / "paper1"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "A3_delta_omega_sweep.json"

    output_data = {
        'experiment_id': config['experiment_id'],
        'timestamp': datetime.now().isoformat(),
        'config': config,
        'sweep_results': all_results,
        'optimal': best
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ A3 Complete")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
