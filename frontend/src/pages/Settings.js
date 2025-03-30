import React, { useEffect, useState } from 'react';

const Settings = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [fontSize, setFontSize] = useState('16px');
  const [buttonColor, setButtonColor] = useState('#007bff');

  // Load settings from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const savedFontSize = localStorage.getItem('font-size');
    const savedButtonColor = localStorage.getItem('button-color');

    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.body.classList.add('dark-theme');
    }

    if (savedFontSize) {
      setFontSize(savedFontSize);
      document.body.style.fontSize = savedFontSize;
    }

    if (savedButtonColor) {
      setButtonColor(savedButtonColor);
      document.documentElement.style.setProperty('--button-color', savedButtonColor);
    }
  }, []);

  // Handle theme toggle
  const handleThemeToggle = () => {
    setIsDarkMode((prevState) => {
      const newState = !prevState;
      if (newState) {
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
      } else {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
      }
      return newState;
    });
  };

  // Handle font size change
  const handleFontSizeChange = (event) => {
    const newFontSize = event.target.value;
    setFontSize(newFontSize);
    document.body.style.fontSize = newFontSize;
    localStorage.setItem('font-size', newFontSize);
  };

  // Handle button color change
  const handleButtonColorChange = (event) => {
    const newButtonColor = event.target.value;
    setButtonColor(newButtonColor);
    document.documentElement.style.setProperty('--button-color', newButtonColor);
    localStorage.setItem('button-color', newButtonColor);
  };

  // Reset to default theme
  const resetTheme = () => {
    document.body.classList.remove('dark-theme');
    localStorage.removeItem('theme');
    setIsDarkMode(false);
    document.body.style.fontSize = '16px';
    localStorage.setItem('font-size', '16px');
    setFontSize('16px');
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>

      {/* Dark Mode Toggle */}
      <div className="setting-item">
        <label htmlFor="theme-toggle">Dark Mode: </label>
        <input
          type="checkbox"
          id="theme-toggle"
          checked={isDarkMode}
          onChange={handleThemeToggle}
        />
        <span>{isDarkMode ? 'Light' : 'Dark'}</span> {/* Dynamically update text */}
      </div>

      {/* Font Size Selector */}
      <div className="setting-item">
        <label htmlFor="font-size">Font Size: </label>
        <select id="font-size" value={fontSize} onChange={handleFontSizeChange}>
          <option value="14px">14px</option>
          <option value="16px">16px</option>
          <option value="18px">18px</option>
          <option value="20px">20px</option>
        </select>
      </div>

      {/* Button Color Picker */}
      <div className="setting-item">
        <label htmlFor="button-color">Button Color: </label>
        <input
          type="color"
          id="button-color"
          value={buttonColor}
          onChange={handleButtonColorChange}
        />
      </div>

      {/* Reset Theme Button */}
      <button onClick={resetTheme} className="reset-theme-btn">
        Reset Current Theme
      </button>
    </div>
  );
};

export default Settings;
