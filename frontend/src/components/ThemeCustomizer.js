import React, { useState, useEffect } from "react";

const ThemeCustomizer = () => {
  // Define states for each color option
  const [bgColor, setBgColor] = useState("#ffffff");
  const [textColor, setTextColor] = useState("#000000");
  const [buttonColor, setButtonColor] = useState("#4CAF50");

  // Load saved theme from localStorage when the component mounts
  useEffect(() => {
    const savedBgColor = localStorage.getItem("bgColor") || "#ffffff";
    const savedTextColor = localStorage.getItem("textColor") || "#000000";
    const savedButtonColor = localStorage.getItem("buttonColor") || "#4CAF50";

    setBgColor(savedBgColor);
    setTextColor(savedTextColor);
    setButtonColor(savedButtonColor);

    // Apply saved theme to document body and buttons
    document.body.style.backgroundColor = savedBgColor;
    document.body.style.color = savedTextColor;
    const buttons = document.querySelectorAll("button");
    buttons.forEach((button) => {
      button.style.backgroundColor = savedButtonColor;
    });
  }, []);

  // Apply the selected theme to the document
  const applyTheme = () => {
    // Apply background and text color to body
    document.body.style.backgroundColor = bgColor;
    document.body.style.color = textColor;

    // Apply button color
    const buttons = document.querySelectorAll("button");
    buttons.forEach((button) => {
      button.style.backgroundColor = buttonColor;
    });

    // Save theme to localStorage
    localStorage.setItem("bgColor", bgColor);
    localStorage.setItem("textColor", textColor);
    localStorage.setItem("buttonColor", buttonColor);
  };

  return (
    <div className="container">
      <h2>Customize Your Theme</h2>

      <label htmlFor="bg-color">Background Color:</label>
      <input
        type="color"
        id="bg-color"
        value={bgColor}
        onChange={(e) => setBgColor(e.target.value)}
      />

      <label htmlFor="text-color">Text Color:</label>
      <input
        type="color"
        id="text-color"
        value={textColor}
        onChange={(e) => setTextColor(e.target.value)}
      />

      <label htmlFor="button-color">Button Color:</label>
      <input
        type="color"
        id="button-color"
        value={buttonColor}
        onChange={(e) => setButtonColor(e.target.value)}
      />

      <button id="apply-theme" onClick={applyTheme}>
        Apply Theme
      </button>
    </div>
  );
};

export default ThemeCustomizer;
