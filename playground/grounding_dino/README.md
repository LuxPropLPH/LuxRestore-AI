# GroundingDINO Technology Validation Playground

This folder contains the experimental setup for evaluating the zero-shot detector GroundingDINO for watermark detection.

## Directory Structure

```text
playground/grounding_dino/
  config.py       # Playground configurations (device, threshold, prompt)
  loader.py       # Handles validation image input
  locator.py      # GroundingDINOLocator logic
  visualizer.py   # Draws outputs and overlays detections
  utils.py        # Shared logger configuration
  run.py          # Batch/single validation entrypoint
```

## Setup Requirements

Install the playground AI dependencies:

```bash
pip install -r playground/requirements.txt
```

## Running Evaluations

Run the validation suite against all images in `validation/` from the repository root:

```bash
python playground/grounding_dino/run.py
```

This will:

1. Load all supported images (JPEG, PNG, WEBP) from `validation/`.
2. Use local GroundingDINO model files from `weights/grounding_dino`.
3. Compute predictions using prompt `"watermark"`.
4. Output results to `output/` with bounding box overlays.
5. Create a report in `experiments/experiment_001.md`.
