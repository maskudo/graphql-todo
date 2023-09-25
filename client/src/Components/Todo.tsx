import { gql, useMutation } from '@apollo/client';
import { DELETE_TODO, UPDATE_TODO } from '../graphql/Mutations';
import { ChangeEvent } from 'react';

export default function Todo({
  todo,
}: {
  todo: {
    text: string;
    id: number;
    created_by: {
      id: number;
      name: number;
    };
    is_done: boolean;
  };
}) {
  const [deleteTodo] = useMutation(DELETE_TODO, {
    update(cache) {
      cache.modify({
        fields: {
          getTodosByUser(existingTodos = [], { readField }) {
            return existingTodos.filter(
              (oldTodo) => readField('id', oldTodo) !== todo.id
            );
          },
        },
      });
    },
  });

  const [updateTodo] = useMutation(UPDATE_TODO, {
    update(cache, { data: { updateTodo } }) {
      cache.modify({
        fields: {
          getTodosByUser(existingTodos = [], { readField }) {
            const newTodoRef = cache.writeFragment({
              data: updateTodo,
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

            return existingTodos.map((oldTodo) =>
              readField('id', oldTodo) === todo.id ? newTodoRef : oldTodo
            );
          },
        },
      });
    },
  });

  const handleUpdate = async (e: ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    await updateTodo({
      variables: {
        todo: {
          id: todo.id,
          is_done: e.target.checked,
        },
      },
    });
  };

  const handleDelete = async () => {
    await deleteTodo({
      variables: {
        todoId: todo.id,
      },
    });
  };
  return (
    <div>
      <span className={'text ' + (todo.is_done ? 'line-through' : '')}>
        {todo.text}
      </span>
      <input type="checkbox" checked={todo.is_done} onChange={handleUpdate} />
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
