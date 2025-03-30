import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import logo from "./logo.svg";
import "./styles/App.css";
import TaskBar from "./TaskBar";
import Home from "./pages/Home";
import HabitTracker from "./components/HabitTracker";
import Progress from "./pages/Progress";
import { Settings } from './pages/Settings';
import Profile from "./pages/Profile";

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isTaskbarVisible, setIsTaskbarVisible] = useState(false);

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "light";
    setIsDarkMode(savedTheme === "dark");
    document.body.classList.add(`${savedTheme}-theme`);
  }, []);

  // Toggle theme function
  const toggleTheme = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.body.classList.remove(isDarkMode ? "dark-theme" : "light-theme");
    document.body.classList.add(`${newTheme}-theme`);
    localStorage.setItem("theme", newTheme);
  };

  // Handle taskbar visibility toggle
  const toggleTaskbarVisibility = () => {
    setIsTaskbarVisible(!isTaskbarVisible);
  };

  return (
    <div className={`App ${isDarkMode ? "dark" : "light"}`}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="App Logo" />
      </header>

      <button onClick={toggleTaskbarVisibility} className="taskbar-toggle-btn">
        ☰
      </button>

      <TaskBar isVisible={isTaskbarVisible} toggleTaskbar={toggleTaskbarVisibility} />

      <main style={{ marginTop: "60px", padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Home />} /> {/* Home page as the default route */}
          <Route path="/habit-tracker" element={<HabitTracker />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/settings" element={<Settings toggleTheme={toggleTheme} isDarkMode={isDarkMode} />} />
          <Route path="/profile" element={<Profile />} />
          {/* Default Route */}
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
