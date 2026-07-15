# Troubleshooting

## Git LFS

Symptom:

- Model files are missing or tiny pointer files.

Fix:

```powershell
git lfs install
git lfs pull
```

## Torch Installation

Symptom:

- `ModuleNotFoundError: No module named 'torch'`

Fix:

```powershell
python -m pip install -r playground\requirements.txt
```

For CUDA, install the PyTorch build matching your CUDA/NVIDIA driver.

## CUDA Mismatch

Symptom:

- `torch.cuda.is_available()` returns `False`.

Fix:

- Update NVIDIA driver.
- Install CUDA-compatible PyTorch.
- Confirm GPU support:

```powershell
.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available())"
```

## Transformers Version Mismatch

Symptom:

- GroundingDINO post-processing keyword errors.

Validated fix:

- The playground adapter uses `threshold=` and `text_threshold=` for the installed Transformers API.

## GroundingDINO Loading

Symptom:

- Missing files under `weights/grounding_dino/`.

Required files are listed in [MODELS.md](MODELS.md).

## SAM2 Loading

Symptom:

- Missing files under `weights/sam2/`.

Required files are listed in [MODELS.md](MODELS.md).

Known warning:

```text
You are using a model of type `sam2_video` to instantiate a model of type `sam2`.
```

This appeared during validation and did not prevent mask generation.

## LaMa Loading

Symptom:

- Missing `config.yaml` or `models/best.ckpt`.

Fix:

- Place the local LaMa files under:

```text
weights/lama/config.yaml
weights/lama/models/best.ckpt
```

## Albumentations Compatibility

Symptom:

```text
cannot import name 'DualIAATransform'
```

Fix:

```powershell
python -m pip install "albumentations==0.5.2" "imgaug==0.4.0"
```

## NumPy Compatibility

Symptom:

```text
np.sctypes was removed in the NumPy 2.0 release
```

Validated workaround:

- The LaMa playground adapter applies a local compatibility shim before importing old LaMa dependencies.

## PyTorch weights_only Changes

Symptom:

```text
Weights only load failed
```

Validated workaround:

- The LaMa playground adapter loads the trusted local checkpoint with `weights_only=False`.

## Hydra Configuration

Symptom:

- LaMa config or Hydra import errors.

Fix:

```powershell
python -m pip install hydra-core omegaconf
```

## Model Path Errors

Symptom:

- Loader reports files missing.

Fix:

- Confirm the exact folder and filenames in [MODELS.md](MODELS.md).
- Paths are relative to repository root.

## Missing Checkpoint Errors

Symptom:

- LaMa cannot find `best.ckpt`.

Fix:

```text
weights/lama/models/best.ckpt
```

## Windows Path Issues

Use PowerShell paths:

```powershell
.\.venv\Scripts\Activate.ps1
.venv\Scripts\python.exe -B playground\grounding_dino\run.py --image validation\1.jpg
```

## Permission Errors

Symptoms:

- Access denied creating cache folders.
- Git index lock permission errors in sandboxed environments.

Fix:

- Use a writable project-local cache where supported.
- Re-run Git operations with appropriate permissions.

## Git Push Issues

If large weights were accidentally staged:

```powershell
git status
git rm --cached <large-file>
```

Weights should not be committed directly unless Git LFS is configured.

## GitHub Large File Issues

Use Git LFS for large model files:

```powershell
git lfs track "*.ckpt"
git lfs track "*.safetensors"
```

## Codex Environment Issues

Observed:

- Network access may require approval for `pip install`.
- `.pytest_cache/` may show permission warnings.
- Git index writes may require approval.

## Common Python Package Conflicts

Known validated pins:

```powershell
python -m pip install "albumentations==0.5.2" "imgaug==0.4.0"
```

If package conflicts appear, create a fresh `.venv` and reinstall from the documented commands.
