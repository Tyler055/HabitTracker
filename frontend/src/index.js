import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client'; // React 18+ syntax
import './styles/styles.css'; // Link to your CSS
import './styles/taskbar.css';

// App component
function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Effect to apply the saved theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
      document.body.classList.add(savedTheme + '-theme');
    }
  }, []);

  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
    const newTheme = !isDarkMode ? 'dark' : 'light';
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme); // Save theme preference
  };

  // Reset habits logic (move this to React as well)
  const resetHabits = () => {
    const resetButton = document.getElementById('reset-button');
    if (resetButton) {
      resetButton.disabled = true;
      resetButton.textContent = "Resetting...";

      fetch('/reset_habits', { method: 'POST' })
        .then(response => {
          if (response.ok) {
            window.location.reload();
          } else {
            throw new Error("Error resetting habits.");
          }
        })
        .catch(error => {
          alert(error.message);
        })
        .finally(() => {
          resetButton.disabled = false;
          resetButton.textContent = "Reset Habits";
        });
    }
  };

  return (
    <div className="container">
      {/* Taskbar */}
      <div className="taskbar">
        <div className="taskbar-item">Home</div>
        <div className="taskbar-item">Tasks</div>
        <div className="taskbar-item">Settings</div>
        <div className="taskbar-item">Profile</div>
      </div>

      <h1>Habit Tracker</h1>

      {/* Theme Toggle */}
      <label className="switch">
        <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} />
        <span className="slider"></span>
      </label>
      <span>{isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}</span>

      {/* Habit Item */}
      <div className="habit-item">
        <span>Read a Book</span>
        <button className="delete-btn">Delete</button>
      </div>

      {/* New Habit Input */}
      <input type="text" className="input-box" placeholder="Add new habit" />
      <button type="submit" id="add-habit-btn">Submit</button>

      {/* Reset Button */}
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
