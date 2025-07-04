import uvicorn
from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container

app = FastAPI()
app.include_router(router=user_routers)
app.include_router(router=note_routers)
app.container = Container()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
