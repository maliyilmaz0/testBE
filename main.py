import os
import sys
import uvicorn
import asyncio

if sys.path.__contains__(os.getcwd()):
    sys.path.append(os.getcwd())
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from dependencies import initialize_dependencies

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


async def start_up():
    await initialize_dependencies(app)


async def build_uvicorn_app():
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)


app.add_event_handler('startup', start_up)
if __name__ == "__main__":
    asyncio.run(build_uvicorn_app())
