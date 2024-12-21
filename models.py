from sqlmodel import Field, Session, SQLModel
from typing import Union

class Blog(SQLModel, table=True):
    __tablename__="blog"
    id: Union[int, None] = Field(primary_key=True, index=True)
    title:str = Field(index=True)
    body:str

class User(SQLModel, table = True):
    __tablename__="user"
    id: Union[int, None] = Field(primary_key=True, index=True)
    user_name:str
    email:str
    password:str
