import React, { useState, useEffect } from "react";

const Habits = () => {
  const [habits, setHabits] = useState([]);

  useEffect(() => {
    // Replace this with your logic to fetch the user's habits
    setHabits(["Drink water", "Exercise", "Read a book"]);
  }, []);

  return (
    <div>
      <h2>Your Habits</h2>
      <ul>
        {habits.map((habit, index) => (
          <li key={index}>{habit}</li>
        ))}
      </ul>
    </div>
  );
};

export default Habits;
