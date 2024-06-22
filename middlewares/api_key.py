from fastapi import Header, HTTPException
from config.global_config import global_config


async def validate_api_key(x_api_gateway: str = Header(...)):
    if x_api_gateway is None or global_config["api_key"] != x_api_gateway:
        raise HTTPException(detail={"data": {}, "message": "Unknown Client", "requirement": "", "status_code": 401}, status_code=401)
