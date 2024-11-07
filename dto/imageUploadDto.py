from pydantic import BaseModel
from pydantic import Field
from fastapi import UploadFile, File
from typing import Optional


class ImageUploadDTO(BaseModel):
    """
    DTO cho việc tải lên hình ảnh, có thể mở rộng thêm các trường khác.
    """
    description: str = Field(..., min_length=4)
    file: UploadFile = File(...)  # Trường tệp tải lên (UploadFile là kiểu dữ liệu cho file tải lên)

    class Config:
        # Tùy chọn thêm cho Pydantic model
        arbitrary_types_allowed = True
