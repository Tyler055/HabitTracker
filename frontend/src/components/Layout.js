import React from "react";
import { Link } from "react-router-dom";

const Layout = ({ children }) => {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/habits">Habits</Link>
          </li>
          <li>
            <Link to="/settings">Settings</Link>
          </li>
        </ul>
      </nav>
      <main>{children}</main>
    </div>
  );
};

export default Layout;
