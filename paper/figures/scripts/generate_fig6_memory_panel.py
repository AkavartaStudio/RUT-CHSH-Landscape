#!/usr/bin/env python3
"""
Generate Figure 6: Memory Beyond Violations Panel

Shows that memory (PLI, ρ_S) persists even after CHSH violations
vanish at the classical bound.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load B1 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "B1_minimal_echo.json") as f:
    data = json.load(f)

# Extract results
results = data['results']

sigma_names = [r['sigma_name'].capitalize() for r in results]
sigma_values = [r['sigma'] for r in results]
abs_S = [r['abs_S_mean'] for r in results]
abs_S_err = [r['abs_S_std'] for r in results]
PLI = [r['PLI_mean'] for r in results]
PLI_err = [r['PLI_std'] for r in results]
rho_S = [r['rho_S_autocorr_mean'] for r in results]
rho_S_err = [r['rho_S_autocorr_std'] for r in results]

# Create figure with three subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

x_pos = np.arange(len(sigma_names))
width = 0.6

# Panel 1: |S|
ax1 = axes[0]
bars1 = ax1.bar(x_pos, abs_S, width, yerr=abs_S_err,
                color=['#06A77D', '#F77F00', '#E63946'],
                edgecolor='black', linewidth=1.5, capsize=8)
ax1.axhline(y=2.0, color='red', linestyle='--', linewidth=2,
            label='Classical bound', alpha=0.7)
ax1.set_ylabel('CHSH Value $|S|$', fontsize=10)
ax1.yaxis.labelpad = 10  # Professional spacing from ticks
ax1.set_title('Violations Vanish', fontsize=11)
ax1.set_xticks(x_pos)
ax1.set_xticklabels([f'{n}\n($\sigma={v:.1f}$)' for n, v in zip(sigma_names, sigma_values)])
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, alpha=0.3, axis='y', linestyle=':')
ax1.set_ylim(0, 3)

# Panel 2: PLI
ax2 = axes[1]
bars2 = ax2.bar(x_pos, PLI, width, yerr=PLI_err,
                color=['#06A77D', '#F77F00', '#E63946'],
                edgecolor='black', linewidth=1.5, capsize=8)
ax2.set_ylabel('Phase Coherence r', fontsize=10)
ax2.yaxis.labelpad = 10  # Professional spacing from ticks
ax2.set_title('Phase Coherence Decays', fontsize=11)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'{n}\n($\sigma={v:.1f}$)' for n, v in zip(sigma_names, sigma_values)])
ax2.grid(True, alpha=0.3, axis='y', linestyle=':')
ax2.set_ylim(0, 1.1)

# Panel 3: ρ_S
ax3 = axes[2]
bars3 = ax3.bar(x_pos, rho_S, width, yerr=rho_S_err,
                color=['#06A77D', '#F77F00', '#E63946'],
                edgecolor='black', linewidth=1.5, capsize=8)
ax3.set_ylabel('Temporal Coherence $\\rho_S$', fontsize=10)
ax3.yaxis.labelpad = 10  # Professional spacing from ticks
ax3.set_title('Memory Persists!', fontsize=11, color='#E63946')
ax3.set_xticks(x_pos)
ax3.set_xticklabels([f'{n}\n($\sigma={v:.1f}$)' for n, v in zip(sigma_names, sigma_values)])
ax3.grid(True, alpha=0.3, axis='y', linestyle=':')
ax3.set_ylim(0, 1.1)

# Add annotation on panel 3 - moved left with smaller font
ax3.annotate('High coherence\ndespite no violations!',
            xy=(2, rho_S[2]), xytext=(0.8, 0.95),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=9, fontweight='bold', color='#E63946',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.3))

fig.suptitle('Memory Beyond Violations: Evidence of Structural Persistence',
             fontsize=12, y=1.02)

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'fig6_memory_panel.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig6_memory_panel.png', dpi=300, bbox_inches='tight')

print("✓ Figure 6 saved: Memory beyond violations panel")
print(f"  Ridge: |S|={abs_S[0]:.2f}, ρ_S={rho_S[0]:.2f}")
print(f"  Boundary: |S|={abs_S[1]:.2f}, ρ_S={rho_S[1]:.2f}")
print(f"  Classical: |S|={abs_S[2]:.2f}, ρ_S={rho_S[2]:.2f}")
print(f"  → Memory persists while violations vanish!")
