from fastapi            import FastAPI, Request, status, Request
from fastapi.encoders   import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses  import JSONResponse


app = FastAPI()

class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    loc = exc.errors()[0]['loc'][0].upper()
    item = exc.errors()[0]['loc'][1].upper()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'data': '', 'message': f'ERROR_{item}_IN_{loc}'})
    )


@app.exception_handler(CustomException)
def NotFoundHandler(request: Request, exc: CustomException):
    return JSONResponse(status_code = 404, content = {'data': '', 'message': exc.message})


