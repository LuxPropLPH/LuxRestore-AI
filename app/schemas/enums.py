from enum import Enum

class DetectionType(str, Enum):
    WATERMARK = "WATERMARK"
    LOGO = "LOGO"
    TEXT_OVERLAY = "TEXT_OVERLAY"
    TIMESTAMP = "TIMESTAMP"
    OBJECT = "OBJECT"

class ProviderType(str, Enum):
    YOLO = "YOLO"
    GROUNDING_DINO = "GROUNDING_DINO"
    FLORENCE2 = "FLORENCE2"
    SAM2 = "SAM2"
    LAMA = "LAMA"
    MAT = "MAT"
    SDXL = "SDXL"
    MOCK = "MOCK"
    OPENCV = "OPENCV"
