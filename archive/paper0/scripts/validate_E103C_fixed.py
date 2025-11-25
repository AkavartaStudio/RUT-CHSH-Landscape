#!/usr/bin/env python3
"""
E103C Validation Re-run with FIXED Noise
Validates time-varying coupling + noise with correct noise scaling
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
import rut_core

def main():
    """Re-run E103C with fixed noise implementation"""

    print(f"\n{'='*80}")
    print(f"E103C VALIDATION RE-RUN (Fixed Noise)")
    print(f"{'='*80}")
    print(f"Time-varying coupling K(t) = 0.7 + 0.1·sin(0.1t)")
    print(f"Noise: σ = 0.1 (NOW CORRECTLY SCALED)")
    print(f"Seeds: 5")
    print(f"{'='*80}\n")

    # E103C parameters from reproducibility_runner
    params = {
        'K': 0.7,
        'delta_omega': 0.3,
        'sigma': 0.1,
        'angles': {
            'a': 0.0,
            'a_prime': 45.0,
            'b': 22.5,
            'b_prime': 67.5
        },
        'T': 5000,
        'dt': 0.01,
        'transient': 1000,
        'K_modulation': {
            'amplitude': 0.1,
            'frequency': 0.1
        }
    }

    results = []

    # Run 5 seeds
    for seed in range(5):
        print(f"Running seed {seed}...", end=" ")
        result = rut_core.run_single_experiment(params, seed=seed)

        result_record = {
            'experiment': 'E103C',
            'seed': seed,
            'parameters': params.copy(),
            'S': result['abs_S'],
            'PLI': result['PLI'],
            'rho_echo': result['rho_echo'],
            'violation': result['violation'],
            'correlations': result['correlations'],
            'timestamp': datetime.now().isoformat()
        }
        results.append(result_record)
        print(f"|S|={result['abs_S']:.3f}, PLI={result['PLI']:.3f}")

    # Compute statistics
    S_values = [r['S'] for r in results]
    PLI_values = [r['PLI'] for r in results]
    rho_values = [r['rho_echo'] for r in results]

    stats = {
        'experiment_id': 'E103C',
        'name': 'Time-Varying Coupling (Fixed Noise)',
        'n_runs': len(results),
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
        'violation_rate': sum(r['violation'] for r in results) / len(results),
        'timestamp': datetime.now().isoformat()
    }

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "reruns" / "2025-11-17-noise-fix"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "E103C_fixed_noise.json"
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'experiment_id': 'E103C',
                'description': 'Re-run with FIXED noise scaling',
                'fix_applied': 'rut_core.py noise injection corrected',
                'timestamp': datetime.now().isoformat()
            },
            'statistics': stats,
            'all_runs': results
        }, f, indent=2)

    print(f"\n{'='*80}")
    print(f"E103C Results (FIXED NOISE):")
    print(f"{'='*80}")
    print(f"⟨|S|⟩ = {stats['S']['mean']:.3f} ± {stats['S']['std']:.3f}")
    print(f"⟨PLI⟩ = {stats['PLI']['mean']:.3f} ± {stats['PLI']['std']:.3f}")
    print(f"⟨ρ_echo⟩ = {stats['rho_echo']['mean']:.3f} ± {stats['rho_echo']['std']:.3f}")
    print(f"Violation rate: {stats['violation_rate']*100:.0f}%")
    print(f"\nOriginal expectation: |S|≈2.42, PLI≈0.95")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

    return stats

if __name__ == "__main__":
    main()
