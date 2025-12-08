#!/bin/bash
# Paper 2 - Mission 1: Run σ_mem(K) Curve
#
# This sweeps K ∈ {0.10, 0.15, ..., 1.00} and σ ∈ {0.00, 0.02, ..., 0.40}
# to map the memory-collapse threshold across the full CHSH ridge.
#
# Expected runtime: ~30-60 minutes depending on hardware
# (19 K values × 21 σ values × 5 seeds = 1995 simulations)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Paper 2 - Mission 1: σ_mem(K) Curve"
echo "========================================"
echo ""
echo "Starting at: $(date)"
echo ""

python3 E211_sigma_mem_curve.py

echo ""
echo "Completed at: $(date)"
echo "========================================"
