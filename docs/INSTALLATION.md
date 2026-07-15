# Installation Guide

This guide sets up LuxRestore-AI on a brand-new Windows machine.

## Prerequisites

Install:

- Windows 10 or Windows 11
- Python 3.10 or newer
- Git
- Git LFS
- Microsoft Visual Studio Build Tools, if native Python packages need compilation
- NVIDIA driver, if using CUDA
- CUDA-compatible PyTorch, if using GPU acceleration

## Hardware

Minimum:

- CPU-only machine
- 16 GB RAM
- 15 GB free disk space

Recommended:

- NVIDIA GPU with 8 GB+ VRAM
- 32 GB RAM
- 30 GB free disk space
- NVMe SSD

## Environment Variables

Optional:

```powershell
$env:DEVICE="cpu"
$env:DEVICE="cuda"
$env:CONF_THRESHOLD="0.25"
$env:SECONDARY_DETECTION_THRESHOLD="0.30"
$env:LAMA_MASK_DILATION_PX="11"
$env:LAMA_REPO_DIR="D:\lama"
```

If `DEVICE` is not set, playground modules default to automatic CPU/CUDA selection.

## Fresh Machine Setup

Preferred command sequence requested for the repository:

```powershell
git clone <repository>
cd LuxRestore-AI

.\scripts\setup_windows.ps1

python scripts\verify_install.py

uvicorn app.main:app --reload
```

Current repository note: `scripts/setup_windows.ps1` and `scripts/verify_install.py` are not present yet. Use the manual setup below until those scripts are added.

## Manual Setup

Clone the repository:

```powershell
git clone <repository>
cd LuxRestore-AI
```

Initialize Git LFS:

```powershell
git lfs install
git lfs pull
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install application dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Install playground dependencies:

```powershell
python -m pip install -r playground\requirements.txt
```

Install LaMa runtime dependencies used during validation:

```powershell
python -m pip install hydra-core omegaconf easydict pytorch-lightning kornia scikit-image webdataset scikit-learn pandas matplotlib tabulate
python -m pip install "albumentations==0.5.2" "imgaug==0.4.0"
```

## Model Weights

Model weights are loaded locally only. Nothing is downloaded automatically.

Expected folders:

```text
weights/
  grounding_dino/
  sam2/
  lama/
```

See [MODELS.md](MODELS.md) for exact required files.

## Verify Installation

Check Python:

```powershell
python --version
```

Check installed package import basics:

```powershell
.venv\Scripts\python.exe -B -c "import fastapi, torch, transformers, PIL, cv2; print('ok')"
```

Run tests:

```powershell
pytest
```

## Run Playground Modules

GroundingDINO:

```powershell
.venv\Scripts\python.exe -B playground\grounding_dino\run.py --image validation\1.jpg
```

SAM2:

```powershell
.venv\Scripts\python.exe -B playground\sam2\run.py --image validation\1.jpg
```

LaMa:

```powershell
.venv\Scripts\python.exe -B playground\lama\run.py --image validation\1.jpg
```

First 10 images:

```powershell
foreach ($i in 1..10) {
  .venv\Scripts\python.exe -B playground\grounding_dino\run.py --image "validation\$i.jpg"
  .venv\Scripts\python.exe -B playground\sam2\run.py --image "validation\$i.jpg"
  .venv\Scripts\python.exe -B playground\lama\run.py --image "validation\$i.jpg"
}
```

## Start the API

```powershell
uvicorn app.main:app --reload
```

Verify:

```powershell
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

## Quick Verification Checklist

- [ ] Python installed
- [ ] Git installed
- [ ] Git LFS initialized
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] GroundingDINO weights detected
- [ ] SAM2 weights detected
- [ ] LaMa checkpoint detected
- [ ] Validation images detected
- [ ] Tests pass
- [ ] Playground runs
- [ ] API starts
- [ ] n8n ready

## Estimated Setup Time

Developer with GPU:

- 30-60 minutes, assuming compatible CUDA/PyTorch versions.

Developer with CPU only:

- 30-45 minutes, but validation runs will be slower.

Fresh Windows installation:

- 1-3 hours, depending on Python, Git, Git LFS, Visual Studio Build Tools, NVIDIA driver, and CUDA setup.
