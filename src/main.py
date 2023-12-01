from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.create_all import create_all_tables
from app.database.database import engine
from config import settings
from app.routes import user, auth, profile
create_all_tables()
# print(settings)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

@app.get("/")
async def root():
    return {"message": "HelloWorld"}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(profile.router)
