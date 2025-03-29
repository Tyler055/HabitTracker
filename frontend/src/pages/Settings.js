document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById("settings-root");

    const settingsContainer = document.createElement("div");
    const heading = document.createElement("h2");
    heading.textContent = "Settings Page";

    // Theme Toggle Section
    const themeToggleLabel = document.createElement("label");
    themeToggleLabel.textContent = "Dark Mode: ";
    const themeToggle = document.createElement("input");
    themeToggle.type = "checkbox";
    themeToggle.classList.add("theme-toggle");

    themeToggle.addEventListener("change", () => {
        if (themeToggle.checked) {
            document.body.classList.add("dark-theme");
            localStorage.setItem("theme", "dark");
        } else {
            document.body.classList.remove("dark-theme");
            localStorage.setItem("theme", "light");
        }
    });

    // Check if dark theme is previously selected
    if (localStorage.getItem("theme") === "dark") {
        themeToggle.checked = true;
        document.body.classList.add("dark-theme");
    }

    themeToggleLabel.appendChild(themeToggle);

    // Font Size Section
    const fontSizeLabel = document.createElement("label");
    fontSizeLabel.textContent = "Font Size: ";
    const fontSizeSelect = document.createElement("select");
    const fontSizeOptions = ["14px", "16px", "18px", "20px"];

    fontSizeOptions.forEach(size => {
        const option = document.createElement("option");
        option.value = size;
        option.textContent = size;
        fontSizeSelect.appendChild(option);
    });

    fontSizeSelect.addEventListener("change", () => {
        document.body.style.fontSize = fontSizeSelect.value;
        localStorage.setItem("font-size", fontSizeSelect.value);
    });

    // Set the previously selected font size from localStorage
    if (localStorage.getItem("font-size")) {
        document.body.style.fontSize = localStorage.getItem("font-size");
        fontSizeSelect.value = localStorage.getItem("font-size");
    }

    // Button Color Section
    const buttonColorLabel = document.createElement("label");
    buttonColorLabel.textContent = "Button Color: ";
    const buttonColorInput = document.createElement("input");
    buttonColorInput.type = "color";
    buttonColorInput.value = "#007bff"; // default color

    buttonColorInput.addEventListener("input", () => {
        document.documentElement.style.setProperty('--button-color', buttonColorInput.value);
        localStorage.setItem("button-color", buttonColorInput.value);
    });

    // Set the previously selected button color from localStorage
    if (localStorage.getItem("button-color")) {
        buttonColorInput.value = localStorage.getItem("button-color");
        document.documentElement.style.setProperty('--button-color', localStorage.getItem("button-color"));
    }

    // Append all settings options to the settings container
    settingsContainer.appendChild(heading);
    settingsContainer.appendChild(themeToggleLabel);
    settingsContainer.appendChild(document.createElement("br")); // for line break
    settingsContainer.appendChild(fontSizeLabel);
    settingsContainer.appendChild(fontSizeSelect);
    settingsContainer.appendChild(document.createElement("br"));
    settingsContainer.appendChild(buttonColorLabel);
    settingsContainer.appendChild(buttonColorInput);

    // Append settings container to root
    root.appendChild(settingsContainer);
});
