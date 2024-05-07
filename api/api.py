from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from config import API_HOST, API_PORT

from .oauth import discord_oauth_router
from .routers import (
    stock_router,
    trade_router,
)

app = FastAPI(
    title="Colten Pancake Bot API",
    version="1.0.0"
)


origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(discord_oauth_router.router)

app.include_router(stock_router)
app.include_router(trade_router)


@app.get("/version", tags=["Info"])
def get_app_version() -> str:
    return app.version


async def run():
    config = Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
    )
    server = Server(config=config)

    await server.serve()
