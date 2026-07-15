from typing import Any, Dict, List

from PIL import Image


class SAM2TransformersAdapter:
    """Hugging Face Transformers adapter for SAM2 image segmentation."""

    def __init__(self):
        self.processor = None
        self.model = None
        self.device = "cpu"

    def load(self, model_path: str, device: str) -> None:
        from transformers import Sam2Model, Sam2Processor

        self.device = device
        self.processor = Sam2Processor.from_pretrained(model_path, local_files_only=True)
        self.model = Sam2Model.from_pretrained(model_path, local_files_only=True)
        self.model.to(self.device)
        self.model.eval()

    def generate_masks(
        self,
        image: Image.Image,
        boxes: List[List[float]],
        mask_threshold: float,
    ) -> Dict[str, Any]:
        import torch

        inputs = self.processor(
            images=image,
            input_boxes=[boxes],
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs, multimask_output=False)

        masks = self.processor.post_process_masks(
            outputs.pred_masks.detach().cpu(),
            inputs["original_sizes"].detach().cpu(),
            mask_threshold=mask_threshold,
            binarize=True,
        )[0]

        return {
            "masks": masks,
            "iou_scores": getattr(outputs, "iou_scores", None),
        }
