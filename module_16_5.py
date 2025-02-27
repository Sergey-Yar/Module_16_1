from fastapi import FastAPI, Path, HTTPException, Request, Body
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Создаем экземпляр приложения FastAPI
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

# Настраиваем папку с шаблонами
templates = Jinja2Templates(directory='templates')

# Создаем пустой список
users = []

#Создаем класс пользователя
class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(
        request: Request,
        user_id: int = Path(gt=0,
                            le=100,
                            description="Enter User ID",
                            example="1")) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
        else:
            raise HTTPException(status_code=404, detail='User was not found')



@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=5,
                                      max_length=20,
                                      description="Enter username",
                                      example="Vasya")],
        age: Annotated[int, Path(ge=18,
                                 le=120,
                                 description="Enter age",
                                 example="24")]) -> User:
    user_id = max(user.id for user in users) + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user



@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(gt=0,
                                le=100,
                                description="Enter User ID",
                                example="1")],
        username: Annotated[str, Path(min_length=5,
                                  max_length=20,
                                  description="Enter username",
                                  example="Vasya")],
        age: Annotated[int, Path(ge=18,
                                le=120,
                                description="Enter age",
                                example="24")]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: int = Path(gt=0,
                            le=100,
                            description="Enter User ID",
                            example="1")) -> str:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {'message': f'The user {user_id} is delete'}
    raise HTTPException(status_code=404, detail='User was not found')

# Запуск сервера uvicorn module_16_5:app --reload