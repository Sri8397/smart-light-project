from fastapi import FastAPI
from api.control_routes import router as control_router

def create_app():
    app = FastAPI()
    app.include_router(control_router)
    return app
