import { useEffect, useState } from "react";
import api from '../utils/api';
import HabitItem from "./HabitItem";
import { PuffLoader } from "react-spinners";
 // You can replace with any spinner of your choice

export default function HabitList() {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch habits from API
  const fetchHabits = async () => {
    try {
      const res = await api.get("/habits");
      setHabits(res.data);
    } catch (err) {
      setError("Failed to load habits.");
      console.error("Error fetching habits:", err); // Log the error for debugging
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  // Handle habit deletion with confirmation
  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this habit?")) {
      try {
        await api.delete(`/habits/${id}`);
        fetchHabits(); // Refresh habit list after deletion
      } catch (err) {
        alert("Failed to delete habit. Please try again.");
        console.error("Error deleting habit:", err);
      }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Puff color="#f44336" size={60} /> {/* Customize the color and size */}
        <p>Loading habits...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
      </div>
    );
  }

  return (
    <div>
      {habits.length > 0 ? (
        habits.map((habit) => (
          <HabitItem key={habit.id} habit={habit} onDelete={handleDelete} />
        ))
      ) : (
        <div>
          <p>No habits found. Add a new habit to get started!</p>
          {/* Add an optional button or link to navigate to a habit form */}
        </div>
      )}
    </div>
  );
}
