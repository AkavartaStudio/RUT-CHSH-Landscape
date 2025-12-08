#!/usr/bin/env python3
"""
Paper 2 Figure 1: σ_mem(K) vs σ_c(K) Comparison

Two-panel figure showing:
(a) σ_mem and σ_c vs K — reveals the huge vertical gap
(b) Ratio r(K) = σ_mem / σ_c — shows ~0.03 fragility ratio

Data sources:
- σ_mem(K): E211 (Paper2_Mission1/analysis/data/memory_threshold_curve.json)
- σ_c(K): A1 (RUT-CHSH-Landscape/analysis/data/paper1/A1_sigma_c_K_sweep.json)

Output: Fig1_sigma_mem_vs_sigma_c.png/.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
MISSION1_DATA = SCRIPT_DIR.parent / "data"
PAPER1_DATA = Path("/Users/kellymcrae/Akavarta/research/phys/Paper1/published/analysis/data/paper1")
OUTPUT_DIR = SCRIPT_DIR

# Akavarta brand colors
TEAL = "#00B4A0"
CORAL = "#FF6B6B"
GRAPHITE = "#4A4A4A"
OBSIDIAN = "#1A1A1A"


def load_sigma_mem():
    """Load σ_mem(K) from E211"""
    with open(MISSION1_DATA / "memory_threshold_curve.json") as f:
        data = json.load(f)
    return np.array(data['K_values']), np.array(data['sigma_mem_values'])


def load_sigma_c():
    """Load σ_c(K) from Paper 1 A1 sweep"""
    with open(PAPER1_DATA / "A1_sigma_c_K_sweep.json") as f:
        data = json.load(f)
    analysis = data['sigma_c_analysis']
    return np.array(analysis['K_values']), np.array(analysis['sigma_c_values'])


def main():
    # Load data
    K_mem, sigma_mem = load_sigma_mem()
    K_c, sigma_c = load_sigma_c()

    # Interpolate σ_c to match K_mem grid for ratio calculation
    # Only use K values present in both datasets
    K_common = np.array([k for k in K_mem if k in K_c or any(np.isclose(k, K_c, atol=0.01))])

    # For ratio, interpolate σ_c at K_mem points
    sigma_c_interp = np.interp(K_mem, K_c, sigma_c)

    # Compute ratio
    ratio = sigma_mem / sigma_c_interp

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # ===== Panel (a): σ_mem and σ_c vs K =====
    ax1.semilogy(K_mem, sigma_mem, 'o-', color=CORAL, linewidth=2.5, markersize=8,
                 label=r'$\sigma_{\mathrm{mem}}(K)$ — Memory collapse', zorder=3)
    ax1.semilogy(K_c, sigma_c, 's-', color=TEAL, linewidth=2.5, markersize=8,
                 label=r'$\sigma_c(K)$ — CHSH collapse (Paper 1)', zorder=2)

    # Shade the gap region
    ax1.fill_between(K_mem, sigma_mem, sigma_c_interp, alpha=0.2, color=GRAPHITE,
                     label='Memory-fragile zone')

    ax1.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax1.set_ylabel(r'Noise Threshold $\sigma$', fontsize=13)
    ax1.set_title('(a) Memory vs CHSH Collapse Thresholds', fontsize=14, fontweight='bold')
    ax1.set_xlim(0.05, 1.05)
    ax1.set_ylim(0.01, 1.5)
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(loc='upper left', fontsize=11, framealpha=0.95)

    # Add annotation for the gap (no arrow)
    ax1.text(0.35, 0.12, '30× gap',
             fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=GRAPHITE, alpha=0.9))

    # ===== Panel (b): Ratio r(K) = σ_mem / σ_c =====
    ax2.plot(K_mem, ratio, 'o-', color=OBSIDIAN, linewidth=2.5, markersize=8)

    # Add horizontal reference line at mean ratio
    mean_ratio = np.mean(ratio)
    ax2.axhline(y=mean_ratio, color=CORAL, linestyle='--', linewidth=2, alpha=0.7,
                label=f'Mean ratio = {mean_ratio:.3f}')

    # Add horizontal reference at 1/30
    ax2.axhline(y=1/30, color=TEAL, linestyle=':', linewidth=1.5, alpha=0.7,
                label=r'$1/30 \approx 0.033$')

    ax2.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax2.set_ylabel(r'Fragility Ratio $r(K) = \sigma_{\mathrm{mem}} / \sigma_c$', fontsize=13)
    ax2.set_title('(b) Memory Fragility Ratio Across Ridge', fontsize=14, fontweight='bold')
    ax2.set_xlim(0.05, 1.05)
    ax2.set_ylim(0, 0.12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right', fontsize=11, framealpha=0.95)

    # Add annotation
    ax2.annotate(f'Memory collapses at\n~3% of CHSH threshold',
                 xy=(0.6, mean_ratio), xytext=(0.65, 0.08),
                 fontsize=11, ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=GRAPHITE, alpha=0.9),
                 arrowprops=dict(arrowstyle='->', color=OBSIDIAN, lw=1.5))

    plt.tight_layout()

    # Save figures
    output_png = OUTPUT_DIR / "Fig1_sigma_mem_vs_sigma_c.png"
    output_pdf = OUTPUT_DIR / "Fig1_sigma_mem_vs_sigma_c.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_pdf}")

    plt.close()

    # Print summary statistics
    print("\n" + "="*60)
    print("Figure 1 Summary Statistics")
    print("="*60)
    print(f"σ_mem range: [{sigma_mem.min():.4f}, {sigma_mem.max():.4f}]")
    print(f"σ_c range:   [{sigma_c.min():.4f}, {sigma_c.max():.4f}]")
    print(f"Ratio r(K) range: [{ratio.min():.4f}, {ratio.max():.4f}]")
    print(f"Mean ratio: {mean_ratio:.4f}")
    print(f"σ_mem is constant at {sigma_mem[0]:.2f} across all K")
    print("="*60)


if __name__ == "__main__":
    main()
