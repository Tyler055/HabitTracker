document.addEventListener("DOMContentLoaded", function () {
    const homeLink = document.getElementById("home-link");
    const goalsLink = document.getElementById("load-goals");
    const dailyLink = document.getElementById("load-daily-goals");
    const weeklyLink = document.getElementById("load-weekly-goals");
    const monthlyLink = document.getElementById("load-monthly-goals");
    const yearlyLink = document.getElementById("load-yearly-goals");
    const goalsContainer = document.getElementById("goals-container");
    const navbar = document.getElementById("navbar");

    if (goalsContainer) goalsContainer.style.display = "none";

    let currentContent = "";

    if (navbar) {
        navbar.addEventListener("mouseenter", () => document.body.classList.add("nav-expanded"));
        navbar.addEventListener("mouseleave", () => document.body.classList.remove("nav-expanded"));
    }

    if (homeLink) {
        homeLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (goalsContainer) goalsContainer.style.display = "none";
            currentContent = "";
            document.body.style.backgroundImage = "url('https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')";
            document.body.style.backgroundSize = "cover";
            document.body.style.backgroundPosition = "center";
            document.body.style.backgroundAttachment = "fixed";
        });
    }

    if (goalsLink) goalsLink.addEventListener("click", e => { e.preventDefault(); toggleContent('Locations/allgoals.html'); });
    if (dailyLink) dailyLink.addEventListener("click", e => { e.preventDefault(); toggleContent('Locations/daily.html'); });
    if (weeklyLink) weeklyLink.addEventListener("click", e => { e.preventDefault(); toggleContent('Locations/weekly.html'); });
    if (monthlyLink) monthlyLink.addEventListener("click", e => { e.preventDefault(); toggleContent('Locations/monthly.html'); });
    if (yearlyLink) yearlyLink.addEventListener("click", e => { e.preventDefault(); toggleContent('Locations/yearly.html'); });

    function toggleContent(url) {
        if (currentContent === url) {
            if (goalsContainer) goalsContainer.style.display = "none";
            currentContent = "";
        } else {
            loadContent(url);
        }
    }

    function loadContent(url) {
        if (!goalsContainer) return;

        goalsContainer.innerHTML = "";

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error(`Failed to load ${url}: ${response.status} ${response.statusText}`);
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const content = doc.querySelector("#content");
                const input = doc.querySelector("#input");

                if (!content) throw new Error(`No content found in ${url}`);

                if (content) goalsContainer.appendChild(content);
                if (input) goalsContainer.appendChild(input);

                initializeDragAndDrop();
                loadSavedGoals();
                bindGoalForm();

                goalsContainer.style.display = "block";
                currentContent = url;
            })
            .catch(error => {
                console.error("Failed to load content:", error.message);
                goalsContainer.innerHTML = `<div class="error-message">Failed to load content: ${error.message}</div>`;
                goalsContainer.style.display = "block";
            });
    }

    initializeDragAndDrop();
});

// --- Drag & Drop ---
let draggedItem = null;

function initializeDragAndDrop() {
    const listIds = ['daily-goals-list', 'weekly-goals-list', 'monthly-goals-list', 'yearly-goals-list'];

    listIds.forEach(listId => {
        const list = document.getElementById(listId);
        if (list) {
            list.addEventListener('dragover', e => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            });

            list.addEventListener('drop', handleDrop);

            const items = list.getElementsByTagName('li');
            Array.from(items).forEach(item => {
                if (!item.hasAttribute('draggable')) item.setAttribute('draggable', 'true');
                if (!item.classList.contains('drag-enabled')) {
                    item.classList.add('drag-enabled');

                    item.addEventListener('dragstart', function (e) {
                        draggedItem = this;
                        setTimeout(() => this.classList.add('dragging'), 0);
                        e.dataTransfer.effectAllowed = 'move';
                        e.dataTransfer.setData('text/plain', this.textContent);
                    });

                    item.addEventListener('dragend', function () {
                        this.classList.remove('dragging');
                        document.querySelectorAll('li').forEach(li => {
                            li.classList.remove('drag-over');
                            li.style.borderTop = '';
                            li.style.borderBottom = '';
                        });
                    });

                    item.addEventListener('dragenter', function (e) {
                        e.preventDefault();
                        if (this !== draggedItem) {
                            const offset = this.getBoundingClientRect().y + this.getBoundingClientRect().height / 2;
                            if (e.clientY > offset) {
                                this.style.borderBottom = '2px solid #4CAF50';
                                this.style.borderTop = '';
                            } else {
                                this.style.borderTop = '2px solid #4CAF50';
                                this.style.borderBottom = '';
                            }
                        }
                    });

                    item.addEventListener('dragleave', function () {
                        this.style.borderTop = '';
                        this.style.borderBottom = '';
                    });
                }
            });
        }
    });
}

