#!/usr/bin/env python3
"""
Generate Figure 1: 3D CHSH Landscape using A1 Experiment Data

Uses the actual K-σ grid sweep from Paper 1 Experiment A1.
Shows |S| as a 3D surface with reference planes at |S| = 2.0 and 2.3.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

print(f"Loaded {len(results)} measured points from A1 experiment")
print(f"K range: [{K_measured.min():.1f}, {K_measured.max():.1f}]")
print(f"σ range: [{sigma_measured.min():.1f}, {sigma_measured.max():.1f}]")
print(f"|S| range: [{abs_S_measured.min():.2f}, {abs_S_measured.max():.2f}]")

# Create smooth interpolated grid for surface
K_grid_fine = np.linspace(K_measured.min(), K_measured.max(), 100)
sigma_grid_fine = np.linspace(sigma_measured.min(), sigma_measured.max(), 100)
K_mesh, sigma_mesh = np.meshgrid(K_grid_fine, sigma_grid_fine)

# Interpolate |S| values onto fine grid
abs_S_mesh = griddata(
    points=(K_measured, sigma_measured),
    values=abs_S_measured,
    xi=(K_mesh, sigma_mesh),
    method='cubic'
)

# Create 3D figure
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with colormap
surf = ax.plot_surface(K_mesh, sigma_mesh, abs_S_mesh,
                       cmap='viridis', alpha=0.8, edgecolor='none',
                       vmin=0.5, vmax=2.9)

# Add colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('CHSH Parameter $|S|$', fontsize=12, weight='bold')

# Plot ALL measured grid points as small white dots
ax.scatter(K_measured, sigma_measured, abs_S_measured,
          c='white', s=15, edgecolors='black', linewidths=0.5,
          alpha=0.8, zorder=10, label='Measured points')

# Add LARGE gold star at optimal point (K=0.7, σ=0.2, |S|≈2.819)
optimal_K = 0.7
optimal_sigma = 0.2
optimal_S = 2.819

ax.scatter([optimal_K], [optimal_sigma], [optimal_S],
          c='gold', s=500, marker='*', edgecolors='red', linewidths=3,
          alpha=1.0, zorder=20, label='Optimal point')

# Add transparent plane at |S| = 2.0 (classical bound)
K_plane = np.linspace(K_measured.min(), 1.5, 20)
sigma_plane = np.linspace(0, 1.2, 20)
K_plane_mesh, sigma_plane_mesh = np.meshgrid(K_plane, sigma_plane)
Z_classical = np.ones_like(K_plane_mesh) * 2.0

ax.plot_surface(K_plane_mesh, sigma_plane_mesh, Z_classical,
               alpha=0.15, color='pink', edgecolor='red', linewidth=0.5)

# Add text label for classical bound plane - angled along the plane
ax.text(1.3, 0.5, 2.0, 'Classical bound (2.0)',
        fontsize=8, color='red', weight='bold',
        rotation=15, rotation_mode='anchor',
        ha='center', va='center')

# Add transparent plane at |S| = 2.3 (high correlation threshold)
Z_high_corr = np.ones_like(K_plane_mesh) * 2.3

ax.plot_surface(K_plane_mesh, sigma_plane_mesh, Z_high_corr,
               alpha=0.15, color='lightblue', edgecolor='blue', linewidth=0.5)

# Add text label for high correlation plane - angled along the plane
ax.text(1.3, 0.5, 2.3, 'High correlation (2.3)',
        fontsize=8, color='blue', weight='bold',
        rotation=15, rotation_mode='anchor',
        ha='center', va='center')

# Add contour lines on the bottom plane (projection)
contours = ax.contour(K_mesh, sigma_mesh, abs_S_mesh,
                     levels=[2.0, 2.3, 2.6, 2.8],
                     colors='black', alpha=0.4, linewidths=1.5,
                     offset=0)

# Labels and title with increased padding
ax.set_xlabel('Coupling Strength $K$', fontsize=13, weight='bold', labelpad=15)
ax.set_ylabel('Noise Amplitude $\\sigma$', fontsize=13, weight='bold', labelpad=15)
ax.set_zlabel('CHSH Parameter $|S|$', fontsize=13, weight='bold', labelpad=10)
ax.set_title('CHSH Correlation Landscape in Parameter Space',
            fontsize=15, weight='bold', pad=20)

# Set viewing angle to show low-K region better (front-left quadrant)
ax.view_init(elev=20, azim=225)

# Set axis limits - trim σ to [0, 1.2]
ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.2)
ax.set_zlim(0, 3.0)

# Add grid
ax.grid(True, alpha=0.3)

# Add text annotation
ax.text2D(0.05, 0.95,
         f'A1 Experiment\n'
         f'{len(results)} measurements\n'
         f'K ∈ [0.1, 1.5]\n'
         f'σ ∈ [0.0, 2.0]',
         transform=ax.transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig1_landscape_3d.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1_landscape_3d.png', dpi=300, bbox_inches='tight')

print("✓ Figure 1 (3D) saved: CHSH Landscape 3D surface")
print(f"  Surface interpolated from {len(results)} measured points")
print(f"  Planes at |S| = 2.0 (classical) and |S| = 2.3 (high correlation)")
print(f"  Viewing angle: elev=25°, azim=45°")
