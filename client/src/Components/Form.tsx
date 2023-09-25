import { gql, useMutation } from '@apollo/client';
import { FormEvent, useState } from 'react';
import { ADD_TODO } from '../Mutations';
export default function Form() {
  const [text, setText] = useState('');
  const [isDone, setIsDone] = useState(false);
  const [addTodo, { loading }] = useMutation(ADD_TODO, {
    // refetchQueries: [GET_TODOS_BY_USER, 'getTodosByUser'],
    update(cache, { data: { addTodo } }) {
      cache.modify({
        fields: {
          getTodosByUser(existingTodos = []) {
            const newTodoRef = cache.writeFragment({
              data: addTodo,
              fragment: gql`
                fragment NewTodo on Todo {
                  id
                  text
                  created_by {
                    id
                    name
                  }
                  is_done
                }
              `,
            });
            return [...existingTodos, newTodoRef];
          },
        },
      });
    },
  });
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await addTodo({
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
