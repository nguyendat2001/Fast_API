import os
import shutil

from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import FastAPI, Form

from typing import Annotated

from dto.coreResponseDto import CoreResponseDto
from dto.imageUploadDto import ImageUploadDTO, ArrayImageUploadDTO

from utils.loggerUtils import Logger

from handleDeeplearning.ocrLLM.unitOcr import llm_json, Unit_OCR

logger = Logger(__name__)

router = APIRouter(
    prefix="/invoice",
    tags=[""]
)


# Đặt khóa vào biến
llama_Index_key = "llx-aXbktTh1fLEFqo9flBkpZJUVYIeI25DIm9LKBkXr6A4ITGKY"

unit_ocr = Unit_OCR(llm_json, "", llama_Index_key)


@router.post("/tam_anh", status_code=status.HTTP_200_OK)
async def hos_tam_anh(data: ArrayImageUploadDTO):
    try:
        upload_dir = "uploaded_files/invoive/tamanhs"
        os.makedirs(upload_dir, exist_ok=True)
        files = data.files
        array_img = []

        # Xử lý mỗi tệp trong danh sách
        for idx, file in enumerate(files):
            # Tạo tên mới cho tệp để tránh trùng lặp (có thể sử dụng các phương pháp khác)
            outPath = os.path.join(upload_dir, f"image_{idx+1}_{file.filename}")
            
            # Đọc nội dung tệp và lưu vào đĩa
            content = await file.read()
            with open(outPath, "wb") as f:
                f.write(content)
            
            # Thêm đường dẫn của tệp vào danh sách
            array_img.append(outPath)

        json_output = unit_ocr.inferenceHosTamAnh(array_img)
        # Trả về thông tin về tệp đã tải lên
        return CoreResponseDto(
            status="success",
            code=status.HTTP_200_OK,
            message="Operation completed successfully.",
            data=json_output
        )

    except Exception as e:
        # Nếu có lỗi, trả về phản hồi lỗi
        logger.ERROR("An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/hos_110", status_code=status.HTTP_200_OK)
async def hos_110(data: ArrayImageUploadDTO):
    try:
        upload_dir = "uploaded_files/invoive/hos_108"
        os.makedirs(upload_dir, exist_ok=True)
        files = data.files
        array_img = []

        # Xử lý mỗi tệp trong danh sách
        for idx, file in enumerate(files):
            # Tạo tên mới cho tệp để tránh trùng lặp (có thể sử dụng các phương pháp khác)
            outPath = os.path.join(upload_dir, f"image_{idx+1}_{file.filename}")
            
            # Đọc nội dung tệp và lưu vào đĩa
            content = await file.read()
            with open(outPath, "wb") as f:
                f.write(content)
            
            # Thêm đường dẫn của tệp vào danh sách
            array_img.append(outPath)

        json_output = unit_ocr.inferenceHos110(array_img)
        # Trả về thông tin về tệp đã tải lên
        return CoreResponseDto(
            status="success",
            code=status.HTTP_200_OK,
            message="Operation completed successfully.",
            data=json_output
        )

    except Exception as e:
        # Nếu có lỗi, trả về phản hồi lỗi
        logger.ERROR("An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/cccd", status_code=status.HTTP_200_OK)
async def upload_image(dto: Annotated[ImageUploadDTO, Form()]):
    try:
        upload_dir = "uploaded_files/documents"
        os.makedirs(upload_dir, exist_ok=True)

        # Đặt tên tệp lưu trữ
        file_location = os.path.join(upload_dir, dto.file.filename)
        
        # Lưu tệp vào thư mục với chế độ nhị phân (binary)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(dto.file.file, buffer)  # Sao chép dữ liệu tệp vào buffer

        json_output = unit_ocr.inferenceIdCard(file_location)

        # Trả về thông tin về tệp đã tải lên
        return CoreResponseDto(
            status="success",
            code=status.HTTP_200_OK,
            message="Operation completed successfully.",
            data=json_output
        )

        # return {"result": result}

    except Exception as e:
        # Nếu có lỗi, trả về phản hồi lỗi
        logger.ERROR("An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")