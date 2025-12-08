#!/usr/bin/env python3
"""
E231: Angle-Resolved CHSH Field Scan
Paper 2, Mission 4

Find optimal CHSH angles across (K, σ) grid and compute:
- S*(K, σ) = max_angles S(a, a', b, b')
- Optimal angle geometry: a*, a'*, b*, b'*
- χ_angle = ∂S*/∂σ (angle-resolved susceptibility)
- Echo_angle = ρ_{S*}(τ=50) (memory at optimal angles)
- Angle flow vectors (how optimal angles shift with noise)

Uses two-stage optimization:
1. Coarse grid search (30° steps) to find approximate maximum
2. Local refinement (6° steps) around the coarse optimum
"""

import numpy as np
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from itertools import product

# Ensure unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# ============================================================================
# PARAMETERS
# ============================================================================

# Grid parameters
K_VALUES = np.linspace(0.10, 1.00, 19)
SIGMA_VALUES = np.linspace(0.0, 0.40, 21)
SEEDS_PER_POINT = 3

# Angle parameters (degrees)
# Per Chase: 15° coarse (13^4 = 28561 combos), then refine top-N candidates
ANGLE_COARSE = np.arange(0, 181, 15)  # 13 values for coarse search
ANGLE_FINE = np.arange(-6, 7, 3)       # ±6° refinement in 3° steps
TOP_N_CANDIDATES = 10                   # Keep top N from coarse for refinement

# Lag values for echo computation
TAU_LAGS = [0, 25, 50]

# Simulation parameters
T_STEPS = 600000
DT = 0.01
TRANSIENT = 300000
SAMPLE_INTERVAL = 100
DELTA_OMEGA = 0.1

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "analysis" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# SIMULATION CORE
# ============================================================================

def run_oscillator_simulation(K, sigma, seed, return_phases=True):
    """
    Run two coupled Kuramoto oscillators.
    Returns sampled phases after transient.
    """
    np.random.seed(seed)

    # Initialize phases
    theta1 = np.random.uniform(0, 2*np.pi)
    theta2 = np.random.uniform(0, 2*np.pi)

    omega1 = 1.0
    omega2 = 1.0 + DELTA_OMEGA

    # Storage for sampled phases
    n_samples = (T_STEPS - TRANSIENT) // SAMPLE_INTERVAL
    phases1 = np.zeros(n_samples)
    phases2 = np.zeros(n_samples)
    sample_idx = 0

    sqrt_dt = np.sqrt(DT)

    for t in range(T_STEPS):
        # Kuramoto dynamics
        coupling1 = K * np.sin(theta2 - theta1)
        coupling2 = K * np.sin(theta1 - theta2)

        # Noise
        if sigma > 0:
            noise1 = sigma * np.random.randn() * sqrt_dt
            noise2 = sigma * np.random.randn() * sqrt_dt
        else:
            noise1 = noise2 = 0

        # Update
        theta1 += (omega1 + coupling1) * DT + noise1
        theta2 += (omega2 + coupling2) * DT + noise2

        # Sample after transient
        if t >= TRANSIENT and (t - TRANSIENT) % SAMPLE_INTERVAL == 0:
            phases1[sample_idx] = theta1
            phases2[sample_idx] = theta2
            sample_idx += 1

    return phases1, phases2


def compute_E_correlation(phases1, phases2, angle1_deg, angle2_deg):
    """
    Compute E(a,b) correlation for given measurement angles.
    E = <cos(θ1 - a)cos(θ2 - b) + sin(θ1 - a)sin(θ2 - b)>
      = <cos((θ1 - a) - (θ2 - b))>
      = <cos(θ1 - θ2 - (a - b))>
    """
    a_rad = np.deg2rad(angle1_deg)
    b_rad = np.deg2rad(angle2_deg)

    # Phase difference relative to measurement angles
    delta = (phases1 - a_rad) - (phases2 - b_rad)

    return np.mean(np.cos(delta))


def compute_CHSH(phases1, phases2, a, ap, b, bp):
    """
    Compute CHSH functional S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    All angles in degrees.
    """
    E_ab = compute_E_correlation(phases1, phases2, a, b)
    E_abp = compute_E_correlation(phases1, phases2, a, bp)
    E_apb = compute_E_correlation(phases1, phases2, ap, b)
    E_apbp = compute_E_correlation(phases1, phases2, ap, bp)

    S = E_ab - E_abp + E_apb + E_apbp
    return S


