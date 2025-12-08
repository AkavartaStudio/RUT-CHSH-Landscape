#!/usr/bin/env python3
"""
Generate Figure 5: Angle-Resolved CHSH Field Panel
Paper 2 - Mission 4

Four-panel figure showing:
(a) S* surface (optimal-angle CHSH)
(b) χ_angle surface (susceptibility at optimal angles)
(c) Echo strength at optimal angles
(d) Angle-flow vector map
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "analysis" / "data"
FIG_DIR = Path(__file__).parent.parent / "analysis" / "figs"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def load_json(filename):
    with open(DATA_DIR / filename, 'r') as f:
        return json.load(f)

def main():
    print("Loading data...")

    # Load surfaces
    s_star = load_json("S_star_surface.json")
    chi_angle = load_json("chi_angle_surface.json")
    echo_angle = load_json("echo_angle_surface.json")
    angle_flow = load_json("angle_flow_vectors.json")

    K_values = np.array(s_star["K_values"])
    sigma_values = np.array(s_star["sigma_values"])
    S_star = np.array(s_star["S_star"])
    chi = np.array(chi_angle["chi_angle"])
    echo = np.array(echo_angle["echo_angle"])

    # Angle flow vectors - derivatives of optimal angles with respect to sigma
    # We have da/dsigma, dap/dsigma, db/dsigma, dbp/dsigma
    # Combine into a composite magnitude for visualization
    da_dsigma = np.array(angle_flow["da_dsigma"])
    dap_dsigma = np.array(angle_flow["dap_dsigma"])
    db_dsigma = np.array(angle_flow["db_dsigma"])
    dbp_dsigma = np.array(angle_flow["dbp_dsigma"])

    # Compute total angle rotation magnitude
    angle_rotation_mag = np.sqrt(da_dsigma**2 + dap_dsigma**2 + db_dsigma**2 + dbp_dsigma**2)

    print(f"S* range: [{np.min(S_star):.4f}, {np.max(S_star):.4f}]")
    print(f"χ range: [{np.min(chi):.4f}, {np.max(chi):.4f}]")
    print(f"Echo range: [{np.min(echo):.4f}, {np.max(echo):.4f}]")

    # Create 2x2 figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel (a): S* surface
    ax = axes[0, 0]
    im = ax.pcolormesh(sigma_values, K_values, S_star,
                       shading='auto', cmap='viridis', vmin=1.4, vmax=2.83)
    ax.set_xlabel(r'$\sigma$', fontsize=12)
    ax.set_ylabel(r'$K$', fontsize=12)
    ax.set_title(r'(a) Optimal-angle CHSH surface $S^*$', fontsize=11)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r'$|S^*|$', fontsize=11)
    # Add |S|=2 contour
    ax.contour(sigma_values, K_values, S_star, levels=[2.0], colors='white',
               linestyles='--', linewidths=1.5)

    # Panel (b): χ_angle surface
    ax = axes[0, 1]
    # Use symmetric colormap for susceptibility
    chi_max = max(abs(np.min(chi)), abs(np.max(chi)))
    im = ax.pcolormesh(sigma_values, K_values, chi,
                       shading='auto', cmap='RdBu_r', vmin=-chi_max, vmax=chi_max)
    ax.set_xlabel(r'$\sigma$', fontsize=12)
    ax.set_ylabel(r'$K$', fontsize=12)
    ax.set_title(r'(b) Susceptibility $\chi_{\mathrm{angle}} = \partial S^*/\partial\sigma$', fontsize=11)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r'$\chi$', fontsize=11)
    # Add χ=0 contour
    contour = ax.contour(sigma_values, K_values, chi, levels=[0.0], colors='white',
               linestyles='-', linewidths=1.5)
    # Add legend for contour in upper right with breathing room
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color='white', linestyle='-', linewidth=1.5, label=r'$\chi=0$')]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9, facecolor='gray',
              edgecolor='white', framealpha=0.9, borderpad=0.8)

    # Panel (c): Echo at optimal angles
    ax = axes[1, 0]
    im = ax.pcolormesh(sigma_values, K_values, echo,
                       shading='auto', cmap='plasma', vmin=0.4, vmax=1.0)
    ax.set_xlabel(r'$\sigma$', fontsize=12)
    ax.set_ylabel(r'$K$', fontsize=12)
    ax.set_title(r'(c) Echo strength $\rho_{S^*}(\tau{=}50)$', fontsize=11)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r'$\rho_{S^*}$', fontsize=11)
    # Add memory threshold line
    ax.axvline(x=0.002, color='cyan', linestyle='--', linewidth=1.5, label=r'$\sigma_{\mathrm{mem}}$')
    ax.legend(loc='upper right', fontsize=9)

    # Panel (d): Angle rotation magnitude
    ax = axes[1, 1]
    # Show magnitude of angle rotation as noise increases
    im = ax.pcolormesh(sigma_values, K_values, angle_rotation_mag,
                       shading='auto', cmap='magma')
    ax.set_xlabel(r'$\sigma$', fontsize=12)
    ax.set_ylabel(r'$K$', fontsize=12)
    ax.set_title(r'(d) Angle rotation magnitude $|\nabla_\sigma \theta^*|$', fontsize=11)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r'$|\nabla_\sigma \theta^*|$ (deg/$\sigma$)', fontsize=10)

    # Add overall figure title
    fig.suptitle('Angle-Resolved CHSH Field Geometry', fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()

    # Save figure
    output_path = FIG_DIR / "fig5_angle_field_panel.pdf"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_path}")

    # Also save PNG for quick viewing
    png_path = FIG_DIR / "fig5_angle_field_panel.png"
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {png_path}")

    plt.close()
    print("\nFigure 5 generation complete!")

if __name__ == "__main__":
    main()
