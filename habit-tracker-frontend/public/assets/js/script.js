document.addEventListener("DOMContentLoaded", function () {
    init(); // Initialize once the DOM is loaded
  });
  
  function init() {
    let currentTheme = localStorage.getItem('theme') || 'dark';
  
    const themeButton = document.getElementById('theme-toggle');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-button');
    const form = document.getElementById('form-id');
  
    // Apply the saved theme
    document.body.classList.add(`${currentTheme}-theme`);
  
    // Update the theme button text
    if (themeButton) {
      updateButtonText();
      themeButton.addEventListener('click', () => {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.classList.toggle('dark-theme');
        document.body.classList.toggle('light-theme');
        localStorage.setItem('theme', currentTheme);
        updateButtonText();
      });
    }
  
    function updateButtonText() {
      if (themeButton) {
        themeButton.textContent = currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
      }
    }
  
    // Reset button logic
    if (resetButton) {
      resetButton.addEventListener('click', () => {
        resetButton.disabled = true;
        resetButton.textContent = "Resetting...";
  
        currentTheme = 'dark';
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme', currentTheme);
  
        fetch('/reset_habits', { method: 'POST' })
          .then(response => {
            if (response.ok) {
              window.location.reload();
            } else {
              throw new Error("Error resetting habits.");
            }
          })
          .catch(error => {
            alert(error.message);
          })
          .finally(() => {
            resetButton.disabled = false;
            resetButton.textContent = "Reset Habits";
          });
      });
    }
  
    // Form submission logic
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
  