# Technology Validation Plan

## Purpose

Before integrating any AI model into the production pipeline, each candidate
must be evaluated in isolation inside the `playground/` directory. This
document defines what "ready for integration" means.

---

## Success Criteria

A model is approved for production integration when it meets **all** of the
following thresholds on the validation image set:

| Stage       | Metric                | Threshold        |
|-------------|----------------------|------------------|
| Locator     | Detection Recall     | ≥ 90%            |
| Locator     | False Positive Rate  | ≤ 5%             |
| Locator     | Latency (per image)  | ≤ 500 ms         |
| Mask        | IoU vs Ground Truth  | ≥ 85%            |
| Mask        | Latency (per image)  | ≤ 300 ms         |
| Inpainter   | LPIPS                | ≤ 0.10           |
| Inpainter   | SSIM                 | ≥ 0.90           |
| Inpainter   | PSNR                 | ≥ 30 dB          |
| Inpainter   | Latency (per image)  | ≤ 2000 ms        |
| Full Pipeline | Total Latency      | ≤ 3000 ms        |
| Full Pipeline | Peak GPU Memory    | ≤ 6 GB           |

---

## Evaluation Metrics

### Detection (Locator)
- **Precision** — ratio of true watermarks among all detections.
- **Recall** — ratio of detected watermarks among all actual watermarks.
- **False Positive Rate** — detections on clean (no-watermark) images.
- **Latency** — wall-clock time per image (ms).
- **GPU Memory** — peak VRAM during inference (MB).

### Segmentation (Mask)
- **IoU (Intersection over Union)** — overlap between predicted and ground truth masks.
- **Boundary Accuracy** — edge quality of predicted masks.
- **Latency / Memory** — same as above.

### Inpainting
- **LPIPS** — perceptual similarity (lower is better).
- **SSIM** — structural similarity (higher is better).
- **PSNR** — signal-to-noise ratio (higher is better).
- **Visual Coherence** — manual inspection for artifacts, color shift, blurring.
- **Latency / Memory** — same as above.

---

## Hardware

Validation will be run on the following hardware configurations:

| Component | Specification                     |
|-----------|-----------------------------------|
| GPU       | NVIDIA RTX 3090 / 4090 (24 GB)   |
| CPU       | AMD Ryzen 9 / Intel i9            |
| RAM       | 32–64 GB DDR5                     |
| Storage   | NVMe SSD                         |
| OS        | Windows 11 / Ubuntu 22.04        |
| Python    | 3.10+                            |
| CUDA      | 12.x                             |

> Models must also be tested on **CPU-only** to verify graceful fallback.

---

## Candidate Models

### Locator (Watermark Detection)

| Model            | Type              | Notes                                    |
|------------------|-------------------|------------------------------------------|
| YOLOv8 / v11     | Supervised        | Fast, accurate, needs training data      |
| GroundingDINO    | Open-set          | Zero-shot with text prompts              |
| Florence-2       | Unified vision    | Multi-task, Microsoft                    |
| OpenCV Templates | Classical CV      | Baseline, no GPU required                |

### Mask Generation (Segmentation)

| Model      | Type                | Notes                                   |
|------------|---------------------|-----------------------------------------|
| SAM2       | Foundation model    | Prompt-based, Meta                      |
| U2-Net     | Salient object      | Lightweight, good for binary masks      |
| GrabCut    | Classical CV        | Baseline, OpenCV built-in               |

### Inpainting (Image Restoration)

| Model            | Type               | Notes                                  |
|------------------|--------------------|----------------------------------------|
| LaMa             | CNN-based          | Fast, excellent for large masks        |
| MAT              | Transformer-based  | Higher quality, slower                 |
| SDXL Inpainting  | Diffusion-based    | Highest quality, highest latency       |
| OpenCV Telea     | Classical CV       | Baseline                               |

---

## Validation Workflow

```
playground/
  01_locator_test.py    →  Evaluate locator candidates
  02_mask_test.py       →  Evaluate mask candidates
  03_inpaint_test.py    →  Evaluate inpainter candidates
  04_pipeline_test.py   →  Chain best performers end-to-end
```

1. Run each `0N_*.py` script with every candidate model.
2. Record results in a comparison table.
3. Models meeting all thresholds above are approved for production integration.
4. Integrate approved models into `app/providers/` via the provider framework.

---

## Status

| Script                  | Status          |
|-------------------------|-----------------|
| `01_locator_test.py`    | PLACEHOLDER     |
| `02_mask_test.py`       | PLACEHOLDER     |
| `03_inpaint_test.py`    | PLACEHOLDER     |
| `04_pipeline_test.py`   | PLACEHOLDER     |
