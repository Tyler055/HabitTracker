// advanced.js
import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

const form = document.getElementById('goal-form');
const titleInput = document.getElementById('goal-title');
const descInput = document.getElementById('goal-description');
const prioritySelect = document.getElementById('goal-priority');
const categorySelect = document.getElementById('goal-category');
const deadlineInput = document.getElementById('goal-deadline');
const timeSelect = document.getElementById('goal-time');

// Load all goals on page load
['daily', 'weekly', 'monthly', 'yearly'].forEach(loadGoals);

function loadGoals(category) {
  fetchContent(category)
    .then(goals => {
      const dropzone = document.querySelector(`#${category} .goal-dropzone`);
      dropzone.innerHTML = ''; // Clear existing
      goals.forEach(goal => renderGoal(goal, category, dropzone));
    })
    .catch(err => console.error(`Failed to load ${category} goals:`, err));
}

// Render a goal into a dropzone
function renderGoal(goal, category, container) {
  const div = document.createElement('div');
  div.className = 'goal-card';
  div.textContent = `${goal.title} (${goal.priority})`;
  div.title = goal.description || '';
  container.appendChild(div);
}

// Collect all goals in a category's dropzone
function collectGoals(category) {
  const dropzone = document.querySelector(`#${category} .goal-dropzone`);
  return Array.from(dropzone.children).map(el => {
    const [title, priority] = el.textContent.split(' (');
    return {
      title: title.trim(),
      priority: priority.replace(')', '').trim(),
      description: el.title,
      category,
    };
  });
}

// Handle form submit
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

  const dropzone = document.querySelector(`#${newGoal.category} .goal-dropzone`);
  renderGoal(newGoal, newGoal.category, dropzone);

  const updatedGoals = collectGoals(newGoal.category);

  saveGoalsData(newGoal.category, updatedGoals)
    .then(() => {
      form.reset();
      timeSelect.value = 'any';
    })
    .catch(err => {
      console.error('Failed to save goals:', err);
      alert('❌ Failed to save your goal. Try again.');
    });
});
