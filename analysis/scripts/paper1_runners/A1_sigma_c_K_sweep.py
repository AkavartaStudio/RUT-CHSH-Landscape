#!/usr/bin/env python3
"""
Paper 1 - Experiment A1: High-Precision σ_c(K) Sweep

Purpose:
--------
Nail the noise-coupling scaling law σ_c ≈ 0.9 K with tight error bars.
This is the foundational scaling relation for Paper 1.

Outputs:
--------
- σ_c(K) values with confidence intervals
- Full (K, σ) grid of |S| and PLI statistics
- Data for Paper 1 Figure: "Noise-Coupling Scaling Law"

Expected Result:
----------------
Linear fit: σ_c = slope × K + intercept
where slope ≈ 0.9 and intercept ≈ small
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy.interpolate import interp1d

# Add rut_core to path
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
from rut_core import run_single_experiment

def load_config():
    """Load A1 configuration"""
    config_path = Path(__file__).parent.parent.parent.parent / "paper" / "configs_paper1" / "A1_sigma_c_K_sweep.json"
    with open(config_path) as f:
        return json.load(f)

def run_single_point(K, sigma, config):
    """Run all seeds for a single (K, σ) point"""
    params = {
        'K': K,
        'delta_omega': config['parameters']['delta_omega'],
        'sigma': sigma,
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
    violations = sum(1 for r in results if r['violation'])

    return {
        'K': K,
        'sigma': sigma,
        'n_seeds': n_seeds,
        'abs_S_mean': float(np.mean(abs_S_vals)),
        'abs_S_std': float(np.std(abs_S_vals, ddof=1)),
        'abs_S_sem': float(np.std(abs_S_vals, ddof=1) / np.sqrt(n_seeds)),
        'PLI_mean': float(np.mean(PLI_vals)),
        'PLI_std': float(np.std(PLI_vals, ddof=1)),
        'violation_count': violations,
        'violation_rate': violations / n_seeds,
        'individual_results': results
    }

def find_sigma_c(K_results, threshold_S=2.3, threshold_viol_rate=0.5):
    """
    Find σ_c for a given K by interpolation

    σ_c is defined as the noise level where:
    - |S| drops below threshold_S (default 2.3)
    - OR violation rate drops below threshold_viol_rate (default 0.5)

    Returns:
    --------
    sigma_c : float or None
        Critical noise level (None if cannot be determined)
    method : str
        Method used ('S_threshold', 'viol_rate', or 'indeterminate')
    """
    K_results_sorted = sorted(K_results, key=lambda r: r['sigma'])
    sigmas = np.array([r['sigma'] for r in K_results_sorted])
    abs_S = np.array([r['abs_S_mean'] for r in K_results_sorted])
    viol_rates = np.array([r['violation_rate'] for r in K_results_sorted])

    # Method 1: |S| threshold crossing
    sigma_c_S = None
    if np.any(abs_S > threshold_S) and np.any(abs_S < threshold_S):
        # Find crossing point by interpolation
        try:
            f = interp1d(abs_S, sigmas, kind='linear', fill_value='extrapolate')
            sigma_c_S = float(f(threshold_S))
        except:
            pass

    # Method 2: Violation rate threshold crossing
    sigma_c_viol = None
    if np.any(viol_rates > threshold_viol_rate) and np.any(viol_rates < threshold_viol_rate):
        try:
            f = interp1d(viol_rates, sigmas, kind='linear', fill_value='extrapolate')
            sigma_c_viol = float(f(threshold_viol_rate))
        except:
            pass

    # Return whichever is available (prefer |S| method)
    if sigma_c_S is not None:
        return sigma_c_S, 'S_threshold'
    elif sigma_c_viol is not None:
        return sigma_c_viol, 'viol_rate'
    else:
        return None, 'indeterminate'

def main():
    """Run A1: High-precision σ_c(K) sweep"""
    print("=" * 80)
    print("Paper 1 - Experiment A1: High-Precision σ_c(K) Sweep")
    print("=" * 80)
    print()

    # Load config
    config = load_config()
    print(f"Configuration: {config['experiment_id']}")
    print(f"Purpose: {config['purpose']}")
    print()

    K_values = config['parameters']['K_values']
    sigma_values = config['parameters']['sigma_values']
    delta_omega = config['parameters']['delta_omega']

    print(f"K values: {K_values}")
    print(f"σ values: {sigma_values}")
    print(f"Δω = {delta_omega}")
    print(f"Seeds per point: {config['parameters']['n_seeds']}")
    print(f"Total runs: {len(K_values) * len(sigma_values) * config['parameters']['n_seeds']}")
    print()
    print("=" * 80)

    # Run full grid
    all_results = []
    total_points = len(K_values) * len(sigma_values)
    point_count = 0

    for K in K_values:
        print(f"\n{'='*80}")
        print(f"K = {K}")
        print(f"{'='*80}")

        K_results = []

        for sigma in sigma_values:
            point_count += 1
            print(f"\n[{point_count}/{total_points}] Running σ = {sigma:.2f}...")

            result = run_single_point(K, sigma, config)
            K_results.append(result)
            all_results.append(result)

            # Report
            abs_S = result['abs_S_mean']
            abs_S_sem = result['abs_S_sem']
            PLI = result['PLI_mean']
            viol_rate = result['violation_rate']

            violation_marker = "✓" if viol_rate > 0.5 else "·"
            print(f"  {violation_marker} |S| = {abs_S:.3f}±{abs_S_sem:.3f}, PLI = {PLI:.3f}, violations = {viol_rate:.1%}")

        # Find σ_c for this K
        sigma_c, method = find_sigma_c(K_results)

        if sigma_c is not None:
            print(f"\n🎯 σ_c({K}) = {sigma_c:.3f} (method: {method})")
        else:
            print(f"\n⚠️  σ_c({K}) indeterminate in this range")

    # Compute σ_c values for all K
    print("\n" + "=" * 80)
    print("SCALING LAW ANALYSIS")
    print("=" * 80)

    sigma_c_values = []
    K_for_fit = []

    for K in K_values:
        K_results = [r for r in all_results if r['K'] == K]
        sigma_c, method = find_sigma_c(K_results)

        if sigma_c is not None:
            sigma_c_values.append(sigma_c)
            K_for_fit.append(K)
            print(f"K = {K:.1f}  →  σ_c = {sigma_c:.3f}")

    # Linear fit
    if len(K_for_fit) >= 2:
        coeffs = np.polyfit(K_for_fit, sigma_c_values, 1)
        slope, intercept = coeffs

        # R-squared
        y_fit = np.polyval(coeffs, K_for_fit)
        ss_res = np.sum((sigma_c_values - y_fit)**2)
        ss_tot = np.sum((sigma_c_values - np.mean(sigma_c_values))**2)
        r_squared = 1 - (ss_res / ss_tot)

        print(f"\nLinear fit: σ_c = {slope:.3f} × K + {intercept:.3f}")
        print(f"R² = {r_squared:.4f}")
        print(f"\nExpected: σ_c ≈ 0.9 × K")
        print(f"Observed slope: {slope:.3f}")

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "data" / "paper1"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "A1_sigma_c_K_sweep.json"

    output_data = {
        'experiment_id': config['experiment_id'],
        'timestamp': datetime.now().isoformat(),
        'config': config,
        'grid_results': all_results,
        'sigma_c_analysis': {
            'K_values': K_for_fit,
            'sigma_c_values': sigma_c_values,
            'linear_fit': {
                'slope': float(slope) if len(K_for_fit) >= 2 else None,
                'intercept': float(intercept) if len(K_for_fit) >= 2 else None,
                'r_squared': float(r_squared) if len(K_for_fit) >= 2 else None
            }
        }
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ A1 Complete")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
