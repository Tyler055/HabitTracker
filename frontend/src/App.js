import React, { useState, useEffect } from 'react';
import AddHabit from './components/AddHabit';
import './styles/styles.css';

const App = () => {
  // State to manage the current theme
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Load saved theme from localStorage when the component mounts
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setIsDarkMode(savedTheme === 'dark');
    document.body.classList.add(`${savedTheme}-theme`);
  }, []);

  const toggleTheme = () => {
    // Toggle between dark and light themes
    const newTheme = !isDarkMode ? 'dark' : 'light';
    setIsDarkMode(!isDarkMode);
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme); // Save theme preference
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

      {/* Habit Adding Component */}
      <AddHabit />

    </div>
  );
};

export default App;
