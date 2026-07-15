# LuxRestore-AI

LuxRestore-AI is a modular AI image-restoration project for detecting, segmenting, and removing watermarks from property images. The project is currently validating its AI pipeline in `playground/` before integrating real inference into the production FastAPI app.

## Features

- FastAPI application scaffold with health and debug locator endpoints.
- Playground-validated GroundingDINO watermark detection.
- Playground-only geometric detection post-processing.
- Playground-validated SAM2 mask generation.
- Playground-validated LaMa inpainting.
- Local-only model loading from `weights/`.
- Reproducible validation outputs under `output/<image>/`.

## Architecture

```text
Validation Image
  |
  v
GroundingDINO
  |
  v
Post Processing
  |
  v
SAM2
  |
  v
LaMa
  |
  v
Restored Image
```

Production architecture under `app/` is frozen and still uses mock/provider abstractions. Real AI inference is currently validated in `playground/` only.

## Technology Stack

- Python 3.10+
- FastAPI
- Pydantic / pydantic-settings
- PyTorch
- Hugging Face Transformers
- GroundingDINO Tiny
- SAM2 Hiera Tiny
- LaMa / Big-LaMa checkpoint
- OpenCV
- Pillow
- pytest

## Directory Structure

```text
app/                     Production FastAPI scaffold and provider abstractions
docs/                    Project documentation
playground/              Real model validation modules
  grounding_dino/        Detection validation
  sam2/                  Mask validation
  lama/                  Inpainting validation
tests/                   Unit/API tests
validation/              Local validation images
weights/                 Local model weights, not downloaded automatically
output/                  Validation artifacts
scripts/                 Reserved for setup/verification scripts
```

## Current Project Status

- Production API: scaffolded.
- Production real inference: not integrated.
- Playground GroundingDINO: validated.
- Playground post-processing: validated.
- Playground SAM2: validated.
- Playground LaMa: validated on `validation/1.jpg` through `validation/10.jpg`.
- Quality evaluation: in progress.

## Current Validated Pipeline

```text
validation/<image>.jpg
  -> playground/grounding_dino/run.py
  -> playground/sam2/run.py
  -> playground/lama/run.py
  -> output/<image>/restored.png
```

## Screenshots

Placeholder: add restored image comparisons from `output/<image>/comparison.jpg`.

## Quick Start

Preferred setup flow:

```powershell
git clone <repository>
cd LuxRestore-AI

.\scripts\setup_windows.ps1

python scripts\verify_install.py

uvicorn app.main:app --reload
```

Note: `scripts/setup_windows.ps1` and `scripts/verify_install.py` are referenced as the intended setup commands, but the current repository only contains `scripts/.gitkeep`. Until those scripts are added, use the manual setup in [docs/INSTALLATION.md](docs/INSTALLATION.md).

Manual API startup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Run tests:

```powershell
pytest
```

Run the latest validated playground pipeline for one image:

```powershell
.venv\Scripts\python.exe -B playground\grounding_dino\run.py --image validation\1.jpg
.venv\Scripts\python.exe -B playground\sam2\run.py --image validation\1.jpg
.venv\Scripts\python.exe -B playground\lama\run.py --image validation\1.jpg
```

## Documentation

- [Project State](docs/PROJECT_STATE.md)
- [Installation](docs/INSTALLATION.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Models](docs/MODELS.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)
- [Architecture](docs/architecture.md)
- [Technology Validation](docs/technology-validation.md)

## Requirements

Minimum:

- Windows 10/11
- Python 3.10+
- Git
- 16 GB RAM
- 15 GB free disk space for repository, dependencies, outputs, and model weights
- CPU-only execution supported for validation, but slow

Recommended:

- Windows 11
- Python 3.10 or 3.11
- NVIDIA GPU with current driver
- CUDA-compatible PyTorch install
- 32 GB RAM
- 8 GB+ VRAM
- 30 GB free disk space

## API Endpoints

- `GET /`
- `GET /health`
- `POST /locate`

`POST /restore` is not implemented yet.

## Roadmap Summary

- Finish quality evaluation for restored outputs.
- Improve batch runtime by reusing loaded models.
- Broaden validation dataset coverage.
- Integrate validated providers into `app/`.
- Add production `POST /restore`.
- Add n8n integration.

## Contributing

Placeholder: contribution guidelines will be added once the project moves beyond local validation.

## License

Placeholder: license information has not been finalized.
