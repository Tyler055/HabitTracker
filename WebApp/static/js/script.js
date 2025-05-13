import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

document.addEventListener("DOMContentLoaded", async function () {
  const logoutBtn = document.getElementById("logout-btn");
  await loadGoalsFromDB();
  initializeDragAndDrop();
  bindGoalForm();

  if (logoutBtn) {
    logoutBtn.style.display = "block";
    logoutBtn.addEventListener("click", () => {
      window.location.href = "/logout";
    });
  }
});

let draggedItem = null;

function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

async function loadGoalsFromDB() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    ul.innerHTML = "";
    addCategoryEditToggle(ul, category);

    try {
      const goals = await fetchContent(category);
      goals.forEach(goal => {
        const li = createGoalElement(goal.text, goal.completed);
        ul.appendChild(li);
      });
    } catch (error) {
      console.error(`Failed loading goals for ${category}:`, error.message);
    }
  }
  initializeDragAndDrop();
}

function addCategoryEditToggle(ul, category) {
  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Show Edit Buttons";
  toggleBtn.className = "toggle-edit-btn";
  toggleBtn.dataset.category = category;

  toggleBtn.addEventListener("click", () => {
    const currentCategory = toggleBtn.dataset.category;
    const editButtons = ul.querySelectorAll('.edit-btn');
    const isVisible = editButtons[0]?.style.display === "inline-block";

    if (isVisible) {
      editButtons.forEach(btn => btn.style.display = "none");
      toggleBtn.textContent = "Show Edit Buttons";
    } else {
      editButtons.forEach(btn => btn.style.display = "inline-block");
      toggleBtn.textContent = "Hide Edit Buttons";
    }
  });

  const li = document.createElement("li");
  li.className = "edit-toggle-li";
  li.appendChild(toggleBtn);
  ul.appendChild(li);
}

function createGoalElement(text, completed = false) {
  const li = document.createElement("li");
  li.setAttribute("draggable", "true");

  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  editBtn.className = "edit-btn";
  editBtn.style.display = "none";
  li.appendChild(editBtn);

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = completed;
  checkbox.addEventListener("change", saveCurrentGoals);
  li.appendChild(checkbox);

  const span = document.createElement("span");
  span.textContent = text;
  span.className = "goal-text";
  li.appendChild(span);

  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "X"; // Changed to "X"
  deleteBtn.className = "delete-btn";
  deleteBtn.addEventListener("click", () => {
    li.remove();
    saveCurrentGoals();
  });
  li.appendChild(deleteBtn);

  editBtn.addEventListener("click", () => {
    const newText = prompt("Edit goal:", span.textContent);
    if (newText && newText.trim()) {
      const trimmedNewText = newText.trim();
      const duplicateCategory = checkForDuplicateGoal(trimmedNewText, li.closest('ul').id);
      if (!duplicateCategory) {
        span.textContent = trimmedNewText;
        saveCurrentGoals();
        alert("Goal has been edited successfully!");
      } else {
        alert(`The goal "${trimmedNewText}" already exists in the "${duplicateCategory}" category.`);
      }
    }
  });

  addDragHandlers(li);
  return li;
}

function addDragHandlers(item) {
  item.addEventListener('dragstart', function () {
    draggedItem = this;
    setTimeout(() => this.classList.add('dragging'), 0);
  });

  item.addEventListener('dragend', function () {
    this.classList.remove('dragging');
    draggedItem = null;
    saveCurrentGoals();
  });
}

function initializeDragAndDrop() {
  const lists = document.querySelectorAll('.goal-category ul');
  lists.forEach(list => {
    list.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });

    list.addEventListener('drop', handleDrop);

    list.querySelectorAll('li').forEach(item => {
      if (!item.classList.contains('edit-toggle-li')) {
        addDragHandlers(item);
      }
    });
  });
}

function handleDrop(e) {
  e.preventDefault();
  if (!draggedItem) return;

  const list = e.currentTarget;
  const target = e.target.closest('li');

  if (target && !target.classList.contains('edit-toggle-li')) {
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
}

async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children)
      .filter(li => !li.classList.contains('edit-toggle-li'))
      .map(li => {
        const span = li.querySelector('span');
        return {
          text: span.textContent.trim(),
          completed: li.querySelector('input').checked
        };
      })
      .filter(goal => goal.text.length > 0); // Ignore empty goals

    try {
      await saveGoalsData(category, goals);
    } catch (error) {
      console.error(`Error saving ${category} goals:`, error.message);
    }
  }
}

function bindGoalForm() {
  const goalForm = document.getElementById("goal-form");
  const goalInput = document.getElementById("goal-input");
  const categorySelect = document.getElementById("goal-category");

  if (goalForm && goalInput) {
    goalForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const newGoalText = goalInput.value.trim();
      let selectedCategory = categorySelect ? categorySelect.value : null;

      // Check if no category is selected in the dropdown
      if (!selectedCategory) {
        // Get the current page category (e.g., "yearly")
        const pageCategory = getPageCategory();
        selectedCategory = pageCategory; // Use the page category as default
      }

      const goalList = document.querySelector(`#${selectedCategory}-goals-list`);

      if (newGoalText && goalList) {
        const duplicateCategory = checkForDuplicateGoal(newGoalText);
        if (duplicateCategory) {
          alert(`The goal "${newGoalText}" already exists in the "${duplicateCategory}" category.`);
        } else {
          const li = createGoalElement(newGoalText);
          goalList.appendChild(li);
          goalInput.value = "";
          await saveCurrentGoals();
          alert(`Goal "${newGoalText}" added successfully!`);
        }
      }
    });
  }
}

function checkForDuplicateGoal(newText, currentListId = "") {
  const allGoalLists = document.querySelectorAll('.goal-category ul');

  for (const list of allGoalLists) {
    const category = list.id.replace('-goals-list', '');
    if (list.id !== currentListId) {
      const goals = list.querySelectorAll('li .goal-text');
      for (const goal of goals) {
        if (goal.textContent.trim() === newText) {
          return category;
        }
      }
    }
  }
  return null;
}

function getPageCategory() {
  if (window.location.pathname.includes("yearly")) {
    return "yearly";
  }
  if (window.location.pathname.includes("monthly")) {
    return "monthly";
  }
  if (window.location.pathname.includes("weekly")) {
    return "weekly";
  }
  if (window.location.pathname.includes("daily")) {
    return "daily";
  }
  return "daily";
}