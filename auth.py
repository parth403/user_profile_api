from config import settings
from jose import jwt
from datetime import timezone,datetime,timedelta
from sqlalchemy import select
from models import User
from fastapi import HTTPException,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from database import get_session

password_hash=PasswordHash((Argon2Hasher(),BcryptHasher()))

async def authenticate_user(username:str,password:str,db:AsyncSession=Depends(get_session)):
    q=select(User).where(User.username==username)
    user=await db.scalar(q)
    if user and password_hash.verify(password,user.password):
        return user
    return None

async def create_access_token(data:dict,expires_delta:timedelta | None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc) + expires_delta
    else:
        expire=datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,key=settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_active_user(token:str,db=AsyncSession):
    try:
        payload=jwt.decode(token,key=settings.SECRET_KEY,algorithms=settings.ALGORITHM)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid authentication token')
    user_id=payload.get('sub')
    user=await db.get(User,int(user_id))
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Inactive user')
    return user
        
def check_admin(token):
    try:
        payload=jwt.decode(token,key=settings.SECRET_KEY,algorithms=settings.ALGORITHM)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='user is not admin')
    is_admin=payload.get('is_admin')
    return is_admin=='True'