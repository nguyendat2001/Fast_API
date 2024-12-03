import os
import shutil

import numpy as np

from datetime import datetime
from datetime import timezone
import time

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import FastAPI, Form

from typing import Annotated

from dto.coreResponseDto import CoreResponseDto
from dto.imageUploadDto import ImageUploadDTO, ArrayImageUploadDTO

from utils.loggerUtils import Logger

from handleDeeplearning.ocrLLM.unitOcr import llm_json, Unit_OCR
from handleDeeplearning.unit.unitOCR import unitOCR as DeepLearningUnit

# from handleDeeplearning.unit.unitOCR import unitOCR as DeepLearningUnit
from utils.utils import convert_to_serializable

logger = Logger(__name__)

router = APIRouter(
    prefix="/invoice/v2",
    tags=[""]
)

text_detection_anotation = "/content/source_weight/meta_data/text_detection/_annotations.coco.json"
doc_structure_anotation = "/content/source_weight/meta_data/doc_structure/_annotations.coco.json"
table_cell_anotation = "/content/source_weight/meta_data/cell_text/_annotations.coco.json"

# Đặt khóa vào biến
llama_Index_key = "llx-aXbktTh1fLEFqo9flBkpZJUVYIeI25DIm9LKBkXr6A4ITGKY"

unit_ocr = Unit_OCR(llm_json, "", llama_Index_key)
dlUnit = DeepLearningUnit(None, text_detection_anotation, doc_structure_anotation, table_cell_anotation)

@router.post("/tam_anh", status_code=status.HTTP_200_OK)
async def hos_tam_anh(data: Annotated[ArrayImageUploadDTO, Form()]):
    try:
        upload_dir = "uploaded_files/invoive/v2/tamanhs"
        os.makedirs(upload_dir, exist_ok=True)
        files = data.files
        array_img = []

        # Xử lý mỗi tệp trong danh sách
        for idx, file in enumerate(files):
            # Tạo tên mới cho tệp để tránh trùng lặp (có thể sử dụng các phương pháp khác)
            outPath = os.path.join(upload_dir, f"image_{int(time.time())}_{file.filename}")
            
            # Đọc nội dung tệp và lưu vào đĩa
            content = await file.read()
            with open(outPath, "wb") as f:
                f.write(content)
            
            # Thêm đường dẫn của tệp vào danh sách
            array_img.append(outPath)
        
        header_text, sumary_text, table_raw_data, confident_scores = dlUnit.predict(array_img)
        json_output = unit_ocr.inferenceHosTamAnhWithOutParse("\n".join(header_text) + "\n" + "\n".join(sumary_text))
        # Trả về thông tin về tệp đã tải lên
        json_output["confident_score"] = np.mean(confident_scores)
        json_output["table_content"] = convert_to_serializable(table_raw_data)

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
async def hos_110(data: Annotated[ArrayImageUploadDTO, Form()]):
    try:
        upload_dir = "uploaded_files/invoive/v2/hos_108"
        os.makedirs(upload_dir, exist_ok=True)
        files = data.files
        array_img = []

        # Xử lý mỗi tệp trong danh sách
        for idx, file in enumerate(files):
            # Tạo tên mới cho tệp để tránh trùng lặp (có thể sử dụng các phương pháp khác)
            outPath = os.path.join(upload_dir, f"image_{int(time.time())}_{file.filename}")
            
            # Đọc nội dung tệp và lưu vào đĩa
            content = await file.read()
            with open(outPath, "wb") as f:
                f.write(content)
            
            # Thêm đường dẫn của tệp vào danh sách
            array_img.append(outPath)

        header_text, sumary_text, table_raw_data = dlUnit.predict(array_img)
        json_output = unit_ocr.inferenceHos110WithOutParse("\n".join(header_text) + "\n" + "\n".join(sumary_text))
        # Trả về thông tin về tệp đã tải lên
        json_output["table_content"] = convert_to_serializable(table_raw_data)

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
    
@router.post("/hos_108", status_code=status.HTTP_200_OK)
async def hos_108(data: Annotated[ArrayImageUploadDTO, Form()]):
    try:
        upload_dir = "uploaded_files/invoive/v2/hos_108"
        os.makedirs(upload_dir, exist_ok=True)
        files = data.files
        array_img = []

        # Xử lý mỗi tệp trong danh sách
        for idx, file in enumerate(files):
            # Tạo tên mới cho tệp để tránh trùng lặp (có thể sử dụng các phương pháp khác)
            outPath = os.path.join(upload_dir, f"image_{int(time.time())}_{file.filename}")
            
            # Đọc nội dung tệp và lưu vào đĩa
            content = await file.read()
            with open(outPath, "wb") as f:
                f.write(content)
            
            # Thêm đường dẫn của tệp vào danh sách
            array_img.append(outPath)

        header_text, sumary_text, table_raw_data = dlUnit.predict(array_img)
        json_output = unit_ocr.inferenceHos108WithOutParse("\n".join(header_text) + "\n" + "\n".join(sumary_text))
        # Trả về thông tin về tệp đã tải lên
        json_output["table_content"] = convert_to_serializable(table_raw_data)

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
    
    