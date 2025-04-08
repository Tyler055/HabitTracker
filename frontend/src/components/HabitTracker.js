// HabitTracker.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import HabitList from "./HabitList";

const HabitTracker = () => {
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState("");
  const [editingHabitId, setEditingHabitId] = useState(null);
  const [editedHabitName, setEditedHabitName] = useState("");
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHabits();
  }, [filter]);

  const fetchHabits = async () => {
    setLoading(true);
    try {
      const response = await axios.get("/api/habits", {
        params: filter === "all" ? {} : { frequency: filter },
      });
      setHabits(response.data);
    } catch (error) {
      console.error("Error fetching habits:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddHabit = async () => {
    if (!newHabit.trim()) return;
    try {
      const response = await axios.post("/api/habits", { name: newHabit });
      setHabits([...habits, response.data]);
      setNewHabit("");
    } catch (error) {
      console.error("Error adding habit:", error);
    }
  };

  const handleDeleteHabit = async (id) => {
    try {
      await axios.delete(`/api/habits/${id}`);
      setHabits(habits.filter((habit) => habit.id !== id));
    } catch (error) {
      console.error("Error deleting habit:", error);
    }
  };

  const handleEditHabit = async (id) => {
    try {
      await axios.put(`/api/habits/${id}`, { name: editedHabitName });
      setHabits(
        habits.map((habit) =>
          habit.id === id ? { ...habit, name: editedHabitName } : habit
        )
      );
      setEditingHabitId(null);
      setEditedHabitName("");
    } catch (error) {
      console.error("Error editing habit:", error);
    }
  };

  const handleCompleteHabit = async (id) => {
    try {
      await axios.post(`/api/habits/${id}/complete`);
      setHabits(
        habits.map((habit) =>
          habit.id === id ? { ...habit, completed_today: true } : habit
        )
      );
    } catch (error) {
      console.error("Error completing habit:", error);
    }
  };

  const handleBulkComplete = async () => {
    try {
      const ids = habits.map((habit) => habit.id);
      await axios.post("/api/habits/complete-bulk", { ids });
      setHabits(
        habits.map((habit) => ({ ...habit, completed_today: true }))
      );
    } catch (error) {
      console.error("Error bulk completing habits:", error);
    }
  };

  const handleResetCompletions = async () => {
    try {
      await axios.post("/api/habits/reset-completions");
      setHabits(
        habits.map((habit) => ({ ...habit, completed_today: false }))
      );
    } catch (error) {
      console.error("Error resetting completions:", error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Habit Tracker</h1>
      <div className="flex space-x-2 mb-4">
        <input
          value={newHabit}
          onChange={(e) => setNewHabit(e.target.value)}
          placeholder="New habit"
          className="flex-1 border px-2 py-1 rounded"
        />
        <button
          onClick={handleAddHabit}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded"
        >
          Add
        </button>
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
      <div className="flex space-x-2 mb-4">
        <button
          onClick={handleBulkComplete}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-1 rounded"
        >
          Complete All
        </button>
        <button
          onClick={handleResetCompletions}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-1 rounded"
        >
          Reset Completions
        </button>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <HabitList
          habits={habits}
          editingHabitId={editingHabitId}
          editedHabitName={editedHabitName}
          setEditingHabitId={setEditingHabitId}
          setEditedHabitName={setEditedHabitName}
          handleEditHabit={handleEditHabit}
          handleDeleteHabit={handleDeleteHabit}
          handleCompleteHabit={handleCompleteHabit}
        />
      )}
    </div>
  );
};

export default HabitTracker;
