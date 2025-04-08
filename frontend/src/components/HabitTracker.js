import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import HabitList from "../pages/HabitsList"; // Assuming this is your component for listing habits

const HabitTracker = () => {
  const [habitInput, setHabitInput] = useState(""); // Input for new habit
  const [description, setDescription] = useState(""); // Habit description
  const [reminderFrequency, setReminderFrequency] = useState(""); // Frequency for reminders
  const [habits, setHabits] = useState([]); // List of all habits
  const [message, setMessage] = useState(""); // For success/error messages
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const [filter, setFilter] = useState("all"); // Filter for habits (e.g., daily, weekly)
  const [selectedHabits, setSelectedHabits] = useState([]); // For bulk actions
  const [editingHabitId, setEditingHabitId] = useState(null); // Track habit being edited
  const [editedHabitName, setEditedHabitName] = useState(""); // Name of the habit being edited

  const token = localStorage.getItem("token") || ""; // Authentication token

  // Display messages
  const showMessage = useCallback((msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(""), 3000); // Clear message after 3 seconds
  }, []);

  // Fetch habits from the API
  const fetchHabits = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await axios.get("http://127.0.0.1:5000/habits", {
        headers: { Authorization: `Bearer ${token}` },
        params: filter === "all" ? {} : { frequency: filter }, // Apply filter when fetching habits
      });
      setHabits(res.data || []);
    } catch (err) {
      console.error(err);
      showMessage("Failed to fetch habits.");
    } finally {
      setIsLoading(false);
    }
  }, [token, filter, showMessage]);

  // Fetch habits on mount or when filter changes
  useEffect(() => {
    fetchHabits();
  }, [fetchHabits]);

  // Add a new habit
  const handleAddHabit = async (e) => {
    e.preventDefault();
    if (!habitInput.trim()) return; // Prevent adding empty habit

    setIsLoading(true);
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/habits",
        {
          name: habitInput,
          description: description,
          frequency: "daily", // Default to daily frequency
          reminder_frequency: reminderFrequency,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setHabits((prev) => [...prev, res.data.habit]);
      setHabitInput(""); // Reset input
      setDescription(""); // Reset description
      setReminderFrequency(""); // Reset reminder frequency
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
    if (!editedHabitName.trim()) return; // Prevent empty edits

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
      setEditingHabitId(null); // Clear editing state
      setEditedHabitName(""); // Clear edited name
      showMessage("Habit updated successfully!");
    } catch (err) {
      console.error(err);
      showMessage("Failed to edit habit.");
    }
  };

  // Delete a habit
  const handleDeleteHabit = async (id) => {
    if (!window.confirm("Are you sure you want to delete this habit?")) return;

    const original = [...habits]; // Backup the original habits list
    setHabits((prev) => prev.filter((h) => h.id !== id)); // Remove from UI optimistically
    setIsLoading(true);
    try {
      await axios.delete(`http://127.0.0.1:5000/habits/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      showMessage("Habit deleted.");
    } catch (err) {
      console.error(err);
      setHabits(original); // Restore original list if deletion fails
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
        `http://127.0.0.1:5000/habits/complete/${id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showMessage("Habit completed successfully!");
      fetchHabits(); // Refresh the habit list
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
      setSelectedHabits([]); // Clear selection
      fetchHabits(); // Refresh the habit list
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
      setHabits([]); // Clear all habits from UI
      showMessage("All habits reset.");
    } catch (err) {
      console.error(err);
      showMessage("Failed to reset habits.");
      fetchHabits(); // Refresh habit list if reset fails
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="habit-container">
      <h1>Habit Tracker</h1>

      {/* Habit Form */}
      <form onSubmit={handleAddHabit}>
        <input
          type="text"
          placeholder="habit name"
          value={habitInput}
          onChange={(e) => setHabitInput(e.target.value)}
        />
        <textarea
          placeholder="Optional description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select
          value={reminderFrequency}
          onChange={(e) => setReminderFrequency(e.target.value)}
        >
          <option value="">Reminder Frequency</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Adding..." : "Add Habit"}
        </button>
      </form>

      {/* Filter by Frequency */}
      <div>
        <select onChange={(e) => setFilter(e.target.value)} value={filter}>
          <option value="all">All</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>

      {/* Habit List Title */}
      <h2>Habit List</h2>

      {/* Habit List */}
      {isLoading ? (
        <div className="spinner">Loading...</div>
      ) : (
        <HabitList
          habits={habits}
          onEditHabit={handleEditHabit}
          onDeleteHabit={handleDeleteHabit}
          onCompleteHabit={handleCompleteHabit}
          onToggleSelection={toggleSelection}
          setEditingHabitId={setEditingHabitId}
          editingHabitId={editingHabitId}
          setEditedHabitName={setEditedHabitName}
          editedHabitName={editedHabitName}
        />
      )}

      {/* Complete Checkboxes */}
      <div>
        {habits.map((habit) => (
          <div key={habit.id}>
            <input
              type="checkbox"
              checked={selectedHabits.includes(habit.id)}
              onChange={() => toggleSelection(habit.id)}
            />
            {habit.name}
          </div>
        ))}
      </div>

      {/* Bulk Complete */}
      {selectedHabits.length > 0 && (
        <button onClick={handleBulkComplete} disabled={isLoading}>
          Complete Selected Habits
        </button>
      )}

      {/* Reset All */}
      <button onClick={handleResetHabits} disabled={isLoading}>
        Reset All Habits
      </button>

      {/* Message */}
      {message && <div>{message}</div>}
    </div>
  );
};

export default HabitTracker;
