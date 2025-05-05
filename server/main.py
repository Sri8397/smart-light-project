from core.mqtt_client import mqtt_client
from api.control_routes import router as control_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.video_transfer import VideoTransfer
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(control_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    mqtt_client.loop_start()
    # Run the app on all network interfaces (0.0.0.0) and port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

