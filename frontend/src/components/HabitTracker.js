import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

const HabitTracker = () => {
  const [habit, setHabit] = useState("");
  const [habits, setHabits] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Reusable function to fetch habits
  const fetchHabits = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5000/habits", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Include the token in the headers
        },
      });
      setHabits(response.data.habits || []);
    } catch (error) {
      setMessage("Failed to fetch habits.");
      console.error("Error fetching habits:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // On mount
  useEffect(() => {
    fetchHabits();
  }, [fetchHabits]);

  // Show temporary message
  const showMessage = (msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(""), 3000);
  };

  // Add a habit
  const handleAddHabit = async (e) => {
    e.preventDefault();
    if (!habit.trim()) return;

    setIsLoading(true);
    const newHabit = { name: habit };

    try {
      // Optimistically add habit to the list
      setHabits((prev) => [
        ...prev,
        { id: Date.now(), name: habit },
      ]);
      
      const response = await axios.post(
        "http://127.0.0.1:5000/habits",
        newHabit,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      // After successfully adding the habit, update the list with the response ID
      setHabits((prev) =>
        prev.map((h) =>
          h.id === Date.now() ? { ...h, id: response.data.id } : h
        )
      );
      setHabit("");
      showMessage("Habit added successfully!");
    } catch (error) {
      setMessage("Failed to add habit.");
      console.error("Error adding habit:", error);
      setHabits((prev) => prev.filter((h) => h.name !== habit)); // Revert optimistically added habit
    } finally {
      setIsLoading(false);
    }
  };

  // Delete a habit
  const handleDeleteHabit = async (id) => {
    if (!window.confirm("Delete this habit?")) return;

    setIsLoading(true);
    const originalHabits = [...habits];
    setHabits((prev) => prev.filter((habit) => habit.id !== id));

    try {
      await axios.delete(`http://127.0.0.1:5000/habits/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Include the token in the headers
        },
      });
      showMessage("Habit deleted.");
    } catch (error) {
      showMessage("Failed to delete habit.");
      setHabits(originalHabits); // rollback
      console.error("Error deleting habit:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Reset all habits
  const handleResetHabits = async () => {
    if (!window.confirm("Reset all habits?")) return;

    setIsLoading(true);
    setHabits([]);
    try {
      await axios.post("http://127.0.0.1:5000/reset_habits", {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Include the token in the headers
        },
      });
      showMessage("All habits reset.");
    } catch (error) {
      showMessage("Failed to reset habits.");
      fetchHabits(); // reload habits
      console.error("Error resetting habits:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="habit-container">
      <h1>Habit Tracker</h1>

      <form onSubmit={handleAddHabit} className="habit-form">
        <input
          type="text"
          className="input-box"
          placeholder="Add new habit"
          value={habit}
          onChange={(e) => setHabit(e.target.value)}
        />
        <button type="submit" className="add-btn" disabled={isLoading}>
          {isLoading ? "Adding..." : "Add Habit"}
        </button>
      </form>

      {message && <p className="message">{message}</p>}

      <h2>Habit List</h2>

      {isLoading ? (
        <div className="spinner">Loading...</div>
      ) : (
        <ul className="habit-list">
          {habits.length ? (
            habits.map((habit) => (
              <li key={habit.id} className="habit-item">
                {habit.name}
                <button
                  className="delete-btn"
                  onClick={() => handleDeleteHabit(habit.id)}
                >
                  Delete
                </button>
              </li>
            ))
          ) : (
            <li>No habits found.</li>
          )}
        </ul>
      )}

      <button
        onClick={handleResetHabits}
        className="reset-btn"
        disabled={isLoading}
      >
        {isLoading ? "Resetting..." : "Reset All Habits"}
      </button>
    </div>
  );
};

export default HabitTracker;
