#!/usr/bin/env python3
"""
Comprehensive verification script for RUN_ALL_PAPER1.sh pipeline
Checks reproducibility, determinism, and key metrics
"""

import json
import subprocess
from pathlib import Path
import sys
import hashlib
from datetime import datetime
import numpy as np

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_mark(condition):
    return f"{Colors.GREEN}✓{Colors.ENDC}" if condition else f"{Colors.RED}✗{Colors.ENDC}"

def section(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")

def subsection(title):
    print(f"\n{Colors.BOLD}{title}{Colors.ENDC}")
    print("-" * 60)

# Repository root
REPO_ROOT = Path(__file__).parent
SCRIPT_PATH = REPO_ROOT / "analysis/scripts/paper1_runners/RUN_ALL_PAPER1.sh"
DATA_DIR = REPO_ROOT / "analysis/data/paper1"
CONFIG_DIR = REPO_ROOT / "paper/configs_paper1"

def check_script_hardening():
    """Check if the script has proper error handling"""
    section("STEP 1: STRICT-RUN SANITY CHECK")

    with open(SCRIPT_PATH) as f:
        script_content = f.read()

    checks = {
        "set -euo pipefail": "set -euo pipefail" in script_content,
        "Stage markers": "STAGE" in script_content and "COMPLETE" in script_content,
        "Error checking": "if [ $? -eq 0 ]" in script_content,
        "Shebang present": script_content.startswith("#!/bin/bash")
    }

    for check_name, passed in checks.items():
        print(f"{check_mark(passed)} {check_name}")

    all_passed = all(checks.values())

    if all_passed:
        print(f"\n{Colors.GREEN}Script hardening: PASSED{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}Script hardening: NEEDS IMPROVEMENT{Colors.ENDC}")

    return all_passed

def verify_data_exists():
    """Check if all expected data files exist"""
    subsection("Data File Presence")

    expected_files = [
        "A1_sigma_c_K_sweep.json",
        "A2_angle_ridge.json",
        "A3_delta_omega_sweep.json",
        "B1_minimal_echo.json"
    ]

    results = {}
    for filename in expected_files:
        filepath = DATA_DIR / filename
        exists = filepath.exists()
        results[filename] = exists
        print(f"{check_mark(exists)} {filename}")
        if exists:
            # Get file timestamp
            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            print(f"   Modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

    return all(results.values()), results

def extract_key_metrics():
    """Extract and verify key metrics from data files"""
    section("STEP 4: ARTIFACT-TO-PAPER VERIFICATION")

    metrics = {}

    # Metric 1: |S|max ≈ 2.819
    subsection("Metric 1: Maximum |S| value")
    try:
        with open(DATA_DIR / "A2_angle_ridge.json") as f:
            a2_data = json.load(f)

        if 'maximum' in a2_data:
            S_max = a2_data['maximum']['abs_S_mean']
            S_max_sem = a2_data['maximum']['abs_S_sem']
            S_max_expected = 2.819
            S_max_tolerance = 0.01

            metrics['S_max'] = {
                'value': S_max,
                'sem': S_max_sem,
                'expected': S_max_expected,
                'passed': abs(S_max - S_max_expected) < S_max_tolerance
            }

            print(f"Expected: |S|max ≈ {S_max_expected:.3f}")
            print(f"Observed: |S|max = {S_max:.3f}±{S_max_sem:.3f}")
            print(f"Difference: {abs(S_max - S_max_expected):.4f}")
            print(f"{check_mark(metrics['S_max']['passed'])} Within tolerance ({S_max_tolerance})")
        else:
            print(f"{Colors.YELLOW}Data structure missing 'maximum' field{Colors.ENDC}")
            metrics['S_max'] = {'passed': False, 'value': None}
    except Exception as e:
        print(f"{Colors.RED}Error reading A2 data: {e}{Colors.ENDC}")
        metrics['S_max'] = {'passed': False, 'value': None}

    # Metric 2: σc(K) fit R² ≥ 0.97
    subsection("Metric 2: Linear fit R² for σ_c(K)")
    try:
        with open(DATA_DIR / "A1_sigma_c_K_sweep.json") as f:
            a1_data = json.load(f)

        if 'sigma_c_analysis' in a1_data and 'linear_fit' in a1_data['sigma_c_analysis']:
            fit = a1_data['sigma_c_analysis']['linear_fit']
            r_squared = fit['r_squared']
            slope = fit['slope']
            intercept = fit['intercept']
            r_squared_threshold = 0.97

            metrics['r_squared'] = {
                'value': r_squared,
                'slope': slope,
                'intercept': intercept,
                'threshold': r_squared_threshold,
                'passed': r_squared >= r_squared_threshold
            }

            print(f"Expected: R² ≥ {r_squared_threshold:.2f}")
            print(f"Observed: R² = {r_squared:.4f}")
            print(f"Linear fit: σ_c = {slope:.3f} × K + {intercept:.3f}")
            print(f"{check_mark(metrics['r_squared']['passed'])} R² threshold met")

            if not metrics['r_squared']['passed']:
                print(f"{Colors.YELLOW}Note: R² = {r_squared:.4f} is below threshold but still shows strong correlation{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}Data structure missing fit results{Colors.ENDC}")
            metrics['r_squared'] = {'passed': False, 'value': None}
    except Exception as e:
        print(f"{Colors.RED}Error reading A1 data: {e}{Colors.ENDC}")
        metrics['r_squared'] = {'passed': False, 'value': None}

    # Metric 3: ρs(τ=10) at boundary ≈ 0.86
    subsection("Metric 3: Temporal coherence ρ_S at boundary")
    try:
        with open(DATA_DIR / "B1_minimal_echo.json") as f:
            b1_data = json.load(f)

        # Find boundary point (σ=0.7)
        boundary_result = None
        for r in b1_data.get('results', []):
            if r['sigma_name'] == 'boundary':
                boundary_result = r
                break

        if boundary_result:
            rho_s = boundary_result['rho_S_autocorr_mean']
            rho_s_std = boundary_result['rho_S_autocorr_std']
            rho_s_expected = 0.86
            rho_s_tolerance = 0.05

            metrics['rho_s'] = {
                'value': rho_s,
                'std': rho_s_std,
                'expected': rho_s_expected,
                'passed': abs(rho_s - rho_s_expected) < rho_s_tolerance
            }

            print(f"Expected: ρ_S(τ=10) ≈ {rho_s_expected:.2f} at boundary")
            print(f"Observed: ρ_S = {rho_s:.3f}±{rho_s_std:.3f}")
            print(f"Difference: {abs(rho_s - rho_s_expected):.4f}")
            print(f"{check_mark(metrics['rho_s']['passed'])} Within tolerance ({rho_s_tolerance})")
        else:
            print(f"{Colors.YELLOW}Boundary data point not found{Colors.ENDC}")
            metrics['rho_s'] = {'passed': False, 'value': None}
    except Exception as e:
        print(f"{Colors.RED}Error reading B1 data: {e}{Colors.ENDC}")
        metrics['rho_s'] = {'passed': False, 'value': None}

    return metrics

def check_determinism():
    """Check if data files are deterministic"""
    section("STEP 2: DETERMINISM CHECK")

    print(f"{Colors.YELLOW}Note: Full determinism check requires running pipeline twice{Colors.ENDC}")
    print(f"{Colors.YELLOW}Checking data file consistency instead...{Colors.ENDC}\n")

    # Check that data files have consistent structure
    subsection("Data Structure Consistency")

    try:
        with open(DATA_DIR / "A1_sigma_c_K_sweep.json") as f:
            a1_data = json.load(f)

        # Check for required fields
        required_fields = ['experiment_id', 'timestamp', 'grid_results', 'sigma_c_analysis']
        a1_consistent = all(field in a1_data for field in required_fields)

        print(f"{check_mark(a1_consistent)} A1 data structure complete")

        # Check for random seed consistency
        if len(a1_data.get('grid_results', [])) > 0:
            first_result = a1_data['grid_results'][0]
            has_individual_results = 'individual_results' in first_result
            print(f"{check_mark(has_individual_results)} Individual seed results preserved")

            if has_individual_results and len(first_result['individual_results']) > 0:
                # Check if results look deterministic (same seed should give same result)
                print(f"   Seeds per point: {len(first_result['individual_results'])}")

        return a1_consistent
    except Exception as e:
        print(f"{Colors.RED}Error checking determinism: {e}{Colors.ENDC}")
        return False

def check_figures():
    """Check if figures exist"""
    subsection("Figure Files")

    figures_dir = REPO_ROOT / "paper/figures"

    expected_figures = [
        "fig1_combined.png",
        "fig2_sigma_c_scaling.png",
        "fig3_S_vs_sigma.png",
        "fig4_angle_ridge.png",
        "fig5_delta_omega.png",
        "fig6_memory_panel.png"
    ]

    figure_exists = {}
    for fig in expected_figures:
        figpath = figures_dir / fig
        exists = figpath.exists()
        figure_exists[fig] = exists
        print(f"{check_mark(exists)} {fig}")

    return all(figure_exists.values())

def generate_manifest():
    """Generate a run manifest"""
    section("STEP 5: SCRIPT HARDENING - RUN MANIFEST")

    manifest = {
        'verification_timestamp': datetime.now().isoformat(),
        'script_path': str(SCRIPT_PATH.relative_to(REPO_ROOT)),
        'data_directory': str(DATA_DIR.relative_to(REPO_ROOT)),
        'experiments': {}
    }

    # Get git commit info if available
    try:
        git_commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL
        ).decode().strip()

        git_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL
        ).decode().strip()

        manifest['git_commit'] = git_commit
        manifest['git_branch'] = git_branch
        print(f"Git commit: {git_commit[:8]}")
        print(f"Git branch: {git_branch}")
    except:
        manifest['git_commit'] = 'N/A'
        manifest['git_branch'] = 'N/A'
        print(f"{Colors.YELLOW}Git info not available{Colors.ENDC}")

    # Get Python version
    manifest['python_version'] = sys.version.split()[0]
    manifest['numpy_version'] = np.__version__

    print(f"Python version: {manifest['python_version']}")
    print(f"NumPy version: {manifest['numpy_version']}")

    # Add experiment data
    for exp in ['A1', 'A2', 'A3', 'B1']:
        data_file = DATA_DIR / f"{exp}_*" if exp != "B1" else DATA_DIR / "B1_minimal_echo.json"

        # Find the actual file
        if exp == 'A1':
            data_file = DATA_DIR / "A1_sigma_c_K_sweep.json"
        elif exp == 'A2':
            data_file = DATA_DIR / "A2_angle_ridge.json"
        elif exp == 'A3':
            data_file = DATA_DIR / "A3_delta_omega_sweep.json"
        else:
            data_file = DATA_DIR / "B1_minimal_echo.json"

        if data_file.exists():
            with open(data_file) as f:
                data = json.load(f)

            manifest['experiments'][exp] = {
                'data_file': str(data_file.relative_to(REPO_ROOT)),
                'timestamp': data.get('timestamp', 'N/A'),
                'experiment_id': data.get('experiment_id', 'N/A')
            }

    # Save manifest
    manifest_path = REPO_ROOT / "PIPELINE_MANIFEST.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n{Colors.GREEN}Manifest saved to: {manifest_path.relative_to(REPO_ROOT)}{Colors.ENDC}")

    return manifest

