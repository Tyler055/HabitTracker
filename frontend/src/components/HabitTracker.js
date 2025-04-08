import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import HabitList from "../pages/HabitsList";

const HabitTracker = () => {
  const [habitInput, setHabitInput] = useState("");
  const [habits, setHabits] = useState([]);
  const [selectedHabits, setSelectedHabits] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState([]);
  const [statsPeriod, setStatsPeriod] = useState("7d");
  const [filter, setFilter] = useState("all");
  const [editingHabitId, setEditingHabitId] = useState(null);
  const [editedHabitName, setEditedHabitName] = useState("");

  const token = localStorage.getItem("token") || "";

  // Display messages
  const showMessage = useCallback((msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(""), 3000);
  }, []);

  // Fetch habits from the API
  const fetchHabits = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await axios.get("http://127.0.0.1:5000/habits", {
        headers: { Authorization: `Bearer ${token}` },
        params: filter === "all" ? {} : { frequency: filter },
      });
      setHabits(res.data.habits || []);
    } catch (err) {
      console.error(err);
      showMessage("Failed to fetch habits.");
    } finally {
      setIsLoading(false);
    }
  }, [token, filter, showMessage]);

  // Fetch stats based on the selected period
  const fetchStats = useCallback(async (period) => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/habits/stats", {
        headers: { Authorization: `Bearer ${token}` },
        params: { period },
      });
      setStats(res.data.stats);
    } catch (err) {
      console.error(err);
      showMessage("Failed to fetch stats.");
    }
  }, [token, showMessage]);

  // Fetch habits and stats on mount
  useEffect(() => {
    fetchHabits();
    fetchStats(statsPeriod);
  }, [fetchHabits, fetchStats, statsPeriod]);

  // Add a new habit
  const handleAddHabit = async (e) => {
    e.preventDefault();
    if (!habitInput.trim()) return;

    setIsLoading(true);
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/habits",
        { name: habitInput },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setHabits((prev) => [...prev, res.data]);
      setHabitInput("");
      showMessage("Habit added successfully!");
    } catch (err) {
      console.error(err);
      showMessage("Failed to add habit.");
    } finally {
      setIsLoading(false);
    }
  };

  // Edit a habit's name
  const handleEditHabit = async (id) => {
    if (!editedHabitName.trim()) return;

    try {
      await axios.put(
        `http://127.0.0.1:5000/habits/${id}`,
        { name: editedHabitName },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setHabits(
        habits.map((habit) =>
          habit.id === id ? { ...habit, name: editedHabitName } : habit
        )
      );
      setEditingHabitId(null);
      setEditedHabitName("");
      showMessage("Habit updated successfully!");
    } catch (err) {
      console.error(err);
      showMessage("Failed to edit habit.");
    }
  };

  // Delete a habit
  const handleDeleteHabit = async (id) => {
    if (!window.confirm("Are you sure you want to delete this habit?")) return;

    const original = [...habits];
    setHabits((prev) => prev.filter((h) => h.id !== id));
    setIsLoading(true);
    try {
      await axios.delete(`http://127.0.0.1:5000/habits/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      showMessage("Habit deleted.");
    } catch (err) {
      console.error(err);
      setHabits(original);
      showMessage("Failed to delete habit.");
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle habit selection for bulk actions
  const toggleSelection = (id) => {
    setSelectedHabits((prev) =>
      prev.includes(id) ? prev.filter((sid) => sid !== id) : [...prev, id]
    );
  };

  // Complete a single habit
  const handleCompleteHabit = async (id) => {
    setIsLoading(true);
    try {
      await axios.post(
        `http://127.0.0.1:5000/habits/${id}/complete`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showMessage("Habit completed successfully!");
      fetchHabits();
    } catch (err) {
      console.error(err);
      showMessage("Failed to complete habit.");
    } finally {
      setIsLoading(false);
    }
  };

  // Complete selected habits in bulk
  const handleBulkComplete = async () => {
    if (selectedHabits.length === 0) {
      showMessage("No habits selected.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/habits/complete_bulk",
        { habit_ids: selectedHabits },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showMessage(`Completed ${res.data.completed_ids.length} habits.`);
      setSelectedHabits([]);
      fetchHabits();
    } catch (err) {
      console.error(err);
      showMessage("Failed to complete selected habits.");
    } finally {
      setIsLoading(false);
    }
  };

  // Reset all habits
  const handleResetHabits = async () => {
    if (!window.confirm("Reset all habits?")) return;

    setIsLoading(true);
    try {
      await axios.post(
        "http://127.0.0.1:5000/reset_habits",
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setHabits([]);
      showMessage("All habits reset.");
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

      {/* Add Habit Form */}
      <form onSubmit={handleAddHabit} className="habit-form">
        <input
          type="text"
          placeholder="Add a new habit"
          value={habitInput}
          onChange={(e) => setHabitInput(e.target.value)}
          className="input-box"
        />
        <button type="submit" disabled={isLoading} className="add-btn">
          {isLoading ? "Adding..." : "Add"}
        </button>
      </form>

      {/* Message Display */}
      {message && <p className="message">{message}</p>}

      {/* Habit Filter */}
      <div className="flex space-x-2 mb-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          <option value="all">All</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>

      {/* Loading State or Habits List */}
      {isLoading ? (
        <div className="spinner">Loading...</div>
      ) : habits.length ? (
        <HabitList
          habits={habits}
          editingHabitId={editingHabitId}
          editedHabitName={editedHabitName}
          setEditingHabitId={setEditingHabitId}
          setEditedHabitName={setEditedHabitName}
          handleEditHabit={handleEditHabit}
          handleDeleteHabit={handleDeleteHabit}
          handleCompleteHabit={(id) => handleCompleteHabit(id)}
          toggleSelection={toggleSelection}
          selectedHabits={selectedHabits}
        />
      ) : (
        <p>No habits found.</p>
      )}

      {/* Bulk Complete & Reset Buttons */}
      <button
        onClick={handleBulkComplete}
        disabled={isLoading || selectedHabits.length === 0}
        className="bulk-complete-btn"
      >
        {isLoading ? "Processing..." : "Bulk Complete Selected"}
      </button>

      <button
        onClick={handleResetHabits}
        disabled={isLoading}
        className="reset-btn"
      >
        {isLoading ? "Resetting..." : "Reset All"}
      </button>

      {/* Stats Section */}
      <div className="stats-container">
        <h2>Habit Stats</h2>
        <div className="stats-controls">
          <button
            onClick={() => setStatsPeriod("7d")}
            disabled={statsPeriod === "7d"}
          >
            Last 7 days
          </button>
          <button
            onClick={() => setStatsPeriod("30d")}
            disabled={statsPeriod === "30d"}
          >
            Last 30 days
          </button>
        </div>
        {stats.length ? (
          <ul className="stats-list">
            {stats.map((stat) => (
              <li key={stat.date}>
                {stat.date}: {stat.count} completions
              </li>
            ))}
          </ul>
        ) : (
          <p>No stats available.</p>
        )}
      </div>
    </div>
  );
};

export default HabitTracker;
