#!/usr/bin/env python3
"""
Generate Figure 2: σ_c vs K Scaling Law

Shows the linear relationship between coupling strength K
and critical noise σ_c where violations collapse.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load A1 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A1_sigma_c_K_sweep.json") as f:
    data = json.load(f)

# Extract scaling law
analysis = data['sigma_c_analysis']
K_values = analysis['K_values']
sigma_c_values = analysis['sigma_c_values']
fit = analysis['linear_fit']

# Create figure
fig, ax = plt.subplots(figsize=(6, 5))

# Plot data points
ax.plot(K_values, sigma_c_values, 'o', markersize=10,
        color='#2E86AB', markeredgewidth=2, markeredgecolor='white',
        label='Measured $\sigma_c$', zorder=3)

# Plot fit line
K_fit = np.linspace(min(K_values) - 0.1, max(K_values) + 0.1, 100)
sigma_fit = fit['slope'] * K_fit + fit['intercept']
ax.plot(K_fit, sigma_fit, '--', linewidth=2, color='#A23B72',
        label=f"$\sigma_c = {fit['slope']:.3f}K + {fit['intercept']:.3f}$\n$R^2 = {fit['r_squared']:.4f}$")

# Styling - match paper body text size
ax.set_xlabel('Coupling Strength $K$', fontsize=10)
ax.set_ylabel('Critical Noise $\sigma_c$', fontsize=10)
ax.xaxis.labelpad = 10  # Professional spacing from ticks
ax.yaxis.labelpad = 10  # Professional spacing from ticks
ax.set_title('Noise-Coupling Scaling Law', fontsize=11, pad=12)
ax.legend(fontsize=11, frameon=True, shadow=True, loc='upper left')
ax.grid(True, alpha=0.3, linestyle=':')
ax.set_xlim(0.2, 1.0)
ax.set_ylim(0.2, 0.9)

# Add annotation (moved down and right to avoid obscuring data)
ax.annotate('Linear scaling:\nviolations require\n$K$-dependent coherence',
            xy=(0.65, 0.35), fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
output_dir.mkdir(exist_ok=True, parents=True)
plt.savefig(output_dir / 'fig2_sigma_c_scaling.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'fig2_sigma_c_scaling.png', dpi=300, bbox_inches='tight')

print("✓ Figure 2 saved: σ_c vs K scaling law")
print(f"  Slope: {fit['slope']:.3f}")
print(f"  Intercept: {fit['intercept']:.3f}")
print(f"  R²: {fit['r_squared']:.4f}")
