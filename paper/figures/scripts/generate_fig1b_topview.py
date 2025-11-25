#!/usr/bin/env python3
"""
Generate Figure 1b: 2D Top-View of CHSH Landscape

Clean quantitative reference view showing |S|(K, σ) as a heatmap
with boundary line, optimal point, and tested configurations.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pathlib import Path

# Load A1 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A1_sigma_c_K_sweep.json") as f:
    data = json.load(f)

# Extract grid results
results = data['grid_results']

# Get measured K, σ, and |S| values
K_measured = np.array([r['K'] for r in results])
sigma_measured = np.array([r['sigma'] for r in results])
abs_S_measured = np.array([r['abs_S_mean'] for r in results])

# Create smooth interpolated grid for heatmap
K_grid_fine = np.linspace(0, 1.6, 200)
sigma_grid_fine = np.linspace(0, 1.2, 200)
K_mesh, sigma_mesh = np.meshgrid(K_grid_fine, sigma_grid_fine)

# Interpolate |S| values onto fine grid
abs_S_mesh = griddata(
    points=(K_measured, sigma_measured),
    values=abs_S_measured,
    xi=(K_mesh, sigma_mesh),
    method='cubic'
)

# Create figure
fig, ax = plt.subplots(figsize=(10, 7))

# Plot heatmap with viridis colormap (same as 3D)
im = ax.imshow(abs_S_mesh, cmap='viridis', aspect='auto', origin='lower',
              extent=[0, 1.6, 0, 1.2],
              vmin=1.5, vmax=2.8, interpolation='bilinear')

# Add colorbar
cbar = plt.colorbar(im, ax=ax, label='CHSH Parameter $|S|$')
cbar.ax.axhline(y=2.0, color='red', linewidth=2, linestyle='-')

# Plot σ_c(K) boundary line
K_line = np.linspace(0.2, 1.5, 100)
sigma_c_line = 0.60 * K_line + 0.22

# Adjust for saturation at high K
sigma_c_line = np.where(K_line < 0.9,
                        0.60 * K_line + 0.22,
                        0.60 * K_line + 0.22 - 0.1 * (K_line - 0.9))

ax.plot(K_line, sigma_c_line, 'k--', linewidth=3,
        label='$\\sigma_c(K)$ boundary', zorder=5, alpha=0.8)

# Mark optimal point with LARGE gold star
ax.plot(0.7, 0.2, marker='*', markersize=30,
        color='gold', markeredgecolor='red', markeredgewidth=2,
        label='Optimal', zorder=10)

# Mark tested points at σ=0.2 only
K_tested = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
sigma_low = [0.2] * len(K_tested)
ax.scatter(K_tested, sigma_low, s=60, c='white',
           edgecolors='black', linewidths=1.5,
           alpha=0.9, zorder=8, label='Tested points')

# Styling
ax.set_xlabel('Coupling Strength $K$', fontsize=13, weight='bold')
ax.set_ylabel('Noise Amplitude $\\sigma$', fontsize=13, weight='bold')
ax.xaxis.labelpad = 10  # Professional spacing
ax.yaxis.labelpad = 10  # Professional spacing
ax.set_title('CHSH Correlation Landscape: Top View',
             fontsize=14, weight='bold', pad=15)

ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.2)

# Subtle grid
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, color='white')

# Legend - nestled in upper left area within purple region
handles, labels = ax.get_legend_handles_labels()
ax.legend(loc='upper left', fontsize=9, framealpha=0.95,
         markerscale=0.5, bbox_to_anchor=(0.07, 0.96))

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig1b_topview.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1b_topview.png', dpi=300, bbox_inches='tight')

print("✓ Figure 1b saved: CHSH Landscape Top View")
print(f"  Clean 2D reference view")
print(f"  Heatmap: K ∈ [0, 1.6], σ ∈ [0, 1.2]")
print(f"  Boundary line: σ_c(K) ≈ 0.60K + 0.22")
print(f"  Optimal point: (K=0.7, σ=0.2)")
