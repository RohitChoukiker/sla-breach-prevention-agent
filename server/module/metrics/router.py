from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

metrics_router = APIRouter()

@metrics_router.get("/metrics", summary="Prometheus metrics endpoint")
def metrics() -> Response:
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )