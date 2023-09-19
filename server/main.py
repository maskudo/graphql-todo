from models import User, Todo, Base
from sqlalchemy.orm import sessionmaker
from ariadne import ObjectType, QueryType, ScalarType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from schema import type_defs

from sqlalchemy import create_engine

from utils import hash_password 
DATABASE_URI='postgresql://postgres:test1234@localhost:5432/todos'
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session  = sessionmaker(bind=engine)
session = Session()

query = QueryType()
mutate = ObjectType("Mutation")
user = ObjectType("User")
todo = ObjectType("Todo")
datetime_scalar  = ScalarType('Datetime')

@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()

@query.field("users")
def resolve_users(*_):
    users = session.query(User)
    return users

@query.field("todos")
def resolve_todos(*_):
    todos = session.query(Todo)
    return todos

@query.field("todo")
def resolve_todo(*_, todoId): 
    todo = session.query(Todo).where(Todo.id == todoId).one()
    return todo

@todo.field("created_by")
def resolve_todo_user(root, *_):
    userId = root.created_by
    user = session.query(User).where(User.id == userId).one()
    return user


@query.field("user")
def resolve_user(*_, userId): 
    user = session.query(User).where(User.id == userId).one()
    return user

@mutate.field("addTodo")
def resolve_add_todo(*_, todo):
    todoObj = Todo(todo['text'], todo['created_by'], todo['is_done'])
    session.add(todoObj)
    session.commit()
    return todoObj

@mutate.field("deleteTodo")
def resolve_delete_todo(*_, todoId):
    try: 
        todo = session.query(Todo).where(Todo.id == todoId).one()
        session.delete(todo)
        session.commit()
        return True
    except: 
        return False

@mutate.field("updateTodo")
def resolve_update_todo(*_, todo):
    current_todo_query = session.query(Todo).where(Todo.id==todo["id"])
    current_todo = current_todo_query.one()
    if(todo.get("is_done") is not None):
        current_todo.is_done = todo.get("is_done")
    current_todo_query.update({
        Todo.text: (todo.get("text") or current_todo.text),
        Todo.is_done:(current_todo.is_done),
    })
    session.flush()
    updated_todo = session.query(Todo).where(Todo.id == todo["id"]).one()
    print(current_todo)
    session.commit()
    return updated_todo

@mutate.field("deleteUser")
def resolve_delete_User(*_, userId):
    try: 
        user = session.query(User).where(User.id == userId).one()
        session.delete(user)
        session.commit()
        return True
    except:
        return False

@mutate.field("addUser")
def resolve_add_user(*_, user):
    userObj = User(user['name'], user['email'], user['password'])
    session.add(userObj)
    session.commit()
    return userObj

@mutate.field("updateUser")
def resolve_update_user(*_, user):
    current_user_query = session.query(User).where(User.id==user["id"])
    current_user = current_user_query.one()
    current_user_query.update({
        User.name: (user.get("name") or current_user.name),
        User.password:(hash_password(user.get("password")) or current_user.password),
        User.email:(user.get("email") or current_user.email),
    })
    session.flush()
    updated_user = session.query(User).where(User.id == user["id"]).one()
    session.commit()
    return updated_user


schema = make_executable_schema(type_defs, query, mutate, todo, user, datetime_scalar)
app = Starlette(debug=True)
app.mount("/graphql/", GraphQL(schema, debug=True))

