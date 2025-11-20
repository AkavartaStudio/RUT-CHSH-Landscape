#!/bin/bash
#
# Paper 1: Run Complete Experimental Suite
#
# Executes A1-A5, B1 in sequence
# Total: ~1890 trajectories

set -e  # Exit on error

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

# A1 already complete
echo "✓ A1: σ_c(K) sweep - COMPLETE"
echo ""

# A2: Angle ridge
echo "Running A2: Angle ridge refinement..."
python3 A2_angle_ridge.py
echo ""

# A3: Δω sweep
echo "Running A3: Δω vs |S| curve..."
python3 A3_delta_omega_sweep.py
echo ""

# A4: Dichotomic variants (skip for now - needs special implementation)
echo "⚠️  A4: Dichotomic variants - SKIPPED (requires custom measurement implementation)"
echo ""

# A5: Quantization threshold (skip for now - needs special implementation)
echo "⚠️  A5: Quantization threshold - SKIPPED (requires phase quantization implementation)"
echo ""

# B1: Minimal echo
echo "Running B1: Minimal echo panel..."
python3 B1_minimal_echo.py
echo ""

echo "================================================================================"
echo "✅ Paper 1 Experimental Suite Complete (A1-A3, B1)"
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
