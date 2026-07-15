# Deployment Guide

Production deployment is not complete yet. The current production app is a FastAPI scaffold with mock/provider abstractions. Real model inference is validated in `playground/`.

## Windows Deployment

Install prerequisites:

- Python 3.10+
- Git
- Git LFS
- Model weights under `weights/`

Start the API:

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

## Linux Deployment

Placeholder. Linux deployment has not been validated in this repository.

## Docker Deployment

Placeholder. Docker deployment has not been added.

## FastAPI Deployment

Current endpoints:

- `GET /`
- `GET /health`
- `POST /locate`

Production `POST /restore` is not implemented.

For production, run behind a process manager and reverse proxy. Example future command:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Model Loading

Current real model loading happens in playground modules only:

- `playground/grounding_dino/`
- `playground/sam2/`
- `playground/lama/`

Production provider loading is not yet connected to these real models.

## Environment Variables

Validated playground variables:

```powershell
$env:DEVICE="cpu"
$env:DEVICE="cuda"
$env:CONF_THRESHOLD="0.25"
$env:SECONDARY_DETECTION_THRESHOLD="0.30"
$env:LAMA_MASK_DILATION_PX="11"
$env:LAMA_REPO_DIR="D:\lama"
```

## GPU Configuration

CPU fallback is validated. CUDA execution is supported by code paths but was not validated in the latest run because the environment reported:

```text
torch.cuda.is_available() == False
```

For GPU deployment:

- Install current NVIDIA driver.
- Install CUDA-compatible PyTorch.
- Set `DEVICE=cuda`.
- Verify all three model stages run on GPU.

## CPU Fallback

CPU fallback works for validation but is slower. The first 10 end-to-end validation images completed on CPU.

## n8n Integration Overview

Future n8n flow:

```text
n8n
  -> receive image
  -> POST /restore
  -> LuxRestore-AI
  -> return restored image
  -> continue workflow
```

This requires production `POST /restore`, which is not implemented yet.

## Logging

Current logging is standard Python logging. Playground modules log progress to stdout.

## Monitoring

Placeholder. Production monitoring is not implemented.

Recommended future metrics:

- Request count
- Runtime per stage
- GPU memory
- Failure rate
- Model load time
- Output quality classification

## Future Production Recommendations

- Add production `POST /restore`.
- Reuse loaded models across requests.
- Add structured logs.
- Add request IDs through the full pipeline.
- Add model warmup.
- Add GPU memory checks.
- Add health endpoint that validates model readiness.
