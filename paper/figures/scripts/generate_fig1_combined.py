#!/usr/bin/env python3
"""
Generate Figure 1: Combined 2D Heatmap + 3D Inset

Main panel: Clean 2D top-view heatmap (quantitative reference)
Inset: Small 3D surface for visual impact (minimal labels)

Best of both worlds: readability + wow factor!
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

# Create smooth interpolated grid
K_grid_fine = np.linspace(0, 1.6, 200)
sigma_grid_fine = np.linspace(0, 1.2, 200)
K_mesh, sigma_mesh = np.meshgrid(K_grid_fine, sigma_grid_fine)

# Interpolate |S| values
abs_S_mesh = griddata(
    points=(K_measured, sigma_measured),
    values=abs_S_measured,
    xi=(K_mesh, sigma_mesh),
    method='cubic'
)

# Create main figure
fig = plt.figure(figsize=(12, 8))

# ============================================
# MAIN PANEL: 2D Heatmap (clean, readable)
# ============================================
ax_main = fig.add_subplot(111)

# Plot heatmap with plasma colormap for better contrast
im = ax_main.imshow(abs_S_mesh, cmap='plasma', aspect='auto', origin='lower',
                    extent=[0, 1.6, 0, 1.2],
                    vmin=1.5, vmax=2.8, interpolation='bilinear')

# Add colorbar with enhanced labeling
cbar = plt.colorbar(im, ax=ax_main, label='CHSH Parameter $|S|$')
cbar.ax.axhline(y=2.0, color='red', linewidth=2.5, linestyle='-')
cbar.ax.axhline(y=2.3, color='orange', linewidth=2, linestyle='--', alpha=0.7)
# Add tick marks at key thresholds
cbar.set_ticks([1.5, 1.8, 2.0, 2.3, 2.5, 2.8])
cbar.ax.tick_params(labelsize=9, width=1.5)

# Plot σ_c(K) boundary line
K_line = np.linspace(0.2, 1.5, 100)
sigma_c_line = 0.60 * K_line + 0.22

# Adjust for saturation at high K
sigma_c_line = np.where(K_line < 0.9,
                        0.60 * K_line + 0.22,
                        0.60 * K_line + 0.22 - 0.1 * (K_line - 0.9))

# Plot boundary with white outline for high visibility
from matplotlib import patheffects
boundary_line = ax_main.plot(K_line, sigma_c_line, 'k--', linewidth=4,
             label='$\\sigma_c(K)$ boundary', zorder=5)[0]
boundary_line.set_path_effects([patheffects.Stroke(linewidth=6, foreground='white'),
                                patheffects.Normal()])

# Mark optimal point with LARGE gold star
ax_main.plot(0.7, 0.2, marker='*', markersize=30,
             color='gold', markeredgecolor='red', markeredgewidth=2,
             label='Optimal', zorder=10)

# Mark tested points at σ=0.2 with stronger visibility
K_tested = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
sigma_low = [0.2] * len(K_tested)
ax_main.scatter(K_tested, sigma_low, s=100, c='white',
                edgecolors='black', linewidths=2.5,
                alpha=1.0, zorder=8, label='Tested points')

# Styling with stronger axis labels
ax_main.set_xlabel('Coupling Strength $K$', fontsize=14, weight='bold')
ax_main.set_ylabel('Noise Amplitude $\\sigma$', fontsize=14, weight='bold')
ax_main.xaxis.labelpad = 10
ax_main.yaxis.labelpad = 10
ax_main.set_title('CHSH Correlation Landscape in Parameter Space',
                  fontsize=14, weight='bold', pad=15)

ax_main.set_xlim(0, 1.6)
ax_main.set_ylim(0, 1.2)

# Subtle grid
ax_main.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, color='white')

# Legend - positioned in pink area, upper center-right with breathing room
handles, labels = ax_main.get_legend_handles_labels()
ax_main.legend(loc='upper right', bbox_to_anchor=(0.85, 0.96),
               fontsize=10, framealpha=0.98, markerscale=0.5,
               edgecolor='black', fancybox=False)

# ============================================
# INSET: Small 3D Surface (visual impact)
# ============================================
# Position inset: sized to fit within purple region, positioned higher
ax_inset = fig.add_axes([0.10, 0.68, 0.24, 0.20], projection='3d')
# Add visible border around inset
for spine in ['top', 'bottom', 'left', 'right']:
    ax_inset.spines[spine].set_visible(True)
    ax_inset.spines[spine].set_color('black')
    ax_inset.spines[spine].set_linewidth(2)

# Create fine grid for 3D surface
K_grid_3d = np.linspace(0.1, 1.5, 50)
sigma_grid_3d = np.linspace(0, 1.2, 50)
K_mesh_3d, sigma_mesh_3d = np.meshgrid(K_grid_3d, sigma_grid_3d)

# Interpolate for 3D
abs_S_mesh_3d = griddata(
    points=(K_measured, sigma_measured),
    values=abs_S_measured,
    xi=(K_mesh_3d, sigma_mesh_3d),
    method='cubic'
)

# Plot 3D surface with full opacity for clarity
surf = ax_inset.plot_surface(K_mesh_3d, sigma_mesh_3d, abs_S_mesh_3d,
                             cmap='plasma', alpha=1.0, edgecolor='none',
                             vmin=0.5, vmax=2.9, antialiased=True)

# Add reference planes
K_plane, sigma_plane = np.meshgrid(np.linspace(0.1, 1.5, 10),
                                    np.linspace(0, 1.2, 10))

# Classical bound plane at |S|=2.0 (red/pink) - slightly more visible
classical_plane = np.ones_like(K_plane) * 2.0
ax_inset.plot_surface(K_plane, sigma_plane, classical_plane,
                     alpha=0.25, color='#FF6B9D', edgecolor='none')

# Tsirelson bound plane at |S|=2.828 (blue) - slightly more visible
tsirelson_plane = np.ones_like(K_plane) * 2.828
ax_inset.plot_surface(K_plane, sigma_plane, tsirelson_plane,
                     alpha=0.25, color='#4A90E2', edgecolor='none')

# Add wall plane at sigma=0 (showing the K-|S| profile at zero noise)
K_wall = np.linspace(0.1, 1.5, 50)
sigma_wall = np.zeros_like(K_wall)
abs_S_wall = griddata(
    points=(K_measured, sigma_measured),
    values=abs_S_measured,
    xi=(K_wall, sigma_wall),
    method='linear'
)
ax_inset.plot(K_wall, sigma_wall, abs_S_wall, color='cyan', linewidth=2, alpha=0.7)

# Add axis labels - K and σ automated, |S| manual placement
ax_inset.set_xlabel('$K$', fontsize=9, labelpad=-8)
ax_inset.set_ylabel('$\\sigma$', fontsize=9, labelpad=-8)
# Manual |S| label - nudged left off the axis line
ax_inset.text2D(0.02, 0.5, '$|S|$', transform=ax_inset.transAxes,
                fontsize=9, ha='center', va='center', rotation=90)

# Keep tick marks for grid structure but remove numeric labels for clean look
ax_inset.set_xticks([0.5, 1.0, 1.5])
ax_inset.set_yticks([0.0, 0.6, 1.2])
ax_inset.set_zticks([1.5, 2.0, 2.5])
ax_inset.set_xticklabels([])
ax_inset.set_yticklabels([])
ax_inset.set_zticklabels([])

# Keep grid subtle
ax_inset.grid(True, alpha=0.2)

# Make panes semi-transparent with thin borders
ax_inset.xaxis.pane.fill = True
ax_inset.yaxis.pane.fill = True
ax_inset.zaxis.pane.fill = True
ax_inset.xaxis.pane.set_alpha(0.05)
ax_inset.yaxis.pane.set_alpha(0.05)
ax_inset.zaxis.pane.set_alpha(0.05)
ax_inset.xaxis.pane.set_edgecolor('gray')
ax_inset.yaxis.pane.set_edgecolor('gray')
ax_inset.zaxis.pane.set_edgecolor('gray')
ax_inset.xaxis.pane.set_linewidth(0.5)
ax_inset.yaxis.pane.set_linewidth(0.5)
ax_inset.zaxis.pane.set_linewidth(0.5)

# Let axes auto-scale to data (no waterfall effect)
# ax_inset.set_xlim/ylim/zlim removed - keeps data inside grid

# Set viewing angle
ax_inset.view_init(elev=20, azim=225)

plt.tight_layout()

# Save combined figure
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig1_combined.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1_combined.png', dpi=300, bbox_inches='tight')

print("✓ Figure 1 (combined) saved!")
print("  Main panel: 2D heatmap (clean, quantitative)")
print("  Inset: 3D surface (visual impact)")

# ============================================
# COMPONENT FIGURES for reuse
# ============================================

# Fig 1a: Standalone 2D heatmap (clean, no inset)
print("\nGenerating fig1a (2D heatmap only)...")
fig_2d = plt.figure(figsize=(10, 7))
ax_2d = fig_2d.add_subplot(111)

# Recreate heatmap
im_2d = ax_2d.imshow(abs_S_mesh, cmap='plasma', aspect='auto', origin='lower',
                     extent=[0, 1.6, 0, 1.2],
                     vmin=1.5, vmax=2.8, interpolation='bilinear')

# Colorbar
cbar_2d = plt.colorbar(im_2d, ax=ax_2d, label='CHSH Parameter $|S|$')
cbar_2d.ax.axhline(y=2.0, color='red', linewidth=2.5, linestyle='-')
cbar_2d.ax.axhline(y=2.3, color='orange', linewidth=2, linestyle='--', alpha=0.7)
cbar_2d.set_ticks([1.5, 1.8, 2.0, 2.3, 2.5, 2.8])
cbar_2d.ax.tick_params(labelsize=9, width=1.5)

# Boundary line
boundary_2d = ax_2d.plot(K_line, sigma_c_line, 'k--', linewidth=4,
                         label='$\\sigma_c(K)$ boundary', zorder=5)[0]
boundary_2d.set_path_effects([patheffects.Stroke(linewidth=6, foreground='white'),
                              patheffects.Normal()])

# Optimal point
ax_2d.plot(0.7, 0.2, marker='*', markersize=30,
          color='gold', markeredgecolor='red', markeredgewidth=2,
          label='Optimal', zorder=10)

# Tested points
ax_2d.scatter(K_tested, sigma_low, s=100, c='white',
             edgecolors='black', linewidths=2.5,
             alpha=1.0, zorder=8, label='Tested points')

# Styling
ax_2d.set_xlabel('Coupling Strength $K$', fontsize=14, weight='bold')
ax_2d.set_ylabel('Noise Amplitude $\\sigma$', fontsize=14, weight='bold')
ax_2d.xaxis.labelpad = 10
ax_2d.yaxis.labelpad = 10
ax_2d.set_title('CHSH Correlation Landscape', fontsize=14, weight='bold', pad=15)
ax_2d.set_xlim(0, 1.6)
ax_2d.set_ylim(0, 1.2)
ax_2d.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, color='white')

# Legend
handles_2d, labels_2d = ax_2d.get_legend_handles_labels()
ax_2d.legend(loc='upper right', bbox_to_anchor=(0.85, 0.96),
            fontsize=10, framealpha=0.98, markerscale=0.5,
            edgecolor='black', fancybox=False)

plt.tight_layout()
plt.savefig(output_dir / 'fig1a_heatmap.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1a_heatmap.png', dpi=300, bbox_inches='tight')
plt.close(fig_2d)

print("✓ Figure 1a (2D heatmap) saved!")

# Fig 1b: Standalone 3D (cashmere minimal - full but elegant labels)
print("\nGenerating fig1b (3D standalone)...")
fig_3d = plt.figure(figsize=(10, 8))
ax_3d = fig_3d.add_subplot(111, projection='3d')

# Plot 3D surface
surf_3d = ax_3d.plot_surface(K_mesh_3d, sigma_mesh_3d, abs_S_mesh_3d,
                             cmap='plasma', alpha=1.0, edgecolor='none',
                             vmin=0.5, vmax=2.9, antialiased=True)

# Reference planes
classical_plane_3d = np.ones_like(K_plane) * 2.0
ax_3d.plot_surface(K_plane, sigma_plane, classical_plane_3d,
                  alpha=0.25, color='#FF6B9D', edgecolor='none')

tsirelson_plane_3d = np.ones_like(K_plane) * 2.828
ax_3d.plot_surface(K_plane, sigma_plane, tsirelson_plane_3d,
                  alpha=0.25, color='#4A90E2', edgecolor='none')

# Zero-noise wall
ax_3d.plot(K_wall, sigma_wall, abs_S_wall, color='cyan', linewidth=2, alpha=0.7)

# Cashmere minimal labels - elegant but informative
ax_3d.set_xlabel('Coupling Strength $K$', fontsize=12, labelpad=8)
ax_3d.set_ylabel('Noise Amplitude $\\sigma$', fontsize=12, labelpad=8)
ax_3d.set_zlabel('CHSH Parameter $|S|$', fontsize=12, labelpad=8)

# Tick labels - present but minimal
ax_3d.set_xticks([0.5, 1.0, 1.5])
ax_3d.set_yticks([0.0, 0.6, 1.2])
ax_3d.set_zticks([1.5, 2.0, 2.5, 2.828])
ax_3d.tick_params(labelsize=10)

# Grid - subtle
ax_3d.grid(True, alpha=0.3)

# Panes - elegant transparency
ax_3d.xaxis.pane.fill = True
ax_3d.yaxis.pane.fill = True
ax_3d.zaxis.pane.fill = True
ax_3d.xaxis.pane.set_alpha(0.05)
ax_3d.yaxis.pane.set_alpha(0.05)
ax_3d.zaxis.pane.set_alpha(0.05)
ax_3d.xaxis.pane.set_edgecolor('gray')
ax_3d.yaxis.pane.set_edgecolor('gray')
ax_3d.zaxis.pane.set_edgecolor('gray')
ax_3d.xaxis.pane.set_linewidth(0.5)
ax_3d.yaxis.pane.set_linewidth(0.5)
ax_3d.zaxis.pane.set_linewidth(0.5)

# Viewing angle
ax_3d.view_init(elev=20, azim=225)

# Add title - warm and elegant
ax_3d.set_title('CHSH Correlation Landscape', fontsize=14, pad=15)

plt.tight_layout()
plt.savefig(output_dir / 'fig1b_3d.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1b_3d.png', dpi=300, bbox_inches='tight')
plt.close(fig_3d)

print("✓ Figure 1b (3D standalone) saved!")
print("\n🎯 Best of both worlds: combined + components for reuse!")
