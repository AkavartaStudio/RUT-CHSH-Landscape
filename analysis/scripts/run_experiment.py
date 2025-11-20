#!/usr/bin/env python3
"""
E107N: Goldilocks Noise - Breaking the Perfect Lock Trap

DISCOVERY: E107 found perfect lock (PLI=1.0) at ALL K → classical
           E103C had σ=0.1 noise → PLI≈0.94 → |S|≈2.4 → violations!

HYPOTHESIS: Noise breaks perfect lock → enables Goldilocks regime

Dynamics:
    dθ₁/dt = ω₁ + K·sin(θ₂ - θ₁) + η₁(t)
    dθ₂/dt = ω₂ + K·sin(θ₁ - θ₂) + η₂(t)

where η(t) ~ N(0, σ²) is Gaussian phase noise

Expected pattern:
    σ = 0.0  → PLI ≈ 1.00 → |S| ≤ 2.0  (perfect lock, classical)
    σ = 0.05 → PLI ≈ 0.97 → |S| ≈ 2.1  (slight breaking)
    σ = 0.1  → PLI ≈ 0.94 → |S| ≈ 2.4  (GOLDILOCKS!)
    σ = 0.2  → PLI ≈ 0.85 → |S| ≈ 2.0  (forgetfulness)
"""

import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load config
config_path = Path(__file__).parent.parent / "config" / "e107n_rut_plateau.json"
with open(config_path) as f:
    config = json.load(f)

# Parameters
K_values = config["parameters"]["K_range"]
delta_omega_values = config["parameters"]["delta_omega_range"]
sigma_values = config["parameters"]["noise_levels"]
N = config["parameters"]["n_oscillators"]
T = config["parameters"]["time_steps"]
dt = config["parameters"]["dt"]
transient = config["parameters"]["transient_cut"]

def kuramoto_with_noise(theta1_0, theta2_0, omega1, omega2, K, sigma, T, dt):
    """Kuramoto coupling with Gaussian phase noise

    Proper Wiener process: noise scales as σ√dt
    This ensures noise strength is consistent across different dt values
    """
    theta1 = np.zeros(T)
    theta2 = np.zeros(T)
    theta1[0] = theta1_0
    theta2[0] = theta2_0

    # Proper noise scaling for stochastic process
    noise_scale = sigma * np.sqrt(dt)

    for t in range(T-1):
        # Kuramoto sine coupling
        coupling1 = K * np.sin(theta2[t] - theta1[t])
        coupling2 = K * np.sin(theta1[t] - theta2[t])

        # Gaussian phase noise with proper √dt scaling (Wiener process)
        noise1 = np.random.normal(0, noise_scale)
        noise2 = np.random.normal(0, noise_scale)

        # Update
        theta1[t+1] = theta1[t] + dt * (omega1 + coupling1) + noise1
        theta2[t+1] = theta2[t] + dt * (omega2 + coupling2) + noise2

    return theta1, theta2

def compute_pli(phase1, phase2):
    """Phase Lag Index: |<exp(i·Δφ)>|"""
    delta_phi = phase2 - phase1
    pli = np.abs(np.mean(np.exp(1j * delta_phi)))
    return pli

def compute_bell_correlation(theta_A, theta_B, angle_a, angle_b):
    """
    Compute Bell-type correlation E(a,b) between two oscillators.

    E(a,b) = ⟨cos((θ^A + a) - (θ^B + b))⟩
           = ⟨cos(Δθ + (a - b))⟩

    This is the CORRECT formula used in E104B/E103C.
    """
    # Apply measurement offsets
    measured_A = theta_A + angle_a
    measured_B = theta_B + angle_b

    # Compute correlation
    phase_diff = measured_A - measured_B
    correlation = np.mean(np.cos(phase_diff))

    return float(correlation)

def compute_chsh_score(theta_A, theta_B):
    """
    Compute CHSH Bell inequality score using optimal angles.

    S = E(a,b) - E(a,b') + E(a',b) + E(a',b')

    Optimal angles (from E103C/E104B):
    - a = 0°, a' = 45°
    - b = 22.5°, b' = 67.5°

    Classical limit: |S| ≤ 2
    Quantum limit: |S| ≤ 2√2 ≈ 2.828
    """
    # Optimal CHSH angles (in radians)
    a = 0.0
    a_prime = np.deg2rad(45.0)
    b = np.deg2rad(22.5)
    b_prime = np.deg2rad(67.5)

    # Compute all four correlations
    E_ab = compute_bell_correlation(theta_A, theta_B, a, b)
    E_ab_prime = compute_bell_correlation(theta_A, theta_B, a, b_prime)
    E_a_prime_b = compute_bell_correlation(theta_A, theta_B, a_prime, b)
    E_a_prime_b_prime = compute_bell_correlation(theta_A, theta_B, a_prime, b_prime)

    # CHSH combination
    S = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime

    return S, {
        'E_ab': E_ab,
        'E_ab_prime': E_ab_prime,
        'E_a_prime_b': E_a_prime_b,
        'E_a_prime_b_prime': E_a_prime_b_prime
    }

