import React, { useState } from "react";
import { addHabit, resetHabits } from "../api"; // Use the API module for better structure

const HabitForm = ({ refreshHabits }) => {
  const [habitName, setHabitName] = useState("");
  const [isLoading, setIsLoading] = useState(false); // State to manage loading state
  const [errorMessage, setErrorMessage] = useState(""); // Error message state
  const [successMessage, setSuccessMessage] = useState(""); // Success message state

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!habitName.trim()) return;

    setIsLoading(true); // Start loading
    setErrorMessage(""); // Reset error message before submitting
    setSuccessMessage(""); // Reset success message before submitting

    try {
      await addHabit(habitName); // Send the request to add a habit
      setHabitName(""); // Reset the input field after adding the habit
      refreshHabits(); // Refresh the list of habits after adding
      setSuccessMessage("Habit added successfully!"); // Show success message
    } catch (error) {
      setErrorMessage("Error adding habit. Please try again."); // Show error message
      console.error("Error adding habit:", error);
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  const handleReset = async () => {
    if (!window.confirm("Are you sure you want to reset all habits?")) return;

    setIsLoading(true); // Start loading
    setErrorMessage(""); // Reset error message before resetting
    setSuccessMessage(""); // Reset success message before resetting

    try {
      await resetHabits(); // Reset all habits
      refreshHabits(); // Refresh the habit list after resetting
      setSuccessMessage("All habits have been reset!"); // Show success message
    } catch (error) {
      setErrorMessage("Error resetting habits. Please try again."); // Show error message
      console.error("Error resetting habits:", error);
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={habitName}
          onChange={(e) => setHabitName(e.target.value)}
          placeholder="Enter new habit"
          required
        />
        <button type="submit" disabled={isLoading || !habitName.trim()}>
          {isLoading ? "Adding..." : "Add Habit"}
        </button>
      </form>

      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <button onClick={handleReset} disabled={isLoading}>
        {isLoading ? "Resetting..." : "Reset Habits"}
      </button>
    </div>
  );
};

export default HabitForm;
