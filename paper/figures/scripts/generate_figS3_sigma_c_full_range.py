#!/usr/bin/env python3
"""
Extended σ_c(K) Curve - Full Range
===================================

Generates:
1. figS3_sigma_c_full_range.png - σ_c(K) curve using |S|=2.3 threshold
2. tableS3_sigma_c_full_range.csv - K, sigma_c_2p3 data

Shows:
- No-violation zone at low K
- Linear mid-range (where we fit)
- Saturation/bending at high K
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path
import csv

# Load A1 data (original + extended)
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "A1_sigma_c_K_sweep.json") as f:
    data1 = json.load(f)

# Load extended data
try:
    with open(data_dir / "A1_extended_sigma_sweep.json") as f:
        data_ext = json.load(f)
    extended_results = data_ext['results']
except FileNotFoundError:
    extended_results = []

# Merge results
results = data1['grid_results'] + extended_results
K_values = sorted(set(r['K'] for r in results))

print(f"Computing σ_c(K) for {len(K_values)} K values")
print(f"K range: [{min(K_values)}, {max(K_values)}]")
print(f"Threshold: |S| = 2.3")
print()

# ============================================
# Compute σ_c for each K
# ============================================

threshold = 2.3

def find_sigma_c(K_val, results, threshold):
    """Find σ_c where |S| crosses threshold for given K"""
    # Get data for this K
    K_data = [r for r in results if abs(r['K'] - K_val) < 0.01]
    K_data.sort(key=lambda r: r['sigma'])

    sigma_vals = np.array([r['sigma'] for r in K_data])
    abs_S_vals = np.array([r['abs_S_mean'] for r in K_data])

    # Check if we ever reach the threshold
    if abs_S_vals.max() < threshold:
        return None  # Never reaches threshold

    # Find crossing
    f = interp1d(sigma_vals, abs_S_vals, kind='linear', fill_value='extrapolate')

    # Find where |S| = threshold
    sigma_fine = np.linspace(sigma_vals.min(), sigma_vals.max(), 1000)
    abs_S_fine = f(sigma_fine)

    idx = np.where(abs_S_fine < threshold)[0]
    if len(idx) == 0:
        return None

    return sigma_fine[idx[0]]

# Compute σ_c for each K
K_list = []
sigma_c_list = []

print("K       σ_c(2.3)")
print("-" * 25)

for K_val in K_values:
    sigma_c = find_sigma_c(K_val, results, threshold)

    if sigma_c is not None:
        K_list.append(K_val)
        sigma_c_list.append(sigma_c)
        print(f"{K_val:4.1f}    {sigma_c:6.3f}")
    else:
        print(f"{K_val:4.1f}    (no crossing)")

# Convert to arrays
K_arr = np.array(K_list)
sigma_c_arr = np.array(sigma_c_list)

# ============================================
# Generate Figure (same style as Fig 2)
# ============================================

fig, ax = plt.subplots(figsize=(10, 7))

# Plot data points
ax.plot(K_arr, sigma_c_arr, 'o', markersize=10, color='steelblue',
        markeredgecolor='darkblue', markeredgewidth=1.5, label='Computed $\\sigma_c(K)$')

# Add linear fit for mid-range (K ∈ [0.3, 0.9] like in paper)
fit_mask = (K_arr >= 0.3) & (K_arr <= 0.9)
if fit_mask.sum() > 0:
    K_fit = K_arr[fit_mask]
    sigma_c_fit = sigma_c_arr[fit_mask]

    # Linear fit
    coeffs = np.polyfit(K_fit, sigma_c_fit, 1)
    slope, intercept = coeffs

    # Plot fit line
    K_line = np.linspace(0, K_arr.max(), 100)
    sigma_c_line = slope * K_line + intercept

    ax.plot(K_line, sigma_c_line, '--', linewidth=2, color='red', alpha=0.7,
            label=f'Linear fit: $\\sigma_c = {slope:.3f}K + {intercept:.3f}$')

    # Compute R²
    residuals = sigma_c_fit - (slope * K_fit + intercept)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((sigma_c_fit - np.mean(sigma_c_fit))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # Add text annotation
    ax.text(0.05, 0.95, f'Linear region: K ∈ [0.3, 0.9]\\nR² = {r_squared:.4f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Labels
ax.set_xlabel('Coupling Strength $K$', fontsize=13, fontweight='bold')
ax.set_ylabel('Collapse Threshold $\\sigma_c(K)$ at $|S|=2.3$', fontsize=13, fontweight='bold')
ax.set_title('Extended $\\sigma_c(K)$ Curve: Full Range', fontsize=14, fontweight='bold', pad=15)

# Grid
ax.grid(True, alpha=0.3, linestyle='--')

# Legend
ax.legend(loc='upper left', fontsize=11, framealpha=0.95)

# Set limits
ax.set_xlim(0, K_arr.max() * 1.05)
ax.set_ylim(0, sigma_c_arr.max() * 1.1)

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'figS3_sigma_c_full_range.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'figS3_sigma_c_full_range.pdf', dpi=300, bbox_inches='tight')

print(f"\n✓ Figure saved: figS3_sigma_c_full_range.png")

# ============================================
# Export CSV
# ============================================

csv_file = output_dir / 'tableS3_sigma_c_full_range.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['K', 'sigma_c_2p3'])

    for K_val, sigma_c in zip(K_list, sigma_c_list):
        writer.writerow([f'{K_val:.2f}', f'{sigma_c:.3f}'])

print(f"✓ Table saved: tableS3_sigma_c_full_range.csv")

# Print summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"K range: [{K_arr.min():.1f}, {K_arr.max():.1f}]")
print(f"σ_c range: [{sigma_c_arr.min():.3f}, {sigma_c_arr.max():.3f}]")
print(f"Linear region slope: {slope:.3f}")
print(f"Linear region intercept: {intercept:.3f}")
print(f"R²: {r_squared:.4f}")
print(f"\nFiles created:")
print(f"  - figS3_sigma_c_full_range.png")
print(f"  - figS3_sigma_c_full_range.pdf")
print(f"  - tableS3_sigma_c_full_range.csv")
print(f"{'='*60}\n")
