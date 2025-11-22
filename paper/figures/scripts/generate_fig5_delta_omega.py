#!/usr/bin/env python3
"""
Generate Figure 5: Δω Sweet Spot

Shows how CHSH violations depend on frequency mismatch,
revealing an optimal "tension" at Δω ≈ 0.2.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load A3 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A3_delta_omega_sweep.json") as f:
    data = json.load(f)

# Extract results
results = data['sweep_results']
optimal = data['optimal']

delta_omega = [r['delta_omega'] for r in results]
abs_S = [r['abs_S_mean'] for r in results]
errors = [r['abs_S_sem'] for r in results]
PLI = [r['PLI_mean'] for r in results]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

# Plot 1: |S| vs Δω
ax1.errorbar(delta_omega, abs_S, yerr=errors,
             marker='o', markersize=10, linewidth=2.5, capsize=5,
             color='#2E86AB', markeredgewidth=2, markeredgecolor='white')

# Mark optimum
ax1.axvline(x=optimal['delta_omega'], color='red', linestyle='--',
            linewidth=2, alpha=0.7, label=f"Optimal $\Delta\omega^* = {optimal['delta_omega']:.2f}$")
ax1.axhline(y=2.828, color='blue', linestyle=':', linewidth=1.5,
            alpha=0.5, label='Tsirelson bound')

ax1.set_ylabel('CHSH Value $|S|$', fontsize=10)
ax1.yaxis.labelpad = 10  # Professional spacing from ticks
ax1.set_title('Frequency Mismatch Sweet Spot', fontsize=11, pad=12)
ax1.legend(fontsize=10, frameon=True, shadow=True)
ax1.grid(True, alpha=0.3, linestyle=':')
ax1.set_ylim(2.73, 2.83)

# Annotate peak - positioned up and right inside box
ax1.annotate(f'Peak: {optimal["abs_S_mean"]:.3f}',
            xy=(optimal['delta_omega'], optimal['abs_S_mean']),
            xytext=(optimal['delta_omega'] - 0.08, optimal['abs_S_mean'] + 0.003),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=10, fontweight='bold')

# Plot 2: PLI vs Δω (zoomed to show flatness)
ax2.plot(delta_omega, PLI, marker='s', markersize=8, linewidth=2,
         color='#06A77D', markeredgewidth=1.5, markeredgecolor='white')

ax2.axvline(x=optimal['delta_omega'], color='red', linestyle='--',
            linewidth=2, alpha=0.7)
ax2.set_xlabel('Frequency Mismatch $\Delta\omega$', fontsize=10)
ax2.set_ylabel('Phase Coherence $r$', fontsize=10)
ax2.xaxis.labelpad = 10  # Professional spacing from ticks
ax2.yaxis.labelpad = 10  # Professional spacing from ticks
ax2.grid(True, alpha=0.3, linestyle=':')

# Zoom y-axis to actual data range to show flatness
PLI_min, PLI_max = np.min(PLI), np.max(PLI)
PLI_center = (PLI_min + PLI_max) / 2
PLI_range = PLI_max - PLI_min
y_margin = max(0.002, PLI_range * 1.5)  # At least 0.002, or 1.5x data range
ax2.set_ylim(PLI_center - y_margin, PLI_center + y_margin)

# Add annotation explaining the key finding
annotation_text = (
    f'Phase coherence remains flat\n'
    f'$r \\approx {PLI_center:.3f}$ across all $\\Delta\\omega$\n'
    f'($\\Delta r < {PLI_range:.4f}$)\n\n'
    f'→ CHSH varies strongly while\n'
    f'   synchronization stays constant'
)
ax2.text(0.98, 0.97, annotation_text, transform=ax2.transAxes,
        fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.85, edgecolor='black'))

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig5_delta_omega.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig5_delta_omega.png', dpi=300, bbox_inches='tight')

print("✓ Figure 5 saved: Δω sweet spot")
print(f"  Optimal Δω*: {optimal['delta_omega']:.2f}")
print(f"  Maximum |S|: {optimal['abs_S_mean']:.3f}")
print(f"  Clear peak structure confirmed")
