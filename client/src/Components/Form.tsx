import { useQuery, gql, useMutation } from '@apollo/client';
import { FormEvent, useState } from 'react';
import { GET_TODOS_BY_USER } from '../App';
const ADD_TODO = gql`
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
export default function Form() {
  const [text, setText] = useState('');
  const [isDone, setIsDone] = useState(false);
  const [addTodo, { loading, error, data }] = useMutation(ADD_TODO, {
    refetchQueries: [GET_TODOS_BY_USER, 'getTodosByUser'],
  });
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    addTodo({
      variables: {
        todo: {
          text,
          is_done: isDone,
          created_by: 5,
        },
      },
    });
  };
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="text"
        required
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <input
        type="checkbox"
        name="is_done"
        checked={isDone}
        onChange={(e) => setIsDone(e.target.checked)}
      />
      <input
        type="submit"
        value={loading ? 'Loading...' : 'Add'}
        disabled={loading}
      />
    </form>
  );
}
