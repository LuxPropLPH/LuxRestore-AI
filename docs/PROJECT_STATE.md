# Project Overview

LuxRestore-AI is a modular AI image-restoration project focused on automatic watermark detection, segmentation, and removal from property images.

Current objective: validate the complete playground-only pipeline before any production integration.

Architecture status: production architecture is frozen. No `app/` production code has been modified during playground validation.

Current sprint: Repository Cleanup Sprint.

Current ticket: Repository Cleanup - GitHub release preparation.

# Current Pipeline

Validation Image

↓

GroundingDINO - ✅ Complete

↓

Post Processing - ✅ Complete

↓

SAM2 - ✅ Complete

↓

LaMa - ✅ Complete

↓

Quality Evaluation - 🚧 In Progress

# Completed Tickets

## Sprint 4 - Ticket 4.4

Objective: install and validate real GroundingDINO inference in the playground.

Files modified:
- `playground/grounding_dino/config.py`
- `playground/grounding_dino/model_manager.py`
- `playground/grounding_dino/run.py`
- `playground/grounding_dino/adapter.py`
- `playground/grounding_dino/visualizer.py`
- `playground/grounding_dino/README.md`

Validation performed:
- Loaded local GroundingDINO model from `weights/grounding_dino/`.
- Ran `validation/1.jpg`.
- Ran the first 10 validation images.

Result:
- Real GroundingDINO inference works locally on CPU.
- Initial prompt detected the red watermark text but missed the gold logo.

Important design decisions:
- Models are never downloaded automatically.
- GroundingDINO remains playground-only.

## Sprint 4 - Ticket 4.6

Objective: improve GroundingDINO prompt quality so the gold logo and red IMPERA text are detected.

Files modified:
- `playground/grounding_dino/config.py`
- `playground/grounding_dino/prompt_experiment.py`

Validation performed:
- Compared prompts on `validation/1.jpg`.
- Generated prompt comparison outputs under `output/1/prompt_experiments/`.

Result:
- Best prompt became `gold logo. red text.`
- It detected the gold logo and IMPERA text but still missed the smaller lower watermark.

Important design decisions:
- Threshold stayed at `0.25`.
- Prompt tuning was preferred over lowering thresholds.

## Sprint 4 - Ticket 4.7

Objective: add playground-only post-processing for GroundingDINO detections.

Files modified:
- `playground/grounding_dino/postprocess.py`
- `playground/grounding_dino/run.py`
- `playground/grounding_dino/visualizer.py`
- `playground/sam2/mask_generator.py`

Validation performed:
- Ran `validation/1.jpg`.
- Saved raw, filtered, and merged detections.
- Ran SAM2 with merged detections.

Result:
- Ceiling-light false positive was removed.
- Gold logo and IMPERA text were merged into one SAM2-ready region.
- Smaller lower watermark was still filtered out.

Important design decisions:
- Post-processing uses simple geometry only.
- No extra AI model was introduced.

## Sprint 4 - Ticket 4.8

Objective: preserve legitimate secondary watermarks while continuing to filter false positives.

Files modified:
- `playground/grounding_dino/config.py`
- `playground/grounding_dino/postprocess.py`
- `playground/grounding_dino/run.py`
- `playground/grounding_dino/visualizer.py`
- `playground/sam2/mask_generator.py`

Validation performed:
- Ran `validation/1.jpg`.
- Generated raw, filtered, merged, and final detections.
- Ran SAM2 using `detections_final.json`.

Result:
- Final detections contain:
  - merged gold logo + IMPERA text
  - smaller lower watermark
- Ceiling false positive is removed.
- SAM2 masks both watermark regions.

Important design decisions:
- Current prompt is `gold logo. red text. small watermark.`
- Main group is merged; lower watermark remains separate.
- SAM2 prefers `detections_final.json`.

## Sprint 5 - Ticket 5.1

Objective: integrate SAM2 into the playground and validate mask generation using GroundingDINO detections.

Files modified:
- `playground/sam2/config.py`
- `playground/sam2/model_manager.py`
- `playground/sam2/adapter.py`
- `playground/sam2/mask_generator.py`
- `playground/sam2/visualizer.py`
- `playground/sam2/run.py`
- `playground/sam2/README.md`

Validation performed:
- Loaded SAM2 from `weights/sam2/`.
- Ran `validation/1.jpg`.

Result:
- Real SAM2 mask generation works locally on CPU.
- SAM2 produces `mask.png`, `mask_overlay.jpg`, `mask_metadata.json`, and `experiment_mask.txt`.

Important design decisions:
- SAM2 reads GroundingDINO outputs from `output/<image>/`.
- SAM2 does not download weights.

