from pathlib import Path
import logging

logger = logging.getLogger("grounding_dino_playground.model_manager")

class ModelManager:
    """Manages local model weights and configurations."""
    
    def __init__(self, cache_dir: Path, model_id: str):
        self.cache_dir = cache_dir
        self.model_id = model_id

    def check_model_files(self) -> bool:
        """Checks if model files are present locally."""
        if not self.cache_dir.exists():
            return False
        
        config_exists = any(self.cache_dir.glob("config.json")) or any(self.cache_dir.glob("**/config.json"))
        weights_exists = any(self.cache_dir.glob("*.bin")) or any(self.cache_dir.glob("**/pytorch_model.bin")) or any(self.cache_dir.glob("**/*.safetensors"))
        
        return config_exists and weights_exists

    def get_local_path(self) -> str:
        """Returns the local path or raises instruction error if missing."""
        if not self.check_model_files():
            instructions = f"""
[ERROR] GroundingDINO model files are missing in:
{self.cache_dir.resolve()}

To run this playground script, please manually set up the files:
1. Download the config and weights for '{self.model_id}' from Hugging Face:
   - https://huggingface.co/IDEA-Research/groundingdino-tiny/tree/main
2. Save 'config.json', 'preprocessor_config.json', and 'model.safetensors' (or 'pytorch_model.bin') under:
   {self.cache_dir.resolve()}
            """
            raise FileNotFoundError(instructions)
            
        logger.info(f"Model files found locally at: {self.cache_dir.resolve()}")
        return str(self.cache_dir)
