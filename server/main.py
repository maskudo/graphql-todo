from models import User, Todo, Base
from sqlalchemy.orm import sessionmaker
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from schema import type_defs

from sqlalchemy import create_engine 
DATABASE_URI='postgresql://postgres:test1234@localhost:5432/todos'
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session  = sessionmaker(bind=engine)
session = Session()

query = QueryType()

@query.field("todos")
def resolve_todos(*_):
    todos = session.query(Todo)
    return todos


schema = make_executable_schema(type_defs, query)
app = Starlette(debug=True)
app.mount("/graphql/", GraphQL(schema, debug=True))

#
#
# user = User('John Doe', 'johndoe@gmail.com', 'Johndoe@123')
# session.add(user)
# session.flush()
# todo = Todo('Do not work', user.id, False)
# session.add(todo)
#
# session.commit()
