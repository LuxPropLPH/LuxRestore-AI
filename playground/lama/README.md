# LaMa Inpainting Playground

Runs real LaMa inpainting using outputs from the playground pipeline:

```text
GroundingDINO -> post-processing -> SAM2 -> LaMa
```

The LaMa model is loaded only from:

```text
weights/lama/
```

Required files:

```text
config.yaml
models/best.ckpt
```

Run:

```bash
python playground/lama/run.py --image validation/1.jpg
```

Outputs are written to `output/<image_name>/`:

```text
restored.png
comparison.jpg
experiment_lama.txt
```
