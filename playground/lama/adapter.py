from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch
import yaml
from omegaconf import OmegaConf
from torch.utils.data._utils.collate import default_collate


class LaMaAdapter:
    def __init__(self, lama_repo_dir: Path):
        self.lama_repo_dir = lama_repo_dir
        self.model = None
        self.train_config = None
        self.device = "cpu"

    def load(self, model_path: Path, device: str) -> None:
        self._prepare_legacy_imports()

        import sys

        if str(self.lama_repo_dir) not in sys.path:
            sys.path.insert(0, str(self.lama_repo_dir))

        from saicinpainting.training.trainers import load_checkpoint

        self.device = device
        train_config_path = model_path / "config.yaml"
        checkpoint_path = model_path / "models" / "best.ckpt"

        with open(train_config_path, "r", encoding="utf-8") as f:
            self.train_config = OmegaConf.create(yaml.safe_load(f))

        self.train_config.training_model.predict_only = True
        self.train_config.visualizer.kind = "noop"

        original_torch_load = torch.load
        torch.load = lambda *args, **kwargs: original_torch_load(
            *args,
            **{**kwargs, "weights_only": False},
        )
        try:
            self.model = load_checkpoint(
                self.train_config,
                str(checkpoint_path),
                strict=False,
                map_location="cpu",
            )
        finally:
            torch.load = original_torch_load

        self.model.freeze()
        self.model.to(torch.device(self.device))

    def inpaint(self, input_dir: Path) -> np.ndarray:
        self._prepare_legacy_imports()

        from saicinpainting.evaluation.utils import move_to_device
        from saicinpainting.training.data.datasets import make_default_val_dataset

        dataset = make_default_val_dataset(
            str(input_dir),
            kind="default",
            img_suffix=".png",
            pad_out_to_modulo=8,
        )
        if len(dataset) != 1:
            raise ValueError(f"Expected one LaMa input sample, found {len(dataset)}")

        batch = default_collate([dataset[0]])
        with torch.no_grad():
            batch = move_to_device(batch, torch.device(self.device))
            batch["mask"] = (batch["mask"] > 0) * 1
            batch = self.model(batch)
            result = batch["inpainted"][0].permute(1, 2, 0).detach().cpu().numpy()
            unpad_to_size = batch.get("unpad_to_size")
            if unpad_to_size is not None:
                orig_height, orig_width = unpad_to_size
                result = result[:orig_height, :orig_width]

        result = np.clip(result * 255, 0, 255).astype("uint8")
        return cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    def _prepare_legacy_imports(self) -> None:
        # Old LaMa dependencies expect np.sctypes, removed in NumPy 2.x.
        if not hasattr(np, "sctypes"):
            np.sctypes = {
                "float": [np.float16, np.float32, np.float64],
                "int": [np.int8, np.int16, np.int32, np.int64],
                "uint": [np.uint8, np.uint16, np.uint32, np.uint64],
                "complex": [np.complex64, np.complex128],
                "others": [np.bool_, np.object_, np.bytes_, np.str_],
            }
