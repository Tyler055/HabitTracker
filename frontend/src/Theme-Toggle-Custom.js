document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const resetButton = document.getElementById("reset-theme");
    const root = document.documentElement;

    function applyTheme(settings) {
        for (let key in settings) {
            if (settings[key] !== null) {
                root.style.setProperty(`--${key}`, settings[key]);
            }
        }
    }

    function getStoredTheme() {
        return JSON.parse(localStorage.getItem("customTheme")) || {};
    }

    function saveTheme(settings) {
        localStorage.setItem("customTheme", JSON.stringify(settings));
    }

    function resetTheme() {
        localStorage.removeItem("customTheme");
        applyTheme(defaultTheme());
    }

    function defaultTheme() {
        return themeToggle.checked ? darkTheme() : lightTheme();
    }

    function darkTheme() {
        return {
            "bg-color": "#333",
            "text-color": "#f5f5f5",
            "button-color": "#444",
            "input-bg": "#222",
            "input-text": "#fff"
        };
    }

    function lightTheme() {
        return {
            "bg-color": "#f5f5f5",
            "text-color": "#333",
            "button-color": "#007BFF",
            "input-bg": "#fff",
            "input-text": "#000"
        };
    }

    themeToggle.addEventListener("change", function () {
        const storedTheme = getStoredTheme();
        const newTheme = themeToggle.checked ? darkTheme() : lightTheme();

        // Preserve user custom styles unless they conflict with dark mode rules
        for (let key in storedTheme) {
            if (key !== "input-bg" && key !== "input-text") {
                newTheme[key] = storedTheme[key];
            }
        }

        applyTheme(newTheme);
        saveTheme(newTheme);
    });

    resetButton.addEventListener("click", resetTheme);

    applyTheme(getStoredTheme() || defaultTheme());
});
