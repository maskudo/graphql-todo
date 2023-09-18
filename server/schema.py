from ariadne import gql 

type_defs = gql("""
    type User {
        id: Int!
        name: String!
        email: String!
        password: String!
        created_at: String!
    }

    type Todo {
        id: Int!
        text: String!
        created_by: Int!
        is_done: Boolean!
        created_at: String;
    }

    input AddUserInput {
        name: String!
        email: String!
        password: String!
    }
    input DeleteUserInput {
        id: Int!
    }
    input AddTodoInput {
        text: String!
        created_by: Int!
        is_done: Boolean!
    }
    input DeleteTodoInput {
        id: Int!
    }
    
    type Mutation {
        addUser(user: AddUserInput): User!
        deleteUser(user: AddUserInput): User!
        addTodo(todo: AddTodoInput): Todo!
        deleteTodo(todo: AddUserInput): Todo!
    }

    type Query {
        todos: [Todo]
        users: [User]
        todo(todoId: Int!): Todo
        user(userId: Int!): User
    }
    
""")
