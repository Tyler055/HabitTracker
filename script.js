document.addEventListener("DOMContentLoaded", function() {
    let currentTheme = localStorage.getItem('theme') || 'dark'; // Default to dark theme if no theme is set
    const themeButton = document.getElementById('theme-toggle');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-button');

    // Set the theme based on the current theme from localStorage
    document.body.classList.add(currentTheme + '-theme');

    // Update the button text based on the current theme
    function updateButtonText() {
        if (currentTheme === 'dark') {
            themeButton.textContent = 'Switch to Light Mode';
        } else {
            themeButton.textContent = 'Switch to Dark Mode';
        }
    }

    // Call the function initially to set the correct button text
    updateButtonText();

    // Toggle theme function when button is clicked
    if (themeButton) {
        themeButton.addEventListener('click', () => {
            if (currentTheme === 'dark') {
                currentTheme = 'light';
                document.body.classList.remove('dark-theme');
                document.body.classList.add('light-theme');
            } else {
                currentTheme = 'dark';
                document.body.classList.remove('light-theme');
                document.body.classList.add('dark-theme');
            }
            localStorage.setItem('theme', currentTheme); // Save the theme in localStorage

            // Update the button text after the theme changes
            updateButtonText();
        });
    }

    // Reset the habits and theme function
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            // Reset the theme to the base state (dark)
            currentTheme = 'dark';
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', currentTheme); // Save the reset theme

            // Make an API call to reset the habits in the database to their default values
            fetch('/reset_habits', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload(); // Reload the page to reflect changes
                    } else {
                        alert("Error resetting habits.");
                    }
                });
        });
    }

    // Submit form or text action function (if any)
    if (submitButton) {
        submitButton.addEventListener('click', () => {
            // Here, you can add the logic to submit the form or text while preserving the current theme.
            // No need to change the theme here, it stays in the current mode (light or dark).
        });
    }
});
