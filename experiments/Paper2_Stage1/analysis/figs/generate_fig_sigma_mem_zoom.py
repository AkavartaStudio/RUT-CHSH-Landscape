#!/usr/bin/env python3
"""
Paper 2 - Mission 1b Figure: High-Resolution σ_mem Zoom

Shows ρ_S(50) vs σ for K ∈ {0.3, 0.6, 0.9} in the range [0.00, 0.04].
Highlights the sharp memory collapse at σ_mem ≈ 0.002.

Data source: E211_sigma_mem_zoom.json
Output: Fig_sigma_mem_zoom.png/.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUTPUT_DIR = SCRIPT_DIR

# Akavarta brand colors
TEAL = "#00B4A0"
CORAL = "#FF6B6B"
VIOLET = "#8B5CF6"
GRAPHITE = "#4A4A4A"
OBSIDIAN = "#1A1A1A"


def load_zoom_data():
    """Load E211b zoom data."""
    with open(DATA_DIR / "E211_sigma_mem_zoom.json") as f:
        return json.load(f)


def main():
    # Load data
    data = load_zoom_data()
    tau = data['tau']
    threshold_fraction = data['threshold_fraction']

    # Color map for K values
    colors = {
        "0.3": CORAL,
        "0.6": TEAL,
        "0.9": VIOLET
    }

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each K value
    for K_str, K_data in data['results_by_K'].items():
        sigma_vals = np.array(K_data['sigma_values'])
        rho_mean = np.array(K_data['rho_S_mean'])
        rho_std = np.array(K_data['rho_S_std'])
        rho_det = K_data['rho_det']
        sigma_mem = K_data['sigma_mem']

        color = colors[K_str]

        # Plot with error band
        ax.fill_between(sigma_vals, rho_mean - rho_std, rho_mean + rho_std,
                        alpha=0.2, color=color)
        ax.plot(sigma_vals, rho_mean, 'o-', color=color, linewidth=2.5,
                markersize=6, label=f'$K = {K_str}$')

        # Mark σ_mem point
        if sigma_mem is not None:
            idx = list(sigma_vals).index(sigma_mem)
            ax.axvline(x=sigma_mem, color=color, linestyle=':', alpha=0.5)

    # Add threshold line
    rho_det_mean = np.mean([d['rho_det'] for d in data['results_by_K'].values()])
    threshold = threshold_fraction * rho_det_mean
    ax.axhline(y=threshold, color=GRAPHITE, linestyle='--', linewidth=1.5, alpha=0.7,
               label=f'Threshold = {threshold_fraction} × ρ_det')

    # Add σ_mem annotation
    ax.annotate(f'σ_mem = 0.002\n(all K values)',
                xy=(0.002, 0.05), xytext=(0.015, 0.3),
                fontsize=11, ha='left',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                         edgecolor=GRAPHITE, alpha=0.9),
                arrowprops=dict(arrowstyle='->', color=OBSIDIAN, lw=1.5))

    # Labels and formatting
    ax.set_xlabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_ylabel(r'Autocorrelation $\rho_S(\tau=50)$', fontsize=13)
    ax.set_title(f'High-Resolution Memory Collapse: ρ_S({tau}) vs σ',
                 fontsize=14, fontweight='bold')

    ax.set_xlim(-0.001, 0.042)
    ax.set_ylim(-0.1, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)

    # Add text box with key finding
    textstr = '\n'.join([
        'Key Finding:',
        'Memory collapses at σ = 0.002',
        'for all K values tested.',
        '',
        f'ρ_det ≈ 0.954 → ρ ≈ 0.004',
        'in a single step!'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.025, 0.7, textstr, fontsize=10, verticalalignment='top',
            bbox=props)

    plt.tight_layout()

    # Save figures
    output_png = OUTPUT_DIR / "Fig_sigma_mem_zoom.png"
    output_pdf = OUTPUT_DIR / "Fig_sigma_mem_zoom.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_pdf}")

    plt.close()

    # Print summary
    print("\n" + "="*60)
    print("Zoom Figure Summary")
    print("="*60)
    for K_str, K_data in data['results_by_K'].items():
        rho_det = K_data['rho_det']
        rho_at_002 = K_data['rho_S_mean'][1]  # σ = 0.002
        print(f"K = {K_str}: ρ_det = {rho_det:.4f}, ρ(σ=0.002) = {rho_at_002:.4f}")
    print("="*60)


if __name__ == "__main__":
    main()
