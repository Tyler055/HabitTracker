import React, { useState, useEffect } from "react";
import axios from "axios"; // Assuming you're using axios to fetch data from an API

const Habits = () => {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true); // Manage loading state
  const [error, setError] = useState(""); // Manage error state

  useEffect(() => {
    // Fetch habits from the backend
    const fetchHabits = async () => {
      try {
        setLoading(true);
        const response = await axios.get("/habits"); // Replace with your API endpoint
        setHabits(response.data); // Assuming the response contains an array of habits
      } catch (error) {
        setError("Failed to fetch habits. Please try again later.");
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
        {habits.map((habit) => (
          <li key={habit.id || habit}> {/* Assuming each habit has a unique `id` */}
            {habit.name || habit} {/* If habit is an object, display habit.name, else just display the habit */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Habits;
