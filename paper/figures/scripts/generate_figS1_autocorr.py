#!/usr/bin/env python3
"""
Generate Figure S1: ρ_S(τ) Autocorrelation Decay Curves

Three-panel figure showing temporal memory across regimes:
- σ = 0.2 (high |S| regime)
- σ = 0.7 (transition regime with non-monotonicity)
- σ = 1.0 (collapsed |S| regime)

Uses same simulation settings as Fig. 6 (K=0.7, Δω=0.2, optimized angles).
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add analysis scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "analysis" / "scripts"))

from rut_core import kuramoto_with_noise, compute_bell_correlation

# Simulation parameters (matching Fig. 6)
K = 0.7
delta_omega = 0.2
dt = 0.01
T_steps = 20000
transient_steps = 10000
n_seeds = 30

# Noise levels to test
sigma_values = [0.2, 0.7, 1.0]

# Optimized angles from Fig. 4 (in degrees)
angles = {
    'a': 0.0,
    'a_prime': 98.0,
    'b': 45.0,
    'b_prime': 127.0
}

# Convert to radians
a = np.deg2rad(angles['a'])
a_prime = np.deg2rad(angles['a_prime'])
b = np.deg2rad(angles['b'])
b_prime = np.deg2rad(angles['b_prime'])

# Autocorrelation parameters
max_lag = 200
tau_range = np.arange(0, max_lag + 1)

print(f"Computing ρ_S(τ) for σ = {sigma_values}")
print(f"K = {K}, Δω = {delta_omega}")
print(f"Seeds: {n_seeds}, τ range: 0-{max_lag}")
print()

# Storage for results
results = {}

for sigma in sigma_values:
    print(f"Processing σ = {sigma}...")

    rho_S_all_seeds = []

    for seed in range(n_seeds):
        # Run simulation
        theta1, theta2 = kuramoto_with_noise(
            theta1_0=0.0,
            theta2_0=0.0,
            omega1=1.0,
            omega2=1.0 + delta_omega,
            K=K,
            sigma=sigma,
            T=T_steps + transient_steps,
            dt=dt,
            seed=seed
        )

        # Trim transient
        theta1 = theta1[transient_steps:]
        theta2 = theta2[transient_steps:]

        # Compute instantaneous CHSH time series
        S_timeseries = []

        for t in range(len(theta1)):
            # Four correlators at each timestep
            E_ab = np.cos((theta1[t] + a) - (theta2[t] + b))
            E_ab_prime = np.cos((theta1[t] + a) - (theta2[t] + b_prime))
            E_a_prime_b = np.cos((theta1[t] + a_prime) - (theta2[t] + b))
            E_a_prime_b_prime = np.cos((theta1[t] + a_prime) - (theta2[t] + b_prime))

            S = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime
            S_timeseries.append(S)

        S_timeseries = np.array(S_timeseries)

        # Compute autocorrelation
        S_mean = np.mean(S_timeseries)
        S_std = np.std(S_timeseries)

        if S_std < 1e-10:  # Handle edge case
            rho_S_seed = np.ones(len(tau_range))
        else:
            S_centered = S_timeseries - S_mean

            rho_S_seed = []
            for tau in tau_range:
                if tau == 0:
                    rho_tau = 1.0
                else:
                    # Autocorrelation at lag tau
                    rho_tau = np.mean(S_centered[:-tau] * S_centered[tau:]) / (S_std**2)
                rho_S_seed.append(rho_tau)

        rho_S_all_seeds.append(rho_S_seed)

        if (seed + 1) % 10 == 0:
            print(f"  Completed {seed + 1}/{n_seeds} seeds")

    # Convert to array and compute statistics
    rho_S_all_seeds = np.array(rho_S_all_seeds)
    rho_S_mean = np.mean(rho_S_all_seeds, axis=0)
    rho_S_sem = np.std(rho_S_all_seeds, axis=0) / np.sqrt(n_seeds)

    results[sigma] = {
        'mean': rho_S_mean,
        'sem': rho_S_sem
    }

    print(f"  ρ_S(0) = {rho_S_mean[0]:.3f}")
    print(f"  ρ_S(100) = {rho_S_mean[100]:.3f}")
    print()

# Create three-panel figure
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

colors = ['#06A77D', '#F77F00', '#E63946']  # Same as Fig. 6

for idx, sigma in enumerate(sigma_values):
    ax = axes[idx]

    mean = results[sigma]['mean']
    sem = results[sigma]['sem']

    # Plot mean line
    ax.plot(tau_range, mean, linewidth=2.5, color=colors[idx],
           label=f'$\\sigma = {sigma}$')

    # Add SEM shading
    ax.fill_between(tau_range, mean - sem, mean + sem,
                   alpha=0.2, color=colors[idx])

    # Styling
    ax.set_xlabel('Time lag $\\tau$', fontsize=12, fontweight='bold')
    ax.xaxis.labelpad = 10

    if idx == 0:
        ax.set_ylabel('Autocorrelation $\\rho_S(\\tau)$',
                     fontsize=12, fontweight='bold')
        ax.yaxis.labelpad = 10

    ax.set_title(f'$\\sigma = {sigma}$', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.set_xlim(0, max_lag)
    ax.set_ylim(-0.1, 1.05)

    # Add horizontal line at 0
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Overall title
fig.suptitle('Autocorrelation of CHSH Signal Across Noise Regimes',
            fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout()

# Save figure
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'figS1_autocorr.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'figS1_autocorr.png', dpi=300, bbox_inches='tight')

print("✓ Figure S1 saved: Autocorrelation decay curves")
print(f"  Three panels: σ = {sigma_values}")
print(f"  Tau range: 0 to {max_lag}")

# Export CSV data
csv_path = output_dir / 'data_rhoS_tau.csv'
with open(csv_path, 'w') as f:
    f.write('tau,rhoS_sigma0.2,rhoS_sigma0.7,rhoS_sigma1.0\n')
    for i, tau in enumerate(tau_range):
        f.write(f'{tau},{results[0.2]["mean"][i]:.6f},'
               f'{results[0.7]["mean"][i]:.6f},'
               f'{results[1.0]["mean"][i]:.6f}\n')

print(f"✓ Data exported: {csv_path}")
print(f"  CSV contains mean ρ_S(τ) for all three σ values")
