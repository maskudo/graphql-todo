from models import User, Todo, Base
from sqlalchemy.orm import sessionmaker
from ariadne import ObjectType, QueryType, make_executable_schema
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
mutate = ObjectType("Mutation")

@query.field("users")
def resolve_users(*_):
    users = session.query(User)
    return users

@query.field("todos")
def resolve_todos(*_):
    todos = session.query(Todo)
    return todos

@mutate.field("addTodo")
def resolve_add_todo(*_, todo):
    todoObj = Todo(todo['text'], todo['created_by'], todo['is_done'])
    session.add(todoObj)
    session.commit()
    return todoObj

@mutate.field("addUser")
def resolve_add_user(*_, user):
    userObj = User(user['name'], user['email'], user['password'])
    session.add(userObj)
    session.commit()
    return userObj

schema = make_executable_schema(type_defs, query, mutate)
app = Starlette(debug=True)
app.mount("/graphql/", GraphQL(schema, debug=True))

