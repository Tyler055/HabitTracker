document.addEventListener("DOMContentLoaded", function() {
  // Element References
  const addHabitBtn = document.getElementById("add-habit-btn");
  const habitInput = document.getElementById("habit-input");
  const habitList = document.getElementById("habit-list");
  const themeToggleButton = document.getElementById("theme-toggle");

  // Ensure elements exist
  if (!addHabitBtn || !habitInput || !habitList || !themeToggleButton) {
    console.error("Could not find one or more elements in the DOM.");
    return;
  }

  // Load habits from backend (initial load)
  loadHabits();

  // Handle Add Habit
  addHabitBtn.addEventListener("click", async function() {
    const habitName = habitInput.value.trim();
    if (habitName) {
      try {
        const response = await fetch("/api/add-habit", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name: habitName }),
        });

        if (response.ok) {
          const habit = await response.json();
          addHabitToUI(habit); // Add habit to the UI
          habitInput.value = ""; // Clear the input field
        } else {
          alert("Failed to add habit.");
        }
      } catch (error) {
        console.error("Error adding habit:", error);
        alert("Error adding habit.");
      }
    }
  });

  // Handle Delete Habit
  habitList.addEventListener("click", async function(e) {
    if (e.target.classList.contains("delete-btn")) {
      const habitId = e.target.dataset.habitId;
      if (habitId) {
        try {
          const response = await fetch(`/api/delete-habit/${habitId}`, {
            method: "DELETE",
          });

          if (response.ok) {
            e.target.closest(".habit-item").remove(); // Remove habit from UI
          } else {
            alert("Failed to delete habit.");
          }
        } catch (error) {
          console.error("Error deleting habit:", error);
          alert("Error deleting habit.");
        }
      }
    }
  });

  // Handle Theme Toggle
  let currentTheme = localStorage.getItem("theme") || "light";
  setTheme(currentTheme);

  themeToggleButton.addEventListener("click", function() {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    setTheme(currentTheme);
    localStorage.setItem("theme", currentTheme); // Store in localStorage
  });

  // Function to apply theme
  function setTheme(theme) {
    document.body.classList.remove("light-theme", "dark-theme");
    document.body.classList.add(`${theme}-theme`);
    themeToggleButton.textContent = theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
  }

  // Function to load habits on initial page load
  async function loadHabits() {
    try {
      const response = await fetch("/api/habits");
      if (!response.ok) {
        throw new Error(`Failed to load habits: ${response.statusText}`);
      }
      const habits = await response.json();
      habits.forEach(addHabitToUI);
    } catch (error) {
      console.error("Error loading habits:", error);
      alert("Error loading habits.");
    }
  }

  // Function to add habit to UI
  function addHabitToUI(habit) {
    const habitItem = document.createElement("div");
    habitItem.classList.add("habit-item");
    habitItem.innerHTML = `
      <span>${habit.name}</span>
      <button class="delete-btn" data-habit-id="${habit.id}">Delete</button>
    `;
    habitList.appendChild(habitItem);
  }
});
