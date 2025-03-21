import HabitForm from "../components/HabitForm";
import HabitList from "../components/HabitList";

export default function HomePage() {
  return (
    <div>
      <h1>Habit Tracker</h1>
      <HabitForm onHabitAdded={() => window.location.reload()} />
      <HabitList />
    </div>
  );
}
