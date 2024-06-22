from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def generate_response(obj, message, requirement, status_code):
    response_content = {
        "data": jsonable_encoder(obj),
        "message": message,
        "requirement": requirement,
        "status_code": status_code
    }
    response = JSONResponse(content=response_content, status_code=status_code)
    return response
