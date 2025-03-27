import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TaskBar from './components/TaskBar'; // Taskbar for navigation
import ThemeCustomizer from './components/ThemeCustomizer'; // Theme customization component

// Import pages
import Home from './pages/Home';
import HabitTracker from './pages/HabitTracker';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Page1 from './pages/Page1';
import Page2 from './pages/Page2';
import Page3 from './pages/Page3';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Effect to load and apply the saved theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
      document.body.classList.add(savedTheme + '-theme');
    }
  }, []);

  // Toggle between dark and light mode
  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
    const newTheme = !isDarkMode ? 'dark' : 'light';
    document.body.classList.remove(isDarkMode ? 'dark-theme' : 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme);
  };

  return (
    <Router>
      {/* Task Bar (Fixed at the top) */}
      <TaskBar />

      {/* Main Content Area */}
      <div style={{ marginTop: '60px', padding: '20px' }}>
        {/* Theme Customization Section */}
        <ThemeCustomizer toggleTheme={toggleTheme} isDarkMode={isDarkMode} />

        {/* Routes for different pages */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tracker" element={<HabitTracker />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/page1" element={<Page1 />} />
          <Route path="/page2" element={<Page2 />} />
          <Route path="/page3" element={<Page3 />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
