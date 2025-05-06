// Import utility functions for data handling
import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

let draggedItem = null;  // Item currently being dragged
let isDirty = false;     // Tracks unsaved changes

// Wait until page loads before initializing
document.addEventListener("DOMContentLoaded", async () => {
  await initializeApp();  // Main setup
  setupPageLinks();       // Setup navigation buttons
});

// Main initialization logic
async function initializeApp() {
  await loadGoalsFromDB();   // Load stored goals
  bindGoalForm();            // Handle new goal submissions
  setupButtons();            // Handle UI buttons (logout)
  initializeDragAndDrop();   // Enable drag-and-drop
  setupBeforeUnload();       // Warn user about unsaved changes
}

// Warn user before they leave page if there are unsaved changes
function setupBeforeUnload() {
  window.addEventListener('beforeunload', (e) => {
    if (isDirty) {
      e.preventDefault();
    }
  });
}

// Flag the page as having unsaved changes
function markDirty() {
  isDirty = true;
}

// Clear the unsaved changes flag
function clearDirty() {
  isDirty = false;
}

// Setup buttons like logout
function setupButtons() {
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.style.display = "block";
    logoutBtn.addEventListener("click", () => {
      window.location.href = "/logout";
    });
  } else {
    console.warn("Logout button not found in the DOM.");
  }
}

