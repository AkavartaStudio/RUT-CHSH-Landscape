#!/usr/bin/env python3
"""
E107N Validation Subset Re-run with FIXED Noise
Validates RUT plateau noise robustness with correct noise scaling
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
import rut_core

def main():
    """Re-run E107N subset with fixed noise implementation"""

    print(f"\n{'='*80}")
    print(f"E107N VALIDATION SUBSET RE-RUN (Fixed Noise)")
    print(f"{'='*80}")
    print(f"Testing RUT plateau across σ = 0.0, 0.05, 0.1, 0.2")
    print(f"NOW WITH CORRECTLY SCALED NOISE")
    print(f"{'='*80}\n")

    # E107N subset parameters
    params_list = [
        # σ = 0.0 (perfect lock)
        {'K': 0.7, 'delta_omega': 0.3, 'sigma': 0.0},
        {'K': 0.5, 'delta_omega': 0.3, 'sigma': 0.0},
        # σ = 0.05 (minimal noise)
        {'K': 0.7, 'delta_omega': 0.3, 'sigma': 0.05},
        # σ = 0.1 (moderate noise - E103C regime)
        {'K': 0.7, 'delta_omega': 0.3, 'sigma': 0.1},
        {'K': 0.5, 'delta_omega': 0.3, 'sigma': 0.1},
        # σ = 0.2 (plateau edge)
        {'K': 0.7, 'delta_omega': 0.3, 'sigma': 0.2},
    ]

    angles = {
        'a': 0.0,
        'a_prime': 45.0,
        'b': 22.5,
        'b_prime': 67.5
    }

    all_results = []

    # Run each configuration with 3 seeds
    for param_set in params_list:
        print(f"Config: K={param_set['K']}, Δω={param_set['delta_omega']}, σ={param_set['sigma']}")

        config_results = []
        for seed in range(3):
            params = {
                **param_set,
                'angles': angles,
                'T': 5000,
                'dt': 0.01,
                'transient': 1000
            }

            result = rut_core.run_single_experiment(params, seed=seed)

            result_record = {
                'K': param_set['K'],
                'delta_omega': param_set['delta_omega'],
                'sigma': param_set['sigma'],
                'seed': seed,
                'S': result['abs_S'],
                'PLI': result['PLI'],
                'rho_echo': result['rho_echo'],
                'violation': result['violation']
            }
            config_results.append(result_record)
            all_results.append(result_record)

        # Print config summary
        S_mean = np.mean([r['S'] for r in config_results])
        PLI_mean = np.mean([r['PLI'] for r in config_results])
        print(f"  → |S|={S_mean:.3f}, PLI={PLI_mean:.3f}\n")

    # Compute overall statistics
    S_values = [r['S'] for r in all_results]
    PLI_values = [r['PLI'] for r in all_results]
    rho_values = [r['rho_echo'] for r in all_results]

    stats = {
        'experiment_id': 'E107N_subset',
        'name': 'RUT Plateau Survey (Fixed Noise)',
        'n_runs': len(all_results),
        'S': {
            'mean': float(np.mean(S_values)),
            'std': float(np.std(S_values, ddof=1)),
            'min': float(np.min(S_values)),
            'max': float(np.max(S_values))
        },
        'PLI': {
            'mean': float(np.mean(PLI_values)),
            'std': float(np.std(PLI_values, ddof=1)),
            'min': float(np.min(PLI_values)),
            'max': float(np.max(PLI_values))
        },
        'rho_echo': {
            'mean': float(np.mean(rho_values)),
            'std': float(np.std(rho_values, ddof=1)),
            'min': float(np.min(rho_values)),
            'max': float(np.max(rho_values))
        },
        'violation_rate': sum(r['violation'] for r in all_results) / len(all_results)
    }

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "reruns" / "2025-11-17-noise-fix"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "E107N_subset_fixed_noise.json"
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'experiment_id': 'E107N_subset',
                'description': 'Validation subset re-run with FIXED noise scaling',
                'fix_applied': 'rut_core.py noise injection corrected',
                'timestamp': datetime.now().isoformat()
            },
            'statistics': stats,
            'all_runs': all_results
        }, f, indent=2)

    print(f"{'='*80}")
    print(f"E107N Subset Results (FIXED NOISE):")
    print(f"{'='*80}")
    print(f"⟨|S|⟩ = {stats['S']['mean']:.3f} ± {stats['S']['std']:.3f}")
    print(f"⟨PLI⟩ = {stats['PLI']['mean']:.3f} ± {stats['PLI']['std']:.3f}")
    print(f"⟨ρ_echo⟩ = {stats['rho_echo']['mean']:.3f} ± {stats['rho_echo']['std']:.3f}")
    print(f"Violation rate: {stats['violation_rate']*100:.0f}%")
    print(f"\nResults saved to: {output_file}")
    print(f"{'='*80}\n")

    return stats

if __name__ == "__main__":
    main()
