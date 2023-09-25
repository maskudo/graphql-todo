import { gql } from '@apollo/client';

export const ADD_TODO = gql`
  mutation addingTodo($todo: AddTodoInput!) {
    addTodo(todo: $todo) {
      text
      id
      created_by {
        id
        name
      }
      is_done
    }
  }
`;
export const UPDATE_TODO = gql`
  mutation updateTodo($todo: UpdateTodoInput!) {
    updateTodo(todo: $todo) {
      id
      text
      is_done
      created_by {
        id
        name
      }
    }
  }
`;

export const DELETE_TODO = gql`
  mutation deleteTodo($todoId: Int!) {
    deleteTodo(todoId: $todoId)
  }
`;
