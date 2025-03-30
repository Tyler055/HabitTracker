import React from 'react';
import { Link } from 'react-router-dom';
import './styles/TaskBar.css';

const TaskBar = () => (
  <div className="taskbar">
    <nav>
      <ul>
        {["Home", "Tracker", "Settings", "Profile"].map((item) => (
          <li key={item}>
            <Link to={`/${item.toLowerCase()}`} className="taskbar-item">
              {item}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  </div>
);

export default TaskBar;
