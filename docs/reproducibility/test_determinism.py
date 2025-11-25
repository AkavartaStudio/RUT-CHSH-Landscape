#!/usr/bin/env python3
"""
Test determinism of the pipeline by running the same experiment twice
"""

import sys
from pathlib import Path
import json
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / 'analysis/scripts'))
from rut_core import run_single_experiment

def test_determinism():
    """Run the same experiment with same seed twice and verify identical output"""

    print("="*80)
    print("DETERMINISM TEST")
    print("="*80)
    print("\nTesting if same parameters + same seed = identical results\n")

    # Test parameters
    params = {
        'K': 0.7,
        'delta_omega': 0.2,
        'sigma': 0.2,
        'angles': {'a': 0.0, 'a_prime': 98.0, 'b': 45.0, 'b_prime': 127.0},
        'T': 50000,
        'dt': 0.01,
        'transient': 25000,
        'omega1': 1.0,
        'K_modulation': None
    }

    seed = 12345

    print("Running experiment twice with identical parameters and seed...")
    print(f"Seed: {seed}")
    print(f"K={params['K']}, σ={params['sigma']}, Δω={params['delta_omega']}")
    print(f"T={params['T']} steps\n")

    # Run 1
    result1 = run_single_experiment(params, seed=seed)

    # Run 2
    result2 = run_single_experiment(params, seed=seed)

    # Compare results
    print("Results:")
    print("-"*80)
    print(f"{'Metric':<20} {'Run 1':>15} {'Run 2':>15} {'Difference':>15}")
    print("-"*80)

    metrics = ['abs_S', 'PLI', 'violation']
    differences = []

    for metric in metrics:
        val1 = result1[metric]
        val2 = result2[metric]

        if isinstance(val1, bool):
            diff = 0 if val1 == val2 else 1
            print(f"{metric:<20} {str(val1):>15} {str(val2):>15} {diff:>15}")
        else:
            diff = abs(val1 - val2)
            print(f"{metric:<20} {val1:>15.10f} {val2:>15.10f} {diff:>15.2e}")

        differences.append(diff)

    print("-"*80)

    # Check if results are identical
    max_diff = max([d for d in differences if not isinstance(d, (bool, type(None)))])

    print(f"\nMaximum difference: {max_diff:.2e}")

    if max_diff < 1e-15:
        print("\n✓ DETERMINISM: PASSED")
        print("  Results are bit-identical (within machine precision)")
        return True
    elif max_diff < 1e-10:
        print("\n✓ DETERMINISM: PASSED (with numerical tolerance)")
        print("  Results are effectively identical")
        return True
    else:
        print("\n✗ DETERMINISM: FAILED")
        print("  Results differ beyond acceptable tolerance")
        return False

def test_seed_independence():
    """Verify that different seeds give different results"""

    print("\n" + "="*80)
    print("SEED INDEPENDENCE TEST")
    print("="*80)
    print("\nTesting if different seeds produce different results\n")

    params = {
        'K': 0.7,
        'delta_omega': 0.2,
        'sigma': 0.2,
        'angles': {'a': 0.0, 'a_prime': 98.0, 'b': 45.0, 'b_prime': 127.0},
        'T': 50000,
        'dt': 0.01,
        'transient': 25000,
        'omega1': 1.0,
        'K_modulation': None
    }

    results = []
    seeds = [42, 123, 456, 789, 1000]

    print(f"Running {len(seeds)} experiments with different seeds...")
    print(f"Seeds: {seeds}\n")

    for seed in seeds:
        result = run_single_experiment(params, seed=seed)
        results.append(result['abs_S'])

    print("Results:")
    print("-"*40)
    print(f"{'Seed':<10} {'|S|':>15}")
    print("-"*40)
    for seed, S in zip(seeds, results):
        print(f"{seed:<10} {S:>15.10f}")
    print("-"*40)

    # Check variance
    variance = np.var(results)
    mean = np.mean(results)
    std = np.std(results)

    print(f"\nMean |S|: {mean:.6f}")
    print(f"Std dev:  {std:.6f}")
    print(f"Variance: {variance:.6e}")

    if variance > 1e-10:
        print("\n✓ SEED INDEPENDENCE: PASSED")
        print("  Different seeds produce statistically different results")
        return True
    else:
        print("\n✗ SEED INDEPENDENCE: FAILED")
        print("  Different seeds produce identical results (possible RNG issue)")
        return False

if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# PIPELINE DETERMINISM VERIFICATION")
    print("#"*80 + "\n")

    # Test 1: Same seed should give same result
    deterministic = test_determinism()

    # Test 2: Different seeds should give different results
    independent = test_seed_independence()

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    if deterministic and independent:
        print("\n✓ Pipeline is properly deterministic:")
        print("  - Same seed → same results (reproducible)")
        print("  - Different seeds → different results (proper RNG)")
        print("\nThis means the pipeline will give DETERMINISTIC results")
        print("when run multiple times with the same seed configuration.")
    else:
        print("\n✗ Issues detected:")
        if not deterministic:
            print("  - Same seed gives different results (non-deterministic)")
        if not independent:
            print("  - Different seeds give same results (RNG not working)")

    print("\n" + "="*80 + "\n")
