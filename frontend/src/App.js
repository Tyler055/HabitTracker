import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './styles/App.css';
import TaskBar from './TaskBar';
import ThemeCustomizer from './components/ThemeCustomizer';
import Home from './pages/Home';
import HabitTracker from './components/HabitTracker';
import Settings from './pages/Settings';
import Profile from './pages/Profile';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "light";
    setIsDarkMode(savedTheme === "dark");
    document.body.classList.add(`${savedTheme}-theme`);
  }, []);

  // Toggle theme function
  const toggleTheme = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.body.classList.remove(isDarkMode ? "dark-theme" : "light-theme");
    document.body.classList.add(`${newTheme}-theme`);
    localStorage.setItem("theme", newTheme);
  };

  return (
    <div className={`App ${isDarkMode ? 'dark' : 'light'}`}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>
      
      <TaskBar />
      
      <main style={{ marginTop: '60px', padding: '20px' }}>
        <ThemeCustomizer toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tracker" element={<HabitTracker />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
