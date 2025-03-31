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
  const [isTaskbarVisible, setIsTaskbarVisible] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [fontSize, setFontSize] = useState("16px");
  const [buttonColor, setButtonColor] = useState("#007bff");

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "light";
    const savedFontSize = localStorage.getItem("fontSize") || "16px";
    const savedButtonColor = localStorage.getItem("buttonColor") || "#007bff";

    document.body.classList.add(`${savedTheme}-theme`);
    setIsDarkMode(savedTheme === "dark");
    setFontSize(savedFontSize);
    setButtonColor(savedButtonColor);

    applyTheme(savedFontSize, savedButtonColor, savedTheme === "dark");
  }, []);

  // Handle dark mode toggle
  const toggleDarkMode = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.body.classList.toggle("dark-theme", !isDarkMode);
    document.body.classList.toggle("light-theme", isDarkMode);
    localStorage.setItem("theme", newTheme);
    applyTheme(fontSize, buttonColor, !isDarkMode);
  };

  // Apply theme dynamically using CSS variables
  const applyTheme = (fontSize, buttonColor, isDark) => {
    document.documentElement.style.setProperty("--app-font-size", fontSize);
    document.documentElement.style.setProperty("--button-color", buttonColor);
    document.documentElement.style.setProperty("--link-color", isDark ? "#ffffff" : "#333333");
    document.documentElement.style.setProperty("--link-hover-bg", isDark ? "#444" : "#ddd");
    document.documentElement.style.setProperty("--link-hover-color", isDark ? "#fff" : "#000");

    localStorage.setItem("fontSize", fontSize);
    localStorage.setItem("buttonColor", buttonColor);
  };

  // Handle taskbar visibility toggle
  const toggleTaskbar = () => {
    setIsTaskbarVisible((prevState) => !prevState);
  };

  return (
    <div className={`app-container ${isDarkMode ? "dark" : "light"}`} style={{ fontSize }}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="App Logo" />
        <button
          onClick={toggleDarkMode}
          className="dark-mode-toggle-btn"
          aria-label="Toggle Dark Mode"
        >
          {isDarkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>
      </header>

      <button
        onClick={toggleTaskbar}
        className="taskbar-toggle-btn"
        aria-label="Toggle Taskbar"
      >
        
      </button>

      <TaskBar isDarkMode={isDarkMode} toggleTaskbar={toggleTaskbar} isVisible={isTaskbarVisible} />

      <main style={{ marginTop: "60px", padding: "20px" }}>
        <Routes>
          <Route path="/home" element={<Home />} />
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
