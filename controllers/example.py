from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from controllers import CoreResponseDto

router = APIRouter(
    prefix="/",
    tags=[""]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dto.GetUser)
async def example(user: dto.CreateUser):
    try:
        return CoreResponseDto()
    except Exception as e:
        # Code to handle any other exceptions
        print(f"An unexpected error occurred: {e}")
    
        
        