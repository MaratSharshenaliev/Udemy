import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from endpoints import _auth, _mentor, _users
from db.base import database, metadata, engine

app = FastAPI(title="Employment exchange")

app.include_router(_auth.router, prefix="/api", tags=["Authorization"])
app.include_router(_mentor.router, prefix="/api/mentor-service", tags=["Mentor-Service"])
app.include_router(_users.router, prefix="/app/user-service", tags=["User-Service"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    metadata.create_all(bind=engine)
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True, use_colors=True)