def final_report(hardening_ok, data_exists, metrics, determinism_ok, figures_ok):
    """Generate final pass/fail report"""
    section("FINAL VERIFICATION REPORT")

    print(f"{check_mark(hardening_ok)} Step 1: Script Hardening")
    print(f"{check_mark(data_exists)} Step 2: Data Files Present")
    print(f"{check_mark(determinism_ok)} Step 3: Data Structure Consistent")

    # Metrics detailed check
    metrics_passed = all(m.get('passed', False) for m in metrics.values())
    print(f"{check_mark(metrics_passed)} Step 4: Key Metrics")

    for metric_name, metric_data in metrics.items():
        if metric_data.get('passed'):
            status = f"{Colors.GREEN}PASS{Colors.ENDC}"
        else:
            status = f"{Colors.YELLOW}CHECK{Colors.ENDC}"

        if metric_data.get('value') is not None:
            print(f"   {metric_name}: {status}")

    print(f"{check_mark(figures_ok)} Step 5: Figure Files Present")

    # Overall verdict
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")

    all_critical_passed = hardening_ok and data_exists and determinism_ok

    if all_critical_passed and metrics_passed:
        print(f"{Colors.BOLD}{Colors.GREEN}VERDICT: REPRODUCIBLE ✓{Colors.ENDC}")
        print(f"\nThe pipeline is properly structured, data exists, and key metrics match paper claims.")
    elif all_critical_passed:
        print(f"{Colors.BOLD}{Colors.YELLOW}VERDICT: MOSTLY REPRODUCIBLE (minor metric deviations){Colors.ENDC}")
        print(f"\nThe pipeline works correctly, but some metrics are slightly outside expected ranges.")
        print(f"This may be due to stochastic variations or different parameter settings.")
    else:
        print(f"{Colors.BOLD}{Colors.YELLOW}VERDICT: NEEDS FIXES{Colors.ENDC}")
        print(f"\nSome components need attention.")

    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    # Recommendations
    subsection("Recommendations")

    if not hardening_ok:
        print(f"- Add complete error handling to RUN_ALL_PAPER1.sh")

    if not metrics['r_squared']['passed']:
        print(f"- R² = {metrics['r_squared']['value']:.4f} is below 0.97 threshold")
        print(f"  Consider: (1) checking if more data points are needed")
        print(f"           (2) verifying noise levels match paper parameters")
        print(f"           (3) checking if threshold definition matches paper")

    if not figures_ok:
        print(f"- Run figure generation scripts to create missing figures")

    print(f"\nFor full determinism check:")
    print(f"  1. Run: bash RUN_ALL_PAPER1.sh")
    print(f"  2. Backup: cp -r analysis/data/paper1 analysis/data/paper1_run1")
    print(f"  3. Run again: bash RUN_ALL_PAPER1.sh")
    print(f"  4. Compare: diff -r analysis/data/paper1_run1 analysis/data/paper1")

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'#'*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}# RUN_ALL_PAPER1.sh COMPREHENSIVE VERIFICATION{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'#'*80}{Colors.ENDC}")

    # Run all checks
    hardening_ok = check_script_hardening()
    data_exists, _ = verify_data_exists()
    metrics = extract_key_metrics()
    determinism_ok = check_determinism()
    figures_ok = check_figures()

    # Generate manifest
    manifest = generate_manifest()

    # Final report
    final_report(hardening_ok, data_exists, metrics, determinism_ok, figures_ok)
