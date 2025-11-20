#!/usr/bin/env python3
"""
Paper 1 - Experiment B1: Minimal Echo Panel

Purpose:
--------
Show that violations vanish before all memory vanishes.
Simple panel: |S|, PLI, and ρ_S_autocorr at 3 σ values.

NO ECR taxonomy, NO gap metrics - keep simple for Paper 1.

Outputs:
--------
- Three σ points: Ridge (0.2), Boundary (0.7), Classical (1.0)
- Metrics: |S|, PLI, ρ_S_autocorr
- Message: "Memory persists beyond violation boundary"
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

def compute_S_inst(theta1, theta2, angles):
    """Compute instantaneous CHSH field"""
    a = np.deg2rad(angles['a'])
    a_prime = np.deg2rad(angles['a_prime'])
    b = np.deg2rad(angles['b'])
    b_prime = np.deg2rad(angles['b_prime'])

    # Instantaneous correlations
    E_ab = np.cos((theta1 + a) - (theta2 + b))
    E_ab_prime = np.cos((theta1 + a) - (theta2 + b_prime))
    E_a_prime_b = np.cos((theta1 + a_prime) - (theta2 + b))
    E_a_prime_b_prime = np.cos((theta1 + a_prime) - (theta2 + b_prime))

    # Instantaneous S
    S_inst = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime

    return S_inst

def compute_rho_S_autocorr(theta1, theta2, angles, tau, transient):
    """Compute temporal coherence of S_inst(t)"""
    S_inst = compute_S_inst(theta1, theta2, angles)
    S = S_inst[transient:]

    T = len(S) - tau
    S_t = S[:T]
    S_t_plus_tau = S[tau:T+tau]

    rho = np.corrcoef(S_t, S_t_plus_tau)[0, 1]
    return float(rho)

def load_config():
    """Load B1 configuration"""
    config_path = Path(__file__).parent.parent.parent.parent / "paper" / "configs_paper1" / "B1_minimal_echo.json"
    with open(config_path) as f:
        return json.load(f)

def run_sigma_point(sigma_name, sigma, config):
    """Run all seeds for a single σ value"""
    params = {
        'K': config['parameters']['K'],
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
    tau = config['parameters']['autocorr_tau']

    # Need to run trajectories and compute custom ρ_S metric
    all_abs_S = []
    all_PLI = []
    all_rho_S = []

    from rut_core import kuramoto_with_noise, compute_pli
    for seed in range(1, n_seeds + 1):
        # Run trajectory
        omega1 = params['omega1']
        omega2 = omega1 + params['delta_omega']
        np.random.seed(seed)
        theta1_0 = np.random.uniform(0, 2*np.pi)
        theta2_0 = np.random.uniform(0, 2*np.pi)

        theta1, theta2 = kuramoto_with_noise(
            theta1_0, theta2_0, omega1, omega2,
            params['K'], params['sigma'], params['T'], params['dt'],
            seed=seed
        )

        # Compute standard CHSH
        result = run_single_experiment(params, seed=seed)
        all_abs_S.append(result['abs_S'])
        all_PLI.append(result['PLI'])

        # Compute ρ_S_autocorr
        rho_S = compute_rho_S_autocorr(theta1, theta2, params['angles'], tau, params['transient'])
        all_rho_S.append(rho_S)

    return {
        'sigma_name': sigma_name,
        'sigma': sigma,
        'n_seeds': n_seeds,
        'abs_S_mean': float(np.mean(all_abs_S)),
        'abs_S_std': float(np.std(all_abs_S, ddof=1)),
        'PLI_mean': float(np.mean(all_PLI)),
        'PLI_std': float(np.std(all_PLI, ddof=1)),
        'rho_S_autocorr_mean': float(np.mean(all_rho_S)),
        'rho_S_autocorr_std': float(np.std(all_rho_S, ddof=1))
    }

def main():
    """Run B1: Minimal echo panel"""
    print("=" * 80)
    print("Paper 1 - Experiment B1: Minimal Echo Panel")
    print("=" * 80)
    print()

    config = load_config()
    print(f"Configuration: {config['experiment_id']}")
    print(f"Purpose: {config['purpose']}")
    print()

    sigma_points = config['parameters']['sigma_points']
    print(f"σ points: {[p['name'] for p in sigma_points]}")
    print(f"Seeds per point: {config['parameters']['n_seeds']}")
    print(f"Metrics: |S|, PLI, ρ_S_autocorr (τ={config['parameters']['autocorr_tau']})")
    print()
    print("NOTE: NO ECR taxonomy - keeping simple for Paper 1")
    print()
    print("=" * 80)

    # Run all σ points
    results = []

    for i, point in enumerate(sigma_points, 1):
        print(f"\n[{i}/{len(sigma_points)}] {point['name'].upper()} (σ={point['value']})...")

        result = run_sigma_point(point['name'], point['value'], config)
        results.append(result)

        print(f"  |S|          = {result['abs_S_mean']:.3f}±{result['abs_S_std']:.3f}")
        print(f"  PLI          = {result['PLI_mean']:.3f}±{result['PLI_std']:.3f}")
        print(f"  ρ_S_autocorr = {result['rho_S_autocorr_mean']:.3f}±{result['rho_S_autocorr_std']:.3f}")

    # Summary
    print("\n" + "=" * 80)
    print("MEMORY BEYOND VIOLATIONS SUMMARY")
    print("=" * 80)
    print("\nσ        |S|     PLI     ρ_S_auto  Classification")
    print("-" * 60)

    for r in results:
        name = r['sigma_name'].ljust(10)
        abs_S = f"{r['abs_S_mean']:.3f}"
        PLI = f"{r['PLI_mean']:.3f}"
        rho_S = f"{r['rho_S_autocorr_mean']:.3f}"

        # Simple classification
        if r['abs_S_mean'] > 2.0:
            classification = "Violation"
        elif r['PLI_mean'] > 0.6 or r['rho_S_autocorr_mean'] > 0.6:
            classification = "Memory persists"
        else:
            classification = "Forgetful"

        print(f"{name} {abs_S:>6s}  {PLI:>6s}  {rho_S:>7s}   {classification}")

    # Save results
    output_dir = Path(__file__).parent.parent.parent / "data" / "paper1"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "B1_minimal_echo.json"

    output_data = {
        'experiment_id': config['experiment_id'],
        'timestamp': datetime.now().isoformat(),
        'config': config,
        'results': results
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ B1 Complete")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

    print("💡 Key message: Violations vanish at boundary while memory persists")

if __name__ == "__main__":
    main()
