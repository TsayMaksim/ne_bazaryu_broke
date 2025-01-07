from database import get_db
from database.models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "searchingforhotmilfsinmyarea"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user_db(email, password):
    db = next(get_db())
    user = db.query(User).filter_by(email=email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_user_db(name, email, password,  telegram_id):
    db = next(get_db())
    hashed_password = pwd_context.hash(password)
    new_user = User(name=name, email=email, hashed_password=hashed_password, telegram_id=telegram_id)
    db.add(new_user)
    db.commit()
    return True

def get_all_users_db():
    db = next(get_db())
    all_users = db.query(User).all()
    return all_users

def get_exact_user_db(user_id):
    db = next(get_db())
    exact_user = db.query(User).filter_by(id=user_id).first()
    return exact_user

def get_user_by_email_db(email):
    db = next(get_db())
    exact_user = db.query(User).filter_by(email=email).first()
    return exact_user

def change_user_db(user_id, change_info, new_info):
    db = next(get_db())
    update_user = db.query(User).filter_by(id=user_id).first()
    if update_user:
        if hasattr(update_user, change_info):
            setattr(update_user, change_info, new_info)
            db.commit()
            return True
    return False

def delete_user_db(user_id):
    db = next(get_db())
    delete_user = db.query(User).filter_by(id=user_id).first()
    if delete_user:
        db.delete(delete_user)
        db.commit()
        return True
    return False
