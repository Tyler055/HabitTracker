import React, { useState, useEffect } from 'react';
import './styles/styles.css'; // Link to your CSS

const App = () => {
  // State to manage the current theme
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [habits, setHabits] = useState([]); // State to hold the list of habits
  const [newHabit, setNewHabit] = useState(''); // State to hold new habit input

  useEffect(() => {
    // Load saved theme from localStorage when the component mounts
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setIsDarkMode(savedTheme === 'dark');
    document.body.classList.add(`${savedTheme}-theme`);

    // Fetch the list of habits from the backend on load
    const fetchHabits = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/habits');
        const data = await response.json();
        setHabits(data); // Set the habits into the state
      } catch (error) {
        console.error("Error fetching habits:", error);
      }
    };

    fetchHabits();
  }, []);

  const toggleTheme = () => {
    // Toggle between dark and light themes
    const newTheme = !isDarkMode ? 'dark' : 'light';
    setIsDarkMode(!isDarkMode);
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme); // Save theme preference
  };

  const addHabit = async () => {
    if (!newHabit.trim()) return; // Prevent empty habit

    try {
      const response = await fetch('http://127.0.0.1:5000/habits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newHabit }),
      });
      if (response.ok) {
        // After successful add, fetch updated habits list
        const updatedHabit = await response.json();
        setHabits([...habits, updatedHabit]); // Update the list in the state
        setNewHabit(''); // Clear input field
      }
    } catch (error) {
      console.error("Error adding habit:", error);
    }
  };

  const resetHabits = async () => {
    try {
      const response = await fetch('/reset_habits', { method: 'POST' });
      if (!response.ok) throw new Error("Error resetting habits.");
      window.location.reload(); // Reload the page after resetting habits
    } catch (error) {
      alert(error.message);
    }
  };

  const deleteHabit = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/habits/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        setHabits(habits.filter(habit => habit.id !== id)); // Remove habit from state
      } else {
        alert('Failed to delete habit.');
      }
    } catch (error) {
      console.error('Error deleting habit:', error);
    }
  };

  return (
    <div>
      <h1>Habit Tracker</h1>

      {/* Theme Toggle Button */}
      <button id="theme-toggle" onClick={toggleTheme}>
        {isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
      </button>

      {/* Reset Button */}
      <button id="reset-button" onClick={resetHabits}>
        Reset Habits
      </button>

      {/* Habit List */}
      <ul>
        {habits.map((habit, index) => (
          <li key={index}>
            {habit.name}
            <button className="delete-btn" onClick={() => deleteHabit(habit.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {/* Add Habit */}
      <input
        type="text"
        className="input-box"
        placeholder="Add new habit"
        value={newHabit}
        onChange={(e) => setNewHabit(e.target.value)}
      />
      <button onClick={addHabit}>Add Habit</button>
    </div>
  );
};

export default App;
