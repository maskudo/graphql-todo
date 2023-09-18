from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Boolean, Column, Integer, String, Date, create_engine
DATABASE_URI='postgresql://postgres:test1234@localhost:5432/todos'


Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    text  = Column(String, nullable=False)
    created_by  = Column(String, nullable=False)
    created_at = Column(Date , default=datetime.now)
    is_done  = Column(Boolean, default=False)

    def __init__(self, text,  created_by, is_done) -> None:
        self.is_done = is_done
        self.text = text
        self.created_by = created_by

    def __repr__(self) -> str:
        return f"<Todo(text='{self.text}'), created_by='{self.created_by}', created_at='{self.created_at}', is_done='{self.is_done}'"

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)


Session  = sessionmaker(bind=engine)
session = Session()

todo = Todo('Do not work', 'John Doe', False)

session.add(todo)

session.commit()
