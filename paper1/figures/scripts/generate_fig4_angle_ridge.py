#!/usr/bin/env python3
"""
Generate Figure 4: Angle Ridge Heatmap

Shows the 2D landscape of CHSH values over measurement angle space,
revealing the broad ridge and optimal geometry.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load A2 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A2_angle_ridge.json") as f:
    data = json.load(f)

# Extract results
results = data['grid_results']
optimal = data['maximum']

# Get unique Δα and Δβ values
delta_alpha_vals = sorted(list(set(r['delta_alpha'] for r in results)))
delta_beta_vals = sorted(list(set(r['delta_beta'] for r in results)))

# Create 2D grid
S_grid = np.zeros((len(delta_beta_vals), len(delta_alpha_vals)))

for r in results:
    i = delta_alpha_vals.index(r['delta_alpha'])
    j = delta_beta_vals.index(r['delta_beta'])
    S_grid[j, i] = r['abs_S_mean']

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Heatmap
im = ax.imshow(S_grid, cmap='RdYlGn', aspect='auto', origin='lower',
               extent=[delta_alpha_vals[0]-0.5, delta_alpha_vals[-1]+0.5,
                       delta_beta_vals[0]-0.5, delta_beta_vals[-1]+0.5],
               vmin=2.78, vmax=2.82)

# Colorbar
cbar = plt.colorbar(im, ax=ax, label='CHSH Value $|S|$')
cbar.ax.tick_params(labelsize=11)

# Contour lines
levels = np.linspace(2.80, 2.82, 11)
contours = ax.contour(delta_alpha_vals, delta_beta_vals, S_grid,
                      levels=levels, colors='black', alpha=0.3, linewidths=1)
ax.clabel(contours, inline=True, fontsize=9, fmt='%.3f')

# Mark optimum
ax.plot(optimal['delta_alpha'], optimal['delta_beta'], 'r*',
        markersize=25, markeredgewidth=2, markeredgecolor='white',
        label=f"Maximum: ({optimal['delta_alpha']:.0f}°, {optimal['delta_beta']:.0f}°)\n$|S| = {optimal['abs_S_mean']:.3f}$",
        zorder=10)

# Mark E104D point (90°, 75°) for comparison
# Note: This is the traditional Tsirelson-like geometry
# Δα = a' - a = 90° - 0° = 90°
# Δβ = b' - b = 120° - 45° = 75° (using standard 22.5°, 67.5° → 45° offset)
# Actually E104D used (a=0, a'=45, b=22.5, b'=67.5) so Δα=45, Δβ=45
# But the traditional reference is the symmetric case
ax.plot(98, 82, 'bs', markersize=12, markeredgewidth=2,
        markeredgecolor='white', label='Predicted optimum\n(98°, 82°)', zorder=9)

# Styling
ax.set_xlabel('$\Delta\\alpha = a\' - a$ (degrees)', fontsize=13, fontweight='bold')
ax.set_ylabel('$\Delta\\beta = b\' - b$ (degrees)', fontsize=13, fontweight='bold')
ax.xaxis.labelpad = 10  # Professional spacing from ticks
ax.yaxis.labelpad = 10  # Professional spacing from ticks
ax.set_title('CHSH Angle Ridge: Measurement Geometry Optimization',
             fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=11, frameon=True, shadow=True, loc='lower left')
ax.grid(True, alpha=0.3, linestyle=':', color='white', linewidth=0.5)

# Set ticks
ax.set_xticks(delta_alpha_vals)
ax.set_yticks(delta_beta_vals)

# Add text annotation
ax.text(0.98, 0.02, 'Broad ridge:\nRobust to angle choice',
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig4_angle_ridge.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig4_angle_ridge.png', dpi=300, bbox_inches='tight')

print("✓ Figure 4 saved: Angle ridge heatmap")
print(f"  Optimum: (Δα={optimal['delta_alpha']:.0f}°, Δβ={optimal['delta_beta']:.0f}°)")
print(f"  Maximum |S|: {optimal['abs_S_mean']:.3f}")
print(f"  Ridge width: ~4° × ~6°")
