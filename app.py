from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import defaultdict

from motor import motor_asyncio
from config import BaseConfig

from routers.cars import router as cars_router
#from routers.users import router as users_router

settings = BaseConfig()

async def lifespan(app: FastAPI):
    print("Starting up!")
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]

    try:
        app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")

        print("MongoDB address:", settings.DB_URL)
    except Exception as exc:
        print(exc)

    yield

    print("Shutting down!")
    app.client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(cars_router, prefix="/cars", tags=["cars"])

@app.get("/")
async def get_root():
    return {"message": "Root working!"}