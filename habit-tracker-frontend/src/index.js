// index.js
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css'; // Link to your CSS
import './script.js'

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

  return (
    <div className="container">
      <h1>Habit Tracker</h1>

      {/* Toggle Switch */}
      <label className="switch">
        <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} />
        <span className="slider"></span>
      </label>

      <div className="habit-item">
        <span>Read a Book</span>
        <button className="delete-btn">Delete</button>
        <button type="submit" id="add-habit-btn">Add Habit</button>
      </div>
      <input type="text" className="input-box" placeholder="Add new habit" />
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
