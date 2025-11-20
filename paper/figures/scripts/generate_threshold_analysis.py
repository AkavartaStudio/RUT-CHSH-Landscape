#!/usr/bin/env python3
"""
Threshold Analysis: σ_c Justification
======================================

Generates:
1. fig_S1_sigma_derivative.png - Shows ∂|S|/∂σ vs σ at K=0.7
2. table_S1_sigma_thresholds.csv - Compares σ_c at |S|=2.0 vs |S|=2.3

Purpose: Justify why we chose |S|=2.3 as the collapse threshold
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path

# Load A1 data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A1_sigma_c_K_sweep.json") as f:
    data = json.load(f)

# Extract K=0.7 data
results = data['grid_results']
K_target = 0.7

# Filter for K=0.7
k07_data = [r for r in results if abs(r['K'] - K_target) < 0.01]

# Sort by sigma
k07_data.sort(key=lambda r: r['sigma'])

# Extract arrays
sigma_vals = np.array([r['sigma'] for r in k07_data])
abs_S_vals = np.array([r['abs_S_mean'] for r in k07_data])

print(f"Found {len(k07_data)} points for K={K_target}")
print(f"σ range: [{sigma_vals.min():.2f}, {sigma_vals.max():.2f}]")
print(f"|S| range: [{abs_S_vals.min():.2f}, {abs_S_vals.max():.2f}]")

# ============================================
# A. Compute derivative ∂|S|/∂σ
# ============================================

# Use central differences for interior points
d_abs_S_d_sigma = np.zeros_like(sigma_vals)

for i in range(len(sigma_vals)):
    if i == 0:
        # Forward difference
        d_abs_S_d_sigma[i] = (abs_S_vals[i+1] - abs_S_vals[i]) / (sigma_vals[i+1] - sigma_vals[i])
    elif i == len(sigma_vals) - 1:
        # Backward difference
        d_abs_S_d_sigma[i] = (abs_S_vals[i] - abs_S_vals[i-1]) / (sigma_vals[i] - sigma_vals[i-1])
    else:
        # Central difference
        d_abs_S_d_sigma[i] = (abs_S_vals[i+1] - abs_S_vals[i-1]) / (sigma_vals[i+1] - sigma_vals[i-1])

# ============================================
# B. Compute σ_c for both thresholds
# ============================================

def find_crossing(sigma, abs_S, threshold):
    """Find σ_c where |S| crosses threshold using linear interpolation"""
    # Create interpolator
    f = interp1d(sigma, abs_S, kind='linear', fill_value='extrapolate')

    # Find crossing by root finding
    # Look for where |S|(σ) = threshold
    sigma_fine = np.linspace(sigma.min(), sigma.max(), 1000)
    abs_S_fine = f(sigma_fine)

    # Find first crossing from high |S| to low |S|
    idx = np.where(abs_S_fine < threshold)[0]
    if len(idx) == 0:
        return None  # No crossing found

    crossing_idx = idx[0]

    # Linear interpolation between the two bracketing points
    if crossing_idx > 0:
        sigma_c = sigma_fine[crossing_idx]
        return sigma_c
    else:
        return sigma_fine[0]

sigma_c_20 = find_crossing(sigma_vals, abs_S_vals, 2.0)
sigma_c_23 = find_crossing(sigma_vals, abs_S_vals, 2.3)

print(f"\n{'='*50}")
print("THRESHOLD CROSSINGS")
print(f"{'='*50}")
print(f"σ_c(|S|=2.0) = {sigma_c_20:.3f}")
print(f"σ_c(|S|=2.3) = {sigma_c_23:.3f}")
print(f"Δσ_c = {sigma_c_20 - sigma_c_23:.3f}")

# ============================================
# Generate Figure: Derivative Plot
# ============================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top panel: |S| vs σ
ax1.plot(sigma_vals, abs_S_vals, 'o-', color='steelblue',
         linewidth=2, markersize=6, label='$|S|(\\sigma)$')

# Mark thresholds
ax1.axhline(y=2.0, color='red', linewidth=2, linestyle='-', alpha=0.7, label='Classical bound')
ax1.axhline(y=2.3, color='orange', linewidth=2, linestyle='--', alpha=0.7, label='Chosen threshold')

# Mark crossings
if sigma_c_20:
    ax1.axvline(x=sigma_c_20, color='red', linewidth=1.5, linestyle=':', alpha=0.5)
    ax1.text(sigma_c_20, 1.6, f'$\\sigma_c(2.0)={sigma_c_20:.2f}$',
             ha='center', fontsize=9, color='red')

if sigma_c_23:
    ax1.axvline(x=sigma_c_23, color='orange', linewidth=1.5, linestyle=':', alpha=0.5)
    ax1.text(sigma_c_23, 1.8, f'$\\sigma_c(2.3)={sigma_c_23:.2f}$',
             ha='center', fontsize=9, color='orange')

ax1.set_ylabel('CHSH Parameter $|S|$', fontsize=12, fontweight='bold')
ax1.set_ylim(1.5, 2.9)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_title(f'Collapse Threshold Analysis at K={K_target}', fontsize=14, fontweight='bold', pad=15)

# Bottom panel: derivative
ax2.plot(sigma_vals, d_abs_S_d_sigma, 'o-', color='darkred',
         linewidth=2, markersize=6, label='$\\partial|S|/\\partial\\sigma$')
ax2.axhline(y=0, color='black', linewidth=0.8, linestyle='-', alpha=0.3)

# Mark inflection region
if sigma_c_23:
    ax2.axvline(x=sigma_c_23, color='orange', linewidth=1.5, linestyle='--', alpha=0.5)

ax2.set_xlabel('Noise Amplitude $\\sigma$', fontsize=12, fontweight='bold')
ax2.set_ylabel('$\\partial|S|/\\partial\\sigma$', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right', fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Save figure
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'figS1_sigma_derivative.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'figS1_sigma_derivative.pdf', dpi=300, bbox_inches='tight')

print(f"\n✓ Figure saved: figS1_sigma_derivative.png")

# ============================================
# Generate Table: Threshold Comparison
# ============================================

import csv

table_data = [
    ['Threshold', 'sigma_c', 'Justification'],
    ['2.0', f'{sigma_c_20:.3f}', 'Classical bound (theoretical)'],
    ['2.3', f'{sigma_c_23:.3f}', 'Practical threshold (chosen)'],
    ['Delta', f'{sigma_c_20 - sigma_c_23:.3f}', 'Difference in collapse point']
]

table_file = output_dir / 'tableS1_sigma_thresholds.csv'
with open(table_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table_data)

print(f"✓ Table saved: tableS1_sigma_thresholds.csv")

# Print table
print(f"\n{'='*60}")
print("TABLE S1: Threshold Comparison")
print(f"{'='*60}")
for row in table_data:
    print(f"{row[0]:12} {row[1]:12} {row[2]}")
print(f"{'='*60}\n")

print("✅ Threshold analysis complete!")
print(f"\nFiles created:")
print(f"  - figS1_sigma_derivative.png")
print(f"  - figS1_sigma_derivative.pdf")
print(f"  - tableS1_sigma_thresholds.csv")
