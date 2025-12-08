#!/usr/bin/env python3
"""
Paper 2 Figure 2: Memory Curvature Surface Heatmaps

Three-panel figure showing C_mem(K, σ) at different lag scales:
(a) Short-lag (τ_mid = 17.5): fast echo decay
(b) Mid-lag (τ_mid = 37.5): intermediate memory
(c) Long-lag (τ_mid = 75.0): persistent correlations

Uses diverging colormap centered at 0 to highlight sign changes.

Data source: E221 condensed surface files (Cmem_short/mid/long.json)
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

# Akavarta brand colors for annotations
TEAL = "#00B4A0"
CORAL = "#FF6B6B"
GRAPHITE = "#4A4A4A"


def load_surface(name: str) -> dict:
    """Load a condensed surface file."""
    with open(DATA_DIR / f"{name}.json") as f:
        return json.load(f)


def main():
    # Load all three surfaces
    short_data = load_surface("Cmem_short")
    mid_data = load_surface("Cmem_mid")
    long_data = load_surface("Cmem_long")

    K_values = np.array(short_data['K_values'])
    sigma_values = np.array(short_data['sigma_values'])

    # Convert to numpy arrays
    Cmem_short = np.array(short_data['C_mem'])
    Cmem_mid = np.array(mid_data['C_mem'])
    Cmem_long = np.array(long_data['C_mem'])

    # Create figure with 3 panels
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Find global min/max for consistent colorscale
    all_data = np.concatenate([Cmem_short.flatten(), Cmem_mid.flatten(), Cmem_long.flatten()])
    vmin, vmax = all_data.min(), all_data.max()

    # Use symmetric bounds around 0 for diverging colormap
    vabs = max(abs(vmin), abs(vmax))

    # Create meshgrid for pcolormesh
    K_mesh, sigma_mesh = np.meshgrid(K_values, sigma_values, indexing='ij')

    panels = [
        (Cmem_short, 17.5, "(a) Short-lag Curvature"),
        (Cmem_mid, 37.5, "(b) Mid-lag Curvature"),
        (Cmem_long, 75.0, "(c) Long-lag Curvature")
    ]

    for ax, (data, tau_mid, title) in zip(axes, panels):
        # Use diverging colormap centered at 0
        norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)

        im = ax.pcolormesh(K_mesh, sigma_mesh, data,
                          cmap='RdBu_r', norm=norm, shading='auto')

        ax.set_xlabel('Coupling Strength $K$', fontsize=12)
        ax.set_ylabel(r'Noise Level $\sigma$', fontsize=12)
        ax.set_title(f'{title}\n' + r'$\tau_{\mathrm{mid}} = $' + f'{tau_mid}',
                    fontsize=13, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(r'$C_{\mathrm{mem}}(\tau_{\mathrm{mid}})$', fontsize=11)

        # Add contour at C_mem = 0 (sign change boundary)
        ax.contour(K_mesh, sigma_mesh, data, levels=[0],
                  colors='black', linewidths=1.5, linestyles='--')

    plt.tight_layout()

    # Save figures
    output_png = OUTPUT_DIR / "Fig2_memory_curvature_surface.png"
    output_pdf = OUTPUT_DIR / "Fig2_memory_curvature_surface.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_pdf}")

    plt.close()

    # Print summary statistics
    print("\n" + "="*60)
    print("Figure 2 Summary Statistics")
    print("="*60)

    for name, tau_mid, data in [
        ("Short-lag", 17.5, Cmem_short),
        ("Mid-lag", 37.5, Cmem_mid),
        ("Long-lag", 75.0, Cmem_long)
    ]:
        print(f"\n{name} (τ_mid = {tau_mid}):")
        print(f"  C_mem range: [{data.min():.6f}, {data.max():.6f}]")
        print(f"  Mean: {data.mean():.6f}, Std: {data.std():.6f}")

        # Sign analysis
        pos_frac = np.sum(data > 0) / data.size * 100
        neg_frac = np.sum(data < 0) / data.size * 100
        print(f"  Sign: {pos_frac:.1f}% positive, {neg_frac:.1f}% negative")

        # Find where curvature is most negative (steepest decay)
        min_idx = np.unravel_index(np.argmin(data), data.shape)
        print(f"  Most negative at K={K_values[min_idx[0]]:.2f}, σ={sigma_values[min_idx[1]]:.2f}")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
