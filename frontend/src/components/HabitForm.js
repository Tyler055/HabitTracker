import React, { useState } from "react";
import { addHabit, resetHabits } from "../api"; // Use the API module for better structure

const HabitForm = ({ refreshHabits }) => {
  const [habitName, setHabitName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!habitName.trim()) return;

    try {
      await addHabit(habitName); // Send the request to add a habit
      setHabitName(""); // Reset the input field after adding the habit
      refreshHabits(); // Refresh the list of habits after adding
    } catch (error) {
      console.error("Error adding habit:", error);
    }
  };

  const handleReset = async () => {
    if (!window.confirm("Are you sure you want to reset all habits?")) return;

    try {
      await resetHabits(); // Reset all habits
      refreshHabits(); // Refresh the habit list after resetting
    } catch (error) {
      console.error("Error resetting habits:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={habitName}
          onChange={(e) => setHabitName(e.target.value)}
          placeholder="Enter new habit"
          required
        />
        <button type="submit">Add Habit</button>
      </form>
      <button onClick={handleReset}>Reset Habits</button>
    </div>
  );
};

export default HabitForm;
