import React, { useState } from "react";
import api from "../utils/api"; // axiosInstance

export default function HabitForm({ onHabitAdded }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false); // Loading state to show a loading indicator
  const [error, setError] = useState(""); // Error state to show an error message
  const [success, setSuccess] = useState(""); // Success message state

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    
    // Simple validation
    if (!name.trim()) {
      setError("Habit name is required.");
      setLoading(false);
      return;
    }

    try {
      await api.post("/habits", { name, description });
      setSuccess("Habit added successfully!");
      if (onHabitAdded) onHabitAdded(); // Callback function to refresh the habit list
      setName("");
      setDescription("");

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(""), 3000);
    } catch (error) {
      setError("Failed to add habit. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="habit-form">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Habit name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add Habit"}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
    </div>
  );
}
