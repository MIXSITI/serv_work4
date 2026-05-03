# №10.1

from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas import ErrorResponse


class CustomExceptionA(Exception):

    def __init__(self, detail: str = "Condition not met"):
        self.detail = detail
        self.status_code = 400


class CustomExceptionB(Exception):

    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
        self.status_code = 404


async def handle_custom_exception_a(request: Request, exc: CustomExceptionA):
    body = ErrorResponse(
        error_code=exc.status_code,
        message="Custom Error A",
        detail=exc.detail,
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def handle_custom_exception_b(request: Request, exc: CustomExceptionB):
    body = ErrorResponse(
        error_code=exc.status_code,
        message="Custom Error B",
        detail=exc.detail,
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())
