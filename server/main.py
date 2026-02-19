from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from module.auth.router import auth_router
from exceptions import AppException


app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
@app.get("/")
async def read_root():
    return {"message": "Welcome to the SLA Breach Prevention Agent API!"}


@app.get("/health")
async def health_check():
    
    return {"status": "ok", "detail": "System is healthy"}



app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)