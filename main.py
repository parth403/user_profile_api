from fastapi import FastAPI,Depends,HTTPException,status
from schemas import UserCreateResponse,UserCreate,LoginResponse,Token,AdminUserResponse,UserUpdate
from database import get_session
from auth import password_hash,check_admin
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from auth import authenticate_user,create_access_token,get_current_active_user
from sqlalchemy import select
from datetime import timedelta
from config import settings
from typing import Annotated

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

@app.get('/all-users',response_model=list[AdminUserResponse])
async def get_all_users(token:Annotated[str,Depends(oauth2_scheme)],db:AsyncSession=Depends(get_session)):
    # if not check_admin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    q=select(User)
    user=await db.scalars(q)
    return user.all()

# @app.get('/all-users',response_model=list[AdminUserResponse])
# async def get_all_users(db:AsyncSession=Depends(get_session)):
#     # if not check_admin(token):
#     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#     q=select(User)
#     user=await db.scalars(q)
#     return user.all()


@app.post('/token')
async def login(req:LoginResponse,db:AsyncSession=Depends(get_session)):
    user=await authenticate_user(req.username,req.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect username or password')
    access_token_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=await create_access_token(data={"sub":str(user.id),"is_admin":str(user.is_admin)},expires_delta=access_token_expires)
    return Token(token=access_token)

@app.get('/users/me',response_model=UserCreateResponse)
async def get_profile(token:Annotated[str,Depends(oauth2_scheme)],db:AsyncSession=Depends(get_session)):
    user=await get_current_active_user(token=token,db=db)
    return user

@app.patch('/user/update',response_model=UserCreateResponse)
async def update_profile(updateData:UserUpdate,token:Annotated[str,Depends(oauth2_scheme)],db:AsyncSession=Depends(get_session)):
    user=await get_current_active_user(token,db)
    updateDict=updateData.model_dump(exclude_unset=True)
    if user and not updateDict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No data found to update')
    for k,v in updateDict.items():
        setattr(user,k,v)
    await db.commit()
    await db.refresh(user)
    return user

@app.delete('/user/{user_id}')
async def deactive_profile(user_id:int,token:Annotated[str,Depends(oauth2_scheme)],db:AsyncSession=Depends(get_session)):
    if not check_admin(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user = await db.get(User,user_id)
    user.is_active=False
    await db.commit()
    return 