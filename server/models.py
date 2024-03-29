from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date 
from sqlalchemy.orm import declarative_base, relationship

from utils import hash_password 
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email= Column(String(255), nullable=False, unique=True)
    name= Column(String(255), nullable=False)
    password= Column(String, nullable=False)
    created_at = Column(Date , default=datetime.now)
    todos = relationship("Todo",back_populates="owner", cascade="delete, merge, save-update")

    def __init__(self, name:str,  email:str, password:str) -> None:
        self.name = name
        self.email = email
        self.password = hash_password(password)

    def __repr__(self) -> str:
        return f"User(name='{self.name}'), created_at='{self.created_at}', email='{self.email}')"


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    text  = Column(String, nullable=False)
    created_by  = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(Date , default=datetime.now)
    is_done  = Column(Boolean, default=False)
    owner = relationship("User", back_populates="todos")

    def __init__(self, text:str,  created_by: Column[int], is_done:bool) -> None:
        self.is_done = is_done
        self.text = text
        self.created_by = created_by

    def __repr__(self) -> str:
        return f"<Todo(text='{self.text}'), created_by='{self.created_by}', created_at='{self.created_at}', is_done='{self.is_done}'"
