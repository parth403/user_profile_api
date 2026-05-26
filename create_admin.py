from schemas import UserCreate
from auth import password_hash
from database import SessionLocal
from models import User 

class AdminUserCreate(UserCreate):
    is_admin : bool = True

username:str = input("Enter username(only letters , . and _): ")
password:str = input("Enter password(minimum 8 characters): ")
email:str = input("Enter email: ")

admin_data = AdminUserCreate(
    username=username,
    password=password_hash.hash(password),
    email=email,
)

async def create_admin():
    async with SessionLocal() as session:
        admin = User(**admin_data.model_dump())
        session.add(admin)
        await session.commit()
        print("Admin user created successfully")

if __name__ == "__main__":
    import asyncio 
    asyncio.run(create_admin())
