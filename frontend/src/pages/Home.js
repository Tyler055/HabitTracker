import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is already logged in
    const userLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    setIsLoggedIn(userLoggedIn);

    // If logged in, redirect to Habit Tracker
    if (userLoggedIn) {
      navigate("/HabitTracker");
    }
  }, [navigate]);

  const handleLogin = () => {
    navigate("/login");  // Navigate to the login page
  };

  const handleSignup = () => {
    navigate("/signup");  // Navigate to the signup page
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");  // Clear login status
    localStorage.removeItem("token");  // Clear any authentication token
    setIsLoggedIn(false); // Update state
    navigate("/"); // Redirect to the home page
  };

  return (
    <div>
      <h1>Welcome to Your Habit Tracker</h1>
      <p>This is where you can track your habits and progress over time.</p>
      <p>To get started, please log in or create an account.</p>

      {!isLoggedIn ? (
        <div>
          <button onClick={handleLogin}>Log In</button>
          <button onClick={handleSignup}>Sign Up</button>
        </div>
      ) : (
        <div>
          <button onClick={handleLogout}>Log Out</button>
        </div>
      )}

      <p>If you're already a user, logging in will take you straight to your Habit Tracker.</p>
    </div>
  );
};

export default HomePage;
