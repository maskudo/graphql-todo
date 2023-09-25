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
  const handleDelete = () => {
    console.log('deleting');
  };
  return (
    <div>
      {todo.text}
      <input type="checkbox" checked={todo.is_done} onChange={() => {}} />
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