## Sprint 5 - Ticket 5.2

Objective: integrate real LaMa inference and perform the first complete end-to-end watermark removal.

Files modified:
- `playground/lama/config.py`
- `playground/lama/model_manager.py`
- `playground/lama/adapter.py`
- `playground/lama/visualizer.py`
- `playground/lama/run.py`
- `playground/lama/README.md`

Validation performed:
- Copied local LaMa model files into `weights/lama/`.
- Ran full pipeline for `validation/1.jpg`.
- Ran full pipeline for validation images `1.jpg` through `10.jpg`.

Result:
- Real LaMa inference runs locally on CPU.
- `restored.png`, `comparison.jpg`, and `experiment_lama.txt` are generated.
- First 10 images completed successfully.
- Average LaMa inference runtime: `1786.36 ms`.
- Success rate for output generation: `10/10`.

Important design decisions:
- LaMa loads only from `weights/lama/`.
- LaMa input mask uses an 11px dilation to reduce ghosting.
- Original SAM2 `mask.png` is preserved; LaMa writes `lama_input_mask.png`.

## Repository Maintenance - Deployment and Setup Documentation

Objective: create complete setup, deployment, model, and troubleshooting documentation for developers setting up LuxRestore-AI on a new Windows machine.

Files modified:
- `README.md`
- `docs/INSTALLATION.md`
- `docs/DEPLOYMENT.md`
- `docs/MODELS.md`
- `docs/TROUBLESHOOTING.md`
- `docs/CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/PROJECT_STATE.md`

Validation performed:
- Inspected current repository structure.
- Confirmed current API endpoints: `/`, `/health`, `/locate`.
- Confirmed playground modules: `grounding_dino`, `sam2`, `lama`.
- Confirmed local model folders: `weights/grounding_dino/`, `weights/sam2/`, `weights/lama/`.
- Confirmed `scripts/` currently contains only `.gitkeep`.

Result:
- Documentation set completed.
- Setup command sequence requested by the user was documented.
- Missing setup automation scripts were recorded as a known issue and roadmap item.

Important design decisions:
- Documentation only.
- No `app/` files were modified.
- No playground code was modified for this maintenance task.

## Repository Cleanup - GitHub Release Preparation

Objective: prepare the repository for future clean GitHub releases without rewriting history, force pushing, deleting local files, or modifying production code.

Files modified:
- `.gitignore`
- `.gitattributes`
- `docs/PROJECT_STATE.md`
- `docs/CHANGELOG.md`
- `docs/ROADMAP.md`

Validation performed:
- Created root ignore rules for generated outputs, caches, virtual environments, logs, temp folders, and package metadata.
- Configured Git LFS patterns for `*.ckpt`, `*.safetensors`, `*.pth`, `*.pt`, and `*.bin`.
- Verified LFS attributes with `git lfs track` and `git check-attr filter`.
- Removed generated output, cache, package metadata, and Python bytecode files from Git tracking without deleting local files.
- Reviewed `validation/`: 65 images, approximately 1.36 MB total.

Result:
- Repository cleanup is prepared for a future release commit.
- Generated experiment outputs and cache files are no longer tracked in the index.
- Model weight extensions are configured for Git LFS going forward.
- Lightweight model configuration and tokenizer files remain tracked.

Important design decisions:
- No Git history rewrite was performed.
- No local files were deleted.
- No `app/` production source files were modified.
- Validation images were left in place and require a public-release rights review before publishing.

# Current Configuration

Current prompts:
- GroundingDINO prompt: `gold logo. red text. small watermark.`

Current thresholds:
- GroundingDINO threshold: `0.25`
- Secondary detection threshold: `0.30`
- SAM2 mask threshold: `0.0`
- LaMa mask dilation: `11px`

Current model names:
- GroundingDINO: `IDEA-Research/grounding-dino-tiny`
- SAM2: `facebook/sam2-hiera-tiny`
- LaMa: `big-lama`

Current weight locations:
- GroundingDINO: `weights/grounding_dino/`
- SAM2: `weights/sam2/`
- LaMa: `weights/lama/`

Current validation dataset:
- `validation/1.jpg` through `validation/10.jpg` have been used for the latest end-to-end run.

Current output folder layout:
- `output/<image>/original.jpg`
- `output/<image>/detections_raw.json`
- `output/<image>/detections_filtered.json`
- `output/<image>/detections_merged.json`
- `output/<image>/detections_final.json`
- `output/<image>/detections_final.jpg`
- `output/<image>/mask.png`
- `output/<image>/mask_overlay.jpg`
- `output/<image>/mask_metadata.json`
- `output/<image>/experiment_mask.txt`
- `output/<image>/lama_input_mask.png`
- `output/<image>/restored.png`
- `output/<image>/comparison.jpg`
- `output/<image>/experiment_lama.txt`

