import { useState } from 'react';
import axiosInstance from "../utils/api"; // Importing the axios instance

const AddHabit = () => {
  const [habitData, setHabitData] = useState({
    name: '',
    frequency: '', // You can add more fields as needed
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handling the form data change
  const handleChange = (e) => {
    setHabitData({
      ...habitData,
      [e.target.name]: e.target.value,
    });
  };

  // Function to add a habit
  const addHabit = async () => {
    setIsLoading(true);
    setError(null); // Clear any previous errors

    try {
      // Sending the POST request with the habit data
      const response = await axiosInstance.post("/add-habit", habitData);
      console.log('Habit added successfully:', response.data);

      // Optional: Add feedback to the user
      alert('Habit added successfully!');

      // Reset the form after adding the habit
      setHabitData({
        name: '',
        frequency: '',
      });

      // You could update the state with the new habit here if needed
      // Example: setHabits([...habits, response.data]);

    } catch (error) {
      console.error('Error adding habit:', error);

      // Handle different types of errors
      if (error.response) {
        setError("Server error: " + error.response.data.message); // Backend error
      } else if (error.request) {
        setError("Network error: Please check your internet connection.");
      } else {
        setError("Error: " + error.message); // Other errors
      }
    } finally {
      setIsLoading(false); // Stop loading state
    }
  };

  return (
    <div>
      <h2>Add a New Habit</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="text"
        name="name"
        value={habitData.name}
        onChange={handleChange}
        placeholder="Habit Name"
      />
      <input
        type="text"
        name="frequency"
        value={habitData.frequency}
        onChange={handleChange}
        placeholder="Frequency"
      />
      <button onClick={addHabit} disabled={isLoading}>
        {isLoading ? "Adding..." : "Add Habit"}
      </button>
    </div>
  );
};

export default AddHabit;
