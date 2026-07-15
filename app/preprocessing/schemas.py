from pydantic import BaseModel
from typing import Union

class ImageSource(BaseModel):
    data: Union[str, bytes]
    is_path: bool = False
    is_base64: bool = False
    is_url: bool = False
