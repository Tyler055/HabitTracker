import { fetchContent, saveGoalsData } from './saveData.js';

const form = document.getElementById('goal-form');
const titleInput = document.getElementById('goal-title');
const descInput = document.getElementById('goal-description');
const prioritySelect = document.getElementById('goal-priority');
const categorySelect = document.getElementById('goal-category');
const deadlineInput = document.getElementById('goal-deadline');
const timeSelect = document.getElementById('goal-time');

// Initialize goal categories
const categories = ['daily', 'weekly', 'monthly', 'yearly'];

// Load all goals on page load for each category
categories.forEach(loadGoals);

function loadGoals(category) {
  fetchContent(category)
    .then(goals => {
      const dropzone = document.querySelector(`#${category} .goal-dropzone`);
      dropzone.innerHTML = ''; // Clear existing goals
      goals.forEach(goal => renderGoal(goal, category, dropzone));
    })
    .catch(err => {
      console.error(`Failed to load ${category} goals:`, err);
      alert(`❌ Failed to load ${category} goals. Please try again.`);
    });
}

function renderGoal(goal, category, container) {
  const div = document.createElement('div');
  div.className = 'goal-card';
  div.textContent = `${goal.title} (${goal.priority})`;
  div.title = goal.description || ''; // Show description in tooltip
  div.dataset.goalId = goal.id || ''; // Store goal id for later updates or deletions
  container.appendChild(div);

  // Add delete button
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';
  deleteButton.addEventListener('click', () => removeGoal(div, category));
  div.appendChild(deleteButton);
}

// Collect all goals from a category's dropzone (for saving or updating)
function collectGoals(category) {
  const dropzone = document.querySelector(`#${category} .goal-dropzone`);
  return Array.from(dropzone.children).map(el => {
    const [title, priority] = el.textContent.split(' (');
    return {
      id: el.dataset.goalId || '', // Include goal ID for updating
      title: title.trim(),
      priority: priority.replace(')', '').trim(),
      description: el.title,
      category,
    };
  });
}

// Handle form submit to add a new goal
form.addEventListener('submit', e => {
  e.preventDefault();

  const newGoal = {
    title: titleInput.value.trim(),
    description: descInput.value.trim(),
    priority: prioritySelect.value,
    category: categorySelect.value,
    deadline: deadlineInput.value,
    time: timeSelect.value,
  };

  if (!newGoal.title || !newGoal.category || !newGoal.priority) {
    alert('❌ Please fill in all required fields.');
    return;
  }

  // Check for duplicate goals
  const existingGoals = collectGoals(newGoal.category);
  if (existingGoals.some(goal => goal.title === newGoal.title)) {
    alert('❌ This goal already exists!');
    return;
  }

  // Render the new goal and add it to the respective dropzone
  const dropzone = document.querySelector(`#${newGoal.category} .goal-dropzone`);
  renderGoal(newGoal, newGoal.category, dropzone);

  // Collect all goals from the dropzone and save them
  const updatedGoals = collectGoals(newGoal.category);
  saveGoalsData(newGoal.category, updatedGoals)
    .then(() => {
      form.reset();
      timeSelect.value = 'any'; // Reset time field after submission
    })
    .catch(err => {
      console.error('Failed to save goal:', err);
      alert('❌ Failed to save your goal. Try again.');
    });
});

// Remove a goal when the delete button is clicked
function removeGoal(goalItem, category) {
  // Remove goal from the UI
  goalItem.remove();

  // After removal, update saved goals in the category
  const updatedGoals = collectGoals(category);
  saveGoalsData(category, updatedGoals)
    .catch(err => {
      console.error('Failed to save goal removal:', err);
      alert('❌ Failed to update your goals. Try again.');
    });

  // Stop the timer if there are no goals left in the category
  const remainingGoals = document.querySelectorAll(`#${category} .goal-card`);
  if (remainingGoals.length === 0) {
    stopTimer(category);
    const timerElement = document.getElementById(`${category}-timer`);
    if (timerElement) {
      timerElement.textContent = '00:00:00';
    }
  }
}

// Timer management
const timers = {
  daily: 0,
  weekly: 0,
  monthly: 0,
  yearly: 0,
};

function updateTimerDisplay(category) {
  const timerElement = document.getElementById(`${category}-timer`);
  const hours = String(Math.floor(timers[category] / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((timers[category] % 3600) / 60)).padStart(2, "0");
  const seconds = String(timers[category] % 60).padStart(2, "0");
  timerElement.textContent = `${hours}:${minutes}:${seconds}`;
}

function startTimer(category) {
  if (!timers[category].interval) {
    timers[category].interval = setInterval(() => {
      timers[category]++;
      updateTimerDisplay(category);
    }, 1000);
  }
}

function stopTimer(category) {
  clearInterval(timers[category].interval);
  timers[category].interval = null;
}

function resetTimer(category) {
  timers[category] = 0;
  updateTimerDisplay(category);
}

// Notifications
if ("Notification" in window && Notification.permission !== "granted") {
  Notification.requestPermission();
}

function sendReminder(message) {
  if (Notification.permission === "granted") {
    new Notification(message);
  }
}

// Schedule reminders for daily, weekly, monthly, and yearly goals
setInterval(() => sendReminder("🗓️ Daily Goal Reminder: Stay consistent!"), 1000 * 60 * 60 * 24);
setInterval(() => sendReminder("📅 Weekly Goal Reminder: Keep up the momentum!"), 1000 * 60 * 60 * 24 * 7);
setInterval(() => sendReminder("🗓️ Monthly Goal Reminder: Time to review progress!"), 1000 * 60 * 60 * 24 * 30);
setInterval(() => sendReminder("📆 Yearly Goal Reminder: Reflect and plan ahead!"), 1000 * 60 * 60 * 24 * 365);

// Category filter functionality
const categoryFilter = document.getElementById("category-filter");

categoryFilter.addEventListener("change", (e) => {
  const selectedCategory = e.target.value;
  document.querySelectorAll('.goal-section').forEach((section) => {
    section.style.display = section.id === selectedCategory || selectedCategory === 'all' ? 'block' : 'none';
  });
});
