import React, { useEffect, useState } from "react";
import axios from "axios";

const HabitList = () => {
  const [habits, setHabits] = useState([]);

  useEffect(() => {
    axios
      .get("/api/habits")
      .then((response) => {
        setHabits(response.data);
      })
      .catch((error) => {
        console.error("Error fetching habits:", error);
      });
  }, []);

  return (
    <ul>
      {habits.map((habit, index) => (
        <li key={index}>{habit}</li>
      ))}
    </ul>
  );
};

export default HabitList;
