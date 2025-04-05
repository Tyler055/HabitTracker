import React, { useState, useEffect } from "react";
import axios from "axios";

const Habits = () => {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true); // Manage loading state
  const [error, setError] = useState(""); // Manage error state

  useEffect(() => {
    // Fetch habits from the backend
    const fetchHabits = async () => {
      try {
        setLoading(true);
        const response = await axios.get("http://127.0.0.1:5000/habits"); // Ensure correct API URL
        setHabits(response.data); // Assuming the response contains an array of habits
      } catch (error) {
        setError(`Failed to fetch habits. Error: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchHabits();
  }, []);

  return (
    <div>
      <h2>Your Habits</h2>

      {loading && <p>Loading habits...</p>} {/* Show loading text while fetching */}
      {error && <p className="error-message">{error}</p>} {/* Show error message */}
      {habits.length === 0 && !loading && !error && (
        <p>No habits found. Start adding some!</p>
      )}

      <ul>
        {habits.map((habit, index) => (
          <li key={habit.id || index}> {/* Use habit.id or fallback */}
            {habit.name || "Unnamed Habit"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Habits;
