import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './styles/TaskBar.css';

const TaskBar = ({ isVisible, toggleTaskbar }) => {
  const taskbarTimeout = useRef(null);

  // Auto-hide after 5 minutes
  useEffect(() => {
    if (isVisible) {
      taskbarTimeout.current = setTimeout(() => {
        toggleTaskbar(); // Hide taskbar
      }, 300000); // 5 minutes
    }
    return () => clearTimeout(taskbarTimeout.current); // Cleanup on unmount
  }, [isVisible, toggleTaskbar]);

  return (
    <div className={`taskbar ${isVisible ? 'show' : ''}`}>
      <button id="toggle-btn" onClick={toggleTaskbar}>
        ☰
      </button>
      <div className="sidebar">
        <ul>
          <li><Link to="/" onClick={toggleTaskbar}>Home</Link></li>
          <li><Link to="/habit-list" onClick={toggleTaskbar}>Habits</Link></li>
          <li><Link to="/progress" onClick={toggleTaskbar}>Progress</Link></li>
          <li><Link to="/settings" onClick={toggleTaskbar}>Settings</Link></li>
          <li><Link to="/profile" onClick={toggleTaskbar}>Profile</Link></li>
          <li><Link to="/login-signup" onClick={toggleTaskbar}>Login/Sign Up</Link></li>
        </ul>
      </div>
    </div>
  );
};

export default TaskBar;
