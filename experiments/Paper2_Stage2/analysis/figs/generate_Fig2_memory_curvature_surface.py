#!/usr/bin/env python3
"""
Paper 2 Figure 2: Memory Curvature Surface

Heatmap of C_mem(τ_mid=37.5) over (K, σ) grid.
Uses zero-centered diverging colormap to highlight sign changes.

Input: Cmem_mid.json
Output: Fig2_memory_curvature_surface.png/.pdf
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUTPUT_DIR = SCRIPT_DIR

# Akavarta brand colors
TEAL = "#00B4A0"
CORAL = "#FF6B6B"
GRAPHITE = "#4A4A4A"
OBSIDIAN = "#1A1A1A"


def load_cmem_mid() -> dict:
    """Load C_mem(τ_mid=37.5) surface."""
    path = DATA_DIR / "Cmem_mid.json"
    if not path.exists():
        raise FileNotFoundError(f"Cmem_mid.json not found at {path}")
    with open(path) as f:
        return json.load(f)


def main():
    print("=" * 60)
    print("Paper 2 Figure 2: Memory Curvature Surface")
    print("=" * 60)
    print()

    # Load data
    print("Loading Cmem_mid.json...")
    data = load_cmem_mid()

    K_values = np.array(data['K_values'])
    sigma_values = np.array(data['sigma_values'])
    C_mem = np.array(data['C_mem'])
    tau_mid = data['tau_mid']

    print(f"  Grid: {len(K_values)} K × {len(sigma_values)} σ")
    print(f"  τ_mid = {tau_mid}")
    print(f"  C_mem range: [{C_mem.min():.6f}, {C_mem.max():.6f}]")
    print()

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create meshgrid
    K_mesh, sigma_mesh = np.meshgrid(K_values, sigma_values, indexing='ij')

    # Zero-centered diverging colormap
    vabs = max(abs(C_mem.min()), abs(C_mem.max()))
    norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)

    # Heatmap
    im = ax.pcolormesh(K_mesh, sigma_mesh, C_mem,
                       cmap='RdBu_r', norm=norm, shading='auto')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'Memory Curvature $C_{\mathrm{mem}}(\tau_{\mathrm{mid}}=37.5)$',
                   fontsize=12)

    # Add C_mem = 0 contour (sign-change boundary)
    contour = ax.contour(K_mesh, sigma_mesh, C_mem, levels=[0],
                         colors='black', linewidths=2, linestyles='--')
    ax.clabel(contour, fmt={0: '$C_{mem}=0$'}, fontsize=10)

    # Labels
    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Memory Curvature Surface $C_{\mathrm{mem}}(K, \sigma)$',
                 fontsize=14, fontweight='bold')

    # Add annotation box
    pos_frac = np.sum(C_mem > 0) / C_mem.size * 100
    neg_frac = np.sum(C_mem < 0) / C_mem.size * 100

    textstr = '\n'.join([
        r'$\tau_{\mathrm{mid}} = 37.5$',
        f'{neg_frac:.0f}% negative (decaying)',
        f'{pos_frac:.0f}% positive (growing)',
        '',
        'Dashed line: sign change'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()

    # Save
    output_png = OUTPUT_DIR / "Fig2_memory_curvature_surface.png"
    output_pdf = OUTPUT_DIR / "Fig2_memory_curvature_surface.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_pdf}")

    plt.close()

    # Summary
    print()
    print("=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(f"C_mem range: [{C_mem.min():.6f}, {C_mem.max():.6f}]")
    print(f"Mean: {C_mem.mean():.6f}")
    print(f"Sign distribution: {neg_frac:.1f}% negative, {pos_frac:.1f}% positive")

    # Find extrema locations
    min_idx = np.unravel_index(np.argmin(C_mem), C_mem.shape)
    max_idx = np.unravel_index(np.argmax(C_mem), C_mem.shape)
    print(f"Min at K={K_values[min_idx[0]]:.2f}, σ={sigma_values[min_idx[1]]:.2f}")
    print(f"Max at K={K_values[max_idx[0]]:.2f}, σ={sigma_values[max_idx[1]]:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
