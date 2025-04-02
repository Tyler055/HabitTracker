import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./styles/TaskBar.css"; // Ensure correct path
import { FiMenu } from "react-icons/fi"; // Example icon (Install via `npm install react-icons`)

const TaskBar = ({ isDarkMode }) => {
  const [isVisible, setIsVisible] = useState(false);

  // Function to toggle taskbar visibility
  const toggleTaskbar = () => {
    setIsVisible((prev) => !prev);
  };

  // Close taskbar automatically after 5 minutes
  useEffect(() => {
    let timer;
    if (isVisible) {
      timer = setTimeout(() => {
        setIsVisible(false); // Close taskbar after 5 minutes
      }, 300000); // 5 minutes in milliseconds
    }
    return () => clearTimeout(timer); // Clear timeout if taskbar is closed before 5 minutes
  }, [isVisible]);

  return (
    <div>
      {/* Button to Open Taskbar (now toggle button with icon only) */}
      <button
        className="taskbar-toggle-btn"
        onClick={toggleTaskbar}
        aria-label="Toggle Taskbar"
      >
        <FiMenu size={24} />
      </button>

      {/* Taskbar Component */}
      <nav className={`taskbar ${isVisible ? "show" : ""} ${isDarkMode ? "dark-theme" : ""}`}>
        {/* Taskbar Links */}
        <ul>
          {["Home", "Habit Tracker", "Progress", "Settings", "Profile", "Login/Sign Up", "Other", "Test", "test-page"].map(
            (text, index) => (
              <li key={index}>
                <Link
                  to={`/${text.replace(/\s+/g, "-").toLowerCase()}`}
                  onClick={toggleTaskbar} 
                >
                  {text}
                </Link>
              </li>
            )
          )}
        </ul>
      </nav>
    </div>
  );
};

export default TaskBar;
