from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from dto.coreResponseDto import CoreResponseDto

from utils.loggerUtils import Logger

router = APIRouter(
    prefix="/",
    tags=[""]
)

@router.post("/example"
            , status_code=status.HTTP_201_CREATED
            # , response_model=dto.GetUser
            )
async def example(user: dto.CreateUser):
    try:
        return CoreResponseDto()
    except Exception as e:
        # Code to handle any other exceptions
        Logger.ERROR(f"An unexpected error occurred: {e}")
    
        
        