def run_single_experiment(K, delta_omega, sigma):
    """Run one (K, Δω, σ) configuration"""
    # Natural frequencies
    omega1 = 1.0
    omega2 = 1.0 + delta_omega

    # Random initial conditions
    theta1_0 = np.random.uniform(0, 2*np.pi)
    theta2_0 = np.random.uniform(0, 2*np.pi)

    # Evolve
    theta1, theta2 = kuramoto_with_noise(theta1_0, theta2_0, omega1, omega2, K, sigma, T, dt)

    # Remove transient
    theta1_steady = theta1[transient:]
    theta2_steady = theta2[transient:]

    # Measure PLI
    pli = compute_pli(theta1_steady, theta2_steady)

    # Measure CHSH using correct E104B formula
    S, correlations = compute_chsh_score(theta1_steady, theta2_steady)

    return {
        "K": K,
        "delta_omega": delta_omega,
        "sigma": sigma,
        "PLI": float(pli),
        "S": float(S),
        "correlations": correlations,
        "violation": bool(S > 2.0),
        "regime": get_regime(pli, S, sigma)
    }

def get_regime(pli, S, sigma):
    """Classify the regime"""
    if pli > 0.98:
        return "perfect_lock_trap"
    elif 0.90 <= pli <= 0.97 and S > 2.2:
        return "rut_plateau_violations"
    elif pli < 0.85:
        return "forgetfulness_classical"
    else:
        return "transition"

# Main experiment loop
print("=" * 80)
print("E107N: GOLDILOCKS NOISE - Breaking the Perfect Lock Trap")
print("=" * 80)
print()
print("DISCOVERY:")
print("  E107 (no noise): Perfect lock (PLI=1.0) at ALL K → |S|≤2.0 (trap!)")
print("  E103C (σ=0.1):   PLI≈0.94 → |S|≈2.4 (violations!)")
print()
print("HYPOTHESIS:")
print("  Noise breaks perfect lock → enables Goldilocks regime")
print()
print("TESTING:")
print(f"  K: {len(K_values)} values from {min(K_values)} to {max(K_values)}")
print(f"  Δω: {len(delta_omega_values)} values")
print(f"  σ: {sigma_values}")
print(f"  Total runs: {len(K_values) * len(delta_omega_values) * len(sigma_values)}")
print()
print("-" * 80)

results = []
total_runs = len(K_values) * len(delta_omega_values) * len(sigma_values)
run_count = 0

for sigma in sigma_values:
    print(f"\n🔊 NOISE LEVEL: σ = {sigma}")
    print("-" * 60)

    for K in K_values:
        for delta_omega in delta_omega_values:
            run_count += 1

            # Run experiment
            result = run_single_experiment(K, delta_omega, sigma)
            results.append(result)

            # Report
            pli = result["PLI"]
            S = result["S"]
            regime = result["regime"]

            status = "✓" if S > 2.0 else "·"
            print(f"{status} [{run_count:3d}/{total_runs}] K={K:.2f} Δω={delta_omega:.1f} σ={sigma:.2f} → PLI={pli:.3f} |S|={S:.3f} ({regime})")

# Save results
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "e107n_rut_plateau_results.json"

output_data = {
    "experiment_id": "E107N",
    "timestamp": datetime.now().isoformat(),
    "config": config,
    "results": results,
    "summary": {
        "total_runs": len(results),
        "violations": sum(1 for r in results if r["violation"]),
        "violation_rate": sum(1 for r in results if r["violation"]) / len(results)
    }
}

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print()
print("=" * 80)
print("RESULTS SAVED")
print("=" * 80)
print(f"Output: {output_file}")
print()

# Analysis: Find Goldilocks band
print("🎯 GOLDILOCKS ANALYSIS")
print("-" * 80)

for sigma in sigma_values:
    sigma_results = [r for r in results if r["sigma"] == sigma]
    violations = [r for r in sigma_results if r["violation"]]
    avg_pli = np.mean([r["PLI"] for r in sigma_results])
    avg_S = np.mean([r["S"] for r in sigma_results])
    max_S = max([r["S"] for r in sigma_results])

    print(f"\nσ = {sigma:.2f}:")
    print(f"  Avg PLI: {avg_pli:.3f}")
    print(f"  Avg |S|: {avg_S:.3f}")
    print(f"  Max |S|: {max_S:.3f}")
    print(f"  Violations: {len(violations)}/{len(sigma_results)} ({100*len(violations)/len(sigma_results):.1f}%)")

    if len(violations) > 0:
        best = max(violations, key=lambda r: r["S"])
        print(f"  Best: K={best['K']:.2f} Δω={best['delta_omega']:.1f} → PLI={best['PLI']:.3f} |S|={best['S']:.3f}")

