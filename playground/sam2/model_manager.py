from pathlib import Path
from typing import List


class ModelManager:
    """Validates local SAM2 model artifacts without downloading anything."""

    REQUIRED_FILES = [
        "config.json",
        "model.safetensors",
        "preprocessor_config.json",
        "processor_config.json",
    ]

    def __init__(self, cache_dir: Path, model_id: str):
        self.cache_dir = cache_dir
        self.model_id = model_id

    def missing_model_files(self) -> List[str]:
        if not self.cache_dir.exists():
            return ["weights/sam2 directory", *self.REQUIRED_FILES]

        return [
            filename
            for filename in self.REQUIRED_FILES
            if not (self.cache_dir / filename).exists()
        ]

    def get_local_path(self) -> str:
        missing = self.missing_model_files()
        if missing:
            missing_list = "\n".join(f"   - {item}" for item in missing)
            raise FileNotFoundError(
                f"""
[ERROR] SAM2 model files are missing in:
{self.cache_dir.resolve()}

Missing required files:
{missing_list}

Hugging Face model:
   {self.model_id}

Download instructions:
1. Open:
   https://huggingface.co/{self.model_id}/tree/main
2. Download all required files listed above.
3. Save them directly under:
   {self.cache_dir.resolve()}
"""
            )

        return str(self.cache_dir)
