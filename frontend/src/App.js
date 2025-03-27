import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TaskBar from './components/TaskBar'; // Taskbar for navigation
import ThemeCustomizer from './components/ThemeCustomizer'; // Theme customization component

// Import pages
import Home from './pages/Home';
import HabitTracker from './pages/HabitTracker';
import Settings from './pages/Settings';
import Profile from './pages/Profile';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [habit, setHabit] = useState('');
  const [habits, setHabits] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  // Effect to load and apply the saved theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
      document.body.classList.add(savedTheme + '-theme');
    }
    fetchHabits();
  }, []);

  // Toggle between dark and light mode
  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
    const newTheme = !isDarkMode ? 'dark' : 'light';
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme);
  };

  // Fetch habits from the backend
  const fetchHabits = () => {
    fetch('/')
      .then((response) => response.json())
      .then((data) => setHabits(data))
      .catch((error) => setErrorMessage('Error fetching habits.'));
  };

  // Add a new habit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (habit.trim()) {
      fetch('/add', {
        method: 'POST',
        body: new URLSearchParams({ habit_name: habit }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
        .then((response) => response.ok ? fetchHabits() : alert('Error adding habit'))
        .catch((error) => setErrorMessage('Error adding habit.'));
      setHabit('');
    }
  };

  // Delete a habit
  const deleteHabit = (habitId) => {
    fetch(`/delete/${habitId}`, { method: 'GET' })
      .then((response) => response.ok ? fetchHabits() : alert('Error deleting habit'))
      .catch((error) => setErrorMessage('Error deleting habit.'));
  };

  // Reset habits
  const resetHabits = () => {
    setErrorMessage(''); // Clear previous errors
    fetch('/reset_habits', { method: 'POST' })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to reset habits');
        }
        fetchHabits();
      })
      .catch((error) => setErrorMessage(error.message));
  };

  return (
    <Router>
      <TaskBar />
      <div style={{ marginTop: '60px', padding: '20px' }}>
        <ThemeCustomizer toggleTheme={toggleTheme} isDarkMode={isDarkMode} />

        <h1>Habit Tracker</h1>
        
        {errorMessage && <p className="error-message">{errorMessage}</p>}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            className="input-box"
            placeholder="Add new habit"
            value={habit}
            onChange={(e) => setHabit(e.target.value)}
          />
          <button type="submit">Submit</button>
        </form>

        <div className="habit-list">
          {habits.length > 0 ? (
            habits.map((habit) => (
              <div key={habit.id} className="habit-item">
                <span>{habit.name}</span>
                <button className="delete-btn" onClick={() => deleteHabit(habit.id)}>Delete</button>
              </div>
            ))
          ) : (
            <p>No habits found. Start by adding a new one!</p>
          )}
        </div>

        <button onClick={resetHabits}>Reset Habits</button>
      </div>
    </Router>
  );
};

export default App;
