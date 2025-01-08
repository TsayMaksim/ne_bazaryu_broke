from database.user_service import *
from api import result_message
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

user_router = APIRouter(prefix='/user', tags=['Пользователи'])

class AuthModel(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@user_router.post("/login", response_model=TokenResponse)
async def login_user(auth_data: AuthModel):
    user = authenticate_user_db(email=auth_data.email, password=auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/me")
async def get_current_user(token: str = Depends(verify_token)):
    return {"email": token}

@user_router.post('/create_user')
async def create_user(name: str, email: str, password: str, telegram_id: int):
    result = create_user_db(name=name, email=email, password=password, telegram_id=telegram_id)
    return result_message(result)

@user_router.get('/get_all_users')
async def get_all_users():
    result = get_all_users_db()
    return result_message(result)

@user_router.get('/get_exact_user')
async def get_exact_user(user_id: int):
    result = get_exact_user_db(user_id=user_id)
    return result_message(result)

@user_router.get('/get_user_by_email')
async def get_user_by_email(email: str):
    result = get_user_by_email_db(email=email)
    return result_message(result)

@user_router.post('/authenticate_user')
async def authenticate_user(email: str, password: str):
    result = authenticate_user_db(email=email, password=password)
    return result_message(result)

@user_router.put('/change_user')
async def change_user(user_id: int, change_info: str, new_info: str):
    result = change_user_db(user_id=user_id, change_info=change_info, new_info=new_info)
    return result_message(result)

@user_router.delete('/delete_user')
async def delete_user(user_id: int):
    result = delete_user_db(user_id=user_id)
    return result_message(result)
