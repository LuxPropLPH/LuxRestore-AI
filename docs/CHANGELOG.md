# Changelog

## 2026-07-15

- Completed repository cleanup preparation for future GitHub releases.
- Added root `.gitignore`.
- Added root `.gitattributes` for Git LFS model weight tracking.
- Removed generated outputs, caches, package metadata, and Python bytecode from Git tracking without deleting local files.
- Verified `validation/` contains 65 images at approximately 1.36 MB total.
- Confirmed no production source files were modified during cleanup.

- Created complete deployment and setup documentation.
- Rewrote `README.md` as the project entrypoint.
- Added `docs/INSTALLATION.md`.
- Added `docs/DEPLOYMENT.md`.
- Added `docs/MODELS.md`.
- Added `docs/TROUBLESHOOTING.md`.
- Added `docs/ROADMAP.md`.
- Updated `docs/PROJECT_STATE.md`.
- Documented the requested setup command sequence:
  - `git clone <repository>`
  - `cd LuxRestore-AI`
  - `.\scripts\setup_windows.ps1`
  - `python scripts\verify_install.py`
  - `uvicorn app.main:app --reload`

- Validated the playground pipeline state from current repository outputs:
  - GroundingDINO
  - Post-processing
  - SAM2
  - LaMa
