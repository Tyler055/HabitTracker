import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is already logged in
    const userLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    setIsLoggedIn(userLoggedIn);

    // If logged in, redirect to Habit Tracker
    if (userLoggedIn) {
      navigate("/habit-tracker");
    }
  }, [navigate]);

  const handleLogin = () => {
    // Simulate the login process (replace with real API call for production)
    localStorage.setItem("isLoggedIn", "true");
    setIsLoggedIn(true);
    navigate("/habit-tracker");
  };

  const handleLogout = () => {
    // Handle the logout process
    localStorage.removeItem("isLoggedIn");
    setIsLoggedIn(false);
    navigate("/");
  };

  return (
    <div>
      <h1>Welcome to Your Habit Tracker</h1>
      <p>This is where you can track your habits and progress over time.</p>
      <p>To get started, please log in or create an account.</p>

      {!isLoggedIn ? (
        <div>
          <button onClick={handleLogin}>Log In / Sign Up</button>
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

export default Home;
