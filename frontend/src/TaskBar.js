import React from "react";
import { Link } from "react-router-dom";
import "./styles/TaskBar.css"; // Ensure correct path
import { FiMenu } from "react-icons/fi"; // Example icon (Install via `npm install react-icons`)

const TaskBar = ({ isDarkMode, toggleTaskbar, isVisible }) => {
  return (
    <nav className={`taskbar ${isVisible ? "show" : ""} ${isDarkMode ? "dark-mode" : ""}`}>
      {/* Taskbar Toggle Button */}
      <button
        className="taskbar-toggle-btn"
        onClick={toggleTaskbar}
        aria-label="Toggle Taskbar"
      >
        <FiMenu size={24} />
      </button>

      {/* Taskbar Links */}
      <ul>
        {["Home", "Habit Tracker", "Progress", "Settings", "Profile", "Login/Sign Up", "Other", "Test", "test-page"].map(
          (text, index) => (
            <li key={index}>
              <Link to={`/${text.replace(/\s+/g, "-").toLowerCase()}`} onClick={toggleTaskbar}>
                {text}
              </Link>
            </li>
          )
        )}
      </ul>
    </nav>
  );
};

export default TaskBar;
