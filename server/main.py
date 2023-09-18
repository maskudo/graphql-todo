from models import User, Todo, Base
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, create_engine, except_
DATABASE_URI='postgresql://postgres:test1234@localhost:5432/todos'

engine = create_engine(DATABASE_URI)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


Session  = sessionmaker(bind=engine)
session = Session()


user = User('John Doe', 'johndoe@gmail.com', 'Johndoe@123')
session.add(user)
session.flush()
todo = Todo('Do not work', user.id, False)
session.add(todo)

session.commit()
