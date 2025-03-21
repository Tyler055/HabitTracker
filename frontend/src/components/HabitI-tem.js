export default function HabitItem({ habit, onDelete }) {
    return (
      <div>
        <h3>{habit.name}</h3>
        <p>{habit.description}</p>
        <button onClick={() => onDelete(habit.id)}>Delete</button>
      </div>
    );
  }
  