from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scipy.spatial.transform import Rotation as R
import websocket
import json
import uvicorn
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass

app = FastAPI(lifespan=lifespan)

# IP address
IP = "192.168.0.250"

# HTTP
DIRECT_URL = f"http://{IP}:8090"

# WEBSOCKET
DIRECT_URL = f"ws://{IP}:8090"

angle = [0,0,90]

def degrees_to_quartenions(angle):
    rotation_obj = R.from_euler('xyz', angle, degrees=True)
    quartenion = rotation_obj.as_quat()
    print(quartenion)


if __name__ == "__main__":
    # uvicorn.run("websocket:app", host="0.0.0.0", reload=True)
    degrees_to_quartenions(angle)
