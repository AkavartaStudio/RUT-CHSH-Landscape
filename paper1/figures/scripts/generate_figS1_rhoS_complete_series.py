#!/usr/bin/env python3
"""
Figure S1: Complete Temporal Coherence Decay Series
===================================================

Generates complete ρ_S(τ) decay curves across noise range σ ∈ [0.05, 1.0]
in increments of Δσ = 0.05, showing all 20 curves.

Highlights four representative curves (σ = 0.05, 0.20, 0.70, 1.00) that
appear in main text Fig 6B.

Saves:
- figS1_rhoS_complete_series.png
- figS1_rhoS_complete_series.pdf
- data_rhoS_complete_series.csv
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add rut_core to path
SCRIPT_DIR = Path(__file__).resolve().parent
RUT_CORE_PATH = SCRIPT_DIR.parent.parent.parent / 'analysis' / 'scripts'
sys.path.insert(0, str(RUT_CORE_PATH))
from rut_core import kuramoto_with_noise

def compute_rho_S_decay(K, sigma, delta_omega, angles, tau_max=200, n_seeds=10):
    """
    Compute ρ_S(τ) autocorrelation decay curve

    Returns:
        tau_values: lag times
        rho_S_mean: mean autocorrelation
        rho_S_sem: standard error
    """
    T = 100000
    dt = 0.01
    transient = 20000
    omega1 = 1.0
    omega2 = omega1 + delta_omega

    tau_steps = np.arange(0, tau_max + 1, 1)  # Every 1 time unit
    rho_S_all = []

    for seed in range(1, n_seeds + 1):
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

        # Compute S(t) time series manually
        # Extract post-transient data
        theta1_post = theta1[transient:]
        theta2_post = theta2[transient:]

        # Compute instantaneous correlations
        a = np.deg2rad(angles['a'])
        a_prime = np.deg2rad(angles['a_prime'])
        b = np.deg2rad(angles['b'])
        b_prime = np.deg2rad(angles['b_prime'])

        # E(a,b) = <cos(Δθ + (a-b))>
        E_ab_t = np.cos(theta2_post - theta1_post + (a - b))
        E_ab_prime_t = np.cos(theta2_post - theta1_post + (a - b_prime))
        E_a_prime_b_t = np.cos(theta2_post - theta1_post + (a_prime - b))
        E_a_prime_b_prime_t = np.cos(theta2_post - theta1_post + (a_prime - b_prime))

        # S(t) = E(a,b) - E(a,b') + E(a',b) + E(a',b')
        S_series = E_ab_t - E_ab_prime_t + E_a_prime_b_t + E_a_prime_b_prime_t

        # Compute autocorrelation for each lag
        rho_S_seed = []
        for tau in tau_steps:
            if tau == 0:
                rho_S_seed.append(1.0)
            else:
                # Autocorrelation: Corr[S(t), S(t+tau)]
                S_t = S_series[:-tau]
                S_t_tau = S_series[tau:]

                # Pearson correlation
                corr = np.corrcoef(S_t, S_t_tau)[0, 1]
                rho_S_seed.append(corr)

        rho_S_all.append(rho_S_seed)

    # Statistics
    rho_S_all = np.array(rho_S_all)
    rho_S_mean = np.mean(rho_S_all, axis=0)
    rho_S_sem = np.std(rho_S_all, axis=0, ddof=1) / np.sqrt(n_seeds)

    return tau_steps, rho_S_mean, rho_S_sem


def main():
    # Parameters
    K = 0.7
    delta_omega = 0.2
    angles = {'a': 0.0, 'a_prime': 95.0, 'b': 45.0, 'b_prime': 129.0}

    # Sigma range: 0.05 to 1.0 in 0.05 increments
    sigma_values = np.arange(0.05, 1.05, 0.05)

    # Representative curves for Fig 6B
    sigma_highlight = [0.05, 0.20, 0.70, 1.00]

    tau_max = 200
    n_seeds = 10

    print(f"Computing ρ_S(τ) for {len(sigma_values)} σ values")
    print(f"σ range: [{sigma_values[0]:.2f}, {sigma_values[-1]:.2f}]")
    print(f"K = {K}, Δω = {delta_omega}")
    print(f"Seeds: {n_seeds}, τ range: 0-{tau_max}")
    print()

    # Store results
    results = {}

    for i, sigma in enumerate(sigma_values, 1):
        print(f"[{i}/{len(sigma_values)}] Processing σ = {sigma:.2f}...", end='', flush=True)

        tau, rho_mean, rho_sem = compute_rho_S_decay(
            K, sigma, delta_omega, angles, tau_max, n_seeds
        )

        results[sigma] = {
            'tau': tau,
            'rho_mean': rho_mean,
            'rho_sem': rho_sem
        }

        print(f" ρ_S(0)={rho_mean[0]:.3f}, ρ_S(100)={rho_mean[100]:.3f}")

    # ============================================
    # Generate Figure S1
    # ============================================

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot all curves
    for sigma in sigma_values:
        tau = results[sigma]['tau']
        rho_mean = results[sigma]['rho_mean']
        rho_sem = results[sigma]['rho_sem']

        # Highlight special curves
        if sigma in sigma_highlight:
            linewidth = 2.5
            alpha = 1.0
            zorder = 10

            # Color mapping
            color_map = {
                0.05: 'black',
                0.20: 'blue',
                0.70: 'red',
                1.00: 'gray'
            }
            color = color_map[sigma]
            label = f'σ = {sigma:.2f}'
        else:
            linewidth = 1.0
            alpha = 0.3
            color = 'steelblue'
            zorder = 1
            label = None

        ax.plot(tau, rho_mean, linewidth=linewidth, alpha=alpha,
                color=color, zorder=zorder, label=label)

        # Shaded error for highlighted curves only
        if sigma in sigma_highlight:
            ax.fill_between(tau, rho_mean - rho_sem, rho_mean + rho_sem,
                           alpha=0.2, color=color, zorder=zorder-1)

    # Labels and formatting
    ax.set_xlabel('Lag Time $\\tau$ (time units)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Temporal Coherence $\\rho_S(\\tau)$', fontsize=14, fontweight='bold')
    ax.set_title('Complete Temporal Coherence Decay Series\n$K=0.7$, $\\Delta\\omega=0.2$',
                 fontsize=15, fontweight='bold', pad=15)

    # Grid and limits
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, tau_max)
    ax.set_ylim(-0.1, 1.1)

    # Legend
    ax.legend(loc='upper right', fontsize=12, framealpha=0.95,
              title='Representative curves\n(highlighted in Fig 6B)')

    # Annotation
    text = (
        f'Complete series: σ ∈ [0.05, 1.0], Δσ = 0.05\n'
        f'N = {n_seeds} seeds per curve\n'
        f'Shaded regions: ±1 SEM (highlighted curves only)'
    )
    ax.text(0.02, 0.02, text, transform=ax.transAxes,
            fontsize=10, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    # Save
    output_dir = Path(__file__).parent.parent
    plt.savefig(output_dir / 'figS1_rhoS_complete_series.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figS1_rhoS_complete_series.pdf', dpi=300, bbox_inches='tight')

    print(f"\n✓ Figure S1 saved: Complete ρ_S(τ) series")
    print(f"  {len(sigma_values)} curves: σ ∈ [0.05, 1.0]")
    print(f"  Four highlighted: σ = {sigma_highlight}")

    # ============================================
    # Export CSV
    # ============================================

    import csv
    csv_file = output_dir / 'data_rhoS_complete_series.csv'

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        header = ['tau'] + [f'sigma_{s:.2f}_mean' for s in sigma_values] + \
                           [f'sigma_{s:.2f}_sem' for s in sigma_values]
        writer.writerow(header)

        # Data rows
        for i, t in enumerate(tau):
            row = [t]
            # Means
            for sigma in sigma_values:
                row.append(f"{results[sigma]['rho_mean'][i]:.6f}")
            # SEMs
            for sigma in sigma_values:
                row.append(f"{results[sigma]['rho_sem'][i]:.6f}")
            writer.writerow(row)

    print(f"✓ Data exported: data_rhoS_complete_series.csv")
    print(f"  Columns: tau + {len(sigma_values)} mean + {len(sigma_values)} SEM")
    print(f"\nFiles created:")
    print(f"  - figS1_rhoS_complete_series.png")
    print(f"  - figS1_rhoS_complete_series.pdf")
    print(f"  - data_rhoS_complete_series.csv")


if __name__ == "__main__":
    main()
