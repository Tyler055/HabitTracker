import React from "react";
import { Link } from "react-router-dom";
import "./styles/TaskBar.css"; // Ensure correct path
import { FiMenu } from "react-icons/fi"; // Install via `npm install react-icons`

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
        {[
          { name: "Home", path: "/" },
          { name: "Habit Tracker", path: "/tracker" },
          { name: "Progress", path: "/progress" },
          { name: "Settings", path: "/settings" },
          { name: "Profile", path: "/profile" },
          { name: "Login / Sign Up", path: "/login" },
          { name: "Other", path: "/other" },
          { name: "Test", path: "/test" },
          { name: "Test Page", path: "/test-page" }
        ].map(({ name, path }, index) => (
          <li key={index}>
            <Link to={path} onClick={toggleTaskbar}>
              {name}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default TaskBar;
