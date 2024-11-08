import os
import shutil

from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from typing import Annotated

from dto.coreResponseDto import CoreResponseDto
from dto.imageUploadDto import ImageUploadDTO

from utils.loggerUtils import Logger

from handleDeeplearning.detectron.utils.detectronUtils import DetectronUtil
from handleDeeplearning.vietocr.utils.vietOCRUils import VietOCRUtils

import io

logger = Logger(__name__)

router = APIRouter(
    prefix="/example",
    tags=[""]
)

vietOCR = VietOCRUtils()
detectron = DetectronUtil(vietOCR)

@router.post("/", status_code=status.HTTP_200_OK)
async def upload_image(dto: Annotated[ImageUploadDTO, Form()]):
    try:
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)

        # Đặt tên tệp lưu trữ
        file_location = os.path.join(upload_dir, dto.file.filename)
        
        # Lưu tệp vào thư mục với chế độ nhị phân (binary)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(dto.file.file, buffer)  # Sao chép dữ liệu tệp vào buffer
            
        result = detectron.getDetectedObjects(file_location)

        # Trả về thông tin về tệp đã tải lên
        return CoreResponseDto("success",status.HTTP_200_OK,"Operation completed successfully.",result)
        # return {"result": result}

    except Exception as e:
        # Nếu có lỗi, trả về phản hồi lỗi
        logger.ERROR("An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
        
        