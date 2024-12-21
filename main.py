from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel
from database import engine
from sqlmodel import SQLModel, Session, select
from models import Blog, User
from passlib.context import CryptContext

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ShowUser(BaseModel):
    user_name:str
    email:str

class UserLogin(BaseModel):
    user_name:str
    password:str

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def home():
    return {"ho":"me"}

@app.post('/blog')
def create_blog(blog: Blog, session: SessionDep):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@app.get('/blog')
def read_blog(session: SessionDep):
    blogs = session.exec(select(Blog).offset(0).limit(100)).all()
    return blogs

@app.post('/sign-in')
def create_user(request:User, session:SessionDep):
    new_user = User(user_name=request.user_name, email=request.email, password=pwd_context.hash(request.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post('/login')
def login(request:UserLogin, session:SessionDep):
    statement = select(User).where(User.user_name == request.user_name)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found!")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password!")
    return user #For now check only User 3 and pass 3

@app.post('/user/{id}', response_model=ShowUser)
def get_user(id:int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return user