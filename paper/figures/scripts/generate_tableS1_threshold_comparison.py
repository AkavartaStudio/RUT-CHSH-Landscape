#!/usr/bin/env python3
"""
Table S1: σc Threshold Comparison (|S| = 2.0 vs 2.3)
===================================================

Generates Table S1 comparing critical noise values σc across different
coupling strengths K for two threshold definitions:
- Classical bound: |S| = 2.0
- Practical threshold: |S| = 2.3 (used in paper)

Shows that threshold choice affects absolute σc values but not the
scaling relationship σc ≈ 0.9K.

Outputs:
- tableS1_threshold_comparison.csv
"""

import json
import numpy as np
from pathlib import Path
import csv
from scipy.interpolate import interp1d

def find_sigma_c(K, sigma_vals, abs_S_vals, threshold):
    """
    Find σc where |S| crosses below threshold using linear interpolation

    Parameters:
    -----------
    K : float
        Coupling strength
    sigma_vals : array
        Sigma values for this K
    abs_S_vals : array
        Corresponding |S| values
    threshold : float
        |S| threshold (2.0 or 2.3)

    Returns:
    --------
    sigma_c : float or None
        Critical noise where |S| crosses below threshold
    """
    # Sort by sigma
    sorted_idx = np.argsort(sigma_vals)
    sigma_sorted = np.array(sigma_vals)[sorted_idx]
    abs_S_sorted = np.array(abs_S_vals)[sorted_idx]

    # Find where |S| drops below threshold
    below_threshold = abs_S_sorted < threshold

    if not np.any(below_threshold):
        # Never drops below threshold
        return None

    # Find first crossing
    cross_idx = np.where(below_threshold)[0][0]

    if cross_idx == 0:
        # Already below at first point
        return sigma_sorted[0]

    # Linear interpolation between cross_idx-1 and cross_idx
    sigma1, sigma2 = sigma_sorted[cross_idx-1], sigma_sorted[cross_idx]
    S1, S2 = abs_S_sorted[cross_idx-1], abs_S_sorted[cross_idx]

    # Linear interpolation: σc = σ1 + (threshold - S1) * (σ2 - σ1) / (S2 - S1)
    if S2 == S1:
        # Avoid division by zero
        sigma_c = (sigma1 + sigma2) / 2
    else:
        sigma_c = sigma1 + (threshold - S1) * (sigma2 - sigma1) / (S2 - S1)

    return sigma_c


def main():
    # Load A1 K-sweep data
    data_dir = Path(__file__).parent.parent.parent.parent / 'analysis' / 'data' / 'paper1'
    data_file = data_dir / 'A1_sigma_c_K_sweep.json'

    with open(data_file, 'r') as f:
        data = json.load(f)

    print("="*60)
    print("Table S1: σc Threshold Comparison")
    print("="*60)

    # Extract K values
    K_values = data['config']['parameters']['K_values']

    # Storage for results
    results = []

    for K in K_values:
        # Extract (sigma, |S|) pairs for this K
        K_data = [r for r in data['grid_results'] if r['K'] == K]

        sigma_vals = [r['sigma'] for r in K_data]
        abs_S_vals = [r['abs_S_mean'] for r in K_data]

        # Find σc for both thresholds
        sigma_c_20 = find_sigma_c(K, sigma_vals, abs_S_vals, threshold=2.0)
        sigma_c_23 = find_sigma_c(K, sigma_vals, abs_S_vals, threshold=2.3)

        results.append({
            'K': K,
            'sigma_c_20': sigma_c_20,
            'sigma_c_23': sigma_c_23
        })

        print(f"K = {K:.1f}:  σc(2.0) = {sigma_c_20:.3f},  σc(2.3) = {sigma_c_23:.3f}")

    # Filter out None values for fitting
    valid_results = [r for r in results if r['sigma_c_20'] is not None and r['sigma_c_23'] is not None]

    if len(valid_results) > 0:
        K_fit = np.array([r['K'] for r in valid_results])
        sigma_c_20_fit = np.array([r['sigma_c_20'] for r in valid_results])
        sigma_c_23_fit = np.array([r['sigma_c_23'] for r in valid_results])

        # Linear fit: σc = m * K + b
        m_20, b_20 = np.polyfit(K_fit, sigma_c_20_fit, 1)
        m_23, b_23 = np.polyfit(K_fit, sigma_c_23_fit, 1)

        print(f"\n{'='*60}")
        print("Linear fits: σc = m*K + b")
        print(f"{'='*60}")
        print(f"Threshold 2.0:  σc = {m_20:.3f}*K + {b_20:.3f}")
        print(f"Threshold 2.3:  σc = {m_23:.3f}*K + {b_23:.3f}")
        print(f"\nSlope ratio:  m(2.0)/m(2.3) = {m_20/m_23:.3f}")

    # Export CSV
    output_dir = Path(__file__).parent.parent
    csv_file = output_dir / 'tableS1_threshold_comparison.csv'

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(['K', 'sigma_c_2.0', 'sigma_c_2.3', 'Delta'])

        # Data rows
        for r in results:
            if r['sigma_c_20'] is not None and r['sigma_c_23'] is not None:
                delta = r['sigma_c_20'] - r['sigma_c_23']
                writer.writerow([
                    f"{r['K']:.1f}",
                    f"{r['sigma_c_20']:.3f}",
                    f"{r['sigma_c_23']:.3f}",
                    f"{delta:.3f}"
                ])

        # Footer with fit parameters
        writer.writerow([])
        writer.writerow(['# Linear fits: sigma_c = m*K + b'])
        writer.writerow([f'# Threshold 2.0: m={m_20:.3f}, b={b_20:.3f}'])
        writer.writerow([f'# Threshold 2.3: m={m_23:.3f}, b={b_23:.3f}'])

    print(f"\n✓ Table S1 saved: tableS1_threshold_comparison.csv")

    # Print template text
    print(f"\n{'='*60}")
    print("SUGGESTED TEXT FOR SECTION 2.6:")
    print(f"{'='*60}")
    print(f"""
We define the "ridge collapse" threshold at |S| = 2.3 rather than the
classical bound |S| = 2.0. Table S1 shows that this choice shifts σc
values upward but preserves the scaling relationship σc ≈ {m_23:.2f}K
(vs. σc ≈ {m_20:.2f}K for threshold 2.0). The 2.3 threshold provides
a more practical margin for identifying robust correlations above
classical bounds.
""")


if __name__ == "__main__":
    main()
