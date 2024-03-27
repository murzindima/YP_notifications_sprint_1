import logging

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import ValidationError

from src.api.v1 import notifications
from src.core import config
from src.core.logger import LOGGING


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: "notifications-api"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.jaeger_settings.host,
                agent_port=config.jaeger_settings.port,
            )
        )
    )


configure_tracer()


app = FastAPI(
    title=config.app_settings.project_name,
    description="Notifications API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "X-Request-Id is required"},
        )
    return response


app.include_router(
    notifications.router, prefix="/api/v1/notifications", tags=["templates"]
)
# app.include_router(films.router, prefix="/api/v1/templates", tags=["templates"], dependencies=[Depends(security_jwt)])


@app.exception_handler(ValidationError)
async def handler_validation_error(request: Request, exc: ValidationError):
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"errors": exc.errors()}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
