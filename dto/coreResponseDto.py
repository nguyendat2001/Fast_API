from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class CoreResponseDto(BaseModel):
    status: str  # Trạng thái của phản hồi (ví dụ: "success" hoặc "error")
    code: int  # Mã code của phản hồi (ví dụ: mã HTTP hoặc mã riêng cho từng loại phản hồi)
    message: Optional[str] = None  # Thông báo mô tả kết quả hoặc lỗi
    data: Optional[Any] = None  # Nội dung dữ liệu phản hồi (nếu có)

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Operation completed successfully.",
                "data": {
                    "key": "value"
                }
            }
        }