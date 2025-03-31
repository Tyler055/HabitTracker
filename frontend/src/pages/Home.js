import React, { useEffect, useState } from "react";
import { Route, Routes, Link, useNavigate } from "react-router-dom";

// Home Component (Login/Sign Up)
const HomePage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is already logged in
    const userLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    setIsLoggedIn(userLoggedIn);

    // If logged in, redirect to Habit Tracker
    if (userLoggedIn) {
      navigate("/home");  // Redirect to home page if logged in
    }
  }, [navigate]);

  const handleLogin = () => {
    // Simulate the login process (replace with real API call for production)
    localStorage.setItem("isLoggedIn", "true");
    setIsLoggedIn(true);
    navigate("/home");  // Redirect to home after login
  };

  const handleLogout = () => {
    // Handle the logout process
    localStorage.removeItem("isLoggedIn");
    setIsLoggedIn(false);
    navigate("/");  // Redirect to the home page after logout
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

// Component to display data from Flask API
const HomeDataPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/get_html')  // Flask API endpoint
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching HTML:', error));
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      {data ? <div dangerouslySetInnerHTML={{ __html: data.html }} /> : <p>Loading...</p>}
      <nav>
        <Link to="/other">Go to Another Page</Link>
      </nav>
    </div>
  );
};

// Example of another page component
const OtherPage = () => (
  <div>
    <h1>Other Page</h1>
    <nav>
      <Link to="/">Go back to Home Page</Link>
    </nav>
  </div>
);

// Main App Component (Handles Routes)
const App = () => (
  <Routes>
    <Route path="/" element={<HomePage />} />  {/* Login / Sign Up page */}
    <Route path="/home" element={<HomeDataPage />} />  {/* Main page after login */}
    <Route path="/other" element={<OtherPage />} />  {/* Other page */}
  </Routes>
);

export default App;