// Create a new list item for a goal
function createGoalElement({ text, completed = false, color = '', dueDate = '' }) {
  const li = document.createElement("li");
  li.className = "goal-item";
  li.setAttribute("draggable", "true");
  li.setAttribute("role", "listitem");

  // Optional color tag
  if (color) {
    const colorTag = document.createElement("span");
    colorTag.className = "color-tag";
    colorTag.style.backgroundColor = color;
    li.appendChild(colorTag);
  }

  // Checkbox for completion
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = completed;

  // Goal text span
  const span = document.createElement("span");
  const spanId = `goal-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
  span.textContent = text;
  span.id = spanId;
  li.appendChild(span);

  // Accessibility: label checkbox with span text
  checkbox.setAttribute("aria-labelledby", spanId);
  checkbox.addEventListener("change", () => {
    markDirty();
    saveCurrentGoals();  // Save when completed toggled
  });
  li.insertBefore(checkbox, span);

  // Due date display
  if (dueDate) {
    const due = document.createElement("small");
    due.className = "due-date";
    due.textContent = `Due: ${dueDate}`;
    li.appendChild(due);
  }

  // Delete button
  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "x";
  deleteBtn.className = "delete-btn";
  deleteBtn.setAttribute("role", "button");
  deleteBtn.setAttribute("tabindex", "0");
  deleteBtn.setAttribute("aria-label", "Delete goal");
  deleteBtn.addEventListener("click", () => {
    li.remove();
    markDirty();
    saveCurrentGoals();
  });
  deleteBtn.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      li.remove();
      markDirty();
      saveCurrentGoals();
    }
  });

  li.appendChild(deleteBtn);

  // Enable dragging and keyboard reordering
  makeItemDraggable(li);
  addKeyboardDragSupport(li);

  return li;
}

// Enable mouse drag-and-drop for item
function makeItemDraggable(item) {
  item.addEventListener('dragstart', (e) => {
    draggedItem = item;
    e.dataTransfer.effectAllowed = "move";
    item.classList.add('dragging');
    item.style.opacity = '0.5';
    markDirty();
  });

  item.addEventListener('dragend', () => {
    item.classList.remove('dragging');
    item.style.opacity = '';
    draggedItem = null;
    saveCurrentGoals();
  });
}

// Allow items to be dropped in categories
function initializeDragAndDrop() {
  const uls = document.querySelectorAll('.goal-category ul');
  uls.forEach(ul => {
    ul.addEventListener("dragover", (e) => {
      e.preventDefault();
      const draggingItem = document.querySelector('.dragging');
      const afterElement = getDragAfterElement(ul, e.clientY);
      if (!afterElement) {
        ul.appendChild(draggingItem);
      } else {
        ul.insertBefore(draggingItem, afterElement);
      }
    });

    ul.addEventListener("drop", (e) => {
      e.preventDefault();
      markDirty();
      saveCurrentGoals();
    });
  });
}

// Helper to determine where to insert dragged item
function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.goal-item:not(.dragging)')];
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Enable keyboard reordering with arrow keys
function addKeyboardDragSupport(item) {
  item.setAttribute("tabindex", "0");
  item.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" || e.key === "ArrowDown") {
      e.preventDefault();
      const parent = item.parentElement;
      const items = Array.from(parent.children);
      const index = items.indexOf(item);
      if (e.key === "ArrowUp" && index > 0) {
        parent.insertBefore(item, items[index - 1]);
      } else if (e.key === "ArrowDown" && index < items.length - 1) {
        parent.insertBefore(item, items[index + 1].nextSibling);
      }
      markDirty();
      saveCurrentGoals();
      item.focus();
    }
  });
}

// Load all goals for each category (daily, weekly, etc.)
async function loadGoalsFromDB() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    try {
      const goals = await fetchContent(category);
      ul.innerHTML = "";
      goals.forEach(goal => {
        const li = createGoalElement(goal);
        ul.appendChild(li);
      });
    } catch (error) {
      console.error(`Failed loading goals for ${category}:`, error.message);
      showErrorMessage(`Failed to load goals for ${category}. Please try again later.`);
    }
  }
}

// Save current goals in all categories
async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children).map(li => ({
      text: li.querySelector('span')?.textContent || '',
      completed: li.querySelector('input')?.checked || false,
      color: li.querySelector('.color-tag')?.style.backgroundColor || '',
      dueDate: li.querySelector('.due-date')?.textContent?.replace(/^Due:\s*/, '') || ''
    }));

    try {
      await saveGoalsData(category, goals);
    } catch (error) {
      console.error(`Error saving ${category} goals:`, error.message);
      showErrorMessage(`Failed to save ${category} goals. Please try again later.`);
    }
  }
  clearDirty();
}

// Handle goal form submission
function bindGoalForm() {
  const goalForm = document.getElementById("goal-form");
  const goalInput = document.getElementById("goal-input");

  if (!goalForm || !goalInput) return;

  goalForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const goalText = goalInput.value.trim();
    const selectedCategory = document.getElementById("goal-category")?.value;
    const goalList = document.querySelector(`.${selectedCategory}-goals ul`);
    if (!goalText || !goalList) return;

    // Prevent duplicate goals
    const existingGoals = Array.from(goalList.children).map(li =>
      li.querySelector("span").textContent.toLowerCase()
    );
    if (existingGoals.includes(goalText.toLowerCase())) {
      alert("Goal already exists!");
      return;
    }

    const newGoal = { text: goalText, completed: false };
    const li = createGoalElement(newGoal);
    goalList.appendChild(li);
    goalInput.value = "";
    markDirty();
    await saveCurrentGoals();
  });
}

// Determine current category from heading (optional)
function detectCurrentCategory() {
  const heading = document.querySelector("#content h1");
  const text = heading?.textContent.toLowerCase() || '';
  if (text.includes("daily")) return "daily";
  if (text.includes("weekly")) return "weekly";
  if (text.includes("monthly")) return "monthly";
  return "daily"; // Default category
}

// Display error message
function showErrorMessage(message) {
  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";
  errorDiv.textContent = message;
  document.body.appendChild(errorDiv);
  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

// Setup page navigation links (new function)
function setupPageLinks() {
  const pageLinks = document.querySelectorAll('.page-link'); // Adjust the selector for your navigation links
  pageLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      const targetUrl = link.getAttribute('href');
      
      // You can add your logic here, e.g., to load content for the target page
      console.log('Navigating to:', targetUrl);
      
      // Example: navigating to the target page
      window.location.href = targetUrl;
    });
  });
}
