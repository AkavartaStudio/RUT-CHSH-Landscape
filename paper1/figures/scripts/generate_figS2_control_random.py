#!/usr/bin/env python3
"""
Generate Figure S2 (Supplementary): Control Random Parameter Study

Histogram showing random parameter choices yield |S| < 2,
proving optimized parameters are special.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load control data
data_dir = Path(__file__).parent.parent.parent.parent / "analysis" / "data" / "paper1"
with open(data_dir / "CONTROL_random_params.json") as f:
    data = json.load(f)

# Extract |S| values
random_abs_S = np.array([r['abs_S'] for r in data['random_results']])
optimized_abs_S = np.array([r['abs_S'] for r in data['optimized_results']])

stats = data['statistics']

# Create figure with two panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Histogram of random |S| values
ax1.hist(random_abs_S, bins=30, color='#cccccc', edgecolor='black',
         alpha=0.7, label=f'Random (N={len(random_abs_S)})')

# Add vertical lines for reference
ax1.axvline(x=2.0, color='red', linestyle='--', linewidth=2,
            label='Classical bound', alpha=0.8)
ax1.axvline(x=2.828, color='blue', linestyle=':', linewidth=2,
            label='Tsirelson bound', alpha=0.6)

# Mark mean and std
mean_random = stats['random']['mean']
std_random = stats['random']['std']
ax1.axvline(x=mean_random, color='black', linestyle='-', linewidth=2,
            label=f'Mean: {mean_random:.2f} ± {std_random:.2f}')
ax1.axvspan(mean_random - std_random, mean_random + std_random,
            alpha=0.2, color='gray', label='±1 SD')

# Mark optimized mean
mean_opt = stats['optimized']['mean']
ax1.axvline(x=mean_opt, color='#06A77D', linestyle='-', linewidth=3,
            label=f'Optimized: {mean_opt:.2f}', zorder=10)

ax1.set_xlabel('CHSH Value $|S|$', fontsize=13, fontweight='bold')
ax1.set_ylabel('Count', fontsize=13, fontweight='bold')
ax1.xaxis.labelpad = 10  # Professional spacing from ticks
ax1.yaxis.labelpad = 10  # Professional spacing from ticks
ax1.set_title('Random Parameter Distribution', fontsize=14, fontweight='bold')
ax1.legend(fontsize=8, loc='upper left')  # Smaller legend
ax1.grid(True, alpha=0.3, axis='y', linestyle=':')
ax1.set_xlim(0, 3)

# Add text box with statistics - smaller and moved more towards center
textstr = '\n'.join([
    f"Random configs:",
    f"  {stats['random']['frac_above_2']*100:.1f}% exceed 2.0",
    f"  {stats['random']['frac_above_2p5']*100:.1f}% exceed 2.5",
    f"",
    f"Optimized config:",
    f"  {stats['optimized']['frac_above_2']*100:.0f}% exceed 2.0"
])
ax1.text(0.92, 0.97, textstr, transform=ax1.transAxes, fontsize=8,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Panel 2: Violin plot comparing distributions
parts = ax2.violinplot([random_abs_S, optimized_abs_S],
                       positions=[1, 2],
                       showmeans=True, showmedians=True, showextrema=True)

# Color the violins
for pc in parts['bodies']:
    pc.set_facecolor('#cccccc')
    pc.set_alpha(0.7)

# Add scatter points
np.random.seed(42)
jitter = 0.04
ax2.scatter(np.ones(len(random_abs_S)) + np.random.normal(0, jitter, len(random_abs_S)),
           random_abs_S, alpha=0.3, s=20, color='gray', label='Random')
ax2.scatter(2*np.ones(len(optimized_abs_S)) + np.random.normal(0, jitter, len(optimized_abs_S)),
           optimized_abs_S, alpha=0.8, s=50, color='#06A77D',
           edgecolor='black', linewidth=1, label='Optimized', zorder=10)

# Add classical bound line
ax2.axhline(y=2.0, color='red', linestyle='--', linewidth=2, alpha=0.8)
ax2.axhline(y=2.828, color='blue', linestyle=':', linewidth=2, alpha=0.6)

# Add significance annotation
cohens_d = stats['comparison']['cohens_d']
p_value = stats['comparison']['p_value']
percentile = stats['comparison']['percentile_rank']

sig_text = f"Cohen's d = {cohens_d:.2f}\np < {p_value:.1e}\n{percentile:.0f}th percentile"
ax2.text(0.5, 0.88, sig_text, transform=ax2.transAxes,
         fontsize=9, fontweight='bold', verticalalignment='top',
         horizontalalignment='center',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

ax2.set_xticks([1, 2])
ax2.set_xticklabels(['Random\nParameters', 'Optimized\nParameters'], fontsize=12)
ax2.set_ylabel('CHSH Value $|S|$', fontsize=13, fontweight='bold')
ax2.yaxis.labelpad = 10  # Professional spacing from ticks
ax2.set_title('Statistical Comparison', fontsize=14, fontweight='bold')
ax2.set_ylim(0, 3)
ax2.grid(True, alpha=0.3, axis='y', linestyle=':')

# Main title
fig.suptitle('Control Study: Random vs. Optimized Parameters',
             fontsize=16, fontweight='bold', y=1.00)

plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent
plt.savefig(output_dir / 'figS2_control_random.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'figS2_control_random.png', dpi=300, bbox_inches='tight')

print("✓ Figure S2 saved: Control random parameter study")
print(f"  Random mean:    {mean_random:.3f} ± {std_random:.3f}")
print(f"  Optimized mean: {mean_opt:.3f}")
print(f"  Effect size:    Cohen's d = {cohens_d:.2f}")
print(f"  Significance:   p < {p_value:.1e}")
print(f"  Percentile:     {percentile:.1f}th")
