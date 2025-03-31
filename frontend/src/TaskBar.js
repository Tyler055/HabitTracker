import React from "react";
import { Link } from "react-router-dom";
import "./styles/TaskBar.css"; // Ensure correct path


const TaskBar = ({ isDarkMode, toggleTaskbar, isVisible }) => {
  return (
    <nav className={`taskbar ${isVisible ? "show" : ""}`}>
      {/* Taskbar Toggle Button */}
      <button
        className="taskbar-toggle-btn"
        onClick={toggleTaskbar}
        aria-label="Toggle Taskbar"
      >
        
      </button>

      {/* Taskbar Links */}
      <ul>
        {["Home", "Habit Tracker", "Progress", "Settings", "Profile", "Login/Sign Up","other"].map(
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
