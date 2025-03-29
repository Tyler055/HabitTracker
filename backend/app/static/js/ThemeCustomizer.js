import React, { useState, useEffect } from "react";

const ThemeCustomizer = () => {
  const [bgColor, setBgColor] = useState("#ffffff");
  const [textColor, setTextColor] = useState("#000000");
  const [buttonColor, setButtonColor] = useState("#4CAF50");

  // Load saved theme from localStorage
  useEffect(() => {
    const savedBgColor = localStorage.getItem("bgColor") || "#ffffff";
    const savedTextColor = localStorage.getItem("textColor") || "#000000";
    const savedButtonColor = localStorage.getItem("buttonColor") || "#4CAF50";

    setBgColor(savedBgColor);
    setTextColor(savedTextColor);
    setButtonColor(savedButtonColor);

    applyTheme(savedBgColor, savedTextColor, savedButtonColor);
  }, []);

  // Apply theme settings to the page
  const applyTheme = (bg = bgColor, text = textColor, button = buttonColor) => {
    document.body.style.backgroundColor = bg;
    document.body.style.color = text;
    document.querySelectorAll("button").forEach((btn) => {
      btn.style.backgroundColor = button;
    });

    // Save to localStorage for persistence
    localStorage.setItem("bgColor", bg);
    localStorage.setItem("textColor", text);
    localStorage.setItem("buttonColor", button);
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

      <button id="apply-theme" onClick={() => applyTheme()}>
        Apply Theme
      </button>
    </div>
  );
};

export default ThemeCustomizer;
