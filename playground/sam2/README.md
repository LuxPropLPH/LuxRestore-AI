# SAM2 Mask Validation Playground

This playground validates SAM2 mask generation using GroundingDINO detections
already written under `output/<image_name>/`.

## Required Inputs

For `validation/1.jpg`, the GroundingDINO run must already have produced:

```text
output/1/original.jpg
output/1/detections.json
```

## Local Model Files

The SAM2 model is loaded only from:

```text
weights/sam2/
```

Use the official Hugging Face model:

```text
facebook/sam2-hiera-tiny
```

Required files:

```text
config.json
model.safetensors
preprocessor_config.json
processor_config.json
```

## Run

```bash
python playground/sam2/run.py --image validation/1.jpg
```

## Outputs

The run writes these files into `output/1/`:

```text
mask.png
mask_overlay.jpg
mask_metadata.json
experiment_mask.txt
```
