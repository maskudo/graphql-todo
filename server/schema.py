from ariadne import gql 

type_defs = gql("""
    type User {
        id: Int!
        name: String!
        email: String!
        password: String!
        created_at: Datetime!
        todos: [Todo]
    }

    type Todo {
        id: Int!
        text: String!
        is_done: Boolean!
        created_at: Datetime!
        created_by: User!
    }

    input AddUserInput {
        name: String!
        email: String!
        password: String!
    }
    input AddTodoInput {
        text: String!
        created_by: Int!
        is_done: Boolean!
    }
    
    type Mutation {
        addUser(user: AddUserInput!): User!
        deleteUser(userId: Int!): Boolean
        addTodo(todo: AddTodoInput!): Todo!
        deleteTodo(todoId: Int!): Boolean
    }

    type Query {
        todos: [Todo]
        users: [User]
        todo(todoId: Int!): Todo
        user(userId: Int!): User
    }

    scalar Datetime
""")
