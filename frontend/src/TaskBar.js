import React from 'react';
import { Link } from 'react-router-dom';
import './styles/TaskBar.css';

const TaskBar = () => {
  return (
    <div className="taskbar">
      <nav>
        <ul>
          <li><Link to="/" className="taskbar-item">Home</Link></li>
          <li><Link to="/tracker" className="taskbar-item">Habit Tracker</Link></li>
          <li><Link to="/settings" className="taskbar-item">Settings</Link></li>
          <li><Link to="/profile" className="taskbar-item">Profile</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default TaskBar;
