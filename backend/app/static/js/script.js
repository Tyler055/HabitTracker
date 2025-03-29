document.addEventListener("DOMContentLoaded", function () {
    // Initialize the current theme, defaulting to 'dark'
    let currentTheme = localStorage.getItem('theme') || 'dark';

    // Elements
    const themeButton = document.getElementById('theme-toggle');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-button');
    const form = document.getElementById('form-id'); // Example form ID

    // Apply the saved theme
    document.body.classList.add(`${currentTheme}-theme`);

    // Update the theme button text based on the current theme
    function updateButtonText() {
        if (themeButton) {
            themeButton.textContent = currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        }
    }

    // Initialize the button text on page load
    if (themeButton) {
        updateButtonText();
        
        // Toggle theme function when button is clicked
        themeButton.addEventListener('click', () => {
            // Toggle between dark and light themes
            currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.body.classList.toggle('dark-theme');
            document.body.classList.toggle('light-theme');

            // Save the theme in localStorage
            localStorage.setItem('theme', currentTheme);

            // Update the button text after the theme change
            updateButtonText();
        });
    }

    // Reset button logic (reset habits and theme)
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            // Reset the theme to dark
            currentTheme = 'dark';
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', currentTheme); // Save the reset theme

            // Make an API call to reset the habits in the database
            fetch('/reset_habits', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload(); // Reload the page to reflect changes
                    } else {
                        throw new Error("Error resetting habits.");
                    }
                })
                .catch(error => {
                    alert(error.message); // Show detailed error message
                });
        });
    }

    // Form submission logic (if needed)
    if (submitButton && form) {
        submitButton.addEventListener('click', () => {
            // If this is part of a form submission, you can add validation here
            if (form.checkValidity()) {
                form.submit(); // Submit form programmatically if valid
            } else {
                alert("Please fill in all required fields correctly.");
            }
        });
    }
});
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    // all your code from inside DOMContentLoaded goes here...
  }
  resetButton.disabled = true;
resetButton.textContent = "Resetting...";
