#!/usr/bin/env python3
"""
Quick CHSH Verification Script
==============================

Verifies |S| ≈ 2.82 in coupled oscillators in under 5 seconds.

Usage:
    pip install numpy
    python quick_verify_chsh.py

What this shows:
    Two coupled Kuramoto oscillators with low noise exhibit CHSH correlations
    exceeding the classical bound of |S| = 2, reaching |S| ≈ 2.82.

    This is NOT quantum mechanics - it's classical phase-locked oscillators
    where the continuous measurement angles break the hidden-variable
    assumptions underlying Bell's theorem.

Reference:
    McRae, K. (2025). "Continuous-Angle CHSH Correlations in Noisy Coupled
    Oscillators: A Systematic Parameter-Space Study"

Repository: https://github.com/AkavartaStudio/RUT-CHSH-Landscape
"""

import numpy as np

# ============================================================================
# Core Simulation (self-contained, no external dependencies)
# ============================================================================

def simulate_coupled_oscillators(K, sigma, T=5000, dt=0.01, seed=None):
    """
    Simulate two Kuramoto-coupled oscillators with noise.

    Parameters:
        K     : Coupling strength (try 1.0)
        sigma : Noise level (try 0.1 for ridge, 1.0 for classical)
        T     : Number of time steps
        dt    : Time step size
        seed  : Random seed for reproducibility

    Returns:
        theta1, theta2 : Phase trajectories
    """
    if seed is not None:
        np.random.seed(seed)

    # Initialize phases randomly
    theta1 = np.zeros(T)
    theta2 = np.zeros(T)
    theta1[0] = np.random.uniform(0, 2*np.pi)
    theta2[0] = np.random.uniform(0, 2*np.pi)

    # Natural frequencies (identical for simplicity)
    omega1, omega2 = 1.0, 1.0

    # Euler-Maruyama integration
    for t in range(T - 1):
        # Kuramoto coupling: each oscillator pulls toward the other
        coupling1 = K * np.sin(theta2[t] - theta1[t])
        coupling2 = K * np.sin(theta1[t] - theta2[t])

        # Gaussian noise (Wiener process scaling)
        noise1 = np.random.normal(0, sigma * np.sqrt(dt))
        noise2 = np.random.normal(0, sigma * np.sqrt(dt))

        # Update phases
        theta1[t+1] = theta1[t] + dt * (omega1 + coupling1) + noise1
        theta2[t+1] = theta2[t] + dt * (omega2 + coupling2) + noise2

    return theta1, theta2


def compute_correlation(theta1, theta2, angle_a, angle_b):
    """
    Compute Bell-type correlation E(a,b).

    E(a,b) = <cos((theta1 + a) - (theta2 + b))>

    This is the correlation between "measurements" at angles a and b.
    """
    phase_diff = (theta1 + angle_a) - (theta2 + angle_b)
    return np.mean(np.cos(phase_diff))


def compute_chsh(theta1, theta2, angles_deg):
    """
    Compute the CHSH statistic S.

    S = E(a,b) - E(a,b') + E(a',b) + E(a',b')

    Classical bound: |S| <= 2
    Tsirelson bound: |S| <= 2√2 ≈ 2.828

    Parameters:
        theta1, theta2 : Phase trajectories
        angles_deg     : dict with 'a', 'a_prime', 'b', 'b_prime' in degrees

    Returns:
        S : CHSH statistic
        correlations : dict of individual E values
    """
    # Convert to radians
    a = np.deg2rad(angles_deg['a'])
    a_prime = np.deg2rad(angles_deg['a_prime'])
    b = np.deg2rad(angles_deg['b'])
    b_prime = np.deg2rad(angles_deg['b_prime'])

    # Compute four correlations
    E_ab = compute_correlation(theta1, theta2, a, b)
    E_ab_prime = compute_correlation(theta1, theta2, a, b_prime)
    E_a_prime_b = compute_correlation(theta1, theta2, a_prime, b)
    E_a_prime_b_prime = compute_correlation(theta1, theta2, a_prime, b_prime)

    # CHSH combination
    S = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime

    correlations = {
        'E(a,b)': E_ab,
        "E(a,b')": E_ab_prime,
        "E(a',b)": E_a_prime_b,
        "E(a',b')": E_a_prime_b_prime
    }

    return S, correlations


