import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

document.addEventListener("DOMContentLoaded", async function () {
  const logoutBtn = document.getElementById("logout-btn");

  // Load goals and initialize interactions
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
  initializeDragAndDrop(); // ensure drag handlers after loading
}

function addCategoryEditToggle(ul, category) {
  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Show Edit Buttons";
  toggleBtn.className = "toggle-edit-btn";
  toggleBtn.dataset.category = category;

  toggleBtn.addEventListener("click", () => {
    document.querySelectorAll('.goal-category ul').forEach(list => {
      list.querySelectorAll('.edit-btn').forEach(btn => btn.style.display = "none");
    });

    ul.querySelectorAll('.edit-btn').forEach(btn => btn.style.display = "inline-block");
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
  li.appendChild(span);

  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "×";
  deleteBtn.className = "delete-btn";
  deleteBtn.addEventListener("click", () => {
    li.remove();
    saveCurrentGoals();
  });
  li.appendChild(deleteBtn);

  let isEdited = false; // Track if the goal was edited

  editBtn.addEventListener("click", () => {
    const newText = prompt("Edit goal:", span.textContent);
    if (newText && newText.trim()) {
      const trimmedNewText = newText.trim();
      // Check if the new text is a duplicate across all categories
      if (!isDuplicateGoal(trimmedNewText, li.closest('ul').id)) {
        span.textContent = trimmedNewText;
        isEdited = true; // Mark as edited
        saveCurrentGoals();
        
        // Only alert when the goal was actually edited (text changed)
        alert("Goal has been edited successfully!");
      } else {
        alert("The goal already exists in another category."); // This alert is for editing
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
      .map(li => ({
        text: li.querySelector('span').textContent,
        completed: li.querySelector('input').checked
      }));

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

  if (goalForm && goalInput && categorySelect) {
    goalForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const newGoalText = goalInput.value.trim();
      const selectedCategory = categorySelect.value;
      const goalList = document.querySelector(`#${selectedCategory}-goals-list`);

      if (newGoalText && goalList) {
        // Check for duplicate goals across all categories
        const duplicateCategory = checkForDuplicateGoal(newGoalText);
        if (duplicateCategory) {
          alert(`The goal "${newGoalText}" already exists in the "${duplicateCategory}" category.`);
        } else {
          const li = createGoalElement(newGoalText);
          goalList.appendChild(li);
          goalInput.value = "";
          await saveCurrentGoals();
          
          alert(`Goal "${newGoalText}" added successfully!`); // Show add goal success alert
        }
      }
    });
  }
}

// Function to check for duplicates across all categories
function checkForDuplicateGoal(newText) {
  const allGoalLists = document.querySelectorAll('.goal-category ul');
  const categories = ['daily', 'weekly', 'monthly', 'yearly'];

  for (const list of allGoalLists) {
    const category = list.id.replace('-goals-list', '');
    const existingGoals = list.querySelectorAll('li span');
    for (const goal of existingGoals) {
      if (goal.textContent === newText) {
        return category; // Return the category if the goal is a duplicate
      }
    }
  }
  return null; // No duplicate found
}
