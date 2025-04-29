import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

let draggedItem = null;

document.addEventListener("DOMContentLoaded", async function () {
  const logoutBtn = document.getElementById("logout-btn");

  await loadGoalsFromDB();
  initializeDragAndDrop();
  bindGoalForm();

  if (logoutBtn) {
    logoutBtn.style.display = "block";
    logoutBtn.addEventListener("click", () => {
      resetGoalsData();
      window.location.href = "/logout";
    });
  }
});

// Make any goal draggable
function makeItemDraggable(item) {
  item.setAttribute('draggable', 'true');

  item.addEventListener('dragstart', (e) => {
    draggedItem = item;
    e.dataTransfer.setData('text/plain', item.dataset.id || item.id);
    item.classList.add('dragging');
  });

  item.addEventListener('dragend', () => {
    item.classList.remove('dragging');
  });
}

// Add keyboard-based drag support
function addKeyboardDragSupport(item) {
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
      saveCurrentGoals();
      item.focus();
    }
  });
}

// Create a goal list item
function createGoalElement(text, completed = false, color = '', dueDate = '') {
  const li = document.createElement("li");
  li.setAttribute("tabindex", "0");
  li.classList.add('goal-item');

  // Color tag
  if (color) {
    const colorTag = document.createElement("span");
    colorTag.className = "color-tag";
    colorTag.style.backgroundColor = color;
    li.appendChild(colorTag);
  }

  // Checkbox
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = completed;
  checkbox.setAttribute("aria-label", "Mark as complete");
  checkbox.addEventListener("change", saveCurrentGoals);
  li.appendChild(checkbox);

  // Goal text
  const span = document.createElement("span");
  span.textContent = text;
  li.appendChild(span);

  // Due date
  if (dueDate) {
    const due = document.createElement("small");
    due.className = "due-date";
    due.textContent = `Due: ${dueDate}`;
    li.appendChild(due);
  }

  // Delete button
  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "×";
  deleteBtn.className = "delete-btn";
  deleteBtn.setAttribute("aria-label", "Delete goal");
  deleteBtn.addEventListener("click", () => {
    li.remove();
    saveCurrentGoals();
  });
  li.appendChild(deleteBtn);

  makeItemDraggable(li);
  addKeyboardDragSupport(li);
  return li;
}

// Load goals from server
async function loadGoalsFromDB() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    try {
      const goals = await fetchContent(category);
      ul.innerHTML = "";
      goals.forEach(goal => {
        const li = createGoalElement(goal.text, goal.completed, goal.color, goal.dueDate);
        ul.appendChild(li);
      });
    } catch (error) {
      console.error(`Failed loading goals for ${category}:`, error.message);
    }
  }
}

// Save goals to server
async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children).map(li => ({
      text: li.querySelector('span').textContent,
      completed: li.querySelector('input').checked,
      color: li.querySelector('.color-tag')?.style.backgroundColor || '',
      dueDate: li.querySelector('.due-date')?.textContent?.replace(/^Due:\s*/, '') || ''
    }));

    try {
      await saveGoalsData(category, goals);
    } catch (error) {
      console.error(`Error saving ${category} goals:`, error.message);
    }
  }
}

// Bind form submission for adding goals
function bindGoalForm() {
  const goalForm = document.getElementById("goal-form");
  const goalInput = document.getElementById("goal-input");

  if (goalForm && goalInput) {
    goalForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      
      const categorySelect = document.getElementById("goal-category");
      const currentCategory = categorySelect ? categorySelect.value : "daily";
      const goalList = document.querySelector(`.${currentCategory}-goals ul`);

      const goalText = goalInput.value.trim();
      if (!goalText || !goalList) return;

      const existingGoals = Array.from(goalList.children).map(li =>
        li.querySelector("span").textContent.toLowerCase()
      );
      if (existingGoals.includes(goalText.toLowerCase())) {
        alert("Goal already exists!");
        return;
      }

      const li = createGoalElement(goalText);
      goalList.appendChild(li);
      goalInput.value = "";
      await saveCurrentGoals();
    });
  }
}

// Determine which goal category is active
function detectCurrentCategory() {
  const heading = document.querySelector("#content h1");
  if (heading) {
    const text = heading.textContent.toLowerCase();
    if (text.includes("daily")) return "daily";
    if (text.includes("weekly")) return "weekly";
    if (text.includes("monthly")) return "monthly";
    if (text.includes("yearly")) return "yearly";
  }
  return "daily"; // Fallback
}

// Enable drag-and-drop UI
function initializeDragAndDrop() {
  const lists = document.querySelectorAll('.goal-category ul');

  lists.forEach(list => {
    list.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });

    list.addEventListener('dragenter', () => list.classList.add('drag-over'));
    list.addEventListener('dragleave', () => list.classList.remove('drag-over'));

    list.addEventListener('drop', e => {
      e.preventDefault();
      list.classList.remove('drag-over');

      const target = e.target.closest('li');
      if (!draggedItem) return;

      if (target) {
        const offset = target.getBoundingClientRect().y + target.offsetHeight / 2;
        if (e.clientY > offset) {
          list.insertBefore(draggedItem, target.nextSibling);
        } else {
          list.insertBefore(draggedItem, target);
        }
      } else {
        list.appendChild(draggedItem);
      }

      draggedItem = null;
      saveCurrentGoals();
    });
  });
}
