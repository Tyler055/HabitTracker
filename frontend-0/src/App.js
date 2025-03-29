import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/styles.css'; // Link to your CSS
import './styles/taskbar.css';

import TaskBar from './components/TaskBar';
import ThemeCustomizer from './components/ThemeCustomizer';

import Home from './pages/Home';
import HabitTracker from './pages/HabitTracker';
import Settings from './pages/Settings';
import Profile from './pages/Profile';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Effect to apply the saved theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
      document.body.classList.add(savedTheme + '-theme');
    }
  }, []);

  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
    const newTheme = !isDarkMode ? 'dark' : 'light';
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme); // Save theme preference
  };

  return (
    <Router>
      <TaskBar />
      <div style={{ marginTop: '60px', padding: '20px' }}>
        <ThemeCustomizer toggleTheme={toggleTheme} isDarkMode={isDarkMode} />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tracker" element={<HabitTracker />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
