import React, { useState } from "react";

const HabitTracker = () => {
  const [habits, setHabits] = useState([]);
  const [theme, setTheme] = useState("light-theme");

  const handleDelete = (habitId) => {
    if (window.confirm("Are you sure you want to delete this habit?")) {
      setHabits(habits.filter((habit) => habit.id !== habitId));
    }
  };

  const handleThemeToggle = () => {
    setTheme((prevTheme) => {
      const newTheme =
        prevTheme === "light-theme" ? "dark-theme" : "light-theme";
      return newTheme;
    });
  };

  const handleReset = () => {
    if (window.confirm("Are you sure you want to reset all habits?")) {
      setHabits([]); // Clear all habits
    }
  };

  const handleAddHabit = (e) => {
    e.preventDefault();
    const habitName = e.target.elements["habit-name"].value;
    if (habitName) {
      const newHabit = { id: Date.now(), name: habitName };
      setHabits([...habits, newHabit]);
      e.target.reset();
    }
  };

  return (
    <div className={`container ${theme}`}>
      <button id="theme-toggle" onClick={handleThemeToggle}>
        Switch to {theme === "light-theme" ? "Dark" : "Light"} Mode
      </button>
      <button id="reset-button" onClick={handleReset} type="button">
        Reset Habits
      </button>

      <h1>Habit Tracker</h1>

      <h2>Habit List</h2>
      {habits.length > 0 ? (
        <ul>
          {habits.map((habit) => (
            <li key={habit.id} className="habit-item">
              {habit.name}{" "}
              <a
                href="#"
                className="delete-btn"
                onClick={() => handleDelete(habit.id)}
              >
                Delete
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No habits found. Start by adding a new one!</p>
      )}

      <h2>Add a New Habit</h2>
      <form id="habit-form" onSubmit={handleAddHabit}>
        <input
          type="text"
          id="habit-name"
          name="habit_name"
          className="input-box"
          placeholder="Habit Name"
          required
        />
        <button type="submit" id="add-habit-btn" className="add-btn">
          Add Habit
        </button>
      </form>
    </div>
  );
};

export default HabitTracker;
