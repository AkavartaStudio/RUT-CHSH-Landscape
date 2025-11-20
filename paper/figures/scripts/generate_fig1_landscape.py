#!/usr/bin/env python3
"""
Generate Figure 1: CHSH Correlation Landscape (Parameter Space Schematic)

Beautiful visualization showing where |S| > 2 lives in (K, σ) space.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))

# Define parameter space
K = np.linspace(0, 1.6, 200)
sigma = np.linspace(0, 1.2, 200)
K_grid, sigma_grid = np.meshgrid(K, sigma)

# Create |S| landscape (approximate based on data)
def estimate_S(K_val, sigma_val):
    """Estimate |S| based on position relative to σ_c boundary"""
    if K_val < 0.15:
        return 1.5  # No violations possible

    sigma_c = 0.60 * K_val + 0.22 if K_val >= 0.3 else 0.60 * K_val + 0.10

    if sigma_val < sigma_c * 0.3:  # Deep in high-correlation zone
        return 2.8
    elif sigma_val < sigma_c * 0.6:
        return 2.6
    elif sigma_val < sigma_c * 0.9:
        return 2.4
    elif sigma_val < sigma_c:
        return 2.1
    elif sigma_val < sigma_c * 1.3:
        return 1.9
    else:
        return 1.6

# Vectorize the function
estimate_S_vec = np.vectorize(estimate_S)
S_landscape = estimate_S_vec(K_grid, sigma_grid)

# Plot contour lines instead of filled regions
# Define contour levels
contour_levels = [1.5, 1.8, 2.0, 2.3, 2.6, 2.8]

# Plot all contours
contours = ax.contour(K_grid, sigma_grid, S_landscape,
                      levels=contour_levels,
                      colors='black', linewidths=1.5, alpha=0.6)

# Label the contours
ax.clabel(contours, inline=True, fontsize=10, fmt='%.1f')

# Highlight the |S| = 2.0 classical bound with thick dashed line
classical_contour = ax.contour(K_grid, sigma_grid, S_landscape,
                               levels=[2.0],
                               colors='red', linewidths=3, linestyles='--',
                               zorder=4)

# Add grid points as tiny dots to show sampling
K_tested_grid = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
sigma_tested = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0]
for K_val in K_tested_grid:
    for sigma_val in sigma_tested:
        ax.plot(K_val, sigma_val, '.', color='gray', markersize=2, alpha=0.5, zorder=1)

# Plot σ_c(K) boundary line
K_line = np.linspace(0.2, 1.5, 100)
sigma_c_line = 0.60 * K_line + 0.22

# Adjust for saturation at high K
sigma_c_line = np.where(K_line < 0.9,
                        0.60 * K_line + 0.22,
                        0.60 * K_line + 0.22 - 0.1 * (K_line - 0.9))

ax.plot(K_line, sigma_c_line, 'b-', linewidth=3,
        label='$\\sigma_c(K)$ boundary', zorder=5, alpha=0.8)

# K=0.1 marker removed for clarity - caption discusses K_min

# Mark optimal point
ax.plot(0.7, 0.2, marker='*', markersize=25,
        color='white', markeredgecolor='black', markeredgewidth=1.5,
        label='Optimal point\\n($K=0.7$, $\\sigma=0.2$)', zorder=10)

# Mark some experimental points
K_tested = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
sigma_low = [0.2] * len(K_tested)  # Representative low-noise points
ax.scatter(K_tested, sigma_low, s=60, c='white',
           edgecolors='black', linewidths=1.5,
           alpha=0.8, zorder=8, label='Tested points')

# Add text annotations for key regions
ax.text(1.2, 0.15, 'High Correlation\n$|S| > 2.3$',
        ha='center', fontsize=11, weight='bold',
        color='darkblue', zorder=7,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='blue', linewidth=2))

# Add annotation for classical bound contour
ax.text(0.25, 0.65, '$|S| = 2.0$\nClassical bound',
        ha='center', fontsize=10, weight='bold',
        color='red', zorder=7,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red', linewidth=1.5))

# Styling
ax.set_xlabel('Coupling Strength $K$', fontsize=13, weight='bold')
ax.set_ylabel('Noise Amplitude $\\sigma$', fontsize=13, weight='bold')
ax.xaxis.labelpad = 10  # Professional spacing from ticks
ax.yaxis.labelpad = 10  # Professional spacing from ticks
ax.set_title('CHSH Correlation Landscape in Parameter Space',
             fontsize=14, weight='bold', pad=15)

ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.2)

# Light background to make contours pop
ax.set_facecolor('#F5F5F5')

# Grid for reference
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.5, color='white')

# Legend - clean and minimal
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ['Boundary', 'Optimal', 'Tested'],
          loc='upper left', fontsize=10, framealpha=0.95)

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig1_landscape.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig1_landscape.png', dpi=300, bbox_inches='tight')

print("✓ Figure 1 saved: CHSH Correlation Landscape")
print(f"  Beautiful schematic showing (K, σ) parameter space")
print(f"  Optimal point marked at (K=0.7, σ=0.2)")
print(f"  Boundary line: σ_c(K) ≈ 0.60K + 0.22")
