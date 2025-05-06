import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

const form = document.getElementById('goal-form');
const titleInput = document.getElementById('goal-title');
const descInput = document.getElementById('goal-description');
const prioritySelect = document.getElementById('goal-priority');
const categorySelect = document.getElementById('goal-category');
const deadlineInput = document.getElementById('goal-deadline');
const timeSelect = document.getElementById('goal-time');

// Load all goals on page load for each category
['daily', 'weekly', 'monthly', 'yearly'].forEach(loadGoals);

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

// Render a goal into a dropzone
function renderGoal(goal, category, container) {
  const div = document.createElement('div');
  div.className = 'goal-card';
  div.textContent = `${goal.title} (${goal.priority})`;
  div.title = goal.description || ''; // Show description in tooltip
  div.dataset.goalId = goal.id || ''; // Store goal id for later updates or deletions
  container.appendChild(div);
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

  if (!newGoal.title || !newGoal.category) {
    alert('❌ Please fill in both title and category.');
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
