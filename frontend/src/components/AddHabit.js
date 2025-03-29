import React, { useState } from 'react';
import axios from 'axios';

const AddHabit = () => {
  const [habitName, setHabitName] = useState('');  // State to hold the habit name

  // Handle the form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!habitName.trim()) {
      alert('Please enter a habit name');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/add-habit', { name: habitName });

      if (response.status === 201) {
        alert('Habit added successfully!');
        setHabitName('');  // Clear the input field after adding
      }
    } catch (error) {
      alert('Failed to add habit:', error.response?.data?.error || error.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Habit Name:
          <input 
            type="text" 
            value={habitName} 
            onChange={(e) => setHabitName(e.target.value)} 
            placeholder="Enter habit name"
          />
        </label>
        <button type="submit">Add Habit</button>
      </form>
    </div>
  );
};

export default AddHabit;
