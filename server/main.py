from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from module.auth.router import auth_router
from module.admin.router import admin_router
from module.ticket.router import ticket_router
from module.agent.router import agent_router
from module.metrics.router import metrics_router

from exceptions import AppException
from seed import seed_admin
from database import SessionLocal

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_admin(db)
    db.close()


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
app.include_router(admin_router)
app.include_router(ticket_router)
app.include_router(agent_router)
app.include_router(metrics_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)