# Find THE RUT Plateau configuration
rut_plateau_candidates = [r for r in results if r["regime"] == "rut_plateau_violations"]
if rut_plateau_candidates:
    best_rut_plateau = max(rut_plateau_candidates, key=lambda r: r["S"])
    print()
    print("🏆 BEST RUT PLATEAU CONFIGURATION:")
    print(f"  K = {best_rut_plateau['K']:.2f}")
    print(f"  Δω = {best_rut_plateau['delta_omega']:.1f}")
    print(f"  σ = {best_rut_plateau['sigma']:.2f}")
    print(f"  PLI = {best_rut_plateau['PLI']:.3f}")
    print(f"  |S| = {best_rut_plateau['S']:.3f}")

print()
print("=" * 80)
print("PLOTTING")
print("=" * 80)

# Create plots
analysis_dir = Path(__file__).parent.parent / "analysis"
analysis_dir.mkdir(exist_ok=True)

# Plot 1: Heatmap of S vs K and sigma (for Δω = 0.3, matching E103C)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

delta_omega_focus = 0.3  # E103C had Δω=0.3
focus_results = [r for r in results if r["delta_omega"] == delta_omega_focus]

# Prepare data for heatmap
S_matrix = np.zeros((len(sigma_values), len(K_values)))
PLI_matrix = np.zeros((len(sigma_values), len(K_values)))

for i, sigma in enumerate(sigma_values):
    for j, K in enumerate(K_values):
        matches = [r for r in focus_results if r["sigma"] == sigma and r["K"] == K]
        if matches:
            S_matrix[i, j] = matches[0]["S"]
            PLI_matrix[i, j] = matches[0]["PLI"]

# S heatmap
sns.heatmap(S_matrix, ax=axes[0], cmap="RdYlGn", center=2.0, vmin=1.8, vmax=2.6,
            xticklabels=[f"{k:.2f}" for k in K_values],
            yticklabels=[f"{s:.2f}" for s in sigma_values],
            annot=True, fmt=".2f", cbar_kws={"label": "|S|"})
axes[0].set_xlabel("Coupling Strength K")
axes[0].set_ylabel("Noise Level σ")
axes[0].set_title(f"E107N: |S| vs K and σ (Δω={delta_omega_focus})\nRUT Plateau Search")
axes[0].axhline(y=2, color='blue', linestyle='--', linewidth=2, label="σ=0.1 (E103C)")

# PLI heatmap
sns.heatmap(PLI_matrix, ax=axes[1], cmap="viridis", vmin=0.8, vmax=1.0,
            xticklabels=[f"{k:.2f}" for k in K_values],
            yticklabels=[f"{s:.2f}" for s in sigma_values],
            annot=True, fmt=".2f", cbar_kws={"label": "r"})
axes[1].set_xlabel("Coupling Strength K")
axes[1].set_ylabel("Noise Level σ")
axes[1].set_title(f"E107N: r vs K and σ (Δω={delta_omega_focus})\nPhase Coherence Pattern")
axes[1].axhline(y=2, color='yellow', linestyle='--', linewidth=2, label="σ=0.1 (E103C)")

plt.tight_layout()
plt.savefig(analysis_dir / "e107n_rut_plateau_heatmap.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: {analysis_dir / 'e107n_rut_plateau_heatmap.png'}")

# Plot 2: S vs σ for each K (line plot showing RUT Plateau curve)
fig, ax = plt.subplots(figsize=(12, 8))

for K in K_values:
    K_results = [r for r in focus_results if r["K"] == K]
    K_results_sorted = sorted(K_results, key=lambda r: r["sigma"])
    sigmas = [r["sigma"] for r in K_results_sorted]
    S_vals = [r["S"] for r in K_results_sorted]
    ax.plot(sigmas, S_vals, marker='o', label=f"K={K:.2f}", linewidth=2)

ax.axhline(y=2.0, color='red', linestyle='--', linewidth=2, label="Classical bound")
ax.axhline(y=2.828, color='blue', linestyle=':', linewidth=2, label="Tsirelson bound")
ax.set_xlabel("Noise Level σ", fontsize=12)
ax.set_ylabel("|S|", fontsize=12)
ax.set_title("E107N: RUT Plateau Noise Curve\n|S| vs σ for different K values", fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(analysis_dir / "e107n_rut_plateau_curve.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: {analysis_dir / 'e107n_rut_plateau_curve.png'}")

print()
print("=" * 80)
print("E107N COMPLETE!")
print("=" * 80)
print()
print("🎯 KEY FINDINGS:")
print("  1. Did σ=0.0 give perfect lock (PLI=1.0) and classical |S|≤2.0?")
print("  2. Did σ=0.1 create Goldilocks band with PLI≈0.9-0.95 and |S|>2.2?")
print("  3. Did high σ return to classical via forgetfulness?")
print()
print("Check the plots to see the Goldilocks noise ridge!")
