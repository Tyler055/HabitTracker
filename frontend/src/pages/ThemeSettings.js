import React, { useState, useEffect, useCallback } from 'react';
import '../styles/styles.css'; // Import your CSS file for styling

const ThemeSettings = () => {
  const [fontSize, setFontSize] = useState('16px');
  const [buttonColor, setButtonColor] = useState('#007bff');
  const [bgColor, setBgColor] = useState('#ffffff');
  const [textColor, setTextColor] = useState('#000000');
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Apply the theme to the document
  const applyTheme = useCallback(() => {
    const currentBgColor = isDarkMode ? '#333333' : bgColor;
    const currentTextColor = isDarkMode ? '#ffffff' : textColor;
    const currentButtonColor = buttonColor;

    // Apply styles to the document body
    document.documentElement.style.setProperty('--bg-color', currentBgColor);
    document.documentElement.style.setProperty('--text-color', currentTextColor);
    document.documentElement.style.setProperty('--button-color', currentButtonColor);

    document.body.style.backgroundColor = currentBgColor;
    document.body.style.color = currentTextColor;
    document.querySelectorAll('button').forEach((btn) => {
      btn.style.backgroundColor = currentButtonColor;
    });

    // Apply dark or light theme class to body
    if (isDarkMode) {
      document.body.classList.add('dark-theme');
      document.body.classList.remove('light-theme');
    } else {
      document.body.classList.add('light-theme');
      document.body.classList.remove('dark-theme');
    }

    // Store settings in localStorage
    localStorage.setItem('bgColor', currentBgColor);
    localStorage.setItem('textColor', currentTextColor);
    localStorage.setItem('buttonColor', currentButtonColor);
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode, bgColor, textColor, buttonColor]);

  // Load settings from localStorage when the component mounts
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const savedFontSize = localStorage.getItem('font-size');
    const savedButtonColor = localStorage.getItem('button-color');
    const savedBgColor = localStorage.getItem('bgColor') || '#ffffff';
    const savedTextColor = localStorage.getItem('textColor') || '#000000';

    if (savedTheme === 'dark') {
      setIsDarkMode(true); // Set dark mode if saved in localStorage
    } else {
      setIsDarkMode(false); // Default to light theme
    }

    if (savedFontSize) {
      setFontSize(savedFontSize);
      document.body.style.fontSize = savedFontSize;
    }

    if (savedButtonColor) {
      setButtonColor(savedButtonColor);
    }

    setBgColor(savedBgColor);
    setTextColor(savedTextColor);

    applyTheme(); // Apply the saved theme on mount
  }, [applyTheme]);

  const handleFontSizeChange = (event) => {
    const newFontSize = event.target.value;
    setFontSize(newFontSize);
    document.body.style.fontSize = newFontSize;
    localStorage.setItem('font-size', newFontSize);
  };

  const handleButtonColorChange = (event) => {
    const newButtonColor = event.target.value;
    setButtonColor(newButtonColor);
    localStorage.setItem('button-color', newButtonColor);
  };

  const handleBgColorChange = (event) => {
    const newBgColor = event.target.value;
    setBgColor(newBgColor);
  };

  const handleTextColorChange = (event) => {
    const newTextColor = event.target.value;
    setTextColor(newTextColor);
  };

  const resetTheme = () => {
    localStorage.removeItem('theme');
    localStorage.removeItem('bgColor');
    localStorage.removeItem('textColor');
    localStorage.removeItem('buttonColor');
    localStorage.removeItem('font-size');

    setFontSize('16px');
    setBgColor('#ffffff');
    setTextColor('#000000');
    setButtonColor('#007bff');
    setIsDarkMode(false); // Reset to light theme
    applyTheme(); // Reset to default theme
  };

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>

      {/* Dark/Light Theme Toggle */}
      <div className="setting-item">
        <label htmlFor="theme-toggle" className="switch">
          <input
            type="checkbox"
            id="theme-toggle"
            checked={isDarkMode}
            onChange={toggleDarkMode}
          />
          <span className="slider"></span>
        </label>
        <span>{isDarkMode ? 'Dark' : 'Light'}</span>
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

      {/* Background Color Picker */}
      <div className="setting-item">
        <label htmlFor="bg-color">Background Color: </label>
        <input
          type="color"
          id="bg-color"
          value={bgColor}
          onChange={handleBgColorChange}
        />
      </div>

      {/* Text Color Picker */}
      <div className="setting-item">
        <label htmlFor="text-color">Text Color: </label>
        <input
          type="color"
          id="text-color"
          value={textColor}
          onChange={handleTextColorChange}
        />
      </div>

      {/* Apply Changes */}
      <button onClick={applyTheme} className="apply-btn">
        Apply
      </button>

      {/* Reset to Default Theme */}
      <button onClick={resetTheme} className="reset-theme-btn">
        Reset Current Theme
      </button>
    </div>
  );
};

export default ThemeSettings; // Ensure you export ThemeSettings correctly
