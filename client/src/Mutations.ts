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
