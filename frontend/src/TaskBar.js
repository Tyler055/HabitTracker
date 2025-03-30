import React from "react";
import { Link } from "react-router-dom";
import "./styles/TaskBar.css";

const TaskBar = ({ isDarkMode, toggleTaskbar, isVisible }) => (
  <div
    className={`taskbar ${isVisible ? "show" : ""}`}
    style={{
      backgroundColor: isDarkMode ? "#333" : "#f0f0f0",
      color: isDarkMode ? "white" : "black",
    }}
  >
    <button className="taskbar-toggle-btn" onClick={toggleTaskbar} aria-label="Toggle Taskbar">
      ☰
    </button>
    <div className="sidebar">
      <ul>
        {["Home", "Habit Tracker", "Progress", "Settings", "Profile", "Login/Sign Up"].map((text, index) => (
          <li key={index}>
            <Link to={`/${text.replace(/\s+/g, '-').toLowerCase()}`} onClick={toggleTaskbar}>
              {text}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

export default TaskBar;
