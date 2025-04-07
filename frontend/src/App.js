import React, { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import TaskBar from "./TaskBar";
import Home from "./pages/Home";
import HabitTracker from "./components/HabitTracker";
import Progress from "./pages/Progress";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import AuthForm from "./components/AuthForm";
import PrivateRoute from "./components/PrivateRoute";
import logo from "./logo.svg";
import './styles/App.css';
import './styles/styles.css';

const App = () => {
  const navigate = useNavigate();
  const [isTaskbarVisible, setIsTaskbarVisible] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [fontSize, setFontSize] = useState('16px');
  const [buttonColor, setButtonColor] = useState('#007bff');
  const [user, setUser] = useState(localStorage.getItem('token') ? 'user' : null);
  const [flaskData, setFlaskData] = useState(null);
  const [flaskError, setFlaskError] = useState(null);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedFontSize = localStorage.getItem('fontSize') || '16px';
    const savedButtonColor = localStorage.getItem('buttonColor') || '#007bff';

    setIsDarkMode(savedTheme === 'dark');
    setFontSize(savedFontSize);
    setButtonColor(savedButtonColor);

    setTimeout(() => {
      applyTheme(savedFontSize, savedButtonColor, savedTheme === 'dark');
    }, 0);

    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/test");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setFlaskData(data.message);
      } catch (error) {
        console.error("Error fetching data:", error);
        setFlaskError("Failed to fetch data from Flask. Please check the backend.");
      }
    };
    fetchData();
  }, []);

  const applyTheme = (fontSize, buttonColor, isDark) => {
    document.documentElement.style.setProperty('--app-font-size', fontSize);
    document.documentElement.style.setProperty('--button-color', buttonColor);
    document.documentElement.style.setProperty('--link-color', isDark ? '#ffffff' : '#333333');
    document.documentElement.style.setProperty('--link-hover-bg', isDark ? '#444' : '#ddd');
    document.documentElement.style.setProperty('--link-hover-color', isDark ? '#fff' : '#000');

    document.body.classList.toggle('dark-theme', isDark);
    document.body.classList.toggle('light-theme', !isDark);

    localStorage.setItem('fontSize', fontSize);
    localStorage.setItem('buttonColor', buttonColor);
  };

  const toggleDarkMode = () => {
    const newTheme = isDarkMode ? 'light' : 'dark';
    setIsDarkMode(!isDarkMode);
    localStorage.setItem('theme', newTheme);
    applyTheme(fontSize, buttonColor, !isDarkMode);
  };

  const toggleTaskbar = () => {
    setIsTaskbarVisible((prev) => !prev);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate("/login");  // Redirect to login page after logout
  };

  return (
    <div className={`app-container ${isDarkMode ? 'dark' : 'light'}`} style={{ fontSize }}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="App Logo" />
        <button onClick={toggleDarkMode} className="dark-mode-toggle-btn" aria-label="Toggle Dark Mode">
          {isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
        </button>
      </header>

      <button onClick={toggleTaskbar} className="taskbar-toggle-btn" aria-label="Toggle Taskbar">
        ☰
      </button>

      <TaskBar isDarkMode={isDarkMode} toggleTaskbar={toggleTaskbar} isVisible={isTaskbarVisible} />

      <main style={{ marginTop: '40px', padding: '20px' }}>
        {user ? (
          <div>
            <button onClick={handleLogout}>Logout</button>
            <h1>Welcome, {user}</h1>
          </div>
        ) : (
          <h1>Please log in</h1>
        )}

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<AuthForm setUser={setUser} />} />
          <Route path="/signup" element={<AuthForm setUser={setUser} />} />
          <Route path="/habit-tracker" element={<PrivateRoute element={<HabitTracker />} />} />
          <Route path="/progress" element={<PrivateRoute element={<Progress />} />} />
          <Route path="/settings" element={<PrivateRoute element={<Settings />} />} />
          <Route path="/profile" element={<PrivateRoute element={<Profile />} />} />
          <Route
            path="/test"
            element={
              <>
                {flaskError ? (
                  <p style={{ color: "red" }}>{flaskError}</p>
                ) : flaskData ? (
                  <p>{flaskData}</p>
                ) : (
                  <p>
                    <span className="spinner" /> Loading data from backend...
                  </p>
                )}
              </>
            }
          />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
