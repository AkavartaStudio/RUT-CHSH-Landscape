#!/usr/bin/env python3
"""
Paper 2 Figures 3 & 4: Echo Surface and χ Surface

Fig3: ρ_S(τ=50) echo surface - memory persistence across (K, σ)
Fig4: χ_mid = C_mem(37.5) × ρ_S(50) - recursive susceptibility with χ=0 contour

Inputs:
  - P2_echo_surface_tau50.json
  - P2_chi_mid_surface.json

Outputs:
  - Fig3_echo_surface.png/.pdf
  - Fig4_chi_mid_surface.png/.pdf
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


def load_surface(filename: str) -> dict:
    """Load a surface JSON file."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"{filename} not found at {path}")
    with open(path) as f:
        return json.load(f)


def generate_fig3_echo_surface():
    """Generate Figure 3: Echo surface ρ_S(τ=50)."""
    print("Generating Figure 3: Echo Surface...")

    # Load data
    data = load_surface("P2_echo_surface_tau50.json")

    K_values = np.array(data['K_values'])
    sigma_values = np.array(data['sigma_values'])
    rho_S = np.array(data['surface'])

    print(f"  Grid: {len(K_values)} K × {len(sigma_values)} σ")
    print(f"  ρ_S range: [{rho_S.min():.4f}, {rho_S.max():.4f}]")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create meshgrid
    K_mesh, sigma_mesh = np.meshgrid(K_values, sigma_values, indexing='ij')

    # Sequential colormap for echo (0 to 1)
    im = ax.pcolormesh(K_mesh, sigma_mesh, rho_S,
                       cmap='viridis', vmin=0, vmax=1, shading='auto')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'Echo Strength $\rho_S(\tau=50)$', fontsize=12)

    # Add contours at key levels
    levels = [0.1, 0.3, 0.5, 0.7, 0.9]
    contour = ax.contour(K_mesh, sigma_mesh, rho_S, levels=levels,
                         colors='white', linewidths=1, alpha=0.7)
    ax.clabel(contour, fmt='%.1f', fontsize=9)

    # Labels
    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Echo Surface $\rho_S(\tau=50)$',
                 fontsize=14, fontweight='bold')

    # Add annotation
    textstr = '\n'.join([
        r'$\tau = 50$ samples',
        f'Max echo: {rho_S.max():.3f}',
        f'At σ=0: {rho_S[:, 0].mean():.3f}',
        '',
        'Contours: 0.1 to 0.9'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    # Save
    output_png = OUTPUT_DIR / "Fig3_echo_surface.png"
    output_pdf = OUTPUT_DIR / "Fig3_echo_surface.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_pdf}")

    plt.close()

    return rho_S


def generate_fig4_chi_surface():
    """Generate Figure 4: χ_mid surface with χ=0 contour."""
    print("Generating Figure 4: χ_mid Surface...")

    # Load data
    data = load_surface("P2_chi_mid_surface.json")

    K_values = np.array(data['K_values'])
    sigma_values = np.array(data['sigma_values'])
    chi = np.array(data['surface'])
    tau_mid = data.get('tau_mid', 37.5)

    print(f"  Grid: {len(K_values)} K × {len(sigma_values)} σ")
    print(f"  χ range: [{chi.min():.6f}, {chi.max():.6f}]")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create meshgrid
    K_mesh, sigma_mesh = np.meshgrid(K_values, sigma_values, indexing='ij')

    # Zero-centered diverging colormap
    vabs = max(abs(chi.min()), abs(chi.max()))
    if vabs == 0:
        vabs = 1e-6  # Avoid division by zero
    norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)

    # Heatmap
    im = ax.pcolormesh(K_mesh, sigma_mesh, chi,
                       cmap='RdBu_r', norm=norm, shading='auto')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'Recursive Susceptibility $\chi_{\mathrm{mid}}$', fontsize=12)

    # Add χ = 0 contour (critical boundary)
    contour = ax.contour(K_mesh, sigma_mesh, chi, levels=[0],
                         colors='black', linewidths=2.5, linestyles='-')

    # Try to label the contour (matplotlib 3.8+ uses allsegs instead of collections)
    try:
        ax.clabel(contour, fmt={0: r'$\chi=0$'}, fontsize=11, fontweight='bold')
    except Exception:
        pass  # Skip labeling if contour is empty

    # Labels
    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Susceptibility Surface $\chi = C_{\mathrm{mem}} \times \rho_S$',
                 fontsize=14, fontweight='bold')

    # Add annotation
    pos_frac = np.sum(chi > 0) / chi.size * 100
    neg_frac = np.sum(chi < 0) / chi.size * 100

    textstr = '\n'.join([
        r'$\chi = C_{\mathrm{mem}}(37.5) \times \rho_S(50)$',
        '',
        f'{neg_frac:.0f}% negative (stable)',
        f'{pos_frac:.0f}% positive (unstable)',
        '',
        r'Black line: $\chi = 0$ boundary'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()

    # Save
    output_png = OUTPUT_DIR / "Fig4_chi_mid_surface.png"
    output_pdf = OUTPUT_DIR / "Fig4_chi_mid_surface.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_pdf}")

    plt.close()

    return chi


def generate_combined_figure():
    """Generate combined 2-panel figure (Fig3a + Fig3b style)."""
    print("Generating Combined Figure 3: Echo + χ...")

    # Load data
    echo_data = load_surface("P2_echo_surface_tau50.json")
    chi_data = load_surface("P2_chi_mid_surface.json")

    K_values = np.array(echo_data['K_values'])
    sigma_values = np.array(echo_data['sigma_values'])
    rho_S = np.array(echo_data['surface'])
    chi = np.array(chi_data['surface'])

    # Create figure with 2 panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Create meshgrid
    K_mesh, sigma_mesh = np.meshgrid(K_values, sigma_values, indexing='ij')

    # Panel (a): Echo surface
    im1 = ax1.pcolormesh(K_mesh, sigma_mesh, rho_S,
                         cmap='viridis', vmin=0, vmax=1, shading='auto')
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label(r'$\rho_S(\tau=50)$', fontsize=11)

    # Echo contours
    levels = [0.1, 0.5, 0.9]
    contour1 = ax1.contour(K_mesh, sigma_mesh, rho_S, levels=levels,
                           colors='white', linewidths=1, alpha=0.8)
    ax1.clabel(contour1, fmt='%.1f', fontsize=9)

    ax1.set_xlabel('Coupling Strength $K$', fontsize=12)
    ax1.set_ylabel(r'Noise Level $\sigma$', fontsize=12)
    ax1.set_title(r'(a) Echo Surface $\rho_S(\tau=50)$', fontsize=13, fontweight='bold')

    # Panel (b): χ surface
    vabs = max(abs(chi.min()), abs(chi.max()))
    if vabs == 0:
        vabs = 1e-6
    norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)

    im2 = ax2.pcolormesh(K_mesh, sigma_mesh, chi,
                         cmap='RdBu_r', norm=norm, shading='auto')
    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label(r'$\chi_{\mathrm{mid}}$', fontsize=11)

    # χ = 0 contour
    contour2 = ax2.contour(K_mesh, sigma_mesh, chi, levels=[0],
                           colors='black', linewidths=2.5)
    try:
        ax2.clabel(contour2, fmt={0: r'$\chi=0$'}, fontsize=10)
    except Exception:
        pass

    ax2.set_xlabel('Coupling Strength $K$', fontsize=12)
    ax2.set_ylabel(r'Noise Level $\sigma$', fontsize=12)
    ax2.set_title(r'(b) Recursive Susceptibility $\chi = C_{\mathrm{mem}} \times \rho_S$',
                  fontsize=13, fontweight='bold')

    plt.tight_layout()

    # Save
    output_png = OUTPUT_DIR / "Fig3_echo_and_chi_combined.png"
    output_pdf = OUTPUT_DIR / "Fig3_echo_and_chi_combined.pdf"

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")

    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_pdf}")

    plt.close()


def main():
    print("=" * 70)
    print("Paper 2 Figures 3 & 4: Echo Surface and χ Surface")
    print("=" * 70)
    print()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Generate individual figures
        rho_S = generate_fig3_echo_surface()
        print()
        chi = generate_fig4_chi_surface()
        print()

        # Generate combined figure
        generate_combined_figure()
        print()

        # Summary
        print("=" * 70)
        print("Summary Statistics")
        print("=" * 70)
        print(f"Echo ρ_S(50) range: [{rho_S.min():.4f}, {rho_S.max():.4f}]")
        print(f"χ_mid range: [{chi.min():.6f}, {chi.max():.6f}]")

        pos_frac = np.sum(chi > 0) / chi.size * 100
        neg_frac = np.sum(chi < 0) / chi.size * 100
        print(f"χ sign: {neg_frac:.1f}% negative, {pos_frac:.1f}% positive")
        print("=" * 70)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Run build_echo_and_chi_surfaces.py first to generate input data.")
        return


if __name__ == "__main__":
    main()
