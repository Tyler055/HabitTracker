import React, { useState } from 'react';
import axios from 'axios';

const AddHabit = () => {
  const [habitName, setHabitName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/add-habit', { name: habitName });

      if (response.status === 201) {
        alert('Habit added successfully!');
      }
    } catch (error) {
      alert('Failed to add habit:', error.response.data.error);
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
          />
        </label>
        <button type="submit">Add Habit</button>
      </form>
    </div>
  );
};

export default AddHabit;
