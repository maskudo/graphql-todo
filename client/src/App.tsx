import { useQuery, gql } from '@apollo/client';
import Form from './Components/Form';
import Todo from './Components/Todo';
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

function App() {
  const { loading, error, data } = useQuery(GET_TODOS_BY_USER, {
    variables: {
      userId: 5,
    },
  });

  if (loading) return <div> Loading... </div>;
  if (error) return <div> Error...{error.message} </div>;
  console.log({ todos: data?.getTodosByUser });
  return (
    <>
      <Form />
      {data?.getTodosByUser?.map((todo) => (
        <Todo todo={todo} />
      ))}
    </>
  );
}

export default App;
