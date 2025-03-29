import React, { useState, useEffect } from "react";
import "../styles/styles.css"; // Adjust the path to your global styles file

const HabitTracker = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState("");

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "dark";
    setIsDarkMode(savedTheme === "dark");
    document.body.classList.add(`${savedTheme}-theme`);

    // Fetch habits from the backend
    const fetchHabits = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/habits");
        const data = await response.json();
        setHabits(data);
      } catch (error) {
        console.error("Error fetching habits:", error);
      }
    };
    fetchHabits();
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDarkMode ? "dark" : "light";
    setIsDarkMode(!isDarkMode);
    document.body.classList.remove(isDarkMode ? "dark-theme" : "light-theme");
    document.body.classList.add(newTheme + "-theme");
    localStorage.setItem("theme", newTheme);
  };

  const addHabit = async () => {
    if (!newHabit.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/habits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newHabit }),
      });

      if (response.ok) {
        const updatedHabit = await response.json();
        setHabits([...habits, updatedHabit]);
        setNewHabit("");
      }
    } catch (error) {
      console.error("Error adding habit:", error);
    }
  };

  const resetHabits = async () => {
    try {
      const response = await fetch("/reset_habits", { method: "POST" });
      if (!response.ok) throw new Error("Error resetting habits.");
      window.location.reload();
    } catch (error) {
      alert(error.message);
    }
  };

  const deleteHabit = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/habits/${id}`, { method: "DELETE" });
      if (response.ok) {
        setHabits(habits.filter((habit) => habit.id !== id));
      } else {
        alert("Failed to delete habit.");
      }
    } catch (error) {
      console.error("Error deleting habit:", error);
    }
  };

  return (
    <div className="habit-tracker">
      <h1>Habit Tracker</h1>

      <button id="theme-toggle" onClick={toggleTheme}>
        {isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>

      <button id="reset-button" onClick={resetHabits}>
        Reset Habits
      </button>

      <ul>
        {habits.map((habit, index) => (
          <li key={index}>
            {habit.name}
            <button className="delete-btn" onClick={() => deleteHabit(habit.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <input
        type="text"
        className="input-box"
        placeholder="Add new habit"
        value={newHabit}
        onChange={(e) => setNewHabit(e.target.value)}
      />
      <button onClick={addHabit}>Add Habit</button>
    </div>
  );
};

export default HabitTracker;
