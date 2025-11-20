# Paper 1: File Structure

## Directory Organization

```
RUT-CHSH-Landscape/
└── paper/
    ├── PAPER1_OUTLINE.md          ✓ Canonical outline
    ├── PAPER1_FIGURES.md           ✓ Figure plan
    ├── PAPER1_STRUCTURE.md         ✓ This file
    ├── PAPER1_EXPERIMENT_PLAN.md   ✓ Experimental program
    │
    ├── configs_paper1/             ✓ Frozen experimental configs
    │   ├── A1_sigma_c_K_sweep.json
    │   ├── A2_angle_ridge.json
    │   ├── A3_delta_omega_sweep.json
    │   └── B1_minimal_echo.json
    │
    ├── sections/                   ← Paper sections (to be created)
    │   ├── 1_introduction.md
    │   ├── 2_model.md
    │   ├── 3_experiments.md
    │   ├── 4_discussion.md
    │   ├── 5_methods.md
    │   └── 6_references.md
    │
    ├── figures/                    ← Generated figures
    │   ├── fig1_schematic.pdf
    │   ├── fig2_sigma_c_scaling.pdf
    │   ├── fig3_S_vs_sigma.pdf
    │   ├── fig4_angle_ridge.pdf
    │   ├── fig5_delta_omega.pdf
    │   ├── fig6_memory_panel.pdf
    │   └── scripts/
    │       ├── generate_fig2.py
    │       ├── generate_fig3.py
    │       ├── generate_fig4.py
    │       ├── generate_fig5.py
    │       └── generate_fig6.py
    │
    ├── main.tex                    ← LaTeX main file (to be created)
    ├── main.pdf                    ← Compiled paper
    ├── refs.bib                    ✓ Bibliography
    │
    └── supplementary/              ← Supplementary materials
        ├── tables/
        └── extra_figures/
```

---

## Experimental Data Location

```
RUT-CHSH-Landscape/
└── analysis/
    ├── scripts/
    │   ├── rut_core.py                     ✓ Core functions
    │   └── paper1_runners/                 ✓ Experimental runners
    │       ├── A1_sigma_c_K_sweep.py       ✓ Complete
    │       ├── A2_angle_ridge.py           ⏳ Running
    │       ├── A3_delta_omega_sweep.py     ⏳ Running
    │       └── B1_minimal_echo.py          ⏳ Running
    │
    └── data/
        └── paper1/                         ← Results directory
            ├── A1_sigma_c_K_sweep.json     ✓ Complete
            ├── A2_angle_ridge.json         ⏳ Pending
            ├── A3_delta_omega_sweep.json   ⏳ Pending
            └── B1_minimal_echo.json        ⏳ Pending
```

---

## Content Development Workflow

### Phase 1: Scaffold (Current)
- [✓] Create outline
- [✓] Create figure plan
- [✓] Set up directory structure
- [✓] Run experiments A1-A3, B1

### Phase 2: Draft Sections
- [ ] Write Section 1 (Introduction) ← NEXT
- [ ] Write Section 2 (Model)
- [ ] Write Section 3 (Experiments) - can start now with A1 results
- [ ] Write Section 4 (Discussion) - after experiments complete
- [ ] Write Section 5 (Methods)

### Phase 3: Figures
- [ ] Generate Figure 2 (A1 data available)
- [ ] Generate Figure 3 (A1 data available)
- [ ] Generate Figure 4 (awaiting A2)
- [ ] Generate Figure 5 (awaiting A3)
- [ ] Generate Figure 6 (awaiting B1)
- [ ] Create Figure 1 (schematic - independent)

### Phase 4: Assembly
- [ ] Compile main.tex
- [ ] Check references
- [ ] Proofread
- [ ] Generate PDF
- [ ] Review and iterate

### Phase 5: Finalize
- [ ] Git commit with frozen configs
- [ ] Tag release version
- [ ] Prepare arXiv submission
- [ ] Prepare supplementary materials

---

## Version Control Strategy

### What Gets Committed:
- ✓ All `.md` files (outline, sections, plans)
- ✓ All configs (`.json` in `configs_paper1/`)
- ✓ All figure generation scripts
- ✓ Final figures (`.pdf` and `.png`)
- ✓ LaTeX source (`.tex`, `.bib`)
- ✓ Final PDF

### What Gets Ignored:
- Intermediate LaTeX files (`.aux`, `.log`, `.bbl`, etc.)
- Temporary data files
- Draft versions

### Git Tags:
- `paper1-v0.1-draft` - First complete draft
- `paper1-v1.0-submission` - Submitted to arXiv
- `paper1-v1.1-revision` - After referee comments (if applicable)

---

## Current Status

### Complete:
- [✓] Outline finalized
- [✓] Figure plan defined
- [✓] Experimental configs frozen
- [✓] A1 executed and validated
- [✓] Directory structure created

### In Progress:
- [⏳] A2, A3, B1 running
- [⏳] Section 1 (Introduction) - awaiting draft

### Pending:
- [ ] Remaining sections
- [ ] Figure generation
- [ ] LaTeX compilation
- [ ] Proofreading and refinement

---

## Next Immediate Actions

1. **Draft Section 1 (Introduction)** while experiments run
2. **Generate Figures 2-3** using A1 data
3. **Write Section 3.1** (A1 results)
4. **Wait for A2, A3, B1** to complete
5. **Generate remaining figures**
6. **Complete all sections**
7. **Compile and review**

---

## Contact and Collaboration

- **Primary**: Kelly (research direction)
- **Technical**: TC (Claude Code - experimental execution, figure generation)
- **Theory**: Chase (framing, interpretation, writing)

---

## Notes

This structure is designed to:
- Keep Paper 1 cleanly separated from future papers
- Maintain reproducibility through frozen configs
- Enable efficient figure regeneration
- Support collaborative writing
- Facilitate version control
- Prepare for publication submission
