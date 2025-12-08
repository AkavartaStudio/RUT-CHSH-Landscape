#!/usr/bin/env python3
"""
Generate Figure 5: Angle-Resolved Observer Field

Fig 5a — Optimal angle geometry over the CHSH ridge
Fig 5b — χ_angle susceptibility surface
Fig 5c — Echo_angle long-lag memory surface
Fig 5d — Angle-flow vector map
Fig 5 (combined) — All four panels
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import json
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
GRAPHITE = '#2C3E50'


def load_data():
    """Load all E231 output files."""
    with open(DATA_DIR / "S_star_surface.json") as f:
        s_star = json.load(f)
    with open(DATA_DIR / "angle_optimal_grid.json") as f:
        angles = json.load(f)
    with open(DATA_DIR / "chi_angle_surface.json") as f:
        chi = json.load(f)
    with open(DATA_DIR / "echo_angle_surface.json") as f:
        echo = json.load(f)
    with open(DATA_DIR / "angle_flow_vectors.json") as f:
        flow = json.load(f)

    return s_star, angles, chi, echo, flow


def generate_fig5a_angle_geometry():
    """Generate Fig 5a: Optimal angle geometry."""
    print("Generating Figure 5a: Optimal angle geometry...")

    s_star, angles, _, _, _ = load_data()

    K = np.array(s_star["K_values"])
    sigma = np.array(s_star["sigma_values"])
    K_mesh, sigma_mesh = np.meshgrid(K, sigma, indexing='ij')

    # Use S* magnitude as background, overlay angle info
    S_star = np.array(s_star["S_star"])
    angle_a = np.array(angles["angle_a"])
    angle_b = np.array(angles["angle_b"])

    # Angle difference a - b (characterizes geometry)
    angle_diff = angle_a - angle_b

    fig, ax = plt.subplots(figsize=(10, 8))

    # Background: |S*| surface
    im = ax.pcolormesh(K_mesh, sigma_mesh, np.abs(S_star),
                       cmap='plasma', shading='auto', alpha=0.7)
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'$|S^*|$', fontsize=12)

    # Overlay contours of angle difference
    contours = ax.contour(K_mesh, sigma_mesh, angle_diff,
                          levels=np.arange(-90, 91, 15),
                          colors='white', linewidths=1.5, alpha=0.8)
    ax.clabel(contours, fmt='%.0f°', fontsize=9)

    # Mark classical bound
    ax.contour(K_mesh, sigma_mesh, np.abs(S_star), levels=[2.0],
               colors='cyan', linewidths=2.5, linestyles='--')

    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Figure 5a: Optimal Angle Geometry ($a - b$ contours over $|S^*|$)',
                 fontsize=14, fontweight='bold')

    # Annotation
    textstr = '\n'.join([
        r'Background: $|S^*|$ (optimal CHSH)',
        r'Contours: $a - b$ difference (degrees)',
        r'Cyan dashed: $|S| = 2$ boundary'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    output_png = OUTPUT_DIR / "Fig5a_optimal_angle_geometry.png"
    output_pdf = OUTPUT_DIR / "Fig5a_optimal_angle_geometry.pdf"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")
    print(f"  Saved: {output_pdf}")
    plt.close()

    return np.abs(S_star)


def generate_fig5b_chi_angle():
    """Generate Fig 5b: χ_angle susceptibility surface."""
    print("\nGenerating Figure 5b: χ_angle susceptibility surface...")

    _, _, chi_data, _, _ = load_data()

    K = np.array(chi_data["K_values"])
    sigma = np.array(chi_data["sigma_values"])
    K_mesh, sigma_mesh = np.meshgrid(K, sigma, indexing='ij')
    chi = np.array(chi_data["chi_angle"])

    print(f"  Grid: {len(K)} K × {len(sigma)} σ")
    print(f"  χ_angle range: [{chi.min():.4f}, {chi.max():.4f}]")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Diverging colormap centered at 0
    vabs = max(abs(chi.min()), abs(chi.max()))
    if vabs < 1e-6:
        vabs = 1e-6
    norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)

    im = ax.pcolormesh(K_mesh, sigma_mesh, chi,
                       cmap='RdBu_r', norm=norm, shading='auto')
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'$\chi_{\mathrm{angle}} = \partial S^*/\partial\sigma$', fontsize=12)

    # χ = 0 contour
    try:
        contour = ax.contour(K_mesh, sigma_mesh, chi, levels=[0],
                             colors='black', linewidths=2.5)
        ax.clabel(contour, fmt={0: r'$\chi=0$'}, fontsize=11)
    except Exception:
        pass

    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Figure 5b: Angle-Resolved Susceptibility $\chi_{\mathrm{angle}}$',
                 fontsize=14, fontweight='bold')

    # Annotation
    neg_frac = np.sum(chi < 0) / chi.size * 100
    pos_frac = np.sum(chi > 0) / chi.size * 100
    textstr = '\n'.join([
        r'$\chi_{\mathrm{angle}} = \partial S^*/\partial\sigma$',
        '',
        f'{neg_frac:.0f}% negative (S* decreases with noise)',
        f'{pos_frac:.0f}% positive (S* increases with noise)'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    output_png = OUTPUT_DIR / "Fig5b_chi_angle_surface.png"
    output_pdf = OUTPUT_DIR / "Fig5b_chi_angle_surface.pdf"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")
    print(f"  Saved: {output_pdf}")
    plt.close()

    return chi


def generate_fig5c_echo_angle():
    """Generate Fig 5c: Echo_angle long-lag memory surface."""
    print("\nGenerating Figure 5c: Echo_angle surface...")

    _, _, _, echo_data, _ = load_data()

    K = np.array(echo_data["K_values"])
    sigma = np.array(echo_data["sigma_values"])
    K_mesh, sigma_mesh = np.meshgrid(K, sigma, indexing='ij')
    echo = np.array(echo_data["echo_angle"])

    print(f"  Grid: {len(K)} K × {len(sigma)} σ")
    print(f"  Echo_angle range: [{echo.min():.4f}, {echo.max():.4f}]")

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.pcolormesh(K_mesh, sigma_mesh, echo,
                       cmap='viridis', shading='auto', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'$\rho_{S^*}(\tau=50)$', fontsize=12)

    # Contours at key levels
    ax.contour(K_mesh, sigma_mesh, echo, levels=[0.1, 0.5, 0.9],
               colors='white', linewidths=1.5, linestyles=['--', '-', '--'])

    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Figure 5c: Angle-Resolved Echo $\rho_{S^*}(\tau=50)$',
                 fontsize=14, fontweight='bold')

    # Annotation
    echo_at_0 = echo[:, 0].mean()
    textstr = '\n'.join([
        r'Echo at optimal angles',
        '',
        f'At σ=0: mean = {echo_at_0:.3f}',
        f'Range: [{echo.min():.3f}, {echo.max():.3f}]'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    output_png = OUTPUT_DIR / "Fig5c_echo_angle_surface.png"
    output_pdf = OUTPUT_DIR / "Fig5c_echo_angle_surface.pdf"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")
    print(f"  Saved: {output_pdf}")
    plt.close()

    return echo


def generate_fig5d_angle_flow():
    """Generate Fig 5d: Angle flow vector map."""
    print("\nGenerating Figure 5d: Angle flow vectors...")

    s_star, _, _, _, flow_data = load_data()

    K = np.array(flow_data["K_values"])
    sigma = np.array(flow_data["sigma_values"])
    K_mesh, sigma_mesh = np.meshgrid(K, sigma, indexing='ij')

    # Use da/dσ as primary flow indicator
    da = np.array(flow_data["da_dsigma"])
    dap = np.array(flow_data["dap_dsigma"])

    # Magnitude of angle change
    flow_mag = np.sqrt(da**2 + dap**2)

    S_star = np.array(s_star["S_star"])

    fig, ax = plt.subplots(figsize=(10, 8))

    # Background: |S*|
    im = ax.pcolormesh(K_mesh, sigma_mesh, np.abs(S_star),
                       cmap='Greys', shading='auto', alpha=0.4)

    # Quiver plot for angle flow
    # Subsample for clarity
    skip = 2
    K_sub = K_mesh[::skip, ::skip]
    sigma_sub = sigma_mesh[::skip, ::skip]
    da_sub = da[::skip, ::skip]
    dap_sub = dap[::skip, ::skip]

    # Normalize arrows for visibility
    mag = np.sqrt(da_sub**2 + dap_sub**2)
    mag[mag < 1e-6] = 1e-6

    Q = ax.quiver(K_sub, sigma_sub, da_sub/mag, dap_sub/mag,
                  mag, cmap='hot', scale=30, width=0.004,
                  headwidth=4, headlength=5)

    cbar = plt.colorbar(Q, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'Angle flow magnitude $|\partial\theta/\partial\sigma|$', fontsize=12)

    ax.set_xlabel('Coupling Strength $K$', fontsize=13)
    ax.set_ylabel(r'Noise Level $\sigma$', fontsize=13)
    ax.set_title(r'Figure 5d: Angle Flow Field $(\partial a/\partial\sigma, \partial a\prime/\partial\sigma)$',
                 fontsize=14, fontweight='bold')

    # Annotation
    textstr = '\n'.join([
        'Arrows: direction of angle shift with noise',
        'Color: magnitude of angle change',
        'Background: |S*| surface (gray)'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                 edgecolor=GRAPHITE, alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    output_png = OUTPUT_DIR / "Fig5d_angle_flow_vectors.png"
    output_pdf = OUTPUT_DIR / "Fig5d_angle_flow_vectors.pdf"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")
    print(f"  Saved: {output_pdf}")
    plt.close()

    return flow_mag


def generate_fig5_combined():
    """Generate combined 4-panel Figure 5."""
    print("\nGenerating Figure 5 (combined)...")

    s_star, angles, chi_data, echo_data, flow_data = load_data()

    K = np.array(s_star["K_values"])
    sigma = np.array(s_star["sigma_values"])
    K_mesh, sigma_mesh = np.meshgrid(K, sigma, indexing='ij')

    S_star = np.array(s_star["S_star"])
    angle_a = np.array(angles["angle_a"])
    angle_b = np.array(angles["angle_b"])
    chi = np.array(chi_data["chi_angle"])
    echo = np.array(echo_data["echo_angle"])
    da = np.array(flow_data["da_dsigma"])
    dap = np.array(flow_data["dap_dsigma"])

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel a: Angle geometry
    ax = axes[0, 0]
    angle_diff = angle_a - angle_b
    im = ax.pcolormesh(K_mesh, sigma_mesh, np.abs(S_star),
                       cmap='plasma', shading='auto', alpha=0.7)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=r'$|S^*|$')
    contours = ax.contour(K_mesh, sigma_mesh, angle_diff,
                          levels=np.arange(-90, 91, 30),
                          colors='white', linewidths=1.5, alpha=0.8)
    ax.clabel(contours, fmt='%.0f°', fontsize=8)
    ax.contour(K_mesh, sigma_mesh, np.abs(S_star), levels=[2.0],
               colors='cyan', linewidths=2, linestyles='--')
    ax.set_xlabel('$K$', fontsize=11)
    ax.set_ylabel(r'$\sigma$', fontsize=11)
    ax.set_title(r'(a) Optimal Angle Geometry', fontsize=12, fontweight='bold')

    # Panel b: χ_angle
    ax = axes[0, 1]
    vabs = max(abs(chi.min()), abs(chi.max()))
    if vabs < 1e-6:
        vabs = 1e-6
    norm = TwoSlopeNorm(vmin=-vabs, vcenter=0, vmax=vabs)
    im = ax.pcolormesh(K_mesh, sigma_mesh, chi,
                       cmap='RdBu_r', norm=norm, shading='auto')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=r'$\chi_{\mathrm{angle}}$')
    try:
        ax.contour(K_mesh, sigma_mesh, chi, levels=[0],
                   colors='black', linewidths=2)
    except Exception:
        pass
    ax.set_xlabel('$K$', fontsize=11)
    ax.set_ylabel(r'$\sigma$', fontsize=11)
    ax.set_title(r'(b) Angle Susceptibility $\chi_{\mathrm{angle}}$', fontsize=12, fontweight='bold')

    # Panel c: Echo
    ax = axes[1, 0]
    im = ax.pcolormesh(K_mesh, sigma_mesh, echo,
                       cmap='viridis', shading='auto', vmin=0, vmax=1)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=r'$\rho_{S^*}(50)$')
    ax.contour(K_mesh, sigma_mesh, echo, levels=[0.5],
               colors='white', linewidths=1.5)
    ax.set_xlabel('$K$', fontsize=11)
    ax.set_ylabel(r'$\sigma$', fontsize=11)
    ax.set_title(r'(c) Angle-Resolved Echo', fontsize=12, fontweight='bold')

    # Panel d: Flow vectors
    ax = axes[1, 1]
    ax.pcolormesh(K_mesh, sigma_mesh, np.abs(S_star),
                  cmap='Greys', shading='auto', alpha=0.3)
    skip = 2
    K_sub = K_mesh[::skip, ::skip]
    sigma_sub = sigma_mesh[::skip, ::skip]
    da_sub = da[::skip, ::skip]
    dap_sub = dap[::skip, ::skip]
    mag = np.sqrt(da_sub**2 + dap_sub**2)
    mag[mag < 1e-6] = 1e-6
    Q = ax.quiver(K_sub, sigma_sub, da_sub/mag, dap_sub/mag,
                  mag, cmap='hot', scale=30, width=0.005)
    plt.colorbar(Q, ax=ax, fraction=0.046, pad=0.04, label=r'$|\partial\theta/\partial\sigma|$')
    ax.set_xlabel('$K$', fontsize=11)
    ax.set_ylabel(r'$\sigma$', fontsize=11)
    ax.set_title(r'(d) Angle Flow Field', fontsize=12, fontweight='bold')

    plt.suptitle('Figure 5: Angle-Resolved Observer Field',
                 fontsize=16, fontweight='bold', y=1.02)

    plt.tight_layout()

    output_png = OUTPUT_DIR / "Fig5_angle_resolved_field.png"
    output_pdf = OUTPUT_DIR / "Fig5_angle_resolved_field.pdf"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {output_png}")
    print(f"  Saved: {output_pdf}")
    plt.close()


def main():
    print("=" * 70)
    print("Paper 2 Figure 5: Angle-Resolved Observer Field")
    print("=" * 70)

    S_star = generate_fig5a_angle_geometry()
    chi = generate_fig5b_chi_angle()
    echo = generate_fig5c_echo_angle()
    flow = generate_fig5d_angle_flow()
    generate_fig5_combined()

    print("\n" + "=" * 70)
    print("Summary Statistics")
    print("=" * 70)
    print(f"|S*| range: [{S_star.min():.4f}, {S_star.max():.4f}]")
    print(f"χ_angle range: [{chi.min():.4f}, {chi.max():.4f}]")
    print(f"Echo_angle range: [{echo.min():.4f}, {echo.max():.4f}]")
    print("=" * 70)


if __name__ == "__main__":
    main()
