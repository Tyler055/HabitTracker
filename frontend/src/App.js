import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './styles/App.css';
import TaskBar from './TaskBar'; // Make sure TaskBar is imported
import ThemeCustomizer from './components/ThemeCustomizer'; // Make sure ThemeCustomizer is imported
import Home from './pages/Home'; // Make sure Home is imported
import HabitTracker from './components/HabitTracker'; // Make sure HabitTracker is imported
import Settings from './pages/Settings'; // Make sure Settings is imported
import Profile from './pages/Profile'; // Make sure Profile is imported


function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  const toggleTheme = () => setIsDarkMode(prevMode => !prevMode);

  return (
    <div className={`App ${isDarkMode ? 'dark' : 'light'}`}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          
        </a>
      </header>
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
    </div>
  );
}

export default App;
