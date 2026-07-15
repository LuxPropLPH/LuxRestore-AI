from pathlib import Path
import logging
from typing import List

logger = logging.getLogger("grounding_dino_playground.model_manager")

class ModelManager:
    """Manages local model weights and configurations."""

    REQUIRED_FILES = [
        "config.json",
        "preprocessor_config.json",
        "tokenizer_config.json",
        "tokenizer.json",
        "vocab.txt",
        "special_tokens_map.json",
        "added_tokens.json",
    ]
    
    def __init__(self, cache_dir: Path, model_id: str):
        self.cache_dir = cache_dir
        self.model_id = model_id

    def missing_model_files(self) -> List[str]:
        """Return required model artifacts that are not present locally."""
        missing = []

        if not self.cache_dir.exists():
            return [
                "weights/grounding_dino directory",
                *self.REQUIRED_FILES,
                "model.safetensors or pytorch_model.bin",
            ]

        for filename in self.REQUIRED_FILES:
            if not self._has_file(filename):
                missing.append(filename)

        has_safetensors = any(self.cache_dir.glob("*.safetensors")) or any(
            self.cache_dir.glob("**/*.safetensors")
        )
        has_pytorch_bin = self._has_file("pytorch_model.bin") or any(
            self.cache_dir.glob("*.bin")
        )
        if not has_safetensors and not has_pytorch_bin:
            missing.append("model.safetensors or pytorch_model.bin")

        return missing

    def check_model_files(self) -> bool:
        """Checks if model files are present locally."""
        return not self.missing_model_files()

    def get_local_path(self) -> str:
        """Returns the local path or raises instruction error if missing."""
        missing = self.missing_model_files()
        if missing:
            missing_list = "\n".join(f"   - {item}" for item in missing)
            instructions = f"""
[ERROR] GroundingDINO model files are missing in:
{self.cache_dir.resolve()}

Missing required files:
{missing_list}

To run this playground script, please manually set up the files:
Hugging Face model:
   {self.model_id}

Download instructions:
1. Open:
   https://huggingface.co/{self.model_id}/tree/main
2. Download all required files listed above.
3. Save them directly under:
   {self.cache_dir.resolve()}
            """
            raise FileNotFoundError(instructions)
            
        logger.info(f"Model files found locally at: {self.cache_dir.resolve()}")
        return str(self.cache_dir)

    def _has_file(self, filename: str) -> bool:
        return (self.cache_dir / filename).exists() or any(
            self.cache_dir.glob(f"**/{filename}")
        )
