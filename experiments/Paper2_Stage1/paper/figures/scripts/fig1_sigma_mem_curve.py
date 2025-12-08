#!/usr/bin/env python3
"""
Paper 2 Figure 1: σ_mem(K) Curve Across the CHSH Ridge

Shows the memory-collapse threshold σ_mem as a function of coupling strength K.
Key finding: σ_mem = 0.02 uniformly across K ∈ [0.1, 1.0]

Data source: E211
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent.parent.parent / "analysis" / "data"
OUTPUT_DIR = SCRIPT_DIR.parent

# Akavarta brand colors
TEAL = "#00B4A0"
CORAL = "#FF6B6B"
GRAPHITE = "#4A4A4A"
OBSIDIAN = "#1A1A1A"
SILVER = "#C0C0C0"


def load_data():
    """Load E211 σ_mem(K) curve data"""
    with open(DATA_DIR / "memory_threshold_curve.json") as f:
        return json.load(f)


def main():
    data = load_data()

    K_values = np.array(data['K_values'])
    sigma_mem = np.array(data['sigma_mem_values'])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Main plot: σ_mem(K) curve
    ax.plot(K_values, sigma_mem, 'o-', color=CORAL, linewidth=2.5, markersize=8,
            label='σ_mem(K)', zorder=3)

    # Add horizontal reference line at σ_mem = 0.02
    ax.axhline(y=0.02, color=TEAL, linestyle='--', linewidth=1.5, alpha=0.7,
               label='σ_mem = 0.02 (constant)')

    # Shade the region where memory survives (below σ_mem)
    ax.fill_between(K_values, 0, sigma_mem, alpha=0.15, color=TEAL,
                    label='Memory survives')

    # Shade the region where memory collapses (above σ_mem)
    ax.fill_between(K_values, sigma_mem, 0.10, alpha=0.15, color=CORAL,
                    label='Memory collapsed')

    # Labels and title
    ax.set_xlabel('Coupling Strength K', fontsize=14)
    ax.set_ylabel('Memory Threshold σ_mem', fontsize=14)
    ax.set_title('Memory-Collapse Threshold Across CHSH Ridge\nσ_mem(K) from E211',
                 fontsize=16, fontweight='bold')

    # Axis limits
    ax.set_xlim(0.05, 1.05)
    ax.set_ylim(0, 0.08)

    # Grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

    # Add annotation for key finding
    ax.annotate('Key Finding:\nσ_mem = 0.02 independent of K\n(memory fragility is universal)',
                xy=(0.55, 0.02), xytext=(0.55, 0.055),
                fontsize=11, ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                         edgecolor=GRAPHITE, alpha=0.9),
                arrowprops=dict(arrowstyle='->', color=OBSIDIAN, lw=1.5))

    # Add K* marking (typical ridge peak)
    ax.axvline(x=0.6, color=SILVER, linestyle=':', alpha=0.5)
    ax.text(0.6, 0.075, 'K* = 0.6', fontsize=10, ha='center', color=GRAPHITE)

    plt.tight_layout()

    # Save figure
    output_path = OUTPUT_DIR / "fig1_sigma_mem_curve.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

    # Also save PDF for publication
    output_pdf = OUTPUT_DIR / "fig1_sigma_mem_curve.pdf"
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_pdf}")

    plt.close()

    # Print summary
    print("\nFigure 1 Summary:")
    print(f"  K range: [{K_values[0]}, {K_values[-1]}]")
    print(f"  σ_mem values: {np.unique(sigma_mem)}")
    print(f"  Finding: σ_mem = {sigma_mem[0]:.2f} uniformly across all K")


if __name__ == "__main__":
    main()
