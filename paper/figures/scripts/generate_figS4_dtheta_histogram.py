#!/usr/bin/env python3
"""
Δθ Distribution Histogram for Appendix B
=========================================

Generates histogram of phase difference Δθ at ridge point (K=0.7, σ=0.2)
to visualize the asymmetric distribution that causes optimal angle shifts.

Computes:
- ⟨cos Δθ⟩ ≈ 0.44
- ⟨sin Δθ⟩ = ε ≈ 0.037 (asymmetry parameter)

Saves: figS4_dtheta_histogram.png
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add rut_core to path
SCRIPT_DIR = Path(__file__).resolve().parent
# Go up: scripts -> figures -> paper -> root -> analysis/scripts
RUT_CORE_PATH = SCRIPT_DIR.parent.parent.parent / 'analysis' / 'scripts'
sys.path.insert(0, str(RUT_CORE_PATH))

from rut_core import kuramoto_with_noise

def extract_dtheta_distribution(K, sigma, delta_omega, n_seeds=30):
    """
    Run simulation and extract Δθ time series

    Returns:
        dtheta_all: concatenated Δθ values from all seeds (post-transient)
        cos_dtheta_mean: ⟨cos Δθ⟩
        sin_dtheta_mean: ⟨sin Δθ⟩ = ε
    """

    T = 100000
    dt = 0.01
    transient = 20000
    omega1 = 1.0
    omega2 = omega1 + delta_omega

    dtheta_all = []
    cos_dtheta_vals = []
    sin_dtheta_vals = []

    print(f"Running {n_seeds} seeds to extract Δθ distribution...")
    print(f"Parameters: K={K}, σ={sigma}, Δω={delta_omega}")

    for seed in range(1, n_seeds + 1):
        if seed % 10 == 0:
            print(f"  Completed {seed}/{n_seeds} seeds")

        # Run simulation
        theta1, theta2 = kuramoto_with_noise(
            theta1_0=np.random.uniform(0, 2*np.pi),
            theta2_0=np.random.uniform(0, 2*np.pi),
            omega1=omega1,
            omega2=omega2,
            K=K,
            sigma=sigma,
            T=T,
            dt=dt,
            seed=seed
        )

        # Extract post-transient Δθ
        dtheta = theta2[transient:] - theta1[transient:]
        dtheta_all.extend(dtheta)

        # Compute statistics for this seed
        cos_dtheta_vals.append(np.mean(np.cos(dtheta)))
        sin_dtheta_vals.append(np.mean(np.sin(dtheta)))

    dtheta_all = np.array(dtheta_all)

    # Overall statistics
    cos_dtheta_mean = np.mean(cos_dtheta_vals)
    sin_dtheta_mean = np.mean(sin_dtheta_vals)

    cos_dtheta_sem = np.std(cos_dtheta_vals, ddof=1) / np.sqrt(n_seeds)
    sin_dtheta_sem = np.std(sin_dtheta_vals, ddof=1) / np.sqrt(n_seeds)

    print(f"\n{'='*60}")
    print(f"Δθ Distribution Statistics")
    print(f"{'='*60}")
    print(f"⟨cos Δθ⟩ = {cos_dtheta_mean:.4f} ± {cos_dtheta_sem:.4f}")
    print(f"⟨sin Δθ⟩ = ε = {sin_dtheta_mean:.4f} ± {sin_dtheta_sem:.4f}")
    print(f"Total samples: {len(dtheta_all):,}")
    print(f"{'='*60}\n")

    return dtheta_all, cos_dtheta_mean, sin_dtheta_mean, cos_dtheta_sem, sin_dtheta_sem


def main():
    # Ridge regime parameters
    K = 0.7
    sigma = 0.2
    delta_omega = 0.2  # Using original Δω=0.2 for consistency with Appendix B
    n_seeds = 30

    # Extract distribution
    dtheta_all, cos_mean, sin_mean, cos_sem, sin_sem = extract_dtheta_distribution(
        K, sigma, delta_omega, n_seeds
    )

    # ============================================
    # Generate Histogram Figure
    # ============================================

    fig, ax = plt.subplots(figsize=(10, 7))

    # Histogram
    counts, bins, patches = ax.hist(
        dtheta_all,
        bins=100,
        density=True,
        alpha=0.7,
        color='steelblue',
        edgecolor='darkblue',
        linewidth=0.5,
        label='Empirical distribution'
    )

    # Add vertical line at mean
    mean_dtheta = np.mean(dtheta_all)
    ax.axvline(mean_dtheta, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_dtheta:.3f} rad')

    # Add vertical line at zero for reference
    ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.3,
               label='Perfect locking (Δθ = 0)')

    # Labels and title
    ax.set_xlabel('Phase Difference $\\Delta\\theta$ (radians)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=13, fontweight='bold')
    ax.set_title('Phase Difference Distribution at Ridge Point\n$K=0.7$, $\\sigma=0.2$, $\\Delta\\omega=0.2$',
                 fontsize=14, fontweight='bold', pad=15)

    # Add text box with statistics
    stats_text = (
        f'Ridge Regime Statistics:\n'
        f'$\\langle \\cos \\Delta\\theta \\rangle = {cos_mean:.3f} \\pm {cos_sem:.3f}$\n'
        f'$\\langle \\sin \\Delta\\theta \\rangle = \\varepsilon = {sin_mean:.3f} \\pm {sin_sem:.3f}$\n'
        f'Seeds: {n_seeds}, Samples: {len(dtheta_all):,}'
    )
    ax.text(0.98, 0.97, stats_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95)

    plt.tight_layout()

    # Save
    output_dir = Path(__file__).parent.parent
    output_file = output_dir / 'figS4_dtheta_histogram.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figS4_dtheta_histogram.pdf', dpi=300, bbox_inches='tight')

    print(f"✓ Figure saved: {output_file.name}")

    # Also save the raw statistics to a file for reference
    stats_file = output_dir / 'dtheta_statistics.txt'
    with open(stats_file, 'w') as f:
        f.write(f"Δθ Distribution Statistics\n")
        f.write(f"Ridge Regime: K={K}, σ={sigma}, Δω={delta_omega}\n")
        f.write(f"Seeds: {n_seeds}\n")
        f.write(f"Total samples: {len(dtheta_all):,}\n\n")
        f.write(f"⟨cos Δθ⟩ = {cos_mean:.6f} ± {cos_sem:.6f}\n")
        f.write(f"⟨sin Δθ⟩ = ε = {sin_mean:.6f} ± {sin_sem:.6f}\n")
        f.write(f"Mean Δθ = {mean_dtheta:.6f} rad\n")

    print(f"✓ Statistics saved: {stats_file.name}")
    print(f"\nFiles created:")
    print(f"  - figS4_dtheta_histogram.png")
    print(f"  - figS4_dtheta_histogram.pdf")
    print(f"  - dtheta_statistics.txt")


if __name__ == "__main__":
    main()
