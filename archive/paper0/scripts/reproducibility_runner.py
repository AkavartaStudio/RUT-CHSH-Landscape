#!/usr/bin/env python3
"""
Reproducibility Runner
Executes all key experiments with multiple seeds and generates validation reports
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
import rut_core

# ============================================================================
# EXPERIMENT CONFIGURATIONS
# ============================================================================

EXPERIMENTS = {
    'E104D': {
        'name': 'Tsirelson Ridge (Asymmetric Angles)',
        'description': 'Optimized asymmetric measurement angles at perfect lock',
        'params': {
            'K': 0.7,
            'delta_omega': 0.3,
            'sigma': 0.0,
            'angles': {
                'a': 0.0,           # 0°
                'a_prime': 90.0,    # 90° (Δα = 90°)
                'b': 45.0,          # 45°
                'b_prime': 120.0    # 120° (Δβ = 75°)
            },
            'T': 5000,
            'dt': 0.01,
            'transient': 1000,
            'K_modulation': None
        },
        'expected': {
            'S': 2.794,
            'PLI': 1.000,
            'correlations': {
                'E_ab': 0.539,
                'E_ab_prime': -0.674,
                'E_a_prime_b': 0.842,
                'E_a_prime_b_prime': 0.739
            }
        },
        'n_seeds': 5,
        'tolerance': {
            'S': 0.05,  # ±5%
            'PLI': 0.01  # ±0.01
        }
    },

    'E104BC': {
        'name': 'Baseline (Standard CHSH Angles)',
        'description': 'Same dynamics as E104D but with standard CHSH angles',
        'params': {
            'K': 0.7,
            'delta_omega': 0.3,
            'sigma': 0.0,
            'angles': {
                'a': 0.0,           # 0°
                'a_prime': 45.0,    # 45°
                'b': 22.5,          # 22.5°
                'b_prime': 67.5     # 67.5°
            },
            'T': 5000,
            'dt': 0.01,
            'transient': 1000,
            'K_modulation': None
        },
        'expected': {
            'S': None,  # To be determined
            'PLI': 1.000
        },
        'n_seeds': 5,
        'tolerance': {
            'S': 0.05,
            'PLI': 0.01
        }
    },

    'E103C': {
        'name': 'Time-Varying Coupling',
        'description': 'Slow modulation of coupling strength with moderate noise',
        'params': {
            'K': 0.7,
            'delta_omega': 0.3,
            'sigma': 0.1,
            'angles': {
                'a': 0.0,           # 0°
                'a_prime': 45.0,    # 45°
                'b': 22.5,          # 22.5°
                'b_prime': 67.5     # 67.5°
            },
            'T': 5000,
            'dt': 0.01,
            'transient': 1000,
            'K_modulation': {
                'amplitude': 0.1,
                'frequency': 0.1   # slow modulation
            }
        },
        'expected': {
            'S': 2.42,
            'PLI': 0.95
        },
        'n_seeds': 5,
        'tolerance': {
            'S': 0.1,   # ±10% (more variability expected)
            'PLI': 0.02
        }
    },

    'E107N_subset': {
        'name': 'RUT Plateau Survey (Representative Subset)',
        'description': 'Key parameter points from E107N for validation',
        'params_list': [
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
        ],
        'angles': {
            'a': 0.0,
            'a_prime': 45.0,
            'b': 22.5,
            'b_prime': 67.5
        },
        'T': 5000,
        'dt': 0.01,
        'transient': 1000,
        'n_seeds': 3,  # 3 seeds per configuration = 18 runs total
        'tolerance': {
            'S': 0.05,
            'PLI': 0.02
        }
    }
}


def run_experiment(exp_id, exp_config, output_dir):
    """Run a single experiment configuration with multiple seeds"""
    print(f"\n{'='*80}")
    print(f"RUNNING: {exp_id} - {exp_config['name']}")
    print(f"{'='*80}")
    print(f"Description: {exp_config['description']}")
    print()

    results = []

    # Handle E107N subset (multiple parameter sets)
    if exp_id == 'E107N_subset':
        for param_set in exp_config['params_list']:
            params = {
                **param_set,
                'angles': exp_config['angles'],
                'T': exp_config['T'],
                'dt': exp_config['dt'],
                'transient': exp_config['transient']
            }

            print(f"  Running K={params['K']}, Δω={params['delta_omega']}, σ={params['sigma']}")

            for seed in range(exp_config['n_seeds']):
                result = rut_core.run_single_experiment(params, seed=seed)
                results.append(result)

                print(f"    Seed {seed}: |S|={result['abs_S']:.3f}, PLI={result['PLI']:.3f}, "
                      f"ρ_echo={result['rho_echo']:.3f}, regime={result['regime']}")

    # Handle single-parameter experiments
    else:
        params = exp_config['params']
        n_seeds = exp_config['n_seeds']

        for seed in range(n_seeds):
            result = rut_core.run_single_experiment(params, seed=seed)
            results.append(result)

            print(f"  Seed {seed}: |S|={result['abs_S']:.3f}, PLI={result['PLI']:.3f}, "
                  f"ρ_echo={result['rho_echo']:.3f}, regime={result['regime']}")

            # Print correlations for E104D
            if exp_id == 'E104D':
                corr = result['correlations']
                print(f"           E(a,b)={corr['E_ab']:+.3f}, E(a,b')={corr['E_ab_prime']:+.3f}, "
                      f"E(a',b)={corr['E_a_prime_b']:+.3f}, E(a',b')={corr['E_a_prime_b_prime']:+.3f}")

    # Compute statistics
    S_values = [r['abs_S'] for r in results]
    PLI_values = [r['PLI'] for r in results]
    echo_values = [r['rho_echo'] for r in results]

    stats = {
        'experiment_id': exp_id,
        'name': exp_config['name'],
        'n_runs': len(results),
        'S': {
            'mean': np.mean(S_values),
            'std': np.std(S_values),
            'min': np.min(S_values),
            'max': np.max(S_values)
        },
        'PLI': {
            'mean': np.mean(PLI_values),
            'std': np.std(PLI_values),
            'min': np.min(PLI_values),
            'max': np.max(PLI_values)
        },
        'rho_echo': {
            'mean': np.mean(echo_values),
            'std': np.std(echo_values),
            'min': np.min(echo_values),
            'max': np.max(echo_values)
        },
        'violation_rate': sum(1 for r in results if r['violation']) / len(results)
    }

    # Check against expected values
    if 'expected' in exp_config and exp_config['expected']['S'] is not None:
        expected_S = exp_config['expected']['S']
        deviation = abs(stats['S']['mean'] - expected_S)
        tolerance = exp_config['tolerance']['S'] * expected_S

        stats['validation'] = {
            'expected_S': expected_S,
            'measured_S': stats['S']['mean'],
            'deviation': deviation,
            'tolerance': tolerance,
            'passes': deviation <= tolerance
        }

        print(f"\n  VALIDATION:")
        print(f"    Expected |S|: {expected_S:.3f}")
        print(f"    Measured |S|: {stats['S']['mean']:.3f} ± {stats['S']['std']:.3f}")
        print(f"    Deviation: {deviation:.3f} (tolerance: {tolerance:.3f})")
        print(f"    Status: {'✓ PASS' if stats['validation']['passes'] else '✗ FAIL'}")

    # Save detailed results
    output_file = output_dir / f"{exp_id}_detailed.json"
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'experiment_id': exp_id,
                'name': exp_config['name'],
                'description': exp_config['description'],
                'timestamp': datetime.now().isoformat()
            },
            'statistics': stats,
            'all_runs': results
        }, f, indent=2, default=str)

    print(f"\n  Saved: {output_file}")

    return stats


def generate_summary_report(all_stats, output_dir):
    """Generate comprehensive summary report"""
    print(f"\n{'='*80}")
    print("REPRODUCIBILITY SUMMARY")
    print(f"{'='*80}\n")

    # Summary table
    print("EXPERIMENT STATISTICS:")
    print(f"{'Experiment':<20} {'n':<5} {'⟨|S|⟩':<10} {'σ(|S|)':<10} {'⟨PLI⟩':<10} {'⟨ρ_echo⟩':<10} {'Viol%':<8}")
    print("-" * 80)

    for exp_id, stats in all_stats.items():
        print(f"{exp_id:<20} "
              f"{stats['n_runs']:<5} "
              f"{stats['S']['mean']:<10.3f} "
              f"{stats['S']['std']:<10.3f} "
              f"{stats['PLI']['mean']:<10.3f} "
              f"{stats['rho_echo']['mean']:<10.3f} "
              f"{stats['violation_rate']*100:<8.1f}")

    # Validation summary
    print("\n\nVALIDATION RESULTS:")
    print("-" * 80)

    all_pass = True
    for exp_id, stats in all_stats.items():
        if 'validation' in stats:
            val = stats['validation']
            status = '✓ PASS' if val['passes'] else '✗ FAIL'
            print(f"{exp_id:<20} Expected: {val['expected_S']:.3f}, "
                  f"Measured: {val['measured_S']:.3f} ± {stats['S']['std']:.3f} - {status}")

            if not val['passes']:
                all_pass = False

    if all_pass:
        print("\n✅ ALL VALIDATIONS PASSED")
    else:
        print("\n⚠️  SOME VALIDATIONS FAILED - REVIEW REQUIRED")

    # Save summary
    summary_file = output_dir / "REPRODUCIBILITY_SUMMARY.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'all_validations_passed': all_pass,
            'experiments': all_stats
        }, f, indent=2, default=str)

    # Create markdown report
    md_file = output_dir / "REPRODUCIBILITY_REPORT.md"
    with open(md_file, 'w') as f:
        f.write(f"# Reproducibility Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Status:** {'✅ All validations passed' if all_pass else '⚠️ Some validations failed'}\n\n")

        f.write(f"## Summary Statistics\n\n")
        f.write(f"| Experiment | n | ⟨|S|⟩ | σ(|S|) | min(|S|) | max(|S|) | ⟨PLI⟩ | ⟨ρ_echo⟩ | Violation Rate |\n")
        f.write(f"|------------|---|-------|--------|----------|----------|-------|----------|----------------|\n")

        for exp_id, stats in all_stats.items():
            f.write(f"| {exp_id} | {stats['n_runs']} | "
                   f"{stats['S']['mean']:.3f} | {stats['S']['std']:.3f} | "
                   f"{stats['S']['min']:.3f} | {stats['S']['max']:.3f} | "
                   f"{stats['PLI']['mean']:.3f} | {stats['rho_echo']['mean']:.3f} | "
                   f"{stats['violation_rate']*100:.1f}% |\n")

        f.write(f"\n## Validation Results\n\n")
        for exp_id, stats in all_stats.items():
            if 'validation' in stats:
                val = stats['validation']
                status = '✅ PASS' if val['passes'] else '❌ FAIL'
                f.write(f"- **{exp_id}**: Expected |S| = {val['expected_S']:.3f}, "
                       f"Measured = {val['measured_S']:.3f} ± {stats['S']['std']:.3f} - {status}\n")

    print(f"\n📄 Reports saved:")
    print(f"  - {summary_file}")
    print(f"  - {md_file}")

    return all_pass


def main():
    """Run all reproducibility tests"""
    print(f"\n🔬 RUT-CHSH REPRODUCIBILITY SWEEP")
    print(f"{'='*80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Goal: Verify all experiments cited in PRE manuscript")
    print(f"{'='*80}\n")

    # Create output directory
    today = datetime.now().strftime('%Y-%m-%d')
    output_dir = Path(__file__).parent.parent.parent / "reruns" / today
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {output_dir}\n")

    # Run all experiments
    all_stats = {}

    for exp_id in ['E104D', 'E104BC', 'E103C', 'E107N_subset']:
        stats = run_experiment(exp_id, EXPERIMENTS[exp_id], output_dir)
        all_stats[exp_id] = stats

    # Generate summary
    all_pass = generate_summary_report(all_stats, output_dir)

    return all_pass


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
