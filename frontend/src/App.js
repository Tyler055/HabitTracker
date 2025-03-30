import React, { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import logo from "./logo.svg";
import "./styles/App.css";
import "./styles/styles.css";
import TaskBar from "./TaskBar";
import Home from "./pages/Home";
import HabitTracker from "./components/HabitTracker";
import Progress from "./pages/Progress";
import Settings from "./pages/ThemeSettings";
import Profile from "./pages/Profile";

const App = () => {
  const [isTaskbarVisible, setIsTaskbarVisible] = useState(false); // State for taskbar visibility

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "light"; // Default to "light" if no saved theme
    document.body.classList.add(`${savedTheme}-theme`); // Apply saved theme class to body
  }, []);

  // Handle taskbar visibility toggle
  const toggleTaskbarVisibility = () => {
    setIsTaskbarVisible(prev => !prev);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="App Logo" />
      </header>

      {/* Taskbar Toggle Button */}
      <button
        onClick={toggleTaskbarVisibility}
        className="taskbar-toggle-btn"
        aria-label="Toggle Taskbar"
      >
        ☰
      </button>

      {/* TaskBar Component */}
      <TaskBar
        isVisible={isTaskbarVisible}
        toggleTaskbar={toggleTaskbarVisibility}
      />

      <main style={{ marginTop: "60px", padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/habit-tracker" element={<HabitTracker />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
