document.addEventListener("DOMContentLoaded", function () {
  initApp(); // Initialize once the DOM is loaded
});

function initApp() {
  applySavedTheme();
  setupThemeToggle();
  setupResetButton();
  setupFormSubmission();
}

// Function to apply the saved theme from localStorage
function applySavedTheme() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.body.classList.add(`${savedTheme}-theme`);
}

// Function to toggle between light and dark themes
function setupThemeToggle() {
  const themeButton = document.getElementById('theme-toggle');
  if (themeButton) {
    let currentTheme = localStorage.getItem('theme') || 'dark';
    updateButtonText(themeButton, currentTheme);

    themeButton.addEventListener('click', () => {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.body.classList.toggle('dark-theme');
      document.body.classList.toggle('light-theme');
      localStorage.setItem('theme', currentTheme);
      updateButtonText(themeButton, currentTheme);
    });
  }
}

// Function to update the theme toggle button's text
function updateButtonText(button, currentTheme) {
  button.textContent = currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
}

// Function to handle reset button logic
function setupResetButton() {
  const resetButton = document.getElementById('reset-button');
  if (resetButton) {
    resetButton.addEventListener('click', () => {
      resetButton.disabled = true;
      resetButton.textContent = "Resetting...";

      // Reset to dark theme
      resetThemeToDark();

      // Reset habits by making a POST request
      resetHabits()
        .then(() => window.location.reload())
        .catch(error => alert(error.message))
        .finally(() => {
          resetButton.disabled = false;
          resetButton.textContent = "Reset Habits";
        });
    });
  }
}

// Function to reset the theme to dark mode
function resetThemeToDark() {
  document.body.classList.remove('light-theme');
  document.body.classList.add('dark-theme');
  localStorage.setItem('theme', 'dark');
}

// Function to reset habits via a backend request
function resetHabits() {
  return fetch('/reset_habits', { method: 'POST' })
    .then(response => {
      if (!response.ok) {
        throw new Error("Error resetting habits.");
      }
    });
}

// Function to handle form submission
function setupFormSubmission() {
  const submitButton = document.getElementById('submit-button');
  const form = document.getElementById('form-id');

  if (submitButton && form) {
    submitButton.addEventListener('click', () => {
      if (form.checkValidity()) {
        form.submit();
      } else {
        alert("Please fill in all required fields correctly.");
      }
    });
  }
}
