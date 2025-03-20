// app.js

import React from 'react';
import { toggleTheme } from './utils/theme';

const App = () => {
  const resetHabits = async () => {
    if (window.confirm('Are you sure you want to reset your habits? This cannot be undone.')) {
      try {
        const response = await fetch('/reset_habits', { method: 'POST' });
        if (response.ok) {
          window.location.reload();
        } else {
          throw new Error('Error resetting habits.');
        }
      } catch (error) {
        alert(error.message);
      }
    }
  };

  return (
    <div>
      <button id="theme-toggle" onClick={toggleTheme}>
        Switch to Light Mode
      </button>
      <button id="reset-button" onClick={resetHabits}>
        Reset Habits
      </button>
    </div>
  );
};

export default App;
