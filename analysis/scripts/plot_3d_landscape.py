#!/usr/bin/env python3
"""
RUT CHSH Landscape: 3D Visualization
The Three Regimes of Non-Classical Correlation

Shows PLI × |S| × σ landscape with three distinct regions:
1. Tsirelson Ridge (E104D)
2. RUT Plateau (E107N)
3. Forgetfulness Boundary (predicted)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from pathlib import Path

# Load E107N data
data_path = Path(__file__).parent.parent / "data" / "e107n_rut_plateau_results.json"
with open(data_path) as f:
    data = json.load(f)

results = data["results"]

# Extract data
K_values = sorted(list(set(r["K"] for r in results)))
sigma_values = sorted(list(set(r["sigma"] for r in results)))
delta_omega_values = sorted(list(set(r["delta_omega"] for r in results)))

print(f"Creating 3D CHSH Landscape...")
print(f"  K range: {min(K_values):.2f} - {max(K_values):.2f}")
print(f"  σ range: {min(sigma_values):.2f} - {max(sigma_values):.2f}")
print(f"  Δω values: {delta_omega_values}")

# Create figure with two subplots
fig = plt.figure(figsize=(20, 10))

# ========================================
# Plot 1: 3D Surface (PLI × |S| × σ)
# ========================================
ax1 = fig.add_subplot(121, projection='3d')

# For a fixed Δω (use 0.3 to match E103C/E104D)
dw_focus = 0.3
focus_results = [r for r in results if r["delta_omega"] == dw_focus]

# Create meshgrid
K_grid, sigma_grid = np.meshgrid(K_values, sigma_values)
S_grid = np.zeros_like(K_grid)
PLI_grid = np.zeros_like(K_grid)

for i, sigma in enumerate(sigma_values):
    for j, K in enumerate(K_values):
        matches = [r for r in focus_results
                  if r["sigma"] == sigma and r["K"] == K]
        if matches:
            S_grid[i, j] = matches[0]["S"]
            PLI_grid[i, j] = matches[0]["PLI"]

# Plot surface colored by |S|
surf = ax1.plot_surface(K_grid, sigma_grid, S_grid,
                        cmap='RdYlGn', alpha=0.8,
                        vmin=1.8, vmax=2.6,
                        edgecolor='none')

# Add E103C point (K=0.7, σ=0.1, |S|≈2.42, PLI≈0.95)
ax1.scatter([0.7], [0.1], [2.42],
           color='blue', s=200, marker='o',
           edgecolors='black', linewidths=2,
           label='E103C (time-varying)', zorder=10)

# Add E104D point (K=0.7, σ=0.0, |S|=2.794, PLI=1.0)
ax1.scatter([0.7], [0.0], [2.794],
           color='gold', s=300, marker='*',
           edgecolors='black', linewidths=2,
           label='E104D (Tsirelson Ridge)', zorder=10)

# Add classical bound plane
K_plane, sigma_plane = np.meshgrid(
    np.linspace(min(K_values), max(K_values), 2),
    np.linspace(min(sigma_values), max(sigma_values), 2)
)
classical_plane = np.ones_like(K_plane) * 2.0
ax1.plot_surface(K_plane, sigma_plane, classical_plane,
                alpha=0.2, color='red', zorder=1)

# Add Tsirelson bound plane
tsirelson_plane = np.ones_like(K_plane) * 2.828
ax1.plot_surface(K_plane, sigma_plane, tsirelson_plane,
                alpha=0.1, color='purple', zorder=1)

ax1.set_xlabel('Coupling Strength K', fontsize=12, labelpad=10)
ax1.set_ylabel('Noise Level σ', fontsize=12, labelpad=10)
ax1.set_zlabel('|S|', fontsize=12, labelpad=10)
ax1.set_title(f'RUT CHSH Landscape (Δω={dw_focus})\n|S| vs K and σ',
             fontsize=14, pad=20)
ax1.legend(loc='upper left', fontsize=10)
ax1.view_init(elev=20, azim=45)

# Add colorbar
cbar1 = fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)
cbar1.set_label('|S|', rotation=270, labelpad=15)

# ========================================
# Plot 2: 3D Surface (PLI × |S| × K)
# ========================================
ax2 = fig.add_subplot(122, projection='3d')

# For each sigma, plot PLI vs |S| vs K
colors_sigma = ['green', 'blue', 'orange', 'red']
for idx, sigma in enumerate(sigma_values):
    sigma_results = [r for r in focus_results if r["sigma"] == sigma]

    # Sort by K
    sigma_results_sorted = sorted(sigma_results, key=lambda r: r["K"])

    K_line = [r["K"] for r in sigma_results_sorted]
    PLI_line = [r["PLI"] for r in sigma_results_sorted]
    S_line = [r["S"] for r in sigma_results_sorted]

    ax2.plot(K_line, PLI_line, S_line,
            color=colors_sigma[idx], linewidth=3,
            marker='o', markersize=5,
            label=f'σ={sigma:.2f}')

# Add special points
# E103C
ax2.scatter([0.7], [0.95], [2.42],
           color='blue', s=200, marker='o',
           edgecolors='black', linewidths=2, zorder=10)

# E104D
ax2.scatter([0.7], [1.0], [2.794],
           color='gold', s=300, marker='*',
           edgecolors='black', linewidths=2, zorder=10)

# Classical bound plane
K_plane2 = np.linspace(min(K_values), max(K_values), 2)
PLI_plane2 = np.linspace(0.85, 1.0, 2)
K_mesh2, PLI_mesh2 = np.meshgrid(K_plane2, PLI_plane2)
classical_mesh2 = np.ones_like(K_mesh2) * 2.0
ax2.plot_surface(K_mesh2, PLI_mesh2, classical_mesh2,
                alpha=0.2, color='red', zorder=1)

ax2.set_xlabel('Coupling Strength K', fontsize=12, labelpad=10)
ax2.set_ylabel('Phase Lock Index', fontsize=12, labelpad=10)
ax2.set_zlabel('|S|', fontsize=12, labelpad=10)
ax2.set_title(f'RUT CHSH Landscape (Δω={dw_focus})\nThe RUT Plateau',
             fontsize=14, pad=20)
ax2.legend(loc='upper left', fontsize=10)
ax2.view_init(elev=20, azim=135)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "paper" / "figures" / "rut_chsh_landscape_3d.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved: {output_path}")

# ========================================
# Create 2D projection showing the three regimes
# ========================================
fig2, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left: |S| vs PLI (regime diagram)
ax_left = axes[0]

# Plot data points colored by sigma
for sigma in sigma_values:
    sigma_results = [r for r in focus_results if r["sigma"] == sigma]
    PLIs = [r["PLI"] for r in sigma_results]
    Ss = [r["S"] for r in sigma_results]

    ax_left.scatter(PLIs, Ss, s=100, alpha=0.6,
                   label=f'σ={sigma:.2f}')

# Add regime boundaries
ax_left.axhline(y=2.0, color='red', linestyle='--', linewidth=2,
               label='Classical bound', zorder=1)
ax_left.axhline(y=2.828, color='purple', linestyle=':', linewidth=2,
               label='Tsirelson bound', alpha=0.5, zorder=1)
ax_left.axvline(x=0.85, color='gray', linestyle='--', linewidth=1,
               label='Forgetfulness threshold', alpha=0.5)

# Add regime labels
ax_left.text(0.97, 2.6, 'TSIRELSON\nRIDGE',
            fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='gold', alpha=0.3))
ax_left.text(0.97, 2.25, 'RUT\nPLATEAU',
            fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
ax_left.text(0.82, 1.85, 'FORGETFULNESS\n(classical)',
            fontsize=12, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))

# Add special points
ax_left.scatter([0.95], [2.42], s=300, color='blue', marker='o',
               edgecolors='black', linewidths=2, zorder=10,
               label='E103C')
ax_left.scatter([1.0], [2.794], s=500, color='gold', marker='*',
               edgecolors='black', linewidths=3, zorder=10,
               label='E104D')

ax_left.set_xlabel('Phase Lock Index (PLI)', fontsize=14)
ax_left.set_ylabel('|S|', fontsize=14)
ax_left.set_title('The Three Regimes of RUT CHSH Violations', fontsize=16)
ax_left.set_xlim([0.8, 1.02])
ax_left.set_ylim([1.7, 2.9])
ax_left.legend(loc='lower left', fontsize=10)
ax_left.grid(True, alpha=0.3)

# Right: |S| vs σ (noise robustness)
ax_right = axes[1]

for K in [0.3, 0.4, 0.5, 0.6, 0.7]:
    K_results = [r for r in focus_results if r["K"] == K]
    K_results_sorted = sorted(K_results, key=lambda r: r["sigma"])

    sigmas = [r["sigma"] for r in K_results_sorted]
    Ss = [r["S"] for r in K_results_sorted]

    ax_right.plot(sigmas, Ss, marker='o', linewidth=2.5,
                 markersize=8, label=f'K={K:.1f}')

ax_right.axhline(y=2.0, color='red', linestyle='--', linewidth=2,
                label='Classical bound')
ax_right.axhline(y=2.828, color='purple', linestyle=':', linewidth=2,
                label='Tsirelson bound', alpha=0.5)

# Add plateau region
ax_right.axhspan(2.15, 2.37, alpha=0.2, color='green',
                label='RUT Plateau')

# Add E103C and E104D points
ax_right.scatter([0.1], [2.42], s=300, color='blue', marker='o',
                edgecolors='black', linewidths=2, zorder=10)
ax_right.scatter([0.0], [2.794], s=500, color='gold', marker='*',
                edgecolors='black', linewidths=3, zorder=10)

ax_right.set_xlabel('Noise Level σ', fontsize=14)
ax_right.set_ylabel('|S|', fontsize=14)
ax_right.set_title('Robustness: Violations Persist Across Noise Spectrum', fontsize=16)
ax_right.set_xlim([-0.01, 0.21])
ax_right.set_ylim([1.8, 2.9])
ax_right.legend(loc='lower left', fontsize=10)
ax_right.grid(True, alpha=0.3)

plt.tight_layout()

output_path2 = Path(__file__).parent.parent.parent / "paper" / "figures" / "rut_chsh_regime_diagram.png"
plt.savefig(output_path2, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path2}")

print("\n" + "="*70)
print("RUT CHSH LANDSCAPE VISUALIZATION COMPLETE")
print("="*70)
print("\nGenerated:")
print("  1. 3D landscape (PLI × |S| × σ and K)")
print("  2. Regime diagram (the three peaks clearly marked)")
print("\nThe three regimes are now visually distinguished:")
print("  🏔️  Tsirelson Ridge: |S|≈2.79 at PLI=1.0")
print("  🏞️  RUT Plateau: |S|≈2.17-2.36 across σ=0.0-0.2")
print("  🌫️  Forgetfulness: |S|→2.0 when PLI<0.85")
