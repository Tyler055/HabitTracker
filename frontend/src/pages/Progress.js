import React, { useState, useEffect } from 'react';
import '../styles/Progress.css'; // Correct import path for your CSS file

const Progress = () => {
  const [habitsProgress, setHabitsProgress] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(true); // Loading state
  const [compareMode, setCompareMode] = useState(false);
  const [habitColors, setHabitColors] = useState({});

  // Fetching progress data (mocked here for now)
  useEffect(() => {
    // Replace with real API call
    fetch('/api/progress') // Adjust endpoint to match your server's
      .then(res => res.json())
      .then(data => {
        setHabitsProgress(data);
        setLoading(false);

        // Initialize colors dynamically based on habits length
        const colors = data.reduce((acc, habit, index) => {
          acc[`habit${index + 1}`] = `#${Math.floor(Math.random() * 16777215).toString(16)}`; // Random color
          return acc;
        }, {});
        setHabitColors(colors);
      })
      .catch(() => {
        setErrorMessage('Failed to fetch progress.');
        setLoading(false);
      });
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

  if (loading) {
    return <p>Loading...</p>; // Display loading message until data is fetched
  }

  return (
    <div className="progress-page">
      <h1>Your Habit Progress</h1>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <div className="color-customization">
        {habitsProgress.map((habit, index) => (
          <div key={index}>
            <label htmlFor={`habit${index + 1}-color`}>Select Color for {habit.name}:</label>
            <input
              type="color"
              id={`habit${index + 1}-color`}
              value={habitColors[`habit${index + 1}`]}
              onChange={(e) => handleColorChange(`habit${index + 1}`, e.target.value)}
            />
          </div>
        ))}
      </div>

      <button onClick={toggleCompareMode}>
        {compareMode ? 'Show Single Habit' : 'Compare Habits'}
      </button>

      <div className="progress-list">
        {compareMode ? (
          // Compare Mode (Display two habits side-by-side)
          <div className="compare-mode">
            {habitsProgress.length > 0 && habitsProgress.slice(0, 2).map((habit, index) => (
              <div
                key={index}
                className="habit-item"
                style={{ backgroundColor: habitColors[`habit${index + 1}`] }}
              >
                <h3>{habit.name}</h3>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${habit.completionPercentage || 0}%`,
                      backgroundColor: habitColors[`habit${index + 1}`],
                    }}
                  ></div>
                </div>
                <p>{habit.completionPercentage}% completed</p>
              </div>
            ))}
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
