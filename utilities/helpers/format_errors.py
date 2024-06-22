from pydantic import ValidationError


def format_errors(validation_error: ValidationError):
    formatted_errors = []
    for error in validation_error.errors():
        formatted_error = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
        }
        formatted_errors.append(formatted_error)
    return formatted_errors
