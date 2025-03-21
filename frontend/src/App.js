import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from "./components/Dashboard";
import HomePage from "./pages/HomePage"; // Correct the import path
import HabitTracker from './HabitTracker'; // Import the HabitTracker component

const App = () => {
  const isAuthenticated = localStorage.getItem("token"); // Check if user is authenticated

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected route */}
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />

        {/* Habit Tracker route */}
        <Route path="/habit-tracker" element={<HabitTracker />} />
      </Routes>
    </Router>
  );
};

export default App;
