# Model Inventory

LuxRestore-AI currently validates models in `playground/`. Production providers under `app/` remain mock/scaffolded.

## GroundingDINO

Purpose:

- Detect watermark regions from a text prompt.

Version/model:

- `IDEA-Research/grounding-dino-tiny`

Official source:

- `https://huggingface.co/IDEA-Research/grounding-dino-tiny`

Expected folder:

```text
weights/grounding_dino/
```

Required files:

```text
added_tokens.json
config.json
model.safetensors
preprocessor_config.json
special_tokens_map.json
tokenizer.json
tokenizer_config.json
vocab.txt
```

Current prompt:

```text
gold logo. red text. small watermark.
```

Current threshold:

```text
0.25
```

## SAM2

Purpose:

- Convert GroundingDINO bounding boxes into binary masks.

Version/model:

- `facebook/sam2-hiera-tiny`

Official source:

- `https://huggingface.co/facebook/sam2-hiera-tiny`

Expected folder:

```text
weights/sam2/
```

Required files:

```text
config.json
model.safetensors
preprocessor_config.json
processor_config.json
```

## LaMa

Purpose:

- Inpaint the masked watermark regions.

Version/model:

- `big-lama`

Expected folder:

```text
weights/lama/
```

Checkpoint:

```text
weights/lama/models/best.ckpt
```

Config:

```text
weights/lama/config.yaml
```

Current LaMa mask dilation:

```text
11px
```

## Future Models

MAT:

- Placeholder for transformer-based inpainting validation.

Real-ESRGAN:

- Placeholder for restoration/upscaling validation.

SDXL Inpainting:

- Placeholder for diffusion-based inpainting validation.
