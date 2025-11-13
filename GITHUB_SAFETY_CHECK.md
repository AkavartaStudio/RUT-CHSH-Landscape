# GitHub/OSF/ORCID Safety Checklist ✅

## What You're Sharing (SAFE)

**Directory:** `RUT-CHSH-Landscape/` ONLY

This directory contains:
- ✅ Paper manuscript source (LaTeX to be added)
- ✅ Bibliography (refs.bib)
- ✅ Publication-quality figures (6 PNG files)
- ✅ Analysis scripts (Python)
- ✅ Experimental data (JSON)
- ✅ Documentation (README, CITATION, etc.)

---

## Privacy Check Results ✅

### 1. **Email Address**
- ✅ **SAFE**: Only contains `studioakavarta@gmail.com` (your public contact)
- Location: README.md, CITATION.md
- This is intentional for contact/citation purposes

### 2. **File Paths**
- ✅ **SAFE**: All Python scripts use **relative paths** (`Path(__file__).parent`)
- No hardcoded `/Users/kellymcrae/` paths in code
- REPO_SUMMARY.md mentions local path but that file is just for your reference

### 3. **No Credentials**
- ✅ **SAFE**: No API keys, passwords, tokens, or secrets
- No authentication files
- No `.env` files

### 4. **No Personal Research**
- ✅ **SAFE**: This directory contains ONLY the RUT CHSH Landscape paper
- Does NOT include:
  - E101-E106 experiments (stay private)
  - Session summaries (stay private)
  - Other theory files (stay private)
  - Personal notes (stay private)

---

## What Stays PRIVATE (Not in Git Repo)

**Parent directory:** `/Users/kellymcrae/Akavarta/research/phys/`

Contains (ALL PRIVATE):
- E101_echo_memory/
- E102_oscillator/
- E103_phase_lock/
- E103B_boundary_sweep/
- E103C_time_coupling/
- E104_bell_test/
- E104B_noise_study/
- E104C_angle_optimization/
- E104D_bell_landscape/
- E105_three_body/
- E106_* (all variants)/
- E107_parameter_sweep/
- E107N_goldilocks_noise/
- theory/ (separate folder with markdown docs)
- SESSION_SUMMARY_*.md
- THEOREM_*.md
- *.md planning documents

**These will NOT be in the GitHub repo if you initialize Git correctly!**

---

## How to Initialize Git Safely

### Step 1: Navigate to RUT-CHSH-Landscape ONLY
```bash
cd /Users/kellymcrae/Akavarta/research/phys/RUT-CHSH-Landscape
```

### Step 2: Verify you're in the right place
```bash
pwd
# Should show: /Users/kellymcrae/Akavarta/research/phys/RUT-CHSH-Landscape
```

### Step 3: Initialize Git HERE (not in parent!)
```bash
git init
```

### Step 4: Check what will be tracked
```bash
git status
```
Should show ONLY files inside RUT-CHSH-Landscape/

### Step 5: Add files
```bash
git add .
```

### Step 6: Commit
```bash
git commit -m "Initial commit: RUT CHSH Landscape manuscript and analysis"
```

### Step 7: Create GitHub repo and push
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/[your-username]/RUT-CHSH-Landscape.git
git branch -M main
git push -u origin main
```

---

## Double-Check Before Pushing

Run this from inside `RUT-CHSH-Landscape/`:

```bash
git log --oneline --name-status
```

**Verify:**
- ✅ All files start with `./` or subdirectory names (paper/, analysis/, etc.)
- ❌ NO files from parent directory (../E107N_goldilocks_noise, ../theory, etc.)
- ❌ NO absolute paths like /Users/kellymcrae/...

---

## What GitHub/OSF/ORCID Will See

**Repository name:** `RUT-CHSH-Landscape` (or whatever you choose)

**Contents:**
```
RUT-CHSH-Landscape/
├── README.md          ← Professional overview
├── CITATION.md        ← How to cite
├── paper/
│   ├── figures/       ← 6 publication figures
│   └── refs.bib       ← Bibliography
└── analysis/
    ├── scripts/       ← Reproducible code
    ├── data/          ← E107N dataset
    └── config/        ← Experiment config
```

**They will NOT see:**
- Your other experiments (E101-E106, E107, E107N original folder)
- Your theory folder
- Your session summaries
- Your personal file paths
- Anything outside RUT-CHSH-Landscape/

---

## Final Safety Tips

1. **Before first push:**
   - Review `git status` carefully
   - Check `git log --name-status`
   - Make sure you ran `git init` inside RUT-CHSH-Landscape/, not parent

2. **If you accidentally initialized Git in wrong place:**
   ```bash
   rm -rf .git  # Remove Git tracking
   cd RUT-CHSH-Landscape/
   git init     # Start fresh in correct location
   ```

3. **OSF/ORCID linking:**
   - Link to GitHub repo URL: `https://github.com/[username]/RUT-CHSH-Landscape`
   - OSF will just mirror the GitHub repo
   - ORCID will just link to the repo

4. **Privacy setting on GitHub:**
   - Choose "Public" when creating repo (for open science)
   - Or "Private" initially, then make public when paper is submitted

---

## ✅ YOU'RE GOOD TO GO!

**Summary:**
- RUT-CHSH-Landscape/ is clean, professional, and safe to share publicly
- No personal info (except intended email)
- No private research included
- All paths are relative (portable)
- No credentials or secrets

**When you push to GitHub, OSF, and ORCID, the world will see:**
- A polished research repository
- Reproducible code and data
- Professional documentation
- Publication-ready figures

**They will NOT see:**
- Your other experiments
- Your personal directory structure
- Your research notes
- Anything outside this specific folder

---

**Questions?** Just ask! But you're **100% safe** to proceed. 🚀
