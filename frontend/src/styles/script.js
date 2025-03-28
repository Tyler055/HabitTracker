document.addEventListener("DOMContentLoaded", () => {
  let currentTheme = localStorage.getItem("theme") || "dark";

  // Element References
  const elements = {
    themeButton: document.getElementById("theme-toggle"),
    resetButton: document.getElementById("reset-button"),
    statsButton: document.getElementById("stats-button"),
    statsModal: document.getElementById("stats-modal"),
    closeStatsButton: document.getElementById("remove-stats-button"),
    statsSection: document.getElementById("stats-summary"),
    habitFilter: document.getElementById("habit-filter"),
    habitSort: document.getElementById("habit-sort"),
    habitList: document.getElementById("habit-list"),
    habitForm: document.querySelector(".habit-form"),
  };

  applyTheme(currentTheme);
  updateThemeButtonText();
  loadHabits();

  // Event Listeners
  elements.themeButton?.addEventListener("click", toggleTheme);
  elements.resetButton?.addEventListener("click", resetHabits);
  elements.statsButton?.addEventListener("click", showStatsModal);
  elements.closeStatsButton?.addEventListener("click", closeStatsModal);
  elements.habitFilter?.addEventListener("change", filterHabits);
  elements.habitSort?.addEventListener("change", sortHabits);
  elements.habitForm?.addEventListener("submit", addNewHabit);

  // Functions

  // Toggle theme between light and dark
  function toggleTheme() {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(currentTheme);
    localStorage.setItem("theme", currentTheme);
    updateThemeButtonText();
  }

  // Apply theme to the body
  function applyTheme(theme) {
    document.body.classList.remove("dark-theme", "light-theme");
    document.body.classList.add(`${theme}-theme`);
  }

  // Update the theme button text
  function updateThemeButtonText() {
    elements.themeButton.textContent =
      currentTheme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
  }

  // Load habits from backend
  async function loadHabits() {
    try {
      const res = await fetch("/api/habits");
      if (!res.ok) throw new Error("Failed to fetch habits");
      const habits = await res.json();
      habits.forEach(habit => {
        const el = createHabitElement(habit.name, habit.frequency || "daily", habit.id);
        elements.habitList.appendChild(el);
        attachHabitListeners(el);
      });
      updateStatistics();
    } catch (err) {
      console.error(err);
      alert("Error loading habits");
    }
  }

  // Add new habit
  async function addNewHabit(e) {
    e.preventDefault();
    const name = e.target.habit_name.value.trim();
    const frequency = e.target.habit_frequency.value;
    if (!name || !frequency) return;

    try {
      const res = await fetch("/api/add-habit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, frequency }),
      });

      if (!res.ok) throw new Error("Failed to add habit");
      const habit = await res.json();
      const el = createHabitElement(name, frequency, habit.id);
      elements.habitList.appendChild(el);
      attachHabitListeners(el);
      e.target.reset();
      updateStatistics();
    } catch (err) {
      console.error(err);
      alert("Error adding habit");
    }
  }

  // Create habit card
  function createHabitElement(name, frequency, id) {
    const div = document.createElement("div");
    div.className = "habit-card habit-item";
    div.dataset.habitId = id;
    div.innerHTML = `
      <div class="habit-header">
        <h3 class="habit-name">${name}</h3>
        <div class="habit-actions">
          <button class="complete-btn" title="Mark as Complete"><i class="fas fa-check"></i></button>
          <a href="#" class="delete-btn" title="Delete Habit" data-habit-id="${id}"><i class="fas fa-trash-alt"></i></a>
        </div>
      </div>
      <div class="habit-details">
        <div class="habit-frequency"><span class="label">Frequency:</span> <span class="value">${capitalize(frequency)}</span></div>
      </div>`;
    return div;
  }

  // Capitalize the first letter
  function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
  }

  // Attach listeners to habit actions
  function attachHabitListeners(habit) {
    habit.querySelector(".complete-btn")?.addEventListener("click", () => {
      habit.classList.toggle("completed");
      updateStatistics();
    });

    habit.querySelector(".delete-btn")?.addEventListener("click", async (e) => {
      e.preventDefault();
      const habitId = habit.dataset.habitId;
      if (!confirm("Delete this habit?")) return;
      try {
        const res = await fetch(`/api/delete-habit/${habitId}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Delete failed");
        habit.remove();
        updateStatistics();
      } catch (err) {
        console.error(err);
        alert("Error deleting habit");
      }
    });
  }

  // Update habit statistics
  function updateStatistics() {
    const total = document.querySelectorAll(".habit-item").length;
    const completed = document.querySelectorAll(".habit-item.completed").length;
    const rate = total ? ((completed / total) * 100).toFixed(2) : 0;
    document.getElementById("total-habits").textContent = total;
    document.getElementById("completed-habits").textContent = completed;
    document.getElementById("completion-rate").textContent = `${rate}%`;
  }

  // Show stats modal
  function showStatsModal() {
    elements.statsSection.style.display = "block";
    elements.statsModal.style.display = "block";
    updateStatistics();
  }

  // Close stats modal
  function closeStatsModal() {
    elements.statsModal.style.display = "none";
  }

  // Filter habits
  function filterHabits() {
    const value = elements.habitFilter.value;
    document.querySelectorAll(".habit-item").forEach((item) => {
      const isCompleted = item.classList.contains("completed");
      item.style.display =
        value === "active"
          ? isCompleted ? "none" : "block"
          : value === "completed"
          ? isCompleted ? "block" : "none"
          : "block";
    });
  }

  // Sort habits
  function sortHabits() {
    const value = elements.habitSort.value;
    const items = Array.from(document.querySelectorAll(".habit-item"));
    items.sort((a, b) => {
      if (value === "recent") {
        return new Date(b.dataset.createdAt) - new Date(a.dataset.createdAt);
      } else if (value === "oldest") {
        return new Date(a.dataset.createdAt) - new Date(b.dataset.createdAt);
      } else if (value === "alphabetical") {
        const nameA = a.querySelector(".habit-name").textContent;
        const nameB = b.querySelector(".habit-name").textContent;
        return nameA.localeCompare(nameB);
      }
    });
    elements.habitList.innerHTML = "";
    items.forEach((item) => elements.habitList.appendChild(item));
  }

  // Reset habits (local only)
  function resetHabits() {
    if (confirm("Are you sure you want to reset all habits?")) {
      document.querySelectorAll(".habit-item").forEach((el) => el.remove());
      updateStatistics();
    }
  }
});
