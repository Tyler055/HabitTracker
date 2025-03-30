import React, { useState, useEffect } from 'react';
import '../styles/Progress.css'; // Correct import path for your CSS file

const Progress = () => {
  const [habitsProgress, setHabitsProgress] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [compareMode, setCompareMode] = useState(false);
  const [habitColors, setHabitColors] = useState({
    habit1: '#4caf50', // Default color for Habit 1
    habit2: '#ff9800', // Default color for Habit 2
  });

  // Fetching progress data (mocked here for now)
  useEffect(() => {
    // Replace with real API call
    fetch('/api/progress') // Adjust endpoint to match your server's
      .then(res => res.json())
      .then(data => setHabitsProgress(data))
      .catch(() => setErrorMessage('Failed to fetch progress.'));
  }, []);

  // Function to toggle Compare Mode
  const toggleCompareMode = () => {
    setCompareMode(prevState => !prevState);
  };

  // Function to update color for a habit
  const handleColorChange = (habit, color) => {
    setHabitColors(prevColors => ({
      ...prevColors,
      [habit]: color,
    }));
  };

  return (
    <div className="progress-page">
      <h1>Your Habit Progress</h1>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <div className="color-customization">
        <label htmlFor="habit1-color">Select Habit 1 Color:</label>
        <input
          type="color"
          id="habit1-color"
          value={habitColors.habit1}
          onChange={(e) => handleColorChange('habit1', e.target.value)}
        />

        <label htmlFor="habit2-color">Select Habit 2 Color:</label>
        <input
          type="color"
          id="habit2-color"
          value={habitColors.habit2}
          onChange={(e) => handleColorChange('habit2', e.target.value)}
        />
      </div>

      <button onClick={toggleCompareMode}>
        {compareMode ? 'Show Single Habit' : 'Compare Habits'}
      </button>

      <div className="progress-list">
        {compareMode ? (
          // Compare Mode (Display two habits side-by-side)
          <div className="compare-mode">
            {habitsProgress.length > 0 && (
              <>
                <div
                  className="habit-item"
                  style={{ backgroundColor: habitColors.habit1 }}
                >
                  <h3>{habitsProgress[0]?.name || 'Habit 1'}</h3>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${habitsProgress[0]?.completionPercentage || 0}%`,
                        backgroundColor: habitColors.habit1,
                      }}
                    ></div>
                  </div>
                  <p>{habitsProgress[0]?.completionPercentage}% completed</p>
                </div>

                <div
                  className="habit-item"
                  style={{ backgroundColor: habitColors.habit2 }}
                >
                  <h3>{habitsProgress[1]?.name || 'Habit 2'}</h3>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${habitsProgress[1]?.completionPercentage || 0}%`,
                        backgroundColor: habitColors.habit2,
                      }}
                    ></div>
                  </div>
                  <p>{habitsProgress[1]?.completionPercentage}% completed</p>
                </div>
              </>
            )}
          </div>
        ) : (
          // Single Habit View
          habitsProgress.length > 0 ? (
            habitsProgress.map((habit, index) => (
              <div key={index} className="progress-item">
                <h3>{habit.name}</h3>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${habit.completionPercentage}%`,
                      backgroundColor: habitColors[`habit${index + 1}`],
                    }}
                  ></div>
                </div>
                <p>{habit.completionPercentage}% completed</p>
              </div>
            ))
          ) : (
            <p>No progress data available.</p>
          )
        )}
      </div>
    </div>
  );
};

export default Progress;