def compute_S_timeseries(phases1, phases2, a, ap, b, bp, window=100):
    """
    Compute instantaneous CHSH values for autocorrelation.
    Uses rolling window for smoothing.
    """
    n = len(phases1)
    n_windows = n - window + 1
    S_series = np.zeros(n_windows)

    a_rad = np.deg2rad(a)
    ap_rad = np.deg2rad(ap)
    b_rad = np.deg2rad(b)
    bp_rad = np.deg2rad(bp)

    for i in range(n_windows):
        p1 = phases1[i:i+window]
        p2 = phases2[i:i+window]

        E_ab = np.mean(np.cos((p1 - a_rad) - (p2 - b_rad)))
        E_abp = np.mean(np.cos((p1 - a_rad) - (p2 - bp_rad)))
        E_apb = np.mean(np.cos((p1 - ap_rad) - (p2 - b_rad)))
        E_apbp = np.mean(np.cos((p1 - ap_rad) - (p2 - bp_rad)))

        S_series[i] = E_ab - E_abp + E_apb + E_apbp

    return S_series


def compute_echo(S_series, tau_lag):
    """Compute autocorrelation at given lag."""
    if tau_lag == 0:
        return 1.0
    if tau_lag >= len(S_series):
        return 0.0

    S_mean = np.mean(S_series)
    S_var = np.var(S_series)

    if S_var < 1e-12:
        return 1.0

    S_shifted = S_series[tau_lag:]
    S_base = S_series[:-tau_lag]

    cov = np.mean((S_base - S_mean) * (S_shifted - S_mean))
    return cov / S_var


# ============================================================================
# ANGLE OPTIMIZATION
# ============================================================================

def find_optimal_angles_coarse(phases1, phases2):
    """
    Coarse grid search over angles to find top-N candidates.
    Returns list of (angles, S) tuples sorted by |S|.
    """
    candidates = []

    for a in ANGLE_COARSE:
        for ap in ANGLE_COARSE:
            for b in ANGLE_COARSE:
                for bp in ANGLE_COARSE:
                    S = compute_CHSH(phases1, phases2, a, ap, b, bp)
                    candidates.append(((a, ap, b, bp), S))

    # Sort by |S| descending, keep top N
    candidates.sort(key=lambda x: abs(x[1]), reverse=True)
    return candidates[:TOP_N_CANDIDATES]


def find_optimal_angles_refined(phases1, phases2, candidate_angles):
    """
    Refine around each candidate using fine grid.
    Returns best overall (angles, S).
    """
    best_S = 0.0  # Initialize to 0 so abs() comparison works
    best_angles = candidate_angles[0][0]  # Default to best coarse

    for coarse_angles, _ in candidate_angles:
        a0, ap0, b0, bp0 = coarse_angles

        for da in ANGLE_FINE:
            for dap in ANGLE_FINE:
                for db in ANGLE_FINE:
                    for dbp in ANGLE_FINE:
                        a = a0 + da
                        ap = ap0 + dap
                        b = b0 + db
                        bp = bp0 + dbp

                        S = compute_CHSH(phases1, phases2, a, ap, b, bp)
                        if abs(S) > abs(best_S):
                            best_S = S
                            best_angles = (a, ap, b, bp)

    return best_angles, best_S


