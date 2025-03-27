// index.js
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client'; // React 18+ syntax
import './styles/styles.css'; // Link to your CSS
import './styles/script.js'

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
        
      </div>
      <input type="text" className="input-box" placeholder="Add new habit" />
      <button type="submit" id="add-habit-btn">submit</button>
    </div>
  );
}

// Get root element and render the app using createRoot (React 18+)
const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);document.addEventListener("DOMContentLoaded", function () {
  init(); // Initialize once the DOM is loaded
});

function init() {
  let currentTheme = localStorage.getItem('theme') || 'dark';

  const themeButton = document.getElementById('theme-toggle');
  const resetButton = document.getElementById('reset-button');
  const submitButton = document.getElementById('submit-button');
  const form = document.getElementById('form-id');

  // Apply the saved theme
  document.body.classList.add(`${currentTheme}-theme`);

  // Update the theme button text
  if (themeButton) {
    updateButtonText();
    themeButton.addEventListener('click', () => {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.body.classList.toggle('dark-theme');
      document.body.classList.toggle('light-theme');
      localStorage.setItem('theme', currentTheme);
      updateButtonText();
    });
  }

  function updateButtonText() {
    if (themeButton) {
      themeButton.textContent = currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }
  }

  // Reset button logic
  if (resetButton) {
    resetButton.addEventListener('click', () => {
      resetButton.disabled = true;
      resetButton.textContent = "Resetting...";

      currentTheme = 'dark';
      document.body.classList.remove('light-theme');
      document.body.classList.add('dark-theme');
      localStorage.setItem('theme', currentTheme);

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
    });
  }

  // Form submission logic
  if (submitButton && form) {
    submitButton.addEventListener('click', () => {
      if (form.checkValidity()) {
        form.submit();
      } else {
        alert("Please fill in all required fields correctly.");
      }
    });
  }
}