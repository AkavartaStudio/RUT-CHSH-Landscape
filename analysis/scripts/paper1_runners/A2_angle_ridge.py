#!/usr/bin/env python3
"""
Paper 1 - Experiment A2: Best-Angle Ridge Refinement

Purpose:
--------
Confirm optimum and ridge width around (Δα, Δβ) ≈ (98°, 82°)

Outputs:
--------
- 2D heatmap of |S| over (Δα, Δβ) space
- Precise location of maximum with uncertainties
- Ridge contour data

Expected Result:
----------------
Maximum |S| near (Δα*, Δβ*) ≈ (98°, 82°)
Clear ridge structure showing angle sensitivity
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
    """Load A2 configuration"""
    config_path = Path(__file__).parent.parent.parent.parent / "paper" / "configs_paper1" / "A2_angle_ridge.json"
    with open(config_path) as f:
        return json.load(f)

def run_angle_point(delta_alpha, delta_beta, config):
    """Run all seeds for a single angle pair"""
    # Baseline angles: a=0°, b=45°
    a = 0.0
    b = 45.0
    a_prime = a + delta_alpha
    b_prime = b + delta_beta

    params = {
        'K': config['parameters']['K'],
        'delta_omega': config['parameters']['delta_omega'],
        'sigma': config['parameters']['sigma'],
        'angles': {
            'a': a,
            'a_prime': a_prime,
            'b': b,
            'b_prime': b_prime
        },
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
        'delta_alpha': delta_alpha,
        'delta_beta': delta_beta,
        'n_seeds': n_seeds,
        'abs_S_mean': float(np.mean(abs_S_vals)),
        'abs_S_std': float(np.std(abs_S_vals, ddof=1)),
        'abs_S_sem': float(np.std(abs_S_vals, ddof=1) / np.sqrt(n_seeds)),
        'PLI_mean': float(np.mean(PLI_vals)),
        'PLI_std': float(np.std(PLI_vals, ddof=1)),
        'individual_results': results
    }

def main():
    """Run A2: Angle ridge refinement"""
    print("=" * 80)
    print("Paper 1 - Experiment A2: Best-Angle Ridge Refinement")
    print("=" * 80)
    print()

    config = load_config()
    print(f"Configuration: {config['experiment_id']}")
    print(f"Purpose: {config['purpose']}")
    print()

    delta_alpha_range = config['parameters']['delta_alpha_range']
    delta_beta_range = config['parameters']['delta_beta_range']

    print(f"Δα range: {delta_alpha_range}")
    print(f"Δβ range: {delta_beta_range}")
    print(f"Seeds per point: {config['parameters']['n_seeds']}")
    print(f"Total runs: {len(delta_alpha_range) * len(delta_beta_range) * config['parameters']['n_seeds']}")
    print()
    print("=" * 80)

    # Run full grid
    all_results = []
    total_points = len(delta_alpha_range) * len(delta_beta_range)
    point_count = 0

    for delta_alpha in delta_alpha_range:
        for delta_beta in delta_beta_range:
            point_count += 1
            print(f"\n[{point_count}/{total_points}] Running (Δα={delta_alpha:.0f}°, Δβ={delta_beta:.0f}°)...")

            result = run_angle_point(delta_alpha, delta_beta, config)
            all_results.append(result)

            abs_S = result['abs_S_mean']
            abs_S_sem = result['abs_S_sem']
            PLI = result['PLI_mean']

            print(f"  |S| = {abs_S:.3f}±{abs_S_sem:.3f}, PLI = {PLI:.3f}")

    # Find maximum
    best = max(all_results, key=lambda r: r['abs_S_mean'])

    print("\n" + "=" * 80)
    print("RIDGE ANALYSIS")
    print("=" * 80)
    print(f"\nMaximum |S| = {best['abs_S_mean']:.3f}±{best['abs_S_sem']:.3f}")
    print(f"Located at: (Δα={best['delta_alpha']:.0f}°, Δβ={best['delta_beta']:.0f}°)")
    print(f"PLI = {best['PLI_mean']:.3f}")

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "data" / "paper1"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "A2_angle_ridge.json"

    output_data = {
        'experiment_id': config['experiment_id'],
        'timestamp': datetime.now().isoformat(),
        'config': config,
        'grid_results': all_results,
        'maximum': best
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ A2 Complete")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
