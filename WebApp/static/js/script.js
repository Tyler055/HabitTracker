import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

let draggedItem = null;
let isDirty = false;

document.addEventListener("DOMContentLoaded", async () => {
  await initializeApp();
  setupPageLinks(); // Assuming it's defined elsewhere
});

async function initializeApp() {
  await loadGoalsFromDB();
  bindGoalForm();
  setupButtons();
  initializeDragAndDrop();
  setupBeforeUnload();
}

function setupBeforeUnload() {
  window.addEventListener('beforeunload', (e) => {
    if (isDirty) {
      e.preventDefault();
    }
  });
}

function markDirty() {
  isDirty = true;
}

function clearDirty() {
  isDirty = false;
}

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

function createGoalElement({ text, completed = false, color = '', dueDate = '' }) {
  const li = document.createElement("li");
  li.className = "goal-item";
  li.setAttribute("draggable", "true");
  li.setAttribute("role", "listitem");

  if (color) {
    const colorTag = document.createElement("span");
    colorTag.className = "color-tag";
    colorTag.style.backgroundColor = color;
    li.appendChild(colorTag);
  }

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = completed;

  const span = document.createElement("span");
  const spanId = `goal-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
  span.textContent = text;
  span.id = spanId;
  li.appendChild(span);

  checkbox.setAttribute("aria-labelledby", spanId);
  checkbox.addEventListener("change", () => {
    markDirty();
    saveCurrentGoals();
  });
  li.insertBefore(checkbox, span);

  if (dueDate) {
    const due = document.createElement("small");
    due.className = "due-date";
    due.textContent = `Due: ${dueDate}`;
    li.appendChild(due);
  }

  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "×";
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

  makeItemDraggable(li);
  addKeyboardDragSupport(li);

  return li;
}

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

function bindGoalForm() {
  const goalForm = document.getElementById("goal-form");
  const goalInput = document.getElementById("goal-input");

  if (!goalForm || !goalInput) return;

  goalForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const goalText = goalInput.value.trim();
    const currentCategory = detectCurrentCategory();
    const goalList = document.querySelector(`.${currentCategory}-goals ul`);
    if (!goalText || !goalList) return;

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

function detectCurrentCategory() {
  const heading = document.querySelector("#content h1");
  const text = heading?.textContent.toLowerCase() || '';
  if (text.includes("daily")) return "daily";
  if (text.includes("weekly")) return "weekly";
  if (text.includes("monthly")) return "monthly";
  if (text.includes("yearly")) return "yearly";
  return "daily";
}

function showErrorMessage(message) {
  let errorDiv = document.querySelector('.error-message');
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.setAttribute('aria-live', 'polite');
    document.body.appendChild(errorDiv);
  }
  errorDiv.textContent = message;
  clearTimeout(errorDiv.timeoutId);
  errorDiv.timeoutId = setTimeout(() => errorDiv.remove(), 5000);
}
