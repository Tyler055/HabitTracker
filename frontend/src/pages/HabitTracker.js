import React, { useEffect, useState } from "react";

const HabitTracker = () => {
  const [habit, setHabit] = useState("");
  const [habits, setHabits] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchHabits = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/");
      if (!res.ok) throw new Error("Failed to fetch habits.");
      const data = await res.json();
      setHabits(data);
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!habit.trim()) return;

    setIsLoading(true);
    try {
      const res = await fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ habit_name: habit }),
      });

      if (!res.ok) throw new Error("Error adding habit");

      fetchHabits();
      setHabit("");
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteHabit = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this habit?");
    if (!confirmDelete) return;

    setIsLoading(true);
    try {
      const res = await fetch(`/delete/${id}`, { method: "GET" });
      if (!res.ok) throw new Error("Error deleting habit");

      fetchHabits();
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const resetHabits = async () => {
    const confirmReset = window.confirm("Are you sure you want to reset all habits?");
    if (!confirmReset) return;

    setErrorMessage("");
    setIsLoading(true);
    try {
      const res = await fetch("/reset_habits", { method: "POST" });
      if (!res.ok) throw new Error("Failed to reset habits");

      fetchHabits();
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="habit-container">
      <h1>Habit Tracker</h1>

      <form onSubmit={handleSubmit} className="habit-form">
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

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <h2>Habit List</h2>

      {isLoading ? (
        <p>Loading habits...</p>
      ) : (
        <div className="habit-list">
          {habits.length ? (
            habits.map((h) => (
              <div key={h.id} className="habit-item">
                <span>{h.name}</span>
                <button className="delete-btn" onClick={() => deleteHabit(h.id)}>
                  Delete
                </button>
              </div>
            ))
          ) : (
            <p>No habits found.</p>
          )}
        </div>
      )}

      <button onClick={resetHabits} disabled={isLoading} className="reset-btn">
        {isLoading ? "Resetting..." : "Reset Habits"}
      </button>
    </div>
  );
};

export default HabitTracker;
