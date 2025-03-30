import React, { useState, useEffect } from 'react';

const ThemeSettings = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [fontSize, setFontSize] = useState('16px');
  const [buttonColor, setButtonColor] = useState('#007bff');
  const [bgColor, setBgColor] = useState('#ffffff');
  const [textColor, setTextColor] = useState('#000000');

  const applyTheme = React.useCallback((bg = bgColor, text = textColor, button = buttonColor) => {
    document.body.style.backgroundColor = bg;
    document.body.style.color = text;
    document.querySelectorAll("button").forEach((btn) => {
      btn.style.backgroundColor = button;
    });

    // Save to localStorage for persistence
    localStorage.setItem('bgColor', bg);
    localStorage.setItem('textColor', text);
    localStorage.setItem('buttonColor', button);
  }, [bgColor, textColor, buttonColor]);

  // Load settings from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const savedFontSize = localStorage.getItem('font-size');
    const savedButtonColor = localStorage.getItem('button-color');
    const savedBgColor = localStorage.getItem('bgColor') || '#ffffff';
    const savedTextColor = localStorage.getItem('textColor') || '#000000';

    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }

    if (savedFontSize) {
      setFontSize(savedFontSize);
      document.body.style.fontSize = savedFontSize;
    }

    if (savedButtonColor) {
      setButtonColor(savedButtonColor);
      document.documentElement.style.setProperty('--button-color', savedButtonColor);
    }

    setBgColor(savedBgColor);
    setTextColor(savedTextColor);
    applyTheme(savedBgColor, savedTextColor, savedButtonColor);
  }, [applyTheme]);

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

  // Handle background color change
  const handleBgColorChange = (event) => {
    const newBgColor = event.target.value;
    setBgColor(newBgColor);
    applyTheme(newBgColor, textColor, buttonColor);
  };

  // Handle text color change
  const handleTextColorChange = (event) => {
    const newTextColor = event.target.value;
    setTextColor(newTextColor);
    applyTheme(bgColor, newTextColor, buttonColor);
  };

  // Reset to default settings
  const resetTheme = () => {
    document.body.classList.remove('dark-theme');
    localStorage.removeItem('theme');
    setIsDarkMode(false);
    document.body.style.fontSize = '16px';
    localStorage.setItem('font-size', '16px');
    setFontSize('16px');
    setBgColor('#ffffff');
    setTextColor('#000000');
    setButtonColor('#007bff');
    applyTheme('#ffffff', '#000000', '#007bff');
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
        <span>{isDarkMode ? 'Light' : 'Dark'}</span>
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

      {/* Reset Theme Button */}
      <button onClick={resetTheme} className="reset-theme-btn">
        Reset Current Theme
      </button>
    </div>
  );
};

export default ThemeSettings;
