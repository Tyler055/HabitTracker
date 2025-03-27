import React from 'react';
import { Link } from 'react-router-dom';
import './taskbar.css'; // Link to your TaskBar CSS for styling

const TaskBar = () => {
  return (
    <div className="task-bar">
      <nav>
        <ul className="taskbar-items">
          <li className="taskbar-item">
            <Link to="/">Home</Link>
          </li>
          <li className="taskbar-item">
            <Link to="/tracker">Tracker</Link>
          </li>
          <li className="taskbar-item">
            <Link to="/settings">Settings</Link>
          </li>
          <li className="taskbar-item">
            <Link to="/profile">Profile</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default TaskBar;