# ============================================================================
# Main Verification
# ============================================================================

def main():
    print("=" * 70)
    print("CHSH VERIFICATION: Classical Coupled Oscillators")
    print("=" * 70)
    print()
    print("Classical bound:  |S| <= 2")
    print("Tsirelson bound:  |S| <= 2.828...")
    print()

    # Optimal measurement angles (found via parameter sweep)
    # These maximize |S| for phase-locked oscillators
    angles = {
        'a': 0,
        'a_prime': 95,   # Δα ≈ 95°
        'b': 42,
        'b_prime': 126   # Δβ ≈ 84°
    }

    # Parameters
    K = 1.0       # Strong coupling (ensures phase lock)
    sigma = 0.1   # Low noise (on the "ridge")
    n_trials = 10 # Average over multiple runs

    print(f"Parameters: K={K}, σ={sigma}, {n_trials} trials")
    print(f"Angles: a={angles['a']}°, a'={angles['a_prime']}°, "
          f"b={angles['b']}°, b'={angles['b_prime']}°")
    print()
    print("-" * 70)

    # Run trials
    S_values = []
    for trial in range(n_trials):
        theta1, theta2 = simulate_coupled_oscillators(
            K=K, sigma=sigma, T=5000, dt=0.01, seed=42 + trial
        )

        # Discard transient (first 20%)
        transient = len(theta1) // 5
        theta1 = theta1[transient:]
        theta2 = theta2[transient:]

        S, correlations = compute_chsh(theta1, theta2, angles)
        S_values.append(S)

        if trial == 0:
            # Show detailed correlations for first trial
            print(f"\nTrial 1 correlations:")
            for name, val in correlations.items():
                print(f"  {name:12} = {val:+.4f}")
            print(f"  {'S':12} = {S:+.4f}")

    # Statistics
    S_mean = np.mean(S_values)
    S_std = np.std(S_values)
    S_sem = S_std / np.sqrt(n_trials)

    print()
    print("-" * 70)
    print(f"\nRESULTS ({n_trials} trials):")
    print(f"  |S| = {abs(S_mean):.3f} ± {S_sem:.3f}")
    print()

    # Verdict
    if abs(S_mean) > 2.0:
        violation = abs(S_mean) - 2.0
        print(f"  ✓ CLASSICAL BOUND VIOLATED by {violation:.3f}")
        print(f"  ✓ This is {abs(S_mean)/2.828*100:.1f}% of Tsirelson bound")
    else:
        print(f"  ✗ No violation (try lower sigma)")

    print()
    print("=" * 70)
    print("This is NOT quantum mechanics.")
    print("It's classical phase-locked oscillators with continuous angles.")
    print("=" * 70)

    # Also show what happens with high noise (classical regime)
    print()
    print("\nComparison: High noise (σ=1.0) - should NOT violate:")
    print("-" * 70)

    S_classical = []
    for trial in range(n_trials):
        theta1, theta2 = simulate_coupled_oscillators(
            K=K, sigma=1.0, T=5000, dt=0.01, seed=42 + trial
        )
        transient = len(theta1) // 5
        S, _ = compute_chsh(theta1[transient:], theta2[transient:], angles)
        S_classical.append(S)

    S_mean_classical = np.mean(S_classical)
    S_sem_classical = np.std(S_classical) / np.sqrt(n_trials)

    print(f"  |S| = {abs(S_mean_classical):.3f} ± {S_sem_classical:.3f}")
    if abs(S_mean_classical) <= 2.0:
        print(f"  ✓ No violation (as expected for high noise)")
    print()


if __name__ == "__main__":
    main()
