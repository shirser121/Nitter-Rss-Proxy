from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from rss_proxy.core.init import startup_event, shutdown_event
from rss_proxy.api.v1 import rss
from rss_proxy.core.config import SECURITY_CODE
from rss_proxy.utils.logger import logger

app = FastAPI()

app.include_router(rss.router, prefix="/api/v1")
SECURITY_NAME = "Authorization"


@app.on_event("startup")
async def startup():
    await startup_event()


@app.on_event("shutdown")
async def shutdown():
    await shutdown_event()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the proxy server!"}


@app.middleware("http")
async def verify_security_header(request: Request, call_next):
    if SECURITY_CODE:
        header_value = request.headers.get(SECURITY_NAME)
        query_value = request.query_params.get(SECURITY_NAME)

        # If neither header nor query parameter is provided
        if not header_value and not query_value:
            logger.warn(f"Missing security code in both headers and query parameters.")
            return JSONResponse(status_code=400, content={"detail": "Security code is required."})

        # If the provided header or query parameter value doesn't match the expected value
        if ((header_value and header_value != SECURITY_CODE) or
                (query_value and query_value != SECURITY_CODE)):
            logger.warn(f"Invalid security code provided.")
            return JSONResponse(status_code=400, content={"detail": "Invalid security code."})

    response = await call_next(request)
    return response
