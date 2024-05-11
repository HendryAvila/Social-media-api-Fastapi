
from sql_app import models
from sql_app.database import engine, get_db
from fastapi import FastAPI
from app.routers import Posts, Users, auth, votes
#source venv/scripts/activate
#uvicorn app.main:app --reload
#http://127.0.0.1:8000

app = FastAPI()
app.include_router(Posts.router)
app.include_router(Users.router)
app.include_router(auth.router)
app.include_router(votes.router)

#this create the database
models.Base.metadata.create_all(engine)
get_db()

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

