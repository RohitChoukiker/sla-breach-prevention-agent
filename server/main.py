from fastapi import FastAPI

from router import user_router
import uvicorn
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the SLA Breach Prevention Agent API!"}


@app.get("/health")
async def health_check():
    
    return {"status": "ok", "detail": "System is healthy"}



app.include_router(user_router.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)