from fastapi import FastAPI
from motor import motor_asyncio
from config import BaseConfig

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

@app.get("/")
async def get_root():
    return {"message": "Root working!"}