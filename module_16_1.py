from fastapi import FastAPI

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
async def get_user(user_id) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}


@app.get("/user")
async def info_user(username: str, age: int) -> dict:
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}