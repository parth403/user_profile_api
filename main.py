from fastapi import FastAPI,Depends,HTTPException,status
from schemas import UserCreateResponse,UserCreate,LoginResponse,Token
from database import get_session
from auth import password_hash
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from auth import authenticate_user,create_access_token
from sqlalchemy import select
from datetime import timedelta
from config import settings

app=FastAPI()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')


@app.post('/user-create',response_model=UserCreateResponse)
async def create_user(userCreate:UserCreate,db:AsyncSession=Depends(get_session)):
    raw_password=userCreate.password
    hashed_password=password_hash.hash(raw_password)
    userCreate.password=hashed_password

    user=User(**userCreate.model_dump())
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise e
    return user

@app.get('/all-users',response_model=list[UserCreateResponse])
async def get_all_users(db:AsyncSession=Depends(get_session)):
    q=select(User)
    user=await db.scalars(q)
    return user.all()


@app.post('/token')
async def login(req:LoginResponse,db:AsyncSession=Depends(get_session)):
    user=await authenticate_user(req.username,req.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect username or password')
    access_token_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=await create_access_token(data={"sub":str(user.id),"is_admin":str(user.is_admin)},expires_delta=access_token_expires)
    return Token(token=access_token)