import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // Base URL for the API

// Fetch habits from the backend
export const getHabits = () => axios.get(`${API_BASE_URL}/api/habits`);

// Add a new habit
export const addHabit = (name) => axios.post(`${API_BASE_URL}/api/add-habit`, { name });

// Delete a habit
export const deleteHabit = (id) => axios.delete(`${API_BASE_URL}/api/habits/${id}`);

// Reset all habits
export const resetHabits = () => axios.post(`${API_BASE_URL}/api/reset_habits`);
