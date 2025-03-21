import { useEffect, useState } from "react";
import api from "../api";
import HabitItem from "./HabitItem";

export default function HabitList() {
  const [habits, setHabits] = useState([]);

  const fetchHabits = async () => {
    const res = await api.get("/habits");
    setHabits(res.data);
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  const handleDelete = async (id) => {
    await api.delete(`/habits/${id}`);
    fetchHabits();
  };

  return (
    <div>
      {habits.map((habit) => (
        <HabitItem key={habit.id} habit={habit} onDelete={handleDelete} />
      ))}
    </div>
  );
}
