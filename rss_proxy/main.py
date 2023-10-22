from fastapi import FastAPI
from rss_proxy.core.init import startup_event, shutdown_event
from rss_proxy.api.v1 import rss

app = FastAPI()

app.include_router(rss.router, prefix="/v1")


@app.on_event("startup")
async def startup():
    await startup_event()


@app.on_event("shutdown")
async def shutdown():
    await shutdown_event()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the proxy server!"}