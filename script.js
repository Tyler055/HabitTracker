document.addEventListener("DOMContentLoaded", function () {
  let currentTheme = localStorage.getItem("theme") || "dark";
  const themeButton = document.getElementById("theme-toggle");
  const resetButton = document.getElementById("reset-button");
  const statsButton = document.getElementById("stats-button");
  const statsModal = document.getElementById("stats-modal");
  const removeStatsButton = document.getElementById("remove-stats-button");
  const habitFilter = document.getElementById("habit-filter");
  const habitSort = document.getElementById("habit-sort");
  const habitList = document.getElementById("habit-list");

  document.body.classList.add(currentTheme + "-theme");

  function updateButtonText() {
    themeButton.textContent =
      currentTheme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
  }
  updateButtonText();

  themeButton?.addEventListener("click", () => {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme");
    localStorage.setItem("theme", currentTheme);
    updateButtonText();
  });

  resetButton?.addEventListener("click", () => {
    if (confirm("Are you sure you want to reset all habits?")) {
      document.querySelectorAll(".habit-item").forEach((habit) => habit.remove());
      updateStatistics();
    }
  });

  statsButton?.addEventListener("click", () => {
    const statsSection = document.getElementById("stats-summary");
    if (statsSection) statsSection.style.display = "block";
    updateStatistics();
    statsModal.style.display = "block";
  });

  removeStatsButton?.addEventListener("click", () => {
    const statsSection = document.getElementById("stats-summary");
    if (statsSection) {
      statsSection.style.display = "none";
      statsModal.style.display = "none";
    }
  });

  window.addEventListener("click", (event) => {
    if (event.target === statsModal) {
      statsModal.style.display = "none";
    }
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      statsModal.style.display = "none";
    }
  });

  function updateStatistics() {
    const habits = document.querySelectorAll(".habit-item");
    const totalHabits = habits.length;
    const completedHabits = document.querySelectorAll(
      ".habit-item.completed"
    ).length;
    const completionRate = totalHabits
      ? ((completedHabits / totalHabits) * 100).toFixed(2)
      : 0;

    const statsSection = document.getElementById("stats-summary");
    if (statsSection) statsSection.style.display = "block";

    document.getElementById("total-habits").textContent = totalHabits;
    document.getElementById("completed-habits").textContent = completedHabits;
    document.getElementById("completion-rate").textContent = `${completionRate}%`;
  }

  habitFilter?.addEventListener("change", () => {
    const filterValue = habitFilter.value;
    const habitItems = document.querySelectorAll(".habit-item");
    habitItems.forEach((item) => {
      if (filterValue === "active") {
        item.style.display = item.classList.contains("completed") ? "none" : "block";
      } else if (filterValue === "completed") {
        item.style.display = item.classList.contains("completed") ? "block" : "none";
      } else {
        item.style.display = "block";
      }
    });
  });

  habitSort?.addEventListener("change", () => {
    const sortValue = habitSort.value;
    const habitItems = Array.from(document.querySelectorAll(".habit-item"));
    habitItems.sort((a, b) => {
      if (sortValue === "recent") {
        return new Date(b.dataset.createdAt) - new Date(a.dataset.createdAt);
      } else if (sortValue === "oldest") {
        return new Date(a.dataset.createdAt) - new Date(b.dataset.createdAt);
      } else if (sortValue === "alphabetical") {
        return a.querySelector(".habit-name").textContent.localeCompare(
          b.querySelector(".habit-name").textContent
        );
      }
    });
    habitList.innerHTML = "";
    habitItems.forEach((item) => habitList.appendChild(item));
  });

  function attachHabitListeners(habitElement) {
    habitElement.querySelector(".complete-btn")?.addEventListener("click", function () {
      const habitItem = this.closest(".habit-item");

      habitItem.classList.toggle("completed");
      updateStreaks(habitItem);
      updateStatistics();
    });

    habitElement.querySelector(".delete-btn")?.addEventListener("click", function (e) {
      e.preventDefault();
      const habitCard = this.closest(".habit-item");
      if (confirm("Are you sure you want to delete this habit?")) {
        habitCard.remove();
        updateStatistics();
      }
    });
  }

  document.querySelectorAll(".habit-item").forEach(attachHabitListeners);

  function updateStreaks(habitItem) {
    const currentSpan = habitItem.querySelector("[data-current-streak]");
    const longestSpan = habitItem.querySelector("[data-longest-streak]");
    const current = parseInt(currentSpan.dataset.currentStreak || 0) + 1;
    const longest = Math.max(parseInt(longestSpan.dataset.longestStreak || 0), current);
    currentSpan.dataset.currentStreak = current;
    longestSpan.dataset.longestStreak = longest;
    currentSpan.textContent = `${current} days`;
    longestSpan.textContent = `${longest} days`;
  }

  document.querySelector(".habit-form")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const name = this.habit_name.value.trim();
    const frequency = this.habit_frequency.value;
    if (name && frequency) {
      const newHabit = document.createElement("div");
      newHabit.className = "habit-card habit-item";
      newHabit.dataset.habitId = Date.now();
      newHabit.dataset.createdAt = new Date().toISOString();
      newHabit.innerHTML = `
          <div class="habit-header">
            <h3 class="habit-name">${name}</h3>
            <div class="habit-actions">
              <button class="complete-btn" title="Mark as Complete"><i class="fas fa-check"></i></button>
              <a href="#" class="delete-btn" title="Delete Habit"><i class="fas fa-trash-alt"></i></a>
            </div>
          </div>
          <div class="habit-details">
            <div class="habit-frequency">
              <span class="label">Frequency:</span>
              <span class="value">${frequency.charAt(0).toUpperCase() + frequency.slice(1)}</span>
            </div>
            <div class="habit-streak">
              <div class="current-streak">
                <span class="label">Current Streak:</span>
                <span class="value" data-current-streak="0">0 days</span>
              </div>
              <div class="longest-streak">
                <span class="label">Longest Streak:</span>
                <span class="value" data-longest-streak="0">0 days</span>
              </div>
            </div>
            <div class="habit-progress">
              <div class="progress-bar">
                <div class="progress" style="width: 0%;"></div>
              </div>
              <span class="progress-percentage">0%</span>
            </div>
          </div>`;
      habitList.appendChild(newHabit);
      attachHabitListeners(newHabit);
      this.reset();
      updateStatistics();
    }
  });
});
