#!/usr/bin/env python3
"""
Paper 2 - Mission 3: Derive Echo and χ Surfaces from E221

Pure analysis script - no simulation, just transforms E221 memory curvature data
into echo surfaces and recursive susceptibility (χ) surfaces.

Inputs:
  - Paper2_Mission2/analysis/data/E221_memory_curvature_surface.json

Outputs:
  - P2_echo_surface_tau50.json      : ρ_S(τ=50) over (K, σ) grid
  - P2_chi_mid_surface.json         : χ_mid = C_mem(37.5) × ρ_S(50) surface
  - P2_chi_short_surface.json       : χ_short = C_mem(17.5) × ρ_S(50) surface
  - P2_chi_long_surface.json        : χ_long = C_mem(75.0) × ρ_S(50) surface
  - P2_chi_mid_boundary.json        : (K, σ) pairs where χ_mid changes sign

Physical interpretation:
  - ρ_S(τ): Echo strength - how much the CHSH signal "remembers" itself at lag τ
  - C_mem(τ_mid): Memory curvature - rate of echo decay at intermediate lag
  - χ = C_mem × ρ_S: Recursive susceptibility - how strongly memory decay
    couples to echo persistence. Sign changes indicate regime transitions.
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

# Paths
SCRIPT_DIR = Path(__file__).parent
MISSION2_DATA = SCRIPT_DIR.parent.parent / "Paper2_Mission2" / "analysis" / "data"
OUTPUT_DIR = SCRIPT_DIR / "data"


def load_e221() -> dict:
    """Load E221 memory curvature surface data."""
    e221_path = MISSION2_DATA / "E221_memory_curvature_surface.json"
    if not e221_path.exists():
        raise FileNotFoundError(
            f"E221 data not found at {e221_path}. "
            "Run E221_memory_curvature_surface.py first."
        )
    with open(e221_path) as f:
        return json.load(f)


def extract_surfaces(e221: dict) -> Dict[str, np.ndarray]:
    """
    Extract 2D surfaces from E221 entries.

    Returns dict with:
      - rho_S_50: echo surface at τ=50
      - C_mem_short: curvature at τ_mid=17.5
      - C_mem_mid: curvature at τ_mid=37.5
      - C_mem_long: curvature at τ_mid=75.0
    """
    K_values = e221['K_values']
    sigma_values = e221['sigma_values']
    entries = e221['entries']

    n_K = len(K_values)
    n_sigma = len(sigma_values)

    # Initialize arrays
    rho_S_50 = np.zeros((n_K, n_sigma))
    C_mem_short = np.zeros((n_K, n_sigma))
    C_mem_mid = np.zeros((n_K, n_sigma))
    C_mem_long = np.zeros((n_K, n_sigma))

    # Build (K, sigma) -> entry lookup
    entry_map = {}
    for entry in entries:
        key = (entry['K'], entry['sigma'])
        entry_map[key] = entry

    # Fill surfaces
    for i, K in enumerate(K_values):
        for j, sigma in enumerate(sigma_values):
            entry = entry_map.get((K, sigma))
            if entry is None:
                continue

            # Extract ρ_S(τ=50)
            rho_50 = entry['rho_by_tau'].get('50', {}).get('mean', 0.0)
            rho_S_50[i, j] = rho_50

            # Extract curvatures
            for curv in entry['curvature']:
                tau_mid = curv['tau_mid']
                c_mem = curv['C_mem']

                if tau_mid == 17.5:
                    C_mem_short[i, j] = c_mem
                elif tau_mid == 37.5:
                    C_mem_mid[i, j] = c_mem
                elif tau_mid == 75.0:
                    C_mem_long[i, j] = c_mem

    return {
        'rho_S_50': rho_S_50,
        'C_mem_short': C_mem_short,
        'C_mem_mid': C_mem_mid,
        'C_mem_long': C_mem_long
    }


def compute_chi_surfaces(surfaces: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Compute χ = C_mem × ρ_S surfaces.

    χ represents "recursive susceptibility" - how memory curvature
    couples to echo persistence. Sign changes mark regime boundaries.
    """
    rho = surfaces['rho_S_50']

    return {
        'chi_short': surfaces['C_mem_short'] * rho,
        'chi_mid': surfaces['C_mem_mid'] * rho,
        'chi_long': surfaces['C_mem_long'] * rho
    }


def find_sign_change_boundary(
    surface: np.ndarray,
    K_values: List[float],
    sigma_values: List[float]
) -> List[Dict[str, Any]]:
    """
    Find approximate (K, σ) locations where surface changes sign between neighbors.

    Returns list of boundary point dicts with:
      - K, sigma: midpoint coordinates
      - direction: 'horizontal' or 'vertical'
      - sign_change: e.g. 'neg_to_pos' or 'pos_to_neg'
    """
    boundary_points = []
    n_K, n_sigma = surface.shape

    # Check horizontal neighbors (along σ axis)
    for i in range(n_K):
        for j in range(n_sigma - 1):
            v1, v2 = surface[i, j], surface[i, j+1]
            if v1 * v2 < 0:  # Sign change
                boundary_points.append({
                    'K': K_values[i],
                    'sigma': (sigma_values[j] + sigma_values[j+1]) / 2,
                    'direction': 'horizontal',
                    'sign_change': 'neg_to_pos' if v1 < 0 else 'pos_to_neg',
                    'values': [float(v1), float(v2)]
                })

    # Check vertical neighbors (along K axis)
    for i in range(n_K - 1):
        for j in range(n_sigma):
            v1, v2 = surface[i, j], surface[i+1, j]
            if v1 * v2 < 0:  # Sign change
                boundary_points.append({
                    'K': (K_values[i] + K_values[i+1]) / 2,
                    'sigma': sigma_values[j],
                    'direction': 'vertical',
                    'sign_change': 'neg_to_pos' if v1 < 0 else 'pos_to_neg',
                    'values': [float(v1), float(v2)]
                })

    return boundary_points