function handleDrop(e) {
    e.preventDefault();
    if (!draggedItem) return;

    const targetList = e.currentTarget;
    if (e.target.tagName === 'LI') {
        const offset = e.target.getBoundingClientRect().y + e.target.getBoundingClientRect().height / 2;
        if (e.clientY > offset) {
            e.target.parentNode.insertBefore(draggedItem, e.target.nextSibling);
        } else {
            e.target.parentNode.insertBefore(draggedItem, e.target);
        }
    } else {
        targetList.appendChild(draggedItem);
    }

    draggedItem = null;
    document.querySelectorAll('li').forEach(li => {
        li.style.borderTop = '';
        li.style.borderBottom = '';
    });

    saveGoals();
}

function getCurrentCategory() {
    const heading = document.querySelector("#content h1");
    if (heading) {
        const text = heading.textContent.toLowerCase();
        if (text.includes("daily")) return "daily";
        if (text.includes("weekly")) return "weekly";
        if (text.includes("monthly")) return "monthly";
        if (text.includes("yearly")) return "yearly";
    }
    return "all";
}

function loadSavedGoals() {
    const goalLists = document.querySelectorAll(".goal-category ul");
    if (!goalLists.length) return;

    goalLists.forEach(goalList => {
        const category = goalList.closest('.goal-category').classList[1].replace('-goals', '');
        const savedGoals = JSON.parse(localStorage.getItem(category) || '[]');

        const defaultGoals = Array.from(goalList.children).map(li => ({
            text: li.textContent.trim(),
            completed: false,
            isDefault: true
        }));

        goalList.innerHTML = '';

        defaultGoals.forEach(goal => {
            const li = createGoalElement(goal.text, goal.completed, true);
            goalList.appendChild(li);
        });

        savedGoals.forEach(goal => {
            if (!defaultGoals.some(defaultGoal => defaultGoal.text === goal.text)) {
                const li = createGoalElement(goal.text, goal.completed, false);
                goalList.appendChild(li);
            }
        });
    });

    initializeDragAndDrop();
}

function createGoalElement(text, completed = false, isDefault = false) {
    const li = document.createElement("li");
    li.setAttribute("draggable", "true");

    if (!isDefault) {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = completed;
        checkbox.addEventListener("change", () => {
            li.classList.toggle("completed");
            saveGoals();
        });
        li.appendChild(checkbox);
    }

    const span = document.createElement("span");
    span.textContent = text;
    if (completed) li.classList.add("completed");
    li.appendChild(span);

    if (!isDefault) {
        const deleteBtn = document.createElement("span");
        deleteBtn.textContent = "×";
        deleteBtn.className = "delete-btn";
        deleteBtn.addEventListener("click", () => {
            li.remove();
            saveGoals();
        });
        li.appendChild(deleteBtn);
    }

    return li;
}

function saveGoals() {
    const goalLists = document.querySelectorAll(".goal-category ul");

    goalLists.forEach(goalList => {
        const category = goalList.closest('.goal-category').classList[1].replace('-goals', '');
        const goals = Array.from(goalList.children)
            .filter(li => !li.classList.contains('default-goal'))
            .map(li => ({
                text: li.querySelector("span").textContent,
                completed: li.querySelector("input")?.checked || false
            }));

        localStorage.setItem(category, JSON.stringify(goals));
    });
}

function bindGoalForm() {
    const goalForm = document.getElementById("goal-form");
    const goalInput = document.getElementById("goal-input");
    const goalCategory = document.getElementById("goal-category");

    if (goalForm) {
        goalForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const goalText = goalInput.value.trim();

            if (goalText) {
                const category = goalCategory?.value || getCurrentCategory();
                const goalList = document.querySelector(`.${category}-goals ul`);
                if (goalList) {
                    const li = createGoalElement(goalText);
                    goalList.appendChild(li);
                    goalInput.value = "";
                    saveGoals();
                    initializeDragAndDrop();
                }
            }
        });
    }
}
