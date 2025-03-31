import React, { useState, useEffect, useCallback } from "react";
import "../styles/styles.css";

const ThemeSettings = () => {
  const [fontSize, setFontSize] = useState("16px");
  const [buttonColor, setButtonColor] = useState("#007bff");
  const [bgColor, setBgColor] = useState("#ffffff");
  const [textColor, setTextColor] = useState("#000000");
  const [isDarkMode, setIsDarkMode] = useState(false);
  // Removed unused taskbarVisible state

  // Apply theme dynamically using CSS variables
  const applyTheme = useCallback(() => {
    const currentBgColor = isDarkMode ? "#333333" : bgColor;
    const currentTextColor = isDarkMode ? "#ffffff" : textColor;
    const currentButtonColor = buttonColor;

    document.documentElement.style.setProperty("--bg-color", currentBgColor);
    document.documentElement.style.setProperty("--text-color", currentTextColor);
    document.documentElement.style.setProperty("--button-color", currentButtonColor);
    document.documentElement.style.setProperty("--font-size", fontSize);

    document.body.style.backgroundColor = currentBgColor;
    document.body.style.color = currentTextColor;
    document.body.style.fontSize = fontSize;
    document.querySelectorAll("button").forEach((btn) => {
      btn.style.backgroundColor = currentButtonColor;
    });

    if (isDarkMode) {
      document.body.classList.add("dark-theme");
      document.body.classList.remove("light-theme");
    } else {
      document.body.classList.add("light-theme");
      document.body.classList.remove("dark-theme");
    }

    localStorage.setItem("bgColor", currentBgColor);
    localStorage.setItem("textColor", currentTextColor);
    localStorage.setItem("buttonColor", currentButtonColor);
    localStorage.setItem("font-size", fontSize);
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
  }, [isDarkMode, bgColor, textColor, buttonColor, fontSize]);

  // Load saved settings from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    const savedFontSize = localStorage.getItem("font-size");
    const savedButtonColor = localStorage.getItem("button-color");
    const savedBgColor = localStorage.getItem("bgColor") || "#ffffff";
    const savedTextColor = localStorage.getItem("textColor") || "#000000";
    // Removed unused taskbar visibility logic

    if (savedTheme === "dark") {
      setIsDarkMode(true);
    } else {
      setIsDarkMode(false);
    }

    if (savedFontSize) {
      setFontSize(savedFontSize);
    }

    if (savedButtonColor) {
      setButtonColor(savedButtonColor);
    }

    setBgColor(savedBgColor);
    setTextColor(savedTextColor);
    // Removed unused taskbar visibility setter

    applyTheme(); // Apply saved settings when component mounts
  }, [applyTheme]);

  // Handle user input changes
  const handleFontSizeChange = (event) => {
    const newFontSize = event.target.value;
    setFontSize(newFontSize);
    document.body.style.fontSize = newFontSize; // Apply immediately
    localStorage.setItem("font-size", newFontSize);
  };

  const handleButtonColorChange = (event) => {
    const newButtonColor = event.target.value;
    setButtonColor(newButtonColor);
    localStorage.setItem("button-color", newButtonColor);
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
    localStorage.removeItem("theme");
    localStorage.removeItem("bgColor");
    localStorage.removeItem("textColor");
    localStorage.removeItem("buttonColor");
    localStorage.removeItem("font-size");
    localStorage.removeItem("taskbarVisible");

    setFontSize("16px");
    setBgColor("#ffffff");
    setTextColor("#000000");
    setButtonColor("#007bff");
    setIsDarkMode(false);
    applyTheme();
  };

  // Removed unused toggleDarkMode function

  // Removed unused toggleTaskbar function

  return (
    <div className="settings-container">
      <h2>Settings</h2>

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

      {/* Reset Theme */}
      <button onClick={resetTheme} className="reset-btn">Reset Theme</button>

      

    
      {/* Apply Changes */}
      <button onClick={applyTheme} className="apply-btn">Apply</button>
    </div>
  );
};

export default ThemeSettings;
