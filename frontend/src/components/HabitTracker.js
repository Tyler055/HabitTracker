const React = require("react");
const { useState, useEffect } = React;

const HabitTracker = () => {
  const [habits, setHabits] = useState([]);
  const [habitInput, setHabitInput] = useState("");
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  // Load habits from backend on component mount
  useEffect(() => {
    async function fetchHabits() {
      try {
        const response = await fetch("/api/habits");
        if (!response.ok) throw new Error("Failed to fetch habits.");
        const data = await response.json();
        setHabits(data);
      } catch (error) {
        console.error("Error loading habits:", error);
      }
    }
    fetchHabits();
  }, []);

  // Handle adding a new habit
  const addHabit = async () => {
    if (!habitInput.trim()) return;

    try {
      const response = await fetch("/api/add-habit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: habitInput }),
      });

      if (response.ok) {
        const newHabit = await response.json();
        setHabits([...habits, newHabit]); // Update UI
        setHabitInput(""); // Clear input field
      } else {
        alert("Failed to add habit.");
      }
    } catch (error) {
      console.error("Error adding habit:", error);
    }
  };

  // Handle deleting a habit
  const deleteHabit = async (habitId) => {
    try {
      const response = await fetch(`/api/delete-habit/${habitId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setHabits(habits.filter((habit) => habit.id !== habitId)); // Update UI
      } else {
        alert("Failed to delete habit.");
      }
    } catch (error) {
      console.error("Error deleting habit:", error);
    }
  };

  // Theme toggle
  useEffect(() => {
    document.documentElement.classList.toggle("dark-theme", theme === "dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <div className="container">
      <h2>Habit Tracker</h2>

      <div>
        <input
          type="text"
          className="input-box"
          placeholder="Enter a new habit..."
          value={habitInput}
          onChange={(e) => setHabitInput(e.target.value)}
        />
        <button onClick={addHabit}>Add Habit</button>
      </div>

      <ul>
        {habits.map((habit) => (
          <li key={habit.id} className="habit-item">
            <span>{habit.name}</span>
            <button
              className="delete-btn"
              onClick={() => deleteHabit(habit.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
        {theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>
    </div>
  );
};

module.exports = HabitTracker;
