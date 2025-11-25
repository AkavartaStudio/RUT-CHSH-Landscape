#!/usr/bin/env python3
"""
Quick script to regenerate e107n figures with corrected terminology
(RUT Plateau instead of Goldilocks)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load results
data_path = Path(__file__).parent.parent / "data" / "e107n_rut_plateau_results.json"
with open(data_path) as f:
    data = json.load(f)

results = data["results"]

# Extract unique values
K_values = sorted(list(set(r["K"] for r in results)))
delta_omega_values = sorted(list(set(r["delta_omega"] for r in results)))
sigma_values = sorted(list(set(r["sigma"] for r in results)))

print(f"Regenerating E107N figures...")
print(f"K values: {K_values}")
print(f"Δω values: {delta_omega_values}")
print(f"σ values: {sigma_values}")

analysis_dir = Path(__file__).parent.parent.parent / "paper" / "figures"

# === FIGURE 1: Heatmaps (K vs σ) ===
delta_omega_focus = 0.3
focus_results = [r for r in results if r["delta_omega"] == delta_omega_focus]

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Prepare matrices
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

# === FIGURE 2: S vs σ curves ===
fig, ax = plt.subplots(figsize=(12, 8))

for K in K_values:
    K_results = [r for r in focus_results if r["K"] == K]
    K_results_sorted = sorted(K_results, key=lambda r: r["sigma"])
    sigmas = [r["sigma"] for r in K_results_sorted]
    S_vals = [r["S"] for r in K_results_sorted]
    ax.plot(sigmas, S_vals, marker='o', label=f"K={K:.2f}", linewidth=2.5, markersize=8)

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

print("\n✅ Figures regenerated with corrected 'RUT Plateau' terminology!")