def save_surface(
    filename: str,
    K_values: List[float],
    sigma_values: List[float],
    surface: np.ndarray,
    metadata: Dict[str, Any]
) -> Path:
    """Save a 2D surface to JSON."""
    output = {
        'timestamp': datetime.now().isoformat(),
        'K_values': K_values,
        'sigma_values': sigma_values,
        'surface': surface.tolist(),
        **metadata
    }

    path = OUTPUT_DIR / filename
    with open(path, 'w') as f:
        json.dump(output, f, indent=2)

    return path


def main():
    print("=" * 80)
    print("Paper 2 - Mission 3: Build Echo and χ Surfaces")
    print("=" * 80)
    print()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load E221 data
    print("Loading E221 memory curvature surface...")
    try:
        e221 = load_e221()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Please run E221 first, then rerun this script.")
        return

    K_values = e221['K_values']
    sigma_values = e221['sigma_values']

    print(f"  Grid: {len(K_values)} K × {len(sigma_values)} σ")
    print(f"  K range: [{K_values[0]}, {K_values[-1]}]")
    print(f"  σ range: [{sigma_values[0]}, {sigma_values[-1]}]")
    print()

    # Extract surfaces
    print("Extracting surfaces from E221 entries...")
    surfaces = extract_surfaces(e221)

    # Compute χ surfaces
    print("Computing χ = C_mem × ρ_S surfaces...")
    chi_surfaces = compute_chi_surfaces(surfaces)

    print()
    print("=" * 80)
    print("SAVING OUTPUTS")
    print("=" * 80)
    print()

    # Save echo surface
    path = save_surface(
        "P2_echo_surface_tau50.json",
        K_values, sigma_values,
        surfaces['rho_S_50'],
        {
            'description': 'Echo surface: ρ_S(τ=50) over (K, σ) grid',
            'tau': 50,
            'source': 'E221_memory_curvature_surface.json'
        }
    )
    print(f"Saved: {path}")

    # Save χ surfaces
    for name, tau_mid, key in [
        ('P2_chi_short_surface.json', 17.5, 'chi_short'),
        ('P2_chi_mid_surface.json', 37.5, 'chi_mid'),
        ('P2_chi_long_surface.json', 75.0, 'chi_long')
    ]:
        path = save_surface(
            name,
            K_values, sigma_values,
            chi_surfaces[key],
            {
                'description': f'Recursive susceptibility χ = C_mem({tau_mid}) × ρ_S(50)',
                'tau_mid': tau_mid,
                'formula': 'chi = C_mem(tau_mid) * rho_S(50)',
                'source': 'E221_memory_curvature_surface.json'
            }
        )
        print(f"Saved: {path}")

    # Find and save χ_mid sign-change boundary
    print()
    print("Finding χ_mid sign-change boundary...")
    boundary = find_sign_change_boundary(chi_surfaces['chi_mid'], K_values, sigma_values)

    boundary_output = {
        'timestamp': datetime.now().isoformat(),
        'description': 'Sign-change boundary for χ_mid = C_mem(37.5) × ρ_S(50)',
        'n_boundary_points': len(boundary),
        'boundary_points': boundary,
        'source': 'E221_memory_curvature_surface.json'
    }

    boundary_path = OUTPUT_DIR / "P2_chi_mid_boundary.json"
    with open(boundary_path, 'w') as f:
        json.dump(boundary_output, f, indent=2)
    print(f"Saved: {boundary_path}")
    print(f"  Found {len(boundary)} boundary crossing points")

    # Print summary statistics
    print()
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()

    print("Echo Surface ρ_S(τ=50):")
    rho = surfaces['rho_S_50']
    print(f"  Range: [{rho.min():.6f}, {rho.max():.6f}]")
    print(f"  Mean: {rho.mean():.6f}")
    print(f"  At σ=0: mean ρ = {rho[:, 0].mean():.4f}")
    print()

    for name, tau_mid, chi in [
        ('χ_short', 17.5, chi_surfaces['chi_short']),
        ('χ_mid', 37.5, chi_surfaces['chi_mid']),
        ('χ_long', 75.0, chi_surfaces['chi_long'])
    ]:
        print(f"{name} (τ_mid = {tau_mid}):")
        print(f"  Range: [{chi.min():.8f}, {chi.max():.8f}]")
        pos_frac = np.sum(chi > 0) / chi.size * 100
        neg_frac = np.sum(chi < 0) / chi.size * 100
        print(f"  Sign: {pos_frac:.1f}% positive, {neg_frac:.1f}% negative")

        # Find where max |χ| occurs
        max_idx = np.unravel_index(np.argmax(np.abs(chi)), chi.shape)
        print(f"  Max |χ| at K={K_values[max_idx[0]]:.2f}, σ={sigma_values[max_idx[1]]:.2f}")
        print()

    print("=" * 80)
    print("Mission 3 Analysis COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
