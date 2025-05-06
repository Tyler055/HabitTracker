import { fetchContent, saveGoalsData } from './saveData.js';

let draggedItem = null;
let isDirty = false;

document.addEventListener("DOMContentLoaded", async () => {
  await initializeApp();
  setupPageLinks();
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
    if (isDirty) e.preventDefault();
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
  }
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
    }
  }
}

function createGoalElement({ text, completed = false, dueDate = '' }) {
  const li = document.createElement("li");
  li.className = "goal-item";
  li.setAttribute("draggable", "true");

  // Checkbox
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = completed;
  checkbox.addEventListener("change", () => {
    markDirty();
    saveCurrentGoals();
  });
  li.appendChild(checkbox);

  // Goal Text
  const span = document.createElement("span");
  span.textContent = text;
  span.contentEditable = "false";
  li.appendChild(span);

  // Edit Button
  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  editBtn.addEventListener("click", () => {
    span.contentEditable = span.isContentEditable ? "false" : "true";
    editBtn.textContent = span.isContentEditable ? "Save" : "Edit";
    if (!span.isContentEditable) {
      markDirty();
      saveCurrentGoals();
    }
  });
  li.appendChild(editBtn);

  // Due Date
  const dueInput = document.createElement("input");
  dueInput.type = "date";
  dueInput.value = dueDate;
  dueInput.className = "due-date";
  dueInput.addEventListener("change", () => {
    markDirty();
    saveCurrentGoals();
  });
  li.appendChild(dueInput);

  // Delete
  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "×";
  deleteBtn.className = "delete-btn";
  deleteBtn.setAttribute("role", "button");
  deleteBtn.setAttribute("tabindex", "0");
  deleteBtn.addEventListener("click", () => {
    li.remove();
    markDirty();
    saveCurrentGoals();
  });
  li.appendChild(deleteBtn);

  makeItemDraggable(li);
  return li;
}

function bindGoalForm() {
  const form = document.getElementById("goal-form");
  const input = document.getElementById("goal-input");

  if (form && input) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) return;

      const category = detectCurrentCategory();
      const list = document.querySelector(`#${category}-goals-list`);
      const li = createGoalElement({ text });
      list.appendChild(li);
      input.value = "";
      await saveCurrentGoals();
    });
  }
}

function detectCurrentCategory() {
  const heading = document.querySelector("#content h1");
  if (!heading) return "daily";

  const text = heading.textContent.toLowerCase();
  if (text.includes("daily")) return "daily";
  if (text.includes("weekly")) return "weekly";
  if (text.includes("monthly")) return "monthly";
  if (text.includes("yearly")) return "yearly";
  return "daily";
}

function setupPageLinks() {
  // Placeholder
}

function makeItemDraggable(item) {
  item.addEventListener("dragstart", (e) => {
    draggedItem = item;
    item.classList.add("dragging");
    item.style.opacity = "0.5";
  });

  item.addEventListener("dragend", () => {
    item.classList.remove("dragging");
    item.style.opacity = "";
    draggedItem = null;
    markDirty();
    saveCurrentGoals();
  });
}

function initializeDragAndDrop() {
  const lists = document.querySelectorAll('.goal-category ul');
  lists.forEach(list => {
    list.addEventListener('dragover', (e) => {
      e.preventDefault();
      const after = getDragAfterElement(list, e.clientY);
      const draggingItem = document.querySelector('.dragging');
      if (after) list.insertBefore(draggingItem, after);
      else list.appendChild(draggingItem);
    });

    list.addEventListener('drop', () => {
      markDirty();
      saveCurrentGoals();
    });
  });
}

function getDragAfterElement(container, y) {
  const items = [...container.querySelectorAll('.goal-item:not(.dragging)')];
  return items.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset, element: child };
    }
    return closest;
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children).map(li => {
      const span = li.querySelector('span');
      const checkbox = li.querySelector('input[type="checkbox"]');
      const dateInput = li.querySelector('input[type="date"]');
      return {
        text: span?.textContent || '',
        completed: checkbox?.checked || false,
        dueDate: dateInput?.value || ''
      };
    });

    try {
      await saveGoalsData(category, goals);
      clearDirty();
    } catch (error) {
      console.error(`Error saving ${category} goals:`, error.message);
    }
  }
}
