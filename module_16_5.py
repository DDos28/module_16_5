from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import logging
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int):
    try:
        user = next((user for user in users if user.id == user_id), None)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except Exception as e:
        logging.exception(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post('/user/{username}/{age}')
async def create_user(username: str, age: int):
    next_user_id = max(user.id for user in users) + 1 if users else 1
    new_user = User(id=next_user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
