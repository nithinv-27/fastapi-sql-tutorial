from sqlmodel import create_engine 
from models import Blog

engine = create_engine('sqlite:///./blog.db',connect_args= {"check_same_thread":False})

