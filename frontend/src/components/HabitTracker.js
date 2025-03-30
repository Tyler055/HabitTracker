import React, { useState, useEffect } from "react";
import axios from "axios";

const HabitTracker = () => {
  const [habit, setHabit] = useState("");
  const [habits, setHabits] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState(""); // Added success message state
  const [isLoading, setIsLoading] = useState(false);

  // Fetch habits from the backend on mount
  useEffect(() => {
    const fetchHabits = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get("/habits");
        setHabits(response.data);
      } catch (error) {
        setErrorMessage("Failed to fetch habits.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchHabits();
  }, []);

  // Handle adding a new habit
  const handleAddHabit = async (e) => {
    e.preventDefault();
    if (!habit.trim()) return;

    // Optimistically update UI
    const newHabit = { id: Date.now(), name: habit };
    setHabits((prevHabits) => [...prevHabits, newHabit]);

    setIsLoading(true);
    try {
      const response = await axios.post("/habits", { name: habit });
      setHabits((prevHabits) =>
        prevHabits.map((h) =>
          h.id === newHabit.id ? { ...newHabit, id: response.data.id } : h
        )
      );
      setHabit(""); // Reset input field
      setErrorMessage(""); // Clear previous error
      setSuccessMessage("Habit added successfully!"); // Show success message
      setTimeout(() => setSuccessMessage(""), 3000); // Hide after 3 seconds
    } catch (error) {
      setErrorMessage("Failed to add habit.");
      setHabits((prevHabits) => prevHabits.filter((h) => h.id !== newHabit.id)); // Rollback on error
    } finally {
      setIsLoading(false);
    }
  };

  // Handle deleting a habit
  const handleDeleteHabit = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this habit?");
    if (!confirmDelete) return;

    setIsLoading(true);
    try {
      await axios.delete(`/habits/${id}`);
      setHabits((prevHabits) => prevHabits.filter((habit) => habit.id !== id));
    } catch (error) {
      setErrorMessage("Failed to delete habit.");
    } finally {
      setIsLoading(false);
    }
  };

  // Handle resetting all habits
  const handleResetHabits = async () => {
    const confirmReset = window.confirm("Are you sure you want to reset all habits?");
    if (!confirmReset) return;

    setIsLoading(true);
    try {
      await axios.post("/reset_habits");
      setHabits([]);
    } catch (error) {
      setErrorMessage("Failed to reset habits.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="habit-container">
      <h1>Habit Tracker</h1>

      <form onSubmit={handleAddHabit} className="habit-form">
        <label htmlFor="habitInput" className="sr-only">Habit Name</label>
        <input
          id="habitInput"
          type="text"
          className="input-box"
          placeholder="Add new habit"
          value={habit}
          onChange={(e) => setHabit(e.target.value)}
          aria-label="Enter habit name"
        />
        <button
          type="submit"
          className="add-btn"
          disabled={isLoading}
          aria-label="Add a new habit"
        >
          {isLoading ? "Adding..." : "Add Habit"}
        </button>
      </form>

      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>} {/* Success Message */}

      <h2>Habit List</h2>

      {isLoading ? (
        <div className="spinner"></div>
      ) : (
        <div className="habit-list">
          {habits.length ? (
            habits.map((habit) => (
              <div key={habit.id} className="habit-item">
                <span>{habit.name}</span>
                <button
                  className="delete-btn"
                  onClick={() => handleDeleteHabit(habit.id)} // Correctly reference habit.id
                  aria-label={`Delete habit ${habit.name}`}
                >
                  Delete
                </button>
              </div>
            ))
          ) : (
            <p>No habits found.</p>
          )}
        </div>
      )}

      <button
        onClick={handleResetHabits}
        disabled={isLoading}
        className="reset-btn"
        aria-label="Reset all habits"
      >
        {isLoading ? "Resetting..." : "Reset All Habits"}
      </button>
    </div>
  );
};

export default HabitTracker;
