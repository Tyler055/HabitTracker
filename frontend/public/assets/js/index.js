import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client'; // React 18+ syntax
import './styles/styles.css'; // Link to CSS

// App component
function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });

  useEffect(() => {
    const themeClass = isDarkMode ? 'dark-theme' : 'light-theme';
    document.body.classList.remove('dark-theme', 'light-theme');
    document.body.classList.add(themeClass);
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  const resetHabits = async () => {
    if (window.confirm("Are you sure you want to reset your habits?")) {
      try {
        await fetch('http://127.0.0.1:5000/api/reset-habits', { method: 'POST' });
        alert("Habits reset successfully!");
      } catch (error) {
        alert("Failed to reset habits.");
      }
    }
  };

  return (
    <div className="container">
      <h1>Habit Tracker</h1>

      {/* Toggle Switch */}
      <label className="switch">
        <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} />
        <span className="slider"></span>
      </label>
      <button onClick={toggleTheme}>
        {isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>

      <div className="habit-item">
        <span>Read a Book</span>
        <button className="delete-btn">Delete</button>
      </div>

      <input type="text" className="input-box" placeholder="Add new habit" />
      <button type="submit" id="add-habit-btn">Submit</button>

      <button id="reset-button" onClick={resetHabits}>Reset Habits</button>
    </div>
  );
}

// Get root element and render the app using createRoot (React 18+)
const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
