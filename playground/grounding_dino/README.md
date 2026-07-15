# GroundingDINO Technology Validation Playground

This folder contains the experimental setup for evaluating the zero-shot detector GroundingDINO for watermark detection.

## Directory Structure

```
playground/grounding_dino/
  ├── config.py       # Playground configurations (device, threshold, prompt)
  ├── loader.py       # Handles validation image input
  ├── locator.py      # GroundingDINOLocator logic
  ├── visualizer.py   # Draws outputs and overlays detections
  ├── utils.py        # Shared logger configuration
  └── runner.py       # Batch/Single runner CLI script
```

## Setup Requirements

Install the PyTorch and Hugging Face Transformers dependencies:
```bash
pip install torch transformers torchvision pillow
```

## Running Evaluations

Run the validation suite against all images in `validation/`:
```bash
python playground/grounding_dino/runner.py
```

This will:
1. Load all supported images (JPEG, PNG, WEBP) from `validation/`.
2. Download the GroundingDINO model configuration and weights to `weights/grounding_dino` if missing.
3. Compute predictions using prompt `"watermark"`.
4. Output results to `output/` with bounding box overlays.
5. Create a report in `experiments/experiment_001.md`.
