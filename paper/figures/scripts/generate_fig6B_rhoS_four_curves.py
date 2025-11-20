#!/usr/bin/env python3
"""
Figure 6B: Temporal Coherence - Four Representative Curves
===========================================================

Generates ρ_S(τ) decay curves for four representative noise levels
illustrating distinct dynamical regimes for main text Section 3.4.3:

- σ = 0.05 (low noise): High |S|, rapid decorrelation
- σ = 0.20 (ridge): Strong correlations, moderate persistence
- σ = 0.70 (non-monotonic): Reduced |S|, slowest decay
- σ = 1.00 (high noise): Collapsed |S| and ρ_S

Saves:
- fig6B_rhoS_four_curves.png
- fig6B_rhoS_four_curves.pdf
- data_fig6B_rhoS_four_curves.csv
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

def compute_rho_S_decay(K, sigma, delta_omega, angles, tau_max=200, n_seeds=30):
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

    # Four representative noise levels
    sigma_values = [0.05, 0.20, 0.70, 1.00]

    # Color and label mapping
    colors = {
        0.05: 'black',
        0.20: 'blue',
        0.70: 'red',
        1.00: 'gray'
    }

    labels = {
        0.05: 'Low noise (σ = 0.05)',
        0.20: 'Ridge (σ = 0.20)',
        0.70: 'Non-monotonic (σ = 0.70)',
        1.00: 'High noise (σ = 1.00)'
    }

    tau_max = 200
    n_seeds = 30

    print(f"Computing ρ_S(τ) for four representative curves")
    print(f"σ = {sigma_values}")
    print(f"K = {K}, Δω = {delta_omega}")
    print(f"Seeds: {n_seeds}, τ range: 0-{tau_max}")
    print()

    # Store results
    results = {}

    for sigma in sigma_values:
        print(f"Processing σ = {sigma:.2f}...", end='', flush=True)

        tau, rho_mean, rho_sem = compute_rho_S_decay(
            K, sigma, delta_omega, angles, tau_max, n_seeds
        )

        results[sigma] = {
            'tau': tau,
            'rho_mean': rho_mean,
            'rho_sem': rho_sem
        }

        # Compute half-life (τ_1/2 where ρ_S = 0.5)
        idx_half = np.where(rho_mean < 0.5)[0]
        if len(idx_half) > 0:
            tau_half = tau[idx_half[0]]
        else:
            tau_half = None

        print(f" ρ_S(0)={rho_mean[0]:.3f}, ρ_S(100)={rho_mean[100]:.3f}", end='')
        if tau_half is not None:
            print(f", τ_1/2≈{tau_half}")
        else:
            print(f", τ_1/2>200")

    # ============================================
    # Generate Figure 6B
    # ============================================

    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot four curves
    for sigma in sigma_values:
        tau = results[sigma]['tau']
        rho_mean = results[sigma]['rho_mean']
        rho_sem = results[sigma]['rho_sem']

        ax.plot(tau, rho_mean, linewidth=2.5, color=colors[sigma],
                label=labels[sigma], zorder=10)

        ax.fill_between(tau, rho_mean - rho_sem, rho_mean + rho_sem,
                        alpha=0.2, color=colors[sigma], zorder=5)

    # Reference line at ρ_S = 0.5
    ax.axhline(0.5, color='black', linestyle=':', linewidth=1, alpha=0.5,
               label='Half-decay ($\\rho_S = 0.5$)')

    # Labels and formatting
    ax.set_xlabel('Lag Time $\\tau$ (time units)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Temporal Coherence $\\rho_S(\\tau)$', fontsize=13, fontweight='bold')
    ax.set_title('Temporal Coherence Across Noise Regimes\n$K=0.7$, $\\Delta\\omega=0.2$',
                 fontsize=14, fontweight='bold', pad=15)

    # Grid and limits
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, tau_max)
    ax.set_ylim(-0.05, 1.05)

    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)

    # Annotation
    text = (
        f'Four representative noise levels\n'
        f'N = {n_seeds} seeds per curve\n'
        f'Shaded: ±1 SEM\n\n'
        f'Note: σ = 0.70 shows slowest decay\n'
        f'despite reduced instantaneous |S|'
    )
    ax.text(0.02, 0.45, text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    # Save
    output_dir = Path(__file__).parent.parent
    plt.savefig(output_dir / 'fig6B_rhoS_four_curves.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig6B_rhoS_four_curves.pdf', dpi=300, bbox_inches='tight')

    print(f"\n✓ Figure 6B saved: Four representative ρ_S(τ) curves")
    print(f"  σ = {sigma_values}")

    # ============================================
    # Export CSV
    # ============================================

    import csv
    csv_file = output_dir / 'data_fig6B_rhoS_four_curves.csv'

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

    print(f"✓ Data exported: data_fig6B_rhoS_four_curves.csv")
    print(f"\nFiles created:")
    print(f"  - fig6B_rhoS_four_curves.png")
    print(f"  - fig6B_rhoS_four_curves.pdf")
    print(f"  - data_fig6B_rhoS_four_curves.csv")


if __name__ == "__main__":
    main()
