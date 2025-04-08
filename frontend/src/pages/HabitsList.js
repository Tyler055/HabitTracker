import { useEffect, useState } from "react";
import axios from "axios";

const HabitList = () => {
  const [habits, setHabits] = useState([]);

  const fetchHabits = async () => {
    const res = await axios.get("http://localhost:5000/habits/", {
      withCredentials: true
    });
    setHabits(res.data.habits);
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  return (
    <div>
      {habits.map(habit => (
        <div key={habit.id}>
          <h3>{habit.name}</h3>
          <p>Frequency: {habit.frequency}</p>
        </div>
      ))}
    </div>
  );
};

export default HabitList;
