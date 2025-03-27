import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const addHabit = async (habitName) => {
  try {
    const response = await axios.post(`${API_URL}/api/add-habit`, { name: habitName });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
