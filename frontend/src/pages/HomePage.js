import React from "react";
import HabitForm from "../components/HabitForm";
import HabitList from "../components/HabitList";


export default function HomePage() {
  const [habitUpdated, setHabitUpdated] = useState(false);

  const handleHabitAdded = () => {
    setHabitUpdated((prev) => !prev); // Toggle the state to trigger re-render
  };

  return (
    <div>
      <h1>Habit Tracker</h1>
      <HabitForm onHabitAdded={handleHabitAdded} />
      <HabitList habitUpdated={habitUpdated} />
    </div>
  );
}