Repository hygiene:
- Root ignore file: `.gitignore`
- Git LFS attributes file: `.gitattributes`
- Generated outputs ignored: `output/`
- Caches ignored: `.cache/`, `**/__pycache__/`, `*.pyc`, `.pytest_cache/`
- Local environments ignored: `.venv/`, `venv/`
- Package metadata ignored: `luxrestore_ai.egg-info/`
- Logs/temp ignored: `logs/`, `tmp/`

# Commands

Run one complete validation image:

```powershell
.venv\Scripts\python.exe -B playground\grounding_dino\run.py --image validation\1.jpg
.venv\Scripts\python.exe -B playground\sam2\run.py --image validation\1.jpg
.venv\Scripts\python.exe -B playground\lama\run.py --image validation\1.jpg
```

Run the first 10 images:

```powershell
foreach ($i in 1..10) {
  .venv\Scripts\python.exe -B playground\grounding_dino\run.py --image "validation\$i.jpg"
  .venv\Scripts\python.exe -B playground\sam2\run.py --image "validation\$i.jpg"
  .venv\Scripts\python.exe -B playground\lama\run.py --image "validation\$i.jpg"
}
```

# Known Issues

High:
- No automated quality metric yet for restored outputs. Visual QA is still manual.
- Validation images appear to be real property/watermark examples and need rights/privacy review before public GitHub release.

Medium:
- LaMa on CPU reloads the model for every image, so end-to-end batch runtime is slower than necessary.
- Some restored images show mild smoothing or faint wall texture artifacts near removed watermark regions.
- The LaMa wrapper uses compatibility shims for the older LaMa codebase under modern Python dependencies.
- The documented convenience setup commands reference `scripts/setup_windows.ps1` and `scripts/verify_install.py`, but those files are not present yet.

Low:
- Transformers prints a SAM2 model-type warning when loading the local SAM2 checkpoint.
- Pillow emits a deprecation warning for `Image.getdata()`.
- Existing Git history may still contain previously committed generated outputs and large model blobs because cleanup did not rewrite history.

# Next Ticket

Next Ticket ID: Sprint 5 - Ticket 5.3.

Objective: formalize quality evaluation for the first 10 restored images.

Expected outputs:
- Quality summary for each restored image.
- Failure case list.
- Recommendation on whether to proceed toward broader batch validation.

Success criteria:
- Each restored image is classified as acceptable, marginal, or failed.
- Artifact patterns are documented.
- Next model or mask improvements are clearly identified.

# Repository Structure

Important playground folders:

```text
playground/
  grounding_dino/
    adapter.py
    config.py
    model_manager.py
    postprocess.py
    prompt_experiment.py
    run.py
    visualizer.py
  sam2/
    adapter.py
    config.py
    mask_generator.py
    model_manager.py
    run.py
    visualizer.py
  lama/
    adapter.py
    config.py
    model_manager.py
    run.py
    visualizer.py
```

Important model folders:

```text
weights/
  grounding_dino/
  sam2/
  lama/
```

Important output folders:

```text
output/<image>/
```

# Changelog

## 2026-07-15

- Created official setup/deployment/model/troubleshooting documentation.
- Rewrote `README.md` as a professional project entrypoint.
- Added `docs/CHANGELOG.md` and `docs/ROADMAP.md`.
- Documented the requested setup sequence:
  - `git clone <repository>`
  - `cd LuxRestore-AI`
  - `.\scripts\setup_windows.ps1`
  - `python scripts\verify_install.py`
  - `uvicorn app.main:app --reload`
- Validated real GroundingDINO inference from local weights.
- Tuned GroundingDINO prompt to detect logo, IMPERA text, and lower watermark.
- Added geometric post-processing for raw, filtered, merged, and final detections.
- Validated real SAM2 mask generation from local weights.
- Added real LaMa inference from local `big-lama` weights.
- Ran the complete GroundingDINO -> Post Processing -> SAM2 -> LaMa pipeline on `validation/1.jpg`.
- Ran the complete pipeline on validation images `1.jpg` through `10.jpg`.
- Added `docs/PROJECT_STATE.md` as the single source of truth for current validated state.
- Added root `.gitignore` for generated outputs, caches, virtual environments, logs, temp files, and package metadata.
- Added root `.gitattributes` with Git LFS rules for model weight extensions.
- Removed generated outputs, cache files, package metadata, and Python bytecode from Git tracking without deleting local files.
- Reviewed `validation/`: 65 images, approximately 1.36 MB total, requires public-release rights review.
