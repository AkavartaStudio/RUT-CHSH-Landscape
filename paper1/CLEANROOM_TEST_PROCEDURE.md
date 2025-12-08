# Clean-Room Test Procedure for RUN_ALL_PAPER1.sh

This document describes how to verify complete reproducibility of the PAPER1 experimental pipeline from a fresh environment.

## Purpose

Verify that the pipeline can be executed from scratch without manual intervention, ensuring complete reproducibility for scientific validation.

## Prerequisites

- Python 3.8 or higher
- Git
- Basic scientific Python stack (numpy, scipy, matplotlib)

## Step-by-Step Procedure

### 1. Fresh Environment Setup

```bash
# Create a clean test directory
mkdir -p ~/reproducibility_test
cd ~/reproducibility_test

# Note: Record system information
uname -a
python3 --version
```

### 2. Clone Repository

```bash
# Clone from GitHub (or your repository URL)
git clone https://github.com/YOUR_ORG/RUT-CHSH-Landscape.git
cd RUT-CHSH-Landscape

# Verify commit hash
git log -1 --format="%H %ci"
```

### 3. Install Dependencies

```bash
# Option A: Using pip
pip3 install numpy scipy matplotlib

# Option B: Using conda
conda create -n paper1_env python=3.11 numpy scipy matplotlib
conda activate paper1_env

# Verify installations
python3 -c "import numpy; import scipy; import matplotlib; print('Dependencies OK')"
```

### 4. Run Verification Script

```bash
# Run the verification script to check environment
python3 verify_paper1_pipeline.py
```

**Expected output:**
- All script hardening checks should pass
- Data files may not exist yet (this is OK for clean-room test)

### 5. Run the Complete Pipeline

```bash
cd analysis/scripts/paper1_runners

# Run with full logging
bash -x RUN_ALL_PAPER1.sh 2>&1 | tee ../../../full_pipeline_run.log

# Check exit code
echo $?  # Should be 0 for success
```

**Expected duration:** 4-6 hours depending on hardware

### 6. Verify Outputs

```bash
# Return to repo root
cd ../../../

# Check that data files were created
ls -lh analysis/data/paper1/

# Expected files:
# - A1_sigma_c_K_sweep.json
# - A2_angle_ridge.json
# - A3_delta_omega_sweep.json
# - B1_minimal_echo.json

# Run verification again
python3 verify_paper1_pipeline.py
```

**Expected results:**
- All data files present ✓
- |S|max ≈ 2.819 ± 0.01 ✓
- σ_c(K) R² ≥ 0.94 ✓ (0.97 without edge points)
- ρ_S(τ=10) ≈ 0.86 ± 0.05 ✓

### 7. Generate Figures

```bash
cd paper/figures/scripts

# Generate all main figures (Figures 1-7)
python3 generate_fig1_combined.py
python3 generate_fig2_sigma_c_scaling.py
python3 generate_fig3_S_vs_sigma.py
python3 generate_fig4_angle_ridge.py
python3 generate_fig5_delta_omega.py
python3 generate_fig6_memory_panel.py
python3 generate_fig7_rhoS_four_curves.py

# Generate all supplementary figures (Figures S1-S5)
python3 generate_figS1_rhoS_complete_series.py
python3 generate_figS2_control_random.py
python3 generate_figS3_sigma_c_full_range.py
python3 generate_figS4_dtheta_histogram.py
python3 generate_figS5_collapse_logistic.py

# Check outputs (should have 12 figures total)
ls -lh ../*.png | wc -l  # Should output: 12
ls -lh ../*.png
```

### 8. Test Determinism

```bash
# Return to repo root
cd ../../../

# Run determinism test
python3 test_determinism.py
```

**Expected output:**
- Determinism test: PASSED ✓
- Seed independence: PASSED ✓

### 9. Second Run for Full Determinism Check (Optional)

