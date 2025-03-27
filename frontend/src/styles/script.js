document.addEventListener("DOMContentLoaded", function () {
  init();
});

function init() {
  let currentTheme = localStorage.getItem('theme') || 'dark';

  const themeButton = document.getElementById('theme-toggle');
  const resetButton = document.getElementById('reset-button');
  const submitButton = document.getElementById('submit-button');
  const form = document.getElementById('form-id');
  const addHabitBtn = document.getElementById("add-habit-btn");

  // Apply saved theme
  document.body.classList.add(`${currentTheme}-theme`);

  if (themeButton) {
      updateButtonText();
      themeButton.addEventListener('click', toggleTheme);
  }

  if (resetButton) {
      resetButton.addEventListener('click', resetHabits);
  }

  if (submitButton && form) {
      submitButton.addEventListener('click', submitForm);
  }

  if (addHabitBtn) {
      addHabitBtn.addEventListener("click", addHabit);
  }

  function toggleTheme() {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.body.classList.toggle('dark-theme');
      document.body.classList.toggle('light-theme');
      localStorage.setItem('theme', currentTheme);
      updateButtonText();
  }

  function updateButtonText() {
      if (themeButton) {
          themeButton.textContent = currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
      }
  }

  async function resetHabits() {
      resetButton.disabled = true;
      resetButton.textContent = "Resetting...";

      currentTheme = 'dark';
      document.body.classList.remove('light-theme');
      document.body.classList.add('dark-theme');
      localStorage.setItem('theme', currentTheme);

      try {
          const response = await fetch('/reset_habits', { method: 'POST' });
          if (response.ok) {
              alert("Habits reset successfully!");
              location.reload();
          } else {
              throw new Error("Error resetting habits.");
          }
      } catch (error) {
          alert(error.message);
      } finally {
          resetButton.disabled = false;
          resetButton.textContent = "Reset Habits";
      }
  }

  function submitForm() {
      if (form.checkValidity()) {
          form.submit();
      } else {
          alert("Please fill in all required fields correctly.");
      }
  }

  async function addHabit() {
      const habitName = prompt("Enter the habit name:");
      if (!habitName) return;

      try {
          const response = await fetch("/api/add-habit", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({ name: habitName })
          });

          const data = await response.json();
          if (response.ok) {
              alert("Habit added successfully!");
              // Dynamically update UI instead of reloading
              const habitList = document.getElementById("habit-list"); // Assuming you have a list element
              if (habitList) {
                  const newHabit = document.createElement("li");
                  newHabit.textContent = habitName;
                  habitList.appendChild(newHabit);
              }
          } else {
              alert("Error adding habit: " + data.error);
          }
      } catch (error) {
          console.error("Error:", error);
          alert("Failed to connect to the server.");
      }
  }
}
document.addEventListener("DOMContentLoaded", () => {
    const bgColorInput = document.getElementById("bg-color");
    const textColorInput = document.getElementById("text-color");
    const buttonColorInput = document.getElementById("button-color");
    const applyThemeBtn = document.getElementById("apply-theme");
    const resetButton = document.getElementById("reset-button");

    // Load stored theme from localStorage
    const storedBg = localStorage.getItem("bgColor");
    const storedText = localStorage.getItem("textColor");
    const storedBtn = localStorage.getItem("buttonColor");

    if (storedBg) document.body.style.backgroundColor = storedBg;
    if (storedText) document.body.style.color = storedText;
    if (storedBtn) document.documentElement.style.setProperty('--button-color', storedBtn);

    // Apply theme on button click
    applyThemeBtn.addEventListener("click", () => {
        const bgColor = bgColorInput.value;
        const textColor = textColorInput.value;
        const buttonColor = buttonColorInput.value;

        document.body.style.backgroundColor = bgColor;
        document.body.style.color = textColor;
        document.documentElement.style.setProperty('--button-color', buttonColor);

        localStorage.setItem("bgColor", bgColor);
        localStorage.setItem("textColor", textColor);
        localStorage.setItem("buttonColor", buttonColor);
    });

    // Reset habits button click
    resetButton.addEventListener("click", async () => {
        try {
            await fetch("http://127.0.0.1:5000/api/reset-habits", { method: "POST" });
            alert("Habits reset successfully!");
        } catch (error) {
            alert("Failed to reset habits.");
        }
    });
});
