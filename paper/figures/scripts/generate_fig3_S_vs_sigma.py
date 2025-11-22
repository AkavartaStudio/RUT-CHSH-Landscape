#!/usr/bin/env python3
"""
Generate Figure 3: |S| vs σ for Multiple K Values

Shows how CHSH violations decay with noise for different
coupling strengths, illustrating the collapse at σ_c.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load A1 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A1_sigma_c_K_sweep.json") as f:
    data = json.load(f)

# Extract grid results
results = data['grid_results']

# Organize by K
K_values = sorted(list(set(r['K'] for r in results)))
# Extended color palette for more K values
colors = ['#E63946', '#F77F00', '#06A77D', '#2E86AB', '#9D4EDD', '#FF006E', '#8338EC', '#3A86FF', '#FB5607', '#FFBE0B', '#06FFA5', '#FF1654']

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))

for i, K in enumerate(K_values):
    K_data = [r for r in results if r['K'] == K]
    K_data_sorted = sorted(K_data, key=lambda r: r['sigma'])

    sigmas = [r['sigma'] for r in K_data_sorted]
    abs_S = [r['abs_S_mean'] for r in K_data_sorted]
    errors = [r['abs_S_sem'] for r in K_data_sorted]

    ax.errorbar(sigmas, abs_S, yerr=errors,
                marker='o', markersize=8, linewidth=2, capsize=5,
                color=colors[i], label=f'$K = {K}$', alpha=0.9)

# Add bounds
ax.axhline(y=2.0, color='red', linestyle='--', linewidth=2,
           label='Classical bound', alpha=0.7)
ax.axhline(y=2.828, color='blue', linestyle=':', linewidth=2,
           label='$2\sqrt{2}$', alpha=0.7)

# Styling - match paper body text size
ax.set_xlabel('Noise Level $\sigma$', fontsize=10)
ax.set_ylabel('CHSH Value $|S|$', fontsize=10)
ax.xaxis.labelpad = 10  # Professional spacing from ticks
ax.yaxis.labelpad = 10  # Professional spacing from ticks
ax.set_title('CHSH Violations vs Noise: Collapse at $\sigma_c(K)$',
             fontsize=11, pad=12)
# Move legend up and give breathing room - upper left with offset
ax.legend(fontsize=8, frameon=True, shadow=True, loc='upper left',
          bbox_to_anchor=(0.02, 0.75), ncol=1)
ax.grid(True, alpha=0.3, linestyle=':')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0.5, 3.0)

# Add shaded region for violations
ax.fill_between([-0.1, 1.1], 2.0, 3.0, alpha=0.1, color='green',
                label='Violation region')

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig3_S_vs_sigma.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig3_S_vs_sigma.png', dpi=300, bbox_inches='tight')

print("✓ Figure 3 saved: |S| vs σ for multiple K")
print(f"  K values: {K_values}")
print(f"  Clear collapse at σ_c for each K")