```bash
# Backup first run data
cp -r analysis/data/paper1 analysis/data/paper1_run1

# Run pipeline again
cd analysis/scripts/paper1_runners
bash RUN_ALL_PAPER1.sh 2>&1 | tee ../../../second_pipeline_run.log

# Return to root and compare outputs
cd ../../../

# Compare JSON files (should be identical except timestamps)
python3 << 'EOF'
import json
from pathlib import Path

for exp in ['A1_sigma_c_K_sweep', 'A2_angle_ridge', 'A3_delta_omega_sweep', 'B1_minimal_echo']:
    file1 = Path(f'analysis/data/paper1_run1/{exp}.json')
    file2 = Path(f'analysis/data/paper1/{exp}.json')

    with open(file1) as f1, open(file2) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Remove timestamps for comparison
    data1.pop('timestamp', None)
    data2.pop('timestamp', None)

    if data1 == data2:
        print(f"✓ {exp}: IDENTICAL")
    else:
        print(f"✗ {exp}: DIFFERS")
        # Check what differs
        if 'grid_results' in data1 and 'grid_results' in data2:
            for i, (r1, r2) in enumerate(zip(data1['grid_results'], data2['grid_results'])):
                if r1 != r2:
                    print(f"  First difference at grid point {i}")
                    break
EOF
```

## Success Criteria

The clean-room test PASSES if:

1. ✓ Pipeline runs without manual intervention
2. ✓ No missing dependencies errors
3. ✓ All 4 experiment data files generated
4. ✓ Key metrics match paper claims:
   - |S|max within 0.01 of 2.819
   - R² ≥ 0.94 (or ≥ 0.97 without edge points)
   - ρ_S within 0.05 of 0.86
5. ✓ Figures generate successfully
6. ✓ Determinism test passes
7. ✓ (Optional) Second run produces identical results

## Troubleshooting

### Issue: Import errors

```bash
# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Verify rut_core.py is accessible
ls analysis/scripts/rut_core.py
```

### Issue: Slow execution

The pipeline is computationally intensive:
- A1: ~2,880 trajectories × 600k steps = ~4 hours
- A2: ~810 trajectories × 600k steps = ~1 hour
- A3: ~50 trajectories × 100k steps = ~5 minutes
- B1: ~60 trajectories × 600k steps = ~10 minutes

**Total: ~5-6 hours on typical hardware**

To test faster, you can temporarily modify configs to use:
- Fewer K/sigma points
- Fewer seeds (e.g., 5 instead of 20)
- Shorter trajectories (e.g., T=100000 instead of 600000)

### Issue: Memory errors

Each trajectory requires ~5-10 MB RAM. Peak usage: ~2-4 GB.

If memory is constrained, monitor with:
```bash
# On Linux
top -p $(pgrep python3)

# On macOS
top -pid $(pgrep python3)
```

### Issue: Different results

If results differ from expected values:

1. **Check Python/NumPy versions:**
   ```bash
   python3 --version
   python3 -c "import numpy; print(numpy.__version__)"
   ```
   Pipeline tested with Python 3.11-3.13, NumPy 1.24-2.1

2. **Check random seed implementation:**
   ```bash
   python3 test_determinism.py
   ```

3. **Check for numerical precision issues:**
   Different architectures (ARM vs x86) may have minor floating-point differences at ~1e-10 level, which is acceptable.

## Logs and Artifacts

After a successful clean-room test, preserve:

1. `full_pipeline_run.log` - Complete pipeline execution log
2. `PIPELINE_MANIFEST.json` - Run metadata (git commit, versions, timestamps)
3. `analysis/data/paper1/*.json` - All experimental data
4. `paper/figures/*.png` - Generated figures
5. Output of `verify_paper1_pipeline.py`

## Reporting Results

When reporting clean-room test results, include:

```
Clean-Room Test Report
======================
Date: YYYY-MM-DD
Tester: [Name]
System: [OS, Python version, NumPy version]
Git commit: [hash]

Results:
- Pipeline execution: [PASS/FAIL]
- Data generation: [PASS/FAIL]
- Metric verification: [PASS/FAIL]
- Determinism: [PASS/FAIL]

Notes: [Any issues or observations]
```

## Contact

For questions or issues with reproducibility:
- Open an issue on GitHub
- Email: studioakavarta@gmail.com
