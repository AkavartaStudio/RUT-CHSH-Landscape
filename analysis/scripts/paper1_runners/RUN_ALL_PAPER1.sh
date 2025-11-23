#!/bin/bash
#
# Paper 1: Run Complete Experimental Suite
#
# Executes A1-A5, B1 in sequence
# Total: ~1890 trajectories

set -euo pipefail  # Exit on error, undefined vars, pipe failures

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================================================================"
echo "Paper 1: Running Complete Experimental Suite"
echo "================================================================================"
echo ""
echo "This will run:"
echo "  A1: σ_c(K) sweep (720 runs) [✓ COMPLETE]"
echo "  A2: Angle ridge (810 runs)"
echo "  A3: Δω sweep (90 runs)"
echo "  A4: Dichotomic variants (60 runs) - PENDING IMPLEMENTATION"
echo "  A5: Quantization threshold (90 runs) - PENDING IMPLEMENTATION"
echo "  B1: Minimal echo (60 runs)"
echo ""
echo "Total: ~1890 trajectories"
echo "Estimated time: 1-2 hours"
echo ""
echo "================================================================================"
echo ""

# A1: σ_c(K) sweep
echo "================================================================================"
echo "STAGE 1: Running A1 - σ_c(K) sweep"
echo "================================================================================"
python3 A1_sigma_c_K_sweep.py
if [ $? -eq 0 ]; then
    echo "✅ STAGE 1 COMPLETE: A1_sigma_c_K_sweep"
else
    echo "❌ STAGE 1 FAILED: A1_sigma_c_K_sweep"
    exit 1
fi
echo ""

# A2: Angle ridge
echo "================================================================================"
echo "STAGE 2: Running A2 - Angle ridge refinement"
echo "================================================================================"
python3 A2_angle_ridge.py
if [ $? -eq 0 ]; then
    echo "✅ STAGE 2 COMPLETE: A2_angle_ridge"
else
    echo "❌ STAGE 2 FAILED: A2_angle_ridge"
    exit 1
fi
echo ""

# A3: Δω sweep
echo "================================================================================"
echo "STAGE 3: Running A3 - Δω vs |S| curve"
echo "================================================================================"
python3 A3_delta_omega_sweep.py
if [ $? -eq 0 ]; then
    echo "✅ STAGE 3 COMPLETE: A3_delta_omega_sweep"
else
    echo "❌ STAGE 3 FAILED: A3_delta_omega_sweep"
    exit 1
fi
echo ""

# A4: Dichotomic variants (skip for now - needs special implementation)
echo "⚠️  A4: Dichotomic variants - SKIPPED (requires custom measurement implementation)"
echo ""

# A5: Quantization threshold (skip for now - needs special implementation)
echo "⚠️  A5: Quantization threshold - SKIPPED (requires phase quantization implementation)"
echo ""

# B1: Minimal echo
echo "================================================================================"
echo "STAGE 4: Running B1 - Minimal echo panel"
echo "================================================================================"
python3 B1_minimal_echo.py
if [ $? -eq 0 ]; then
    echo "✅ STAGE 4 COMPLETE: B1_minimal_echo"
else
    echo "❌ STAGE 4 FAILED: B1_minimal_echo"
    exit 1
fi
echo ""

echo "================================================================================"
echo "✅ ALL STAGES COMPLETE: Paper 1 Experimental Suite (A1-A3, B1)"
echo "================================================================================"
echo ""
echo "Results saved to: ../../../data/paper1/"
echo ""
echo "Next steps:"
echo "  1. Implement A4 (dichotomic measurements)"
echo "  2. Implement A5 (phase quantization)"
echo "  3. Generate Paper 1 figures"
echo "  4. Update main.tex"
echo ""
