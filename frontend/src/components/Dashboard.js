// src/components/Dashboard.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from '../utils/api';

const Dashboard = () => {
  const [habits, setHabits] = useState([]);
  const navigate = useNavigate();

  // Fetch the list of habits when the component mounts
  useEffect(() => {
    const fetchHabits = async () => {
      try {
        const response = await api.get("/habits"); // Adjust the endpoint based on your API
        setHabits(response.data);
      } catch (error) {
        console.error("Error fetching habits:", error);
      }
    };

    fetchHabits();
  }, []);

  // Handle the deletion of a habit
  const deleteHabit = async (habitId) => {
    try {
      await api.delete(`/habits/${habitId}`);
      setHabits(habits.filter((habit) => habit.id !== habitId)); // Update the state after deletion
    } catch (error) {
      console.error("Error deleting habit:", error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Your Habits</h1>
      {habits.length === 0 ? (
        <p>No habits yet. Add a new one!</p>
      ) : (
        <ul>
          {habits.map((habit) => (
            <li key={habit.id} className="habit-item">
              {habit.name}
              <button
                onClick={() => deleteHabit(habit.id)}
                className="delete-btn"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
      <button onClick={() => navigate("/add-habit")} className="add-btn">
        Add New Habit
      </button>
    </div>
  );
};

export default Dashboard;
