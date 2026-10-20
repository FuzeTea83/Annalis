from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.exeptions import AppError


def setup_exception_handlers(app: FastAPI):

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        status_code = {
            "INVALID_CREDENTIALS": 401,
            "EMAIL_EXISTS": 409,
            "CONFLICT": 409,
            "INVALID_EMAIL_DOMAIN": 409,
            "INVALID_TOKEN": 401,
            "USER_NOT_FOUND": 404,
            "FILE_NOT_FOUND": 404,
            "INVALID_FILE_TYPE": 415,
            "FILE_TOO_LARGE": 400,
            "DOCUMENT_NOT_FOUND": 404
        }.get(exc.code, 400)

        print(f"Erreur gérée: {exc.message} (code: {exc.code})")

        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.message, "code": exc.code}
        )


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"]
            })

        return JSONResponse(
            status_code=422,
            content={"detail": "Erreur de validation", "errors": errors}
        )


    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):

        print(f"Erreur non gérée: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Erreur interne du serveur"}
        )