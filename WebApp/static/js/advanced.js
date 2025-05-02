document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("goal-form");
    const timeSections = document.querySelectorAll(".goal-dropzone");
    let currentEdit = null;
  
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = document.getElementById("goal-title").value.trim();
      const description = document.getElementById("goal-description").value.trim();
      const priority = document.getElementById("goal-priority").value;
      const timeCategory = document.getElementById("goal-time").value;
  
      if (!title || !timeCategory) return alert("Please fill in required fields.");
  
      const goal = {
        title,
        description,
        priority,
        timeCategory
      };
  
      if (currentEdit) {
        updateGoal(currentEdit, goal);
        currentEdit = null;
      } else {
        addGoalCard(goal);
      }
  
      form.reset();
    });
  
    function addGoalCard(goal) {
      const card = document.createElement("div");
      card.className = `goal-card ${goal.priority.toLowerCase()}`;
      card.setAttribute("draggable", true);
  
      card.innerHTML = `
        <div class="goal-header">
          <h3>${goal.title}</h3>
          <div>
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
          </div>
        </div>
        <div class="goal-details">
          <p>${goal.description}</p>
          <strong>Priority:</strong> ${goal.priority}
        </div>
      `;
  
      addDragEvents(card);
      card.querySelector(".edit-btn").addEventListener("click", () => editGoal(card, goal));
      card.querySelector(".delete-btn").addEventListener("click", () => card.remove());
  
      const section = document.querySelector(`#${goal.timeCategory} .goal-dropzone`);
      section.appendChild(card);
    }
  
    function editGoal(card, goal) {
      document.getElementById("goal-title").value = goal.title;
      document.getElementById("goal-description").value = goal.description;
      document.getElementById("goal-priority").value = goal.priority;
      document.getElementById("goal-time").value = goal.timeCategory;
      currentEdit = card;
    }
  
    function updateGoal(card, goal) {
      card.className = `goal-card ${goal.priority.toLowerCase()}`;
      card.innerHTML = `
        <div class="goal-header">
          <h3>${goal.title}</h3>
          <div>
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
          </div>
        </div>
        <div class="goal-details">
          <p>${goal.description}</p>
          <strong>Priority:</strong> ${goal.priority}
        </div>
      `;
      addDragEvents(card);
      card.querySelector(".edit-btn").addEventListener("click", () => editGoal(card, goal));
      card.querySelector(".delete-btn").addEventListener("click", () => card.remove());
  
      const section = document.querySelector(`#${goal.timeCategory} .goal-dropzone`);
      section.appendChild(card);
    }
  
    function addDragEvents(card) {
      card.addEventListener("dragstart", () => {
        card.classList.add("dragging");
      });
  
      card.addEventListener("dragend", () => {
        card.classList.remove("dragging");
      });
    }
  
    timeSections.forEach(zone => {
      zone.addEventListener("dragover", e => {
        e.preventDefault();
        zone.classList.add("dragover");
      });
  
      zone.addEventListener("dragleave", () => {
        zone.classList.remove("dragover");
      });
  
      zone.addEventListener("drop", e => {
        e.preventDefault();
        const dragged = document.querySelector(".dragging");
        if (dragged) {
          zone.appendChild(dragged);
          zone.classList.remove("dragover");
        }
      });
    });
  });
  