import React, { useState } from "react";
import axios from "axios";

const HabitForm = () => {
  const [habit, setHabit] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("/api/habits", { name: habit })
      .then((response) => {
        alert("Habit added!");
      })
      .catch((error) => {
        console.error("Error adding habit:", error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Add a habit"
        value={habit}
        onChange={(e) => setHabit(e.target.value)}
        required
      />
      <button type="submit">Add Habit</button>
    </form>
  );
};

export default HabitForm;
