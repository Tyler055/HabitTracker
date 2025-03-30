import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track if the user is logged in
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is already logged in
    const userLoggedIn = localStorage.getItem('isLoggedIn') === 'true'; // Check login status from localStorage
    setIsLoggedIn(userLoggedIn);

    // If already logged in, redirect to Habit Tracker
    if (userLoggedIn) {
      navigate('/habit-tracker');
    }
  }, [navigate]);

  const handleLogin = () => {
    // Simulate the login process (could be replaced with a real login/signup API)
    localStorage.setItem('isLoggedIn', 'true');
    setIsLoggedIn(true);
    navigate('/habit-tracker');
  };

  return (
    <div>
      <h1>Welcome to Your Habit Tracker</h1>
      <p>This is where you can track your habits and progress over time.</p>
      <p>To get started, please log in or create an account.</p>

      {/* Login button appears only if the user is not logged in */}
      {!isLoggedIn && (
        <div>
          <button onClick={handleLogin}>Log In / Sign Up</button>
        </div>
      )}
      {/* Additional information about the app */}
      <p>If you're already a user, logging in will take you straight to your Habit Tracker.</p>
    </div>
  );
};

export default Home;
