document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("goal-form");
  const timeSections = document.querySelectorAll(".goal-dropzone");
  let currentEditId = null;

  fetchGoals();

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const goal = {
      title: document.getElementById("goal-title").value.trim(),
      description: document.getElementById("goal-description").value.trim(),
      priority: document.getElementById("goal-priority").value,
      timeCategory: document.getElementById("goal-category").value
    };

    if (!goal.title || !goal.timeCategory) {
      return alert("Please fill in required fields.");
    }

    const url = currentEditId ? `/goals/${currentEditId}` : "/goals";
    const method = currentEditId ? "PUT" : "POST";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(goal)
    }).then(() => {
      fetchGoals();
      form.reset();
      currentEditId = null;
    });
  });

  function fetchGoals() {
    fetch("/goals")
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch goals");
        return res.json();
      })
      .then(goals => {
        document.querySelectorAll(".goal-dropzone").forEach(zone => zone.innerHTML = "");
        goals.forEach(addGoalCard);
      })
      .catch(err => {
        console.error("Error loading goals:", err);
      });
  }

  function addGoalCard(goal) {
    const card = document.createElement("div");
    card.className = `goal-card ${goal.priority.toLowerCase()}`;
    card.setAttribute("draggable", true);
    card.dataset.id = goal.id;

    card.innerHTML = `
      <div class="goal-header">
        <h3>${goal.title}</h3>
        <div>
          <button class="edit-btn">Edit</button>
          <button class="delete-btn">Delete</button>
        </div>
      </div>
      <div class="goal-details">
        <p>${goal.description || ''}</p>
        <strong>Priority:</strong> ${goal.priority}
      </div>
    `;

    card.querySelector(".edit-btn").addEventListener("click", () => {
      document.getElementById("goal-title").value = goal.title;
      document.getElementById("goal-description").value = goal.description;
      document.getElementById("goal-priority").value = goal.priority;
      document.getElementById("goal-category").value = goal.timeCategory;
      currentEditId = goal.id;
    });

    card.querySelector(".delete-btn").addEventListener("click", () => {
      fetch(`/goals/${goal.id}`, { method: "DELETE" }).then(fetchGoals);
    });

    addDragEvents(card);
    document.querySelector(`#${goal.timeCategory} .goal-dropzone`).appendChild(card);
  }

  function addDragEvents(card) {
    card.addEventListener("dragstart", () => card.classList.add("dragging"));
    card.addEventListener("dragend", () => card.classList.remove("dragging"));
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
        const goalId = dragged.dataset.id;
        const newCategory = zone.closest(".goal-section").id;
        fetch(`/goals/${goalId}/move`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ timeCategory: newCategory })
        }).then(fetchGoals);
        zone.classList.remove("dragover");
      }
    });
  });
});
