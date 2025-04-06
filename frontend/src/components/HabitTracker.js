import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

const HabitTracker = () => {
  const [habit, setHabit] = useState("");
  const [habits, setHabits] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const token = localStorage.getItem("token");

  const fetchHabits = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await axios.get("http://127.0.0.1:5000/habits", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setHabits(res.data.habits || []);
    } catch (err) {
      setMessage("Failed to fetch habits.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchHabits();
  }, [fetchHabits]);

  const showMessage = (msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(""), 3000);
  };

  const handleAddHabit = async (e) => {
    e.preventDefault();
    if (!habit.trim()) return;

    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/habits",
        { name: habit },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setHabits([...habits, response.data]);
      setHabit("");
      showMessage("Habit added successfully!");
    } catch (err) {
      console.error("Error adding habit:", err);
      showMessage("Failed to add habit.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteHabit = async (id) => {
    if (!window.confirm("Are you sure you want to delete this habit?")) return;

    setIsLoading(true);
    const original = [...habits];
    setHabits((prev) => prev.filter((h) => h.id !== id));
    try {
      await axios.delete(`http://127.0.0.1:5000/habits/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      showMessage("Habit deleted.");
    } catch (err) {
      console.error("Delete error:", err);
      setHabits(original);
      showMessage("Failed to delete habit.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetHabits = async () => {
    if (!window.confirm("Reset all habits?")) return;

    setIsLoading(true);
    try {
      await axios.post(
        "http://127.0.0.1:5000/reset_habits",
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      showMessage("All habits reset.");
      setHabits([]);
    } catch (err) {
      console.error(err);
      showMessage("Failed to reset habits.");
      fetchHabits();
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
          placeholder="Add a new habit"
          value={habit}
          onChange={(e) => setHabit(e.target.value)}
          className="input-box"
        />
        <button type="submit" disabled={isLoading} className="add-btn">
          {isLoading ? "Adding..." : "Add"}
        </button>
      </form>

      {message && <p className="message">{message}</p>}

      <h2>Habits</h2>
      {isLoading ? (
        <div className="spinner">Loading...</div>
      ) : habits.length ? (
        <ul className="habit-list">
          {habits.map((habit) => (
            <li key={habit.id} className="habit-item">
              {habit.name}
              <button
                className="delete-btn"
                onClick={() => handleDeleteHabit(habit.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No habits found.</p>
      )}

      <button onClick={handleResetHabits} disabled={isLoading} className="reset-btn">
        {isLoading ? "Resetting..." : "Reset All"}
      </button>
    </div>
  );
};

export default HabitTracker;
