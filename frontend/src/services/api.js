import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api'; // Use consistent API base URL

const HabitList = () => {
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch habits from the backend
    axios.get(`${API_URL}/habits`)
      .then(response => setHabits(response.data))
      .catch(error => setError(error.response?.data?.error || "Failed to load habits."));
  }, []);

  const addHabit = async () => {
    if (!newHabit.trim()) {
      setError("Habit name cannot be empty.");
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/add-habit`, { name: newHabit });
      setHabits([...habits, { id: response.data.id, name: newHabit }]); // Ensure the correct structure
      setNewHabit('');
      setError(null);
    } catch (error) {
      setError(error.response?.data?.error || "Failed to add habit.");
    }
  };

  return (
    <div>
      <h1>Habit List</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error messages */}
      <ul>
        {habits.map(habit => (
          <li key={habit.id}>{habit.name}</li>
        ))}
      </ul>
      <input
        type="text"
        value={newHabit}
        onChange={(e) => setNewHabit(e.target.value)}
        placeholder="New habit"
      />
      <button onClick={addHabit}>Add Habit</button>
    </div>
  );
};

export default HabitList;
