from fastapi import FastAPI
from dbase.base import Base
from dbase.datebase import engine
from core.config import settings
from routes import route_user, route_bots, route_message

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    server = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    server.include_router(route_user.router)
    server.include_router(route_bots.router)
    server.include_router(route_message.route)
    create_tables()
    return server


app = start_application()

@app.get("/")
async def root():
    return {"message": "Hi"}
