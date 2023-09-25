import { gql } from '@apollo/client';

export const GET_TODOS_BY_USER = gql`
  query gettingTodoByUser($userId: Int!) {
    getTodosByUser(userId: $userId) {
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
