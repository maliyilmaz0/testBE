from pydantic import BaseModel
from fastapi import HTTPException


class BaseResponse(BaseModel):
    data: dict | list
    message: str
    requirement: str
    status_code: int
