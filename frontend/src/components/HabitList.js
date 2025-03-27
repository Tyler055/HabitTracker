import React, { useState, useEffect } from 'react';
import { getHabits, addHabit as addHabitApi, deleteHabit as deleteHabitApi, resetHabits as resetHabitsApi } from './api';

const HabitList = () => {
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState('');
  const [error, setError] = useState(null);

  // Fetch habits on component mount
  useEffect(() => {
    loadHabits();
  }, []);

  // Load habits from the backend
  const loadHabits = async () => {
    try {
      const response = await getHabits();
      setHabits(response.data);
    } catch (error) {
      setError("Failed to load habits.");
    }
  };

  const addHabit = async () => {
    if (!newHabit.trim()) {
      setError("Habit name cannot be empty.");
      return;
    }

    try {
      const response = await addHabitApi(newHabit);
      setHabits(prevHabits => [...prevHabits, response.data]);
      setNewHabit('');
      setError(null);
    } catch (error) {
      setError("Failed to add habit.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this habit?")) return;

    try {
      await deleteHabitApi(id);
      setHabits(habits.filter((habit) => habit.id !== id));
    } catch (error) {
      setError("Failed to delete habit.");
    }
  };

  const resetHabits = async () => {
    if (!window.confirm("Are you sure you want to reset all habits?")) return;

    try {
      await resetHabitsApi();
      setHabits([]); // Clear habits list on successful reset
    } catch (error) {
      setError("Failed to reset habits.");
    }
  };

  return (
    <div>
      <h1>Your Habit Tracker</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error messages */}

      <ul>
        {habits.length === 0 ? (
          <li>No habits found. Start adding some!</li>
        ) : (
          habits.map((habit) => (
            <li key={habit.id}>
              {habit.name}
              <button onClick={() => handleDelete(habit.id)}>Delete</button>
            </li>
          ))
        )}
      </ul>

      <input
        type="text"
        value={newHabit}
        onChange={(e) => setNewHabit(e.target.value)}
        placeholder="New habit"
      />
      <button onClick={addHabit}>Add Habit</button>

      <button onClick={resetHabits}>Reset All Habits</button> {/* Reset all habits */}
    </div>
  );
};

export default HabitList;
