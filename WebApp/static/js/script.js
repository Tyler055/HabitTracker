import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

document.addEventListener("DOMContentLoaded", async function () {
  const logoutBtn = document.getElementById("logout-btn");
  
  try {
    await loadGoalsFromDB();
    initializeDragAndDrop();
    bindGoalForm();

    if (logoutBtn) {
      logoutBtn.style.display = "block";
      logoutBtn.addEventListener("click", () => {
        window.location.href = "/logout";
      });
    }
  } catch (err) {
    console.error("Error during DOMContentLoaded tasks:", err.message);
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
  initializeDragAndDrop();
}

function addCategoryEditToggle(ul, category) {
  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Show Edit Buttons";
  toggleBtn.className = "toggle-edit-btn";
  toggleBtn.dataset.category = category;

  toggleBtn.addEventListener("click", () => {
    const editButtons = ul.querySelectorAll('.edit-btn');
    const isVisible = editButtons[0]?.style.display === "inline-block";
    editButtons.forEach(btn => btn.style.display = isVisible ? "none" : "inline-block");
    toggleBtn.textContent = isVisible ? "Show Edit Buttons" : "Hide Edit Buttons";
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
  checkbox.addEventListener("change", () => {
    saveCurrentGoals().catch(e => console.error("Checkbox save error:", e.message));
  });
  li.appendChild(checkbox);

  const span = document.createElement("span");
  span.textContent = text;
  span.className = "goal-text";
  li.appendChild(span);

  const deleteBtn = document.createElement("span");
  deleteBtn.textContent = "X";
  deleteBtn.className = "delete-btn";
  deleteBtn.addEventListener("click", () => {
    li.remove();
    saveCurrentGoals().catch(e => console.error("Delete save error:", e.message));
  });
  li.appendChild(deleteBtn);

  editBtn.addEventListener("click", () => {
    const currentText = span.textContent;
    const newText = prompt("Edit goal:", currentText);
    if (newText && newText.trim()) {
      const trimmedNewText = newText.trim();
      if (trimmedNewText !== currentText) {
        const duplicateCategory = checkForDuplicateGoal(trimmedNewText, li.closest('ul').id);
        if (!duplicateCategory) {
          span.textContent = trimmedNewText;
          saveCurrentGoals().catch(e => console.error("Edit save error:", e.message));
          alert("Goal has been edited successfully!");
        } else {
          alert(`The goal "${trimmedNewText}" already exists in the "${duplicateCategory}" category.`);
        }
      }
    }
  });

  addDragHandlers(li);
  return li;
}

function addDragHandlers(item) {
  item.addEventListener('dragstart', (e) => {
    draggedItem = item;
    setTimeout(() => item.classList.add('dragging'), 0);
  });

  item.addEventListener('dragend', () => {
    item.classList.remove('dragging');
    draggedItem = null;
    saveCurrentGoals().catch(e => console.error("Drag end save error:", e.message));
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
    list.insertBefore(draggedItem, e.clientY > offset ? target.nextSibling : target);
  } else {
    list.appendChild(draggedItem);
  }

  draggedItem = null;
  saveCurrentGoals().catch(err => console.error("Drop save error:", err.message));
}

async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');

  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children)
      .filter(li => !li.classList.contains('edit-toggle-li'))
      .map(li => ({
        text: li.querySelector('.goal-text').textContent.trim(),
        completed: li.querySelector('input[type="checkbox"]').checked
      }))
      .filter(goal => goal.text.length > 0);

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
      const selectedCategory = categorySelect?.value || getPageCategory();
      const goalList = document.querySelector(`#${selectedCategory}-goals-list`);

      if (newGoalText && goalList) {
        const duplicateCategory = checkForDuplicateGoal(newGoalText);
        if (duplicateCategory) {
          alert(`The goal "${newGoalText}" already exists in the "${duplicateCategory}" category.`);
        } else {
          const li = createGoalElement(newGoalText);
          goalList.appendChild(li);
          goalInput.value = "";
          try {
            await saveCurrentGoals();
            alert(`Goal "${newGoalText}" added successfully!`);
          } catch (err) {
            console.error("Error saving new goal:", err.message);
          }
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
  const path = window.location.pathname;
  if (path.includes("yearly")) return "yearly";
  if (path.includes("monthly")) return "monthly";
  if (path.includes("weekly")) return "weekly";
  return "daily";
}
