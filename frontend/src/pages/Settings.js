import React, { useState, useEffect } from "react";
import "../styles/styles.css";

const Settings = () => {
  const defaultSettings = React.useMemo(() => ({
    fontSize: "16px",
    buttonColor: "#ff4d4d", // Updated button color
    bgColor: "#ffffff",
    textColor: "#000000",
  }), []);

  const [pendingSettings, setPendingSettings] = useState(defaultSettings);
  // Removed unused appliedSettings state

  // Load settings from localStorage on component mount
  useEffect(() => {
    const savedSettings = {
      fontSize: localStorage.getItem("fontSize") || defaultSettings.fontSize,
      buttonColor: localStorage.getItem("buttonColor") || defaultSettings.buttonColor,
      bgColor: localStorage.getItem("bgColor") || defaultSettings.bgColor,
      textColor: localStorage.getItem("textColor") || defaultSettings.textColor,
    };

    // Removed setAppliedSettings as it is not used
    applyTheme(savedSettings);
  }, [defaultSettings]);

  // Apply theme settings to localStorage and document properties
  const applyTheme = (settings) => {
    Object.keys(settings).forEach((key) => localStorage.setItem(key, settings[key]));

    document.documentElement.style.setProperty("--bg-color", settings.bgColor);
    document.documentElement.style.setProperty("--text-color", settings.textColor);
    document.documentElement.style.setProperty("--button-color", settings.buttonColor);
    document.documentElement.style.setProperty("--font-size", settings.fontSize);
  };

  // Handle input changes and update pending settings
  const handleInputChange = (event) => {
    const { id, value } = event.target;
    setPendingSettings((prev) => ({ ...prev, [id]: value }));
  };

  // Apply the pending settings
  const handleApply = () => {
    // Removed setAppliedSettings as it is not used
    applyTheme(pendingSettings);
  };

  // Reset settings to default
  const resetTheme = () => {
    setPendingSettings(defaultSettings);
    // Removed setAppliedSettings as it is not used
    applyTheme(defaultSettings);
  };
  return (
    <div className="settings-container">
      <h2 className="settings-title">Settings</h2>

      {/* Font Size Selector */}
      <div className="setting-item">
        <label htmlFor="fontSize">Font Size:</label>
        <select id="fontSize" value={pendingSettings.fontSize} onChange={handleInputChange}>
          <option value="14px">14px</option>
          <option value="16px">16px</option>
          <option value="18px">18px</option>
          <option value="20px">20px</option>
        </select>
      </div>

      {/* Color Settings */}
      <div className="color-settings">
        <div className="setting-item">
          <label htmlFor="bgColor">Background Color:</label>
          <input type="color" id="bgColor" value={pendingSettings.bgColor} onChange={handleInputChange} />
        </div>

        <div className="setting-item">
          <label htmlFor="textColor">Text Color:</label>
          <input type="color" id="textColor" value={pendingSettings.textColor} onChange={handleInputChange} />
        </div>
      </div>

      {/* Buttons */}
      <button onClick={handleApply} className="apply-btn">Apply Theme</button>
      <div className="button-group">
        <button onClick={resetTheme} className="reset-btn">Reset Theme</button>
      </div>
    </div>
  );
};

export default Settings;
