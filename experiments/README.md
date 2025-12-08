# Experiments

This directory contains reproducible experiment configurations and results for Papers 2 and 3.

## Paper 2 Experiments (Memory Landscape)

| Folder | Description | Size |
|--------|-------------|------|
| `Paper2_Stage1/` | σ_mem threshold identification | ~1 MB |
| `Paper2_Stage2/` | Memory curvature surface | ~800 KB |
| `Paper2_Stage3/` | Echo and χ surfaces | ~1 MB |
| `Paper2_Stage4/` | Angle-resolved analysis | ~600 KB |

## Paper 3 Experiments (Network Topology)

| Folder | Description | Size | Location |
|--------|-------------|------|----------|
| `Paper3_Mission1/` | Chain topology baseline | ~2.5 GB | **External** |
| `Paper3_Mission1B/` | Symmetric cluster analysis | ~1.9 GB | **External** |
| `Paper3_Mission2/` | Star topology | ~100 KB | Included |
| `Paper3_Mission3/` | Triangle topology | ~190 KB | Included |
| `Paper3_Mission4/` | Comparative analysis | ~100 KB | Included |

## Large External Datasets

Mission1 and Mission1B contain large simulation outputs (~4.4 GB combined) that are not tracked in Git.

**Local path:** `/Users/kellymcrae/Akavarta/research/phys/Paper3_Mission1/` and `Paper3_Mission1B/`

**Canonical archive:** OSF repository (link TBD)

To reproduce these experiments, run the configuration files in each mission's `config/` directory using the RUT simulation engine.
