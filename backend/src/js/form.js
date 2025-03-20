// form.js

document.addEventListener('DOMContentLoaded', () => {
  const submitButton = document.getElementById('submit-button');
  const form = document.getElementById('habit-form'); // Replace with your form ID

  if (submitButton && form) {
    submitButton.addEventListener('click', (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        form.reportValidity();
      } else {
        form.submit();
      }
    });
  }
});
