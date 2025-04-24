document.addEventListener("DOMContentLoaded", function () {
    const links = {
        "load-goals": '/static/Locations/all-goals.html',
        "load-daily-goals": '/static/Locations/daily.html',
        "load-weekly-goals": '/static/Locations/weekly.html',
        "load-monthly-goals": '/static/Locations/monthly.html',
        "load-yearly-goals": '/static/Locations/yearly.html',
        "load-advanced-goals": '/static/Locations/advanced.html'
    };

    const navbar = document.getElementById("navbar");
    const goalsContainer = document.getElementById("goals-container");
    const homeLink = document.getElementById("home-link");
    const themeToggle = document.getElementById("theme-toggle");

    // Theme Initialization
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }

    themeToggle?.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
    });

    // Navbar Expand
    navbar?.addEventListener("mouseenter", () => document.body.classList.add("nav-expanded"));
    navbar?.addEventListener("mouseleave", () => document.body.classList.remove("nav-expanded"));

    // Home link background reset
    homeLink?.addEventListener("click", (e) => {
        e.preventDefault();
        goalsContainer.style.display = "none";
        document.body.style.backgroundImage = "url('https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')";
    });

    // Navigation link handlers
    Object.keys(links).forEach(id => {
        document.getElementById(id)?.addEventListener("click", (e) => {
            e.preventDefault();
            loadContent(links[id]);
        });
    });

    async function loadContent(url) {
        goalsContainer.innerHTML = "";
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error("Failed to load content");
            const html = await res.text();
            const doc = new DOMParser().parseFromString(html, "text/html");

            const content = doc.querySelector("#content");
            const input = doc.querySelector("#input");
            if (content) goalsContainer.appendChild(content);
            if (input) goalsContainer.appendChild(input);

            goalsContainer.style.display = "block";

            bindGoalForm();
            initializeDragAndDrop();
            await loadSavedGoals();
        } catch (err) {
            goalsContainer.innerHTML = `<div class="error-message">Error: ${err.message}</div>`;
        }
    }

    function bindGoalForm() {
        const form = document.getElementById("goal-form");
        const suggestBtn = document.getElementById("suggest-goal");

        if (form) {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const text = document.getElementById("goal-text").value.trim();
                const category = document.getElementById("goal-category").value;
                if (!text || !category) return alert("Please enter a goal and select a category.");

                const goal = { id: Date.now(), text, completed: false };
                await saveGoal(goal, category);
                addGoalToDOM(goal, category);
                form.reset();
            });
        }

        if (suggestBtn) {
            suggestBtn.addEventListener("click", async () => {
                const res = await fetch("/api/goal-suggestions");
                const data = await res.json();
                document.getElementById("goal-text").value = data.goal;
            });
        }
    }

    function addGoalToDOM(goal, category) {
        const container = document.getElementById(`${category}-goals`);
        if (!container) return;

        const div = document.createElement("div");
        div.className = "goal-item";
        div.setAttribute("draggable", "true");
        div.dataset.id = goal.id;
        div.innerHTML = `
            <input type="checkbox" ${goal.completed ? "checked" : ""}>
            <span>${goal.text}</span>
            <button class="delete-btn">✖</button>
        `;

        div.querySelector("input").addEventListener("change", async () => {
            goal.completed = div.querySelector("input").checked;
            await updateGoalStatus(goal.id, category, goal.completed);
        });

        div.querySelector("button").addEventListener("click", async () => {
            container.removeChild(div);
            await deleteGoal(goal.id, category);
        });

        div.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text/plain", JSON.stringify({ ...goal, from: category }));
            div.classList.add("dragging");
        });

        div.addEventListener("dragend", () => {
            div.classList.remove("dragging");
        });

        container.appendChild(div);
    }

    function initializeDragAndDrop() {
        const dropZones = document.querySelectorAll(".goal-category");

        dropZones.forEach(zone => {
            zone.addEventListener("dragover", e => e.preventDefault());

            zone.addEventListener("drop", async e => {
                e.preventDefault();
                const { id, from, text, completed } = JSON.parse(e.dataTransfer.getData("text/plain"));
                const targetCategory = zone.id;
                if (from !== targetCategory) {
                    await deleteGoal(id, from);
                    const newGoal = { id, text, completed };
                    await saveGoal(newGoal, targetCategory);
                    addGoalToDOM(newGoal, targetCategory);
                }
            });
        });
    }

    async function loadSavedGoals() {
        const categories = ["daily", "weekly", "monthly", "yearly"];
        for (let cat of categories) {
            try {
                const res = await fetch(`/api/goals/${cat}`);
                const goals = await res.json();
                goals.forEach(goal => addGoalToDOM(goal, cat));
            } catch (err) {
                console.error(`Failed to load ${cat} goals`, err);
            }
        }
    }

    async function saveGoal(goal, category) {
        await fetch(`/api/goals/${category}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(goal)
        });
    }

    async function updateGoalStatus(id, category, completed) {
        await fetch(`/api/goals/${category}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed })
        });
    }

    async function deleteGoal(id, category) {
        await fetch(`/api/goals/${category}/${id}`, { method: "DELETE" });
    }
});