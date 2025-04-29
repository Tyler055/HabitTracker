import { fetchContent, saveGoalsData, resetGoalsData } from './saveData.js';

document.addEventListener("DOMContentLoaded", async function () {
  const logoutBtn = document.getElementById("logout-btn");

  let draggedItem = null;

  // Load goals from DB when the page loads
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

async function loadGoalsFromDB() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    try {
      const goals = await fetchContent(category);
      ul.innerHTML = "";
      goals.forEach(goal => {
        const li = createGoalElement(goal.text, goal.completed);
        ul.appendChild(li);
      });
    } catch (error) {
      console.error(`Failed loading goals for ${category}:`, error.message);
    }
  }
}

function createGoalElement(text, completed = false) {
  const li = document.createElement("li");
  li.setAttribute("draggable", "true");

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

  return li;
}

function initializeDragAndDrop() {
  const lists = document.querySelectorAll('.goal-category ul');
  lists.forEach(list => {
    list.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });

    list.addEventListener('drop', handleDrop);

    Array.from(list.getElementsByTagName('li')).forEach(item => {
      item.addEventListener('dragstart', function () {
        draggedItem = this;
        setTimeout(() => this.classList.add('dragging'), 0);
      });
      item.addEventListener('dragend', function () {
        this.classList.remove('dragging');
        saveCurrentGoals();
      });
    });
  });
}

function handleDrop(e) {
  e.preventDefault();
  if (!draggedItem) return;

  const list = e.currentTarget;
  const target = e.target.closest('li');
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
}

async function saveCurrentGoals() {
  const lists = document.querySelectorAll('.goal-category ul');
  for (const ul of lists) {
    const category = ul.id.replace('-goals-list', '');
    const goals = Array.from(ul.children).map(li => ({
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

  if (goalForm && goalInput) {
    goalForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const currentCategory = detectCurrentCategory();
      const goalList = document.querySelector(`.${currentCategory}-goals ul`);

      if (goalInput.value.trim() && goalList) {
        const li = createGoalElement(goalInput.value.trim());
        goalList.appendChild(li);
        goalInput.value = "";
        await saveCurrentGoals();
      }
    });
  }
}

function detectCurrentCategory() {
  const heading = document.querySelector("#content h1");
  if (heading) {
    const text = heading.textContent.toLowerCase();
    if (text.includes("daily")) return "daily";
    if (text.includes("weekly")) return "weekly";
    if (text.includes("monthly")) return "monthly";
    if (text.includes("yearly")) return "yearly";
    if (text.includes("all")) return "daily"; // Default for all goals page
  }
  return "daily"; // Fallback
}
