import { useQuery } from '@apollo/client';
import Form from './Components/Form';
import Todo from './Components/Todo';
import { GET_TODOS_BY_USER } from './Queries';

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
        <Todo key={todo.id} todo={todo} />
      ))}
    </>
  );
}

export default App;
