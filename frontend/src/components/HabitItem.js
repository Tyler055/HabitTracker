import React, { useState } from "react";

export default function HabitItem({ habit, onDelete }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDelete = async () => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete the habit "${habit.name}"?`
    );

    if (confirmDelete) {
      try {
        setLoading(true);
        await onDelete(habit.id); // Assuming onDelete is an async function (like an API call)
        setLoading(false);
      } catch (err) {
        setLoading(false);
        setError("Failed to delete habit. Please try again.");
      }
    }
  };

  return (
    <div className="habit-item">
      <h3>{habit.name}</h3>
      <p>{habit.description}</p>
      {error && <p className="error-message">{error}</p>}
      <button 
        className="delete-btn" 
        onClick={handleDelete}
        disabled={loading}
      >
        {loading ? "Deleting..." : "Delete"}
      </button>
    </div>
  );
}
