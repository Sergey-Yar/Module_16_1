from fastapi import FastAPI, Path
from typing import Annotated

# Создаем экземпляр приложения FastAPI
app = FastAPI()


# Создаем словарь
users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_users() -> dict:
    global users
    return users

@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=5,
                                  max_length=20,
                                  description="Enter username",
                                  example="Vasya")],
        age: Annotated[int, Path(ge=18,
                                le=120,
                                description="Enter age",
                                example="24")]) -> str:
    user_id = str(int(max(users,key=int)) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered'

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
                                example="24")]) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'

@app.delete('/user/{user_id}')
async def delete_user(
        user_id: int = Path(gt=0,
                            le=100,
                            description="Enter User ID",
                            example="1")) -> str:
    users.pop(user_id)
    return f'The user {user_id} is delete'

# Запуск сервера uvicorn module_16_3:app --reload