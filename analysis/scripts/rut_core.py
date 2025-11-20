#!/usr/bin/env python3
"""
RUT CHSH Core Simulation Module
Extracted from run_experiment.py for reproducibility framework
"""

import numpy as np

def kuramoto_with_noise(theta1_0, theta2_0, omega1, omega2, K, sigma, T, dt, seed=None, K_modulation=None):
    """
    Kuramoto coupling with optional noise and time-varying coupling

    Parameters:
    -----------
    theta1_0, theta2_0 : float
        Initial phases
    omega1, omega2 : float
        Natural frequencies
    K : float or callable
        Coupling strength (constant or function of time)
    sigma : float
        Noise strength
    T : int
        Number of time steps
    dt : float
        Time step
    seed : int, optional
        Random seed for reproducibility
    K_modulation : dict, optional
        If provided: {'amplitude': A, 'frequency': omega} for K(t) = K + A*sin(omega*t)

    Returns:
    --------
    theta1, theta2 : arrays
        Phase trajectories
    """
    if seed is not None:
        np.random.seed(seed)

    theta1 = np.zeros(T)
    theta2 = np.zeros(T)
    theta1[0] = theta1_0
    theta2[0] = theta2_0

    for t in range(T - 1):
        # Time-varying coupling if specified
        if K_modulation is not None:
            K_t = K + K_modulation['amplitude'] * np.sin(K_modulation['frequency'] * t * dt)
        else:
            K_t = K

        # Kuramoto coupling
        coupling1 = K_t * np.sin(theta2[t] - theta1[t])
        coupling2 = K_t * np.sin(theta1[t] - theta2[t])

        # Gaussian noise with proper √dt scaling (Wiener process)
        eta1 = np.random.normal(0, sigma * np.sqrt(dt))
        eta2 = np.random.normal(0, sigma * np.sqrt(dt))

        # Update: deterministic part (×dt) + stochastic part (already scaled)
        theta1[t+1] = theta1[t] + dt * (omega1 + coupling1) + eta1
        theta2[t+1] = theta2[t] + dt * (omega2 + coupling2) + eta2

    return theta1, theta2


def compute_pli(theta1, theta2, transient=0):
    """Compute Phase Lock Index"""
    delta = theta2[transient:] - theta1[transient:]
    pli = np.abs(np.mean(np.exp(1j * delta)))
    return pli


def compute_echo_density(theta1, theta2, transient=0, lambda_decay=0.9):
    """Compute cross-echo density (simplified version)"""
    # Echo signals via exponential smoothing
    T = len(theta1)
    E_A = np.zeros(T, dtype=complex)
    E_B = np.zeros(T, dtype=complex)

    for t in range(1, T):
        dtheta1 = theta1[t] - theta1[t-1]
        dtheta2 = theta2[t] - theta2[t-1]

        E_A[t] = lambda_decay * E_A[t-1] + (1 - lambda_decay) * np.exp(1j * dtheta1)
        E_B[t] = lambda_decay * E_B[t-1] + (1 - lambda_decay) * np.exp(1j * dtheta2)

    # Cross-echo density
    rho_echo = np.abs(np.mean(E_A[transient:] * np.conj(E_B[transient:])))
    return rho_echo


def compute_bell_correlation(theta_A, theta_B, angle_a, angle_b):
    """
    Compute Bell-type correlation E(a,b) between two oscillators.

    E(a,b) = ⟨cos((θ^A + a) - (θ^B + b))⟩
           = ⟨cos(Δθ + (a - b))⟩

    This is the CORRECT formula for coupled oscillators.
    """
    # Apply measurement offsets
    measured_A = theta_A + angle_a
    measured_B = theta_B + angle_b

    # Compute correlation
    phase_diff = measured_A - measured_B
    correlation = np.mean(np.cos(phase_diff))

    return float(correlation)


def compute_chsh_correlations(theta1, theta2, angles, transient=0):
    """
    Compute CHSH correlations E(a,b) for given measurement angles

    Parameters:
    -----------
    theta1, theta2 : arrays
        Phase trajectories
    angles : dict
        {'a': angle_a, 'a_prime': angle_a_prime, 'b': angle_b, 'b_prime': angle_b_prime}
        Angles in degrees
    transient : int
        Discard first N timesteps

    Returns:
    --------
    correlations : dict
        {'E_ab': ..., 'E_ab_prime': ..., 'E_a_prime_b': ..., 'E_a_prime_b_prime': ...}
    S : float
        CHSH statistic
    """
    # Convert angles to radians
    a = np.deg2rad(angles['a'])
    a_prime = np.deg2rad(angles['a_prime'])
    b = np.deg2rad(angles['b'])
    b_prime = np.deg2rad(angles['b_prime'])

    # Trim transient
    th1 = theta1[transient:]
    th2 = theta2[transient:]

    # Compute correlations using CORRECT formula
    E_ab = compute_bell_correlation(th1, th2, a, b)
    E_ab_prime = compute_bell_correlation(th1, th2, a, b_prime)
    E_a_prime_b = compute_bell_correlation(th1, th2, a_prime, b)
    E_a_prime_b_prime = compute_bell_correlation(th1, th2, a_prime, b_prime)

    # CHSH statistic
    S = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime

    correlations = {
        'E_ab': E_ab,
        'E_ab_prime': E_ab_prime,
        'E_a_prime_b': E_a_prime_b,
        'E_a_prime_b_prime': E_a_prime_b_prime
    }

    return correlations, S


def run_single_experiment(params, seed=None):
    """
    Run a single experiment with given parameters

    Parameters:
    -----------
    params : dict
        Experiment parameters including:
        - K: coupling strength
        - delta_omega: frequency mismatch
        - sigma: noise level
        - angles: measurement angles dict
        - T: time steps
        - dt: time step
        - transient: transient cutoff
        - K_modulation: optional time-varying coupling
    seed : int, optional
        Random seed

    Returns:
    --------
    results : dict
        Complete experimental results
    """
    # Extract parameters
    K = params['K']
    delta_omega = params['delta_omega']
    sigma = params['sigma']
    angles = params['angles']
    T = params['T']
    dt = params['dt']
    transient = params['transient']
    K_mod = params.get('K_modulation', None)

    # Set frequencies
    omega1 = 1.0
    omega2 = omega1 + delta_omega

    # Random initial conditions
    if seed is not None:
        np.random.seed(seed)
    theta1_0 = np.random.uniform(0, 2*np.pi)
    theta2_0 = np.random.uniform(0, 2*np.pi)

    # Run simulation
    theta1, theta2 = kuramoto_with_noise(
        theta1_0, theta2_0, omega1, omega2, K, sigma, T, dt,
        seed=seed, K_modulation=K_mod
    )

    # Compute metrics
    pli = compute_pli(theta1, theta2, transient)
    rho_echo = compute_echo_density(theta1, theta2, transient)
    correlations, S = compute_chsh_correlations(theta1, theta2, angles, transient)

    # Package results
    results = {
        'seed': seed,
        'parameters': params.copy(),
        'PLI': pli,
        'rho_echo': rho_echo,
        'S': S,
        'abs_S': abs(S),
        'correlations': correlations,
        'violation': abs(S) > 2.0,
        'regime': classify_regime(pli, abs(S))
    }

    return results


def classify_regime(pli, abs_S):
    """Classify into Tsirelson ridge, RUT plateau, or classical"""
    if abs_S <= 2.0:
        return 'classical'
    elif pli >= 0.98 and abs_S >= 2.6:
        return 'tsirelson_ridge'
    elif pli >= 0.94:
        return 'rut_plateau'
    else:
        return 'intermediate'
