from pathlib import Path
from typing import List


class ModelManager:
    REQUIRED_FILES = [
        "config.yaml",
        "models/best.ckpt",
    ]

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir

    def missing_model_files(self) -> List[str]:
        if not self.cache_dir.exists():
            return ["weights/lama directory", *self.REQUIRED_FILES]
        return [
            filename
            for filename in self.REQUIRED_FILES
            if not (self.cache_dir / filename).exists()
        ]

    def get_model_path(self) -> Path:
        missing = self.missing_model_files()
        if missing:
            missing_list = "\n".join(f"   - {item}" for item in missing)
            raise FileNotFoundError(
                f"""
[ERROR] LaMa model files are missing in:
{self.cache_dir.resolve()}

Missing required files:
{missing_list}

Place the local LaMa model files directly under:
   {self.cache_dir.resolve()}
"""
            )
        return self.cache_dir
