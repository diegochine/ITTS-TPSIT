from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str
    pwd: str
    age: int | None = None
    type: str | None = None


app = FastAPI()


@app.post("/add_user/")
async def add_user(user: User):
    if user.age >= 18:
        user.type = 'adult'
    else:
        user.type = 'underage'
    return user

