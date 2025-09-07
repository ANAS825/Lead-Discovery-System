from fastapi import  Depends, HTTPException, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
import models
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel

router = APIRouter(
    prefix="/user",
    tags=["User"]
)
 

secret_key = "dpij]wpe4866837fewnfdlkwndlsdhfbdkwfd4354f6es4fw"
algorithm = "HS256"
expire_session = 1

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl = "User/login")
db_dependency = Annotated[Session, Depends(get_db)] 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"user_id": user_id, "username": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid authentication credentials",
                             headers={"WWW-Authenticate": "Bearer"})



class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Get all users
@router.get('/all')
async def get_all_users(db: db_dependency):
    result = db.query(models.Users).all()
    return result


# check protected route
@router.get("/protected",  response_class=JSONResponse)
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, welcome to the dashboard!"}



# Create a new user
@router.post('/create', status_code=201)
async def create_user(user:UserCreate, db:db_dependency):
    new_user = models.Users(
        username=user.username,
        email=user.email,
        hashed_password=bycrypt_context.hash(user.password)
    )
    existing_user = db.query(models.Users).filter((models.Users.username == user.username) | (models.Users.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# user login 
@router.post('/login')
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(models.Users).filter(models.Users.username == form_data.username).first()
    if not user or not bycrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token_data = {
        "user_id": user.id,
        "username": user.username
    }
    token = jwt.encode(token_data, secret_key, algorithm=algorithm)
    return {"access_token": token, "token_type": "bearer"}