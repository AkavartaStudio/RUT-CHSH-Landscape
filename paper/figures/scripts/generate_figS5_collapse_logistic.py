#!/usr/bin/env python3
"""
Logistic-Fit Characterization of Collapse Curve (Figure S5)
============================================================

Generates three-panel figure showing:
(A) K=0.7 collapse curve with logistic fit
(B) Fit residuals
(C) σ_c(K) scaling and width parameters

Reads:
- analysis/data/paper1/A1_sigma_c_K_sweep.json (raw data)
- paper/figures/tableS2_logistic_params.csv (fitted parameters)

Saves: figS5_collapse_logistic.png
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit

def logistic_function(sigma, S_high, S_low, sigma_c, w):
    """
    Four-parameter logistic function for collapse curve
    """
    return S_low + (S_high - S_low) / (1 + np.exp((sigma - sigma_c) / w))

def main():
    # Paths
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent.parent
    data_file = repo_root / 'analysis' / 'data' / 'paper1' / 'A1_sigma_c_K_sweep.json'
    table_file = script_dir.parent / 'tableS2_logistic_params.csv'
    output_dir = script_dir.parent

    print("Loading data...")

    # Load A1 data
    with open(data_file, 'r') as f:
        a1_data = json.load(f)

    # Load logistic fit parameters
    table_data = np.genfromtxt(table_file, delimiter=',', skip_header=1,
                               names=['K', 'S_high', 'S_low', 'sigma_c', 'w', 'R2'])

    # Build |S|(sigma, K) grid from results
    S_grid = {}
    for result in a1_data['grid_results']:
        K = result['K']
        sigma = result['sigma']
        S_mean = result['abs_S_mean']  # Note: key is 'abs_S_mean' not 'S_mean'

        if K not in S_grid:
            S_grid[K] = {}
        S_grid[K][sigma] = S_mean

    # Create figure with 3 panels
    fig = plt.figure(figsize=(15, 4))

    # ============================================================
    # Panel A: K=0.7 collapse curve with logistic fit
    # ============================================================
    ax_A = plt.subplot(1, 3, 1)

    K_target = 0.7
    sigma_plot = np.array(sorted(S_grid[K_target].keys()))
    S_plot = np.array([S_grid[K_target][s] for s in sigma_plot])

    # Get fitted parameters for K=0.7
    idx_K07 = np.where(table_data['K'] == K_target)[0][0]
    params_K07 = table_data[idx_K07]

    # Generate smooth logistic curve
    sigma_smooth = np.linspace(0, sigma_plot.max(), 500)
    S_fit = logistic_function(sigma_smooth, params_K07['S_high'], params_K07['S_low'],
                             params_K07['sigma_c'], params_K07['w'])

    # Plot
    ax_A.plot(sigma_plot, S_plot, 'o', color='#2E86AB', markersize=6,
             label='Numerical data', zorder=3)
    ax_A.plot(sigma_smooth, S_fit, '-', color='#A23B72', linewidth=2,
             label=f'Logistic fit ($R^2$ = {params_K07["R2"]:.3f})', zorder=2)

    # Annotations
    ax_A.axhline(2, color='gray', linestyle='--', linewidth=1, alpha=0.5, zorder=1)
    ax_A.axvline(params_K07['sigma_c'], color='gray', linestyle=':', linewidth=1,
                alpha=0.7, zorder=1)
    ax_A.text(params_K07['sigma_c'] + 0.05, 2.5,
             f"$\\sigma_c$ = {params_K07['sigma_c']:.3f}",
             fontsize=10, color='gray')

    ax_A.set_xlabel('Noise amplitude $\\sigma$', fontsize=12)
    ax_A.set_ylabel('CHSH amplitude $|S|$', fontsize=12)
    ax_A.set_title('(A) Collapse curve at $K = 0.7$', fontsize=12, fontweight='bold')
    ax_A.legend(loc='upper right', fontsize=10, frameon=True, framealpha=0.9)
    ax_A.grid(True, alpha=0.2)
    ax_A.set_xlim(0, sigma_plot.max())
    ax_A.set_ylim(0, 3)

    # ============================================================
    # Panel B: Residuals
    # ============================================================
    ax_B = plt.subplot(1, 3, 2)

    # Compute residuals
    S_fit_at_data = logistic_function(sigma_plot, params_K07['S_high'], params_K07['S_low'],
                                     params_K07['sigma_c'], params_K07['w'])
    residuals = S_plot - S_fit_at_data

    ax_B.plot(sigma_plot, residuals, 'o', color='#2E86AB', markersize=6)
    ax_B.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax_B.axhline(0.01, color='lightgray', linestyle=':', linewidth=0.8)
    ax_B.axhline(-0.01, color='lightgray', linestyle=':', linewidth=0.8)

    ax_B.set_xlabel('Noise amplitude $\\sigma$', fontsize=12)
    ax_B.set_ylabel('Residual $|S|_{\\rm data} - |S|_{\\rm fit}$', fontsize=12)
    ax_B.set_title('(B) Fit residuals', fontsize=12, fontweight='bold')
    ax_B.grid(True, alpha=0.2)
    ax_B.set_xlim(0, sigma_plot.max())

    # Add residual statistics
    rms_residual = np.sqrt(np.mean(residuals**2))
    ax_B.text(0.05, 0.95, f'RMS = {rms_residual:.4f}',
             transform=ax_B.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round',
             facecolor='white', alpha=0.8))

    # ============================================================
    # Panel C: σ_c(K) scaling and w(K)
    # ============================================================
    ax_C = plt.subplot(1, 3, 3)

    # Plot σ_c(K) with linear fit
    K_fit = table_data['K']
    sigma_c_fit = table_data['sigma_c']
    w_fit = table_data['w']

    # Linear fit to σ_c(K)
    slope, intercept = np.polyfit(K_fit, sigma_c_fit, 1)
    K_line = np.linspace(K_fit.min(), K_fit.max(), 100)
    sigma_c_line = slope * K_line + intercept

    # Compute R²
    ss_res = np.sum((sigma_c_fit - (slope * K_fit + intercept))**2)
    ss_tot = np.sum((sigma_c_fit - np.mean(sigma_c_fit))**2)
    r_squared = 1 - (ss_res / ss_tot)

    ax_C.plot(K_fit, sigma_c_fit, 'o', color='#2E86AB', markersize=8,
             label=f'$\\sigma_c(K)$ (logistic inflection)', zorder=3)
    ax_C.plot(K_line, sigma_c_line, '--', color='#2E86AB', linewidth=2,
             label=f'Linear fit: $\\sigma_c = {slope:.2f}K + {intercept:.2f}$\n($R^2 = {r_squared:.3f}$)',
             zorder=2)

    ax_C.set_xlabel('Coupling strength $K$', fontsize=12)
    ax_C.set_ylabel('Inflection point $\\sigma_c$', fontsize=12, color='#2E86AB')
    ax_C.tick_params(axis='y', labelcolor='#2E86AB')
    ax_C.set_title('(C) Scaling of $\\sigma_c(K)$ and width $w(K)$',
                  fontsize=12, fontweight='bold')
    ax_C.grid(True, alpha=0.2)

    # Secondary y-axis for w(K)
    ax_C2 = ax_C.twinx()
    ax_C2.plot(K_fit, w_fit, '^', color='#F18F01', markersize=8,
              label='Width $w(K)$', zorder=3)
    ax_C2.set_ylabel('Width parameter $w$', fontsize=12, color='#F18F01')
    ax_C2.tick_params(axis='y', labelcolor='#F18F01')
    ax_C2.set_ylim(0.15, 0.25)

    # Combined legend
    lines_1, labels_1 = ax_C.get_legend_handles_labels()
    lines_2, labels_2 = ax_C2.get_legend_handles_labels()
    ax_C.legend(lines_1 + lines_2, labels_1 + labels_2,
               loc='upper left', fontsize=9, frameon=True, framealpha=0.9)

    # Layout and save
    plt.tight_layout()

    output_file = output_dir / 'figS5_collapse_logistic.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figS5_collapse_logistic.pdf', dpi=300, bbox_inches='tight')

    print(f"✓ Figure saved: {output_file.name}")
    print(f"  Panel A: K=0.7 collapse curve with fit (R² = {params_K07['R2']:.4f})")
    print(f"  Panel B: Residuals (RMS = {rms_residual:.4f})")
    print(f"  Panel C: σ_c(K) scaling (slope = {slope:.3f}, R² = {r_squared:.4f})")
    print(f"\nFit parameters at K=0.7:")
    print(f"  S_high = {params_K07['S_high']:.2f}")
    print(f"  S_low = {params_K07['S_low']:.2f}")
    print(f"  σ_c = {params_K07['sigma_c']:.3f}")
    print(f"  w = {params_K07['w']:.3f}")

if __name__ == "__main__":
    main()
