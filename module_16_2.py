from fastapi import FastAPI, Path
from typing import Annotated

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Определение базового маршрута
@app.get("/")
async def root() -> dict:
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin() -> dict:
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def get_user(
        user_id: int = Path(gt=0,
                            le=100,
                            discription="Enter User ID",
                            example="1")) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}


@app.get("/user/{username}/{age}")
async def info_user(
    username: Annotated[str, Path(min_length=5,
                                  max_length=20,
                                  discription="Enter username",
                                  example="UrbanUser")],
    age: Annotated[int, Path(gt=18,
                             le=120,
                             discription="Enter age",
                             example="24")]) -> dict:
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}

# Запуск сервера uvicorn module_16_2:app --reload