def optimize_angles(phases1, phases2):
    """
    Two-stage angle optimization:
    1. Coarse grid search (15° steps) → top-N candidates
    2. Fine refinement (3° steps) around each candidate
    """
    top_candidates = find_optimal_angles_coarse(phases1, phases2)
    fine_angles, fine_S = find_optimal_angles_refined(phases1, phases2, top_candidates)
    return fine_angles, fine_S


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_experiment():
    """Run E231 angle-resolved field scan."""

    print("=" * 80)
    print("Paper 2 - Mission 4: Angle-Resolved CHSH Field Scan")
    print("=" * 80)

    n_K = len(K_VALUES)
    n_sigma = len(SIGMA_VALUES)
    total_points = n_K * n_sigma
    total_sims = total_points * SEEDS_PER_POINT

    print(f"\nConfiguration:")
    print(f"  K values: {n_K} points [{K_VALUES[0]:.2f}, {K_VALUES[-1]:.2f}]")
    print(f"  σ values: {n_sigma} points [{SIGMA_VALUES[0]:.2f}, {SIGMA_VALUES[-1]:.2f}]")
    print(f"  Seeds per point: {SEEDS_PER_POINT}")
    print(f"  Total simulations: {total_sims}")
    print(f"  Coarse angle grid: {len(ANGLE_COARSE)}^4 = {len(ANGLE_COARSE)**4} combos (15° steps)")
    print(f"  Top-N candidates kept: {TOP_N_CANDIDATES}")
    print(f"  Fine refinement per candidate: {len(ANGLE_FINE)}^4 = {len(ANGLE_FINE)**4} combos (3° steps)")

    run_id = f"E231-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    print(f"\nRun ID: {run_id}")

    # Storage
    results = []

    # Surfaces (mean over seeds)
    S_star_surface = np.zeros((n_K, n_sigma))
    angle_a_surface = np.zeros((n_K, n_sigma))
    angle_ap_surface = np.zeros((n_K, n_sigma))
    angle_b_surface = np.zeros((n_K, n_sigma))
    angle_bp_surface = np.zeros((n_K, n_sigma))
    echo_angle_surface = np.zeros((n_K, n_sigma))

    start_time = datetime.now()
    sim_count = 0

    for i_K, K in enumerate(K_VALUES):
        print(f"\n[{i_K+1}/{n_K}] K = {K:.2f}")

        for i_sigma, sigma in enumerate(SIGMA_VALUES):
            # Storage for seeds
            S_stars = []
            angles_list = []
            echoes = []

            for seed in range(SEEDS_PER_POINT):
                sim_count += 1

                # Run simulation
                phases1, phases2 = run_oscillator_simulation(K, sigma, seed)

                # Find optimal angles
                opt_angles, S_star = optimize_angles(phases1, phases2)
                S_stars.append(S_star)
                angles_list.append(opt_angles)

                # Compute echo at optimal angles
                S_series = compute_S_timeseries(phases1, phases2, *opt_angles)
                echo_50 = compute_echo(S_series, 50)
                echoes.append(echo_50)

                # Store result (convert numpy types to Python native)
                results.append({
                    "K": float(K),
                    "sigma": float(sigma),
                    "seed": int(seed),
                    "S_star": float(S_star),
                    "angle_a": float(opt_angles[0]),
                    "angle_ap": float(opt_angles[1]),
                    "angle_b": float(opt_angles[2]),
                    "angle_bp": float(opt_angles[3]),
                    "echo_50": float(echo_50)
                })

            # Compute means
            mean_S = np.mean(S_stars)
            mean_angles = np.mean(angles_list, axis=0)
            mean_echo = np.mean(echoes)

            S_star_surface[i_K, i_sigma] = mean_S
            angle_a_surface[i_K, i_sigma] = mean_angles[0]
            angle_ap_surface[i_K, i_sigma] = mean_angles[1]
            angle_b_surface[i_K, i_sigma] = mean_angles[2]
            angle_bp_surface[i_K, i_sigma] = mean_angles[3]
            echo_angle_surface[i_K, i_sigma] = mean_echo

            # Progress update
            if (i_sigma + 1) % 5 == 0:
                elapsed = (datetime.now() - start_time).total_seconds() / 60
                rate = sim_count / elapsed if elapsed > 0 else 0
                remaining = (total_sims - sim_count) / rate if rate > 0 else 0
                print(f"    σ = {sigma:.2f} | {sim_count}/{total_sims} sims | ~{remaining:.1f} min remaining")

    # Compute χ_angle = ∂S*/∂σ
    chi_angle_surface = np.zeros((n_K, n_sigma))
    d_sigma = SIGMA_VALUES[1] - SIGMA_VALUES[0]

    for i_K in range(n_K):
        for i_sigma in range(n_sigma):
            if i_sigma == 0:
                # Forward difference
                chi_angle_surface[i_K, i_sigma] = (S_star_surface[i_K, 1] - S_star_surface[i_K, 0]) / d_sigma
            elif i_sigma == n_sigma - 1:
                # Backward difference
                chi_angle_surface[i_K, i_sigma] = (S_star_surface[i_K, -1] - S_star_surface[i_K, -2]) / d_sigma
            else:
                # Central difference
                chi_angle_surface[i_K, i_sigma] = (S_star_surface[i_K, i_sigma+1] - S_star_surface[i_K, i_sigma-1]) / (2 * d_sigma)

    # Compute angle flow vectors (change in optimal angles with σ)
    angle_flow = {
        "da_dsigma": np.zeros((n_K, n_sigma)),
        "dap_dsigma": np.zeros((n_K, n_sigma)),
        "db_dsigma": np.zeros((n_K, n_sigma)),
        "dbp_dsigma": np.zeros((n_K, n_sigma))
    }

    for i_K in range(n_K):
        for i_sigma in range(1, n_sigma):
            angle_flow["da_dsigma"][i_K, i_sigma] = (angle_a_surface[i_K, i_sigma] - angle_a_surface[i_K, i_sigma-1]) / d_sigma
            angle_flow["dap_dsigma"][i_K, i_sigma] = (angle_ap_surface[i_K, i_sigma] - angle_ap_surface[i_K, i_sigma-1]) / d_sigma
            angle_flow["db_dsigma"][i_K, i_sigma] = (angle_b_surface[i_K, i_sigma] - angle_b_surface[i_K, i_sigma-1]) / d_sigma
            angle_flow["dbp_dsigma"][i_K, i_sigma] = (angle_bp_surface[i_K, i_sigma] - angle_bp_surface[i_K, i_sigma-1]) / d_sigma

    # ========================================================================
    # SAVE RESULTS
    # ========================================================================

    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)

    # Main results
    main_output = {
        "experiment_id": "E231",
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "K_values": K_VALUES.tolist(),
            "sigma_values": SIGMA_VALUES.tolist(),
            "seeds_per_point": SEEDS_PER_POINT,
            "tau_lags": TAU_LAGS
        },
        "results": results
    }

    main_path = OUTPUT_DIR / "E231_angle_resolved_field.json"
    with open(main_path, 'w') as f:
        json.dump(main_output, f, indent=2)
    print(f"\nSaved: {main_path}")

    # S* surface
    s_star_output = {
        "K_values": K_VALUES.tolist(),
        "sigma_values": SIGMA_VALUES.tolist(),
        "S_star": S_star_surface.tolist()
    }
    s_star_path = OUTPUT_DIR / "S_star_surface.json"
    with open(s_star_path, 'w') as f:
        json.dump(s_star_output, f, indent=2)
    print(f"Saved: {s_star_path}")

    # Optimal angles
    angles_output = {
        "K_values": K_VALUES.tolist(),
        "sigma_values": SIGMA_VALUES.tolist(),
        "angle_a": angle_a_surface.tolist(),
        "angle_ap": angle_ap_surface.tolist(),
        "angle_b": angle_b_surface.tolist(),
        "angle_bp": angle_bp_surface.tolist()
    }
    angles_path = OUTPUT_DIR / "angle_optimal_grid.json"
    with open(angles_path, 'w') as f:
        json.dump(angles_output, f, indent=2)
    print(f"Saved: {angles_path}")

    # χ_angle surface
    chi_output = {
        "K_values": K_VALUES.tolist(),
        "sigma_values": SIGMA_VALUES.tolist(),
        "chi_angle": chi_angle_surface.tolist()
    }
    chi_path = OUTPUT_DIR / "chi_angle_surface.json"
    with open(chi_path, 'w') as f:
        json.dump(chi_output, f, indent=2)
    print(f"Saved: {chi_path}")

    # Echo surface
    echo_output = {
        "K_values": K_VALUES.tolist(),
        "sigma_values": SIGMA_VALUES.tolist(),
        "echo_angle": echo_angle_surface.tolist()
    }
    echo_path = OUTPUT_DIR / "echo_angle_surface.json"
    with open(echo_path, 'w') as f:
        json.dump(echo_output, f, indent=2)
    print(f"Saved: {echo_path}")

    # Angle flow vectors
    flow_output = {
        "K_values": K_VALUES.tolist(),
        "sigma_values": SIGMA_VALUES.tolist(),
        "da_dsigma": angle_flow["da_dsigma"].tolist(),
        "dap_dsigma": angle_flow["dap_dsigma"].tolist(),
        "db_dsigma": angle_flow["db_dsigma"].tolist(),
        "dbp_dsigma": angle_flow["dbp_dsigma"].tolist()
    }
    flow_path = OUTPUT_DIR / "angle_flow_vectors.json"
    with open(flow_path, 'w') as f:
        json.dump(flow_output, f, indent=2)
    print(f"Saved: {flow_path}")

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    print(f"\nS* surface:")
    print(f"  Range: [{S_star_surface.min():.4f}, {S_star_surface.max():.4f}]")
    print(f"  Mean: {S_star_surface.mean():.4f}")
    print(f"  Max |S*| at K={K_VALUES[np.unravel_index(np.argmax(np.abs(S_star_surface)), S_star_surface.shape)[0]]:.2f}, σ={SIGMA_VALUES[np.unravel_index(np.argmax(np.abs(S_star_surface)), S_star_surface.shape)[1]]:.2f}")

    print(f"\nχ_angle surface:")
    print(f"  Range: [{chi_angle_surface.min():.4f}, {chi_angle_surface.max():.4f}]")

    print(f"\nEcho_angle surface (τ=50):")
    print(f"  Range: [{echo_angle_surface.min():.4f}, {echo_angle_surface.max():.4f}]")
    print(f"  At σ=0: mean = {echo_angle_surface[:, 0].mean():.4f}")

    print(f"\nOptimal angle ranges:")
    print(f"  a:  [{angle_a_surface.min():.1f}°, {angle_a_surface.max():.1f}°]")
    print(f"  a': [{angle_ap_surface.min():.1f}°, {angle_ap_surface.max():.1f}°]")
    print(f"  b:  [{angle_b_surface.min():.1f}°, {angle_b_surface.max():.1f}°]")
    print(f"  b': [{angle_bp_surface.min():.1f}°, {angle_bp_surface.max():.1f}°]")

    elapsed = (datetime.now() - start_time).total_seconds() / 60
    print(f"\nTotal runtime: {elapsed:.1f} minutes")

    print("\n" + "=" * 80)
    print("Mission 4 COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_experiment()
