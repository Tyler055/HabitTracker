document.addEventListener("DOMContentLoaded", function () {
    const homeLink = document.getElementById("home-link");
    const goalsLink = document.getElementById("load-goals");
    const dailyLink = document.getElementById("load-daily-goals");
    const weeklyLink = document.getElementById("load-weekly-goals");
    const monthlyLink = document.getElementById("load-monthly-goals");
    const yearlyLink = document.getElementById("load-yearly-goals");
    const goalsContainer = document.getElementById("goals-container");
    const navbar = document.getElementById("navbar");
    const logoutBtn = document.getElementById("logout-btn");
    const chartsDiv = document.getElementById("category-charts");
    
    // Initialize localStorage goals and charts
    let currentContent = "";
    let charts = {};

    // Show/Hide content on navbar links
    function renderCategoryCharts() {
        const categories = ["daily", "weekly", "monthly", "yearly"];
        const chartIds = ["dailyChart", "weeklyChart", "monthlyChart", "yearlyChart"];
        const categoryColors = ["#28a745", "#17a2b8", "#ffc107", "#dc3545"];
        let allGoals = [];

        categories.forEach(cat => {
            const data = JSON.parse(localStorage.getItem(cat) || "[]");
            allGoals = allGoals.concat(data);
        });
        
        const allTotal = allGoals.length;
        const allCompleted = allGoals.filter(g => g.completed).length;
        const allPercent = allTotal === 0 ? 0 : Math.round((allCompleted / allTotal) * 100);
        const allCtx = document.getElementById("allGoalsChart").getContext('2d');
        if (charts['all']) charts['all'].destroy();
        charts['all'] = new Chart(allCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Incomplete'],
                datasets: [{
                    data: [allPercent, 100 - allPercent],
                    backgroundColor: ['#673ab7', '#e0e0e0'],
                    borderWidth: 2
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: { display: false },
                    tooltip: { callbacks: { label: (context) => `${context.label}: ${context.parsed}%` }},
                    title: { display: true, text: `${allPercent}%`, position: 'center', color: '#333', font: { size: 22, weight: 'bold' }}
                }
            }
        });

        categories.forEach((cat, idx) => {
            const data = JSON.parse(localStorage.getItem(cat) || "[]");
            const total = data.length;
            const completed = data.filter(g => g.completed).length;
            const percent = total === 0 ? 0 : Math.round((completed / total) * 100);
            const ctx = document.getElementById(chartIds[idx]).getContext('2d');
            if (charts[cat]) charts[cat].destroy();
            charts[cat] = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Incomplete'],
                    datasets: [{
                        data: [percent, 100 - percent],
                        backgroundColor: [categoryColors[idx], '#e0e0e0'],
                        borderWidth: 2
                    }]
                },
                options: {
                    cutout: '70%',
                    plugins: {
                        legend: { display: false },
                        tooltip: { callbacks: { label: (context) => `${context.label}: ${context.parsed}%` }},
                        title: { display: true, text: `${percent}%`, position: 'center', color: '#333', font: { size: 22, weight: 'bold' }}
                    }
                }
            });
        });
    }

    // Hide/show specific sections when loading content
    function hideLogoutBtn() {
        if (logoutBtn) logoutBtn.style.display = "none";
    }

    function hideCharts() {
        if (chartsDiv) chartsDiv.style.display = "none";
    }

    function expandGoalsContainer() {
        if (goalsContainer) goalsContainer.classList.add("full-width-goals");
    }

    if (homeLink) {
        homeLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (goalsContainer) goalsContainer.style.display = "none";
            if (logoutBtn) logoutBtn.style.display = "block";
            if (chartsDiv) chartsDiv.style.display = "flex";
            if (goalsContainer) goalsContainer.classList.remove("full-width-goals");
            renderCategoryCharts();
            currentContent = "";
        });
    }

    if (goalsLink) goalsLink.addEventListener("click", e => { e.preventDefault(); hideLogoutBtn(); hideCharts(); expandGoalsContainer(); toggleContent('Locations/all-goals.html'); });
    if (dailyLink) dailyLink.addEventListener("click", e => { e.preventDefault(); hideLogoutBtn(); hideCharts(); expandGoalsContainer(); toggleContent('Locations/daily.html'); });
    if (weeklyLink) weeklyLink.addEventListener("click", e => { e.preventDefault(); hideLogoutBtn(); hideCharts(); expandGoalsContainer(); toggleContent('Locations/weekly.html'); });
    if (monthlyLink) monthlyLink.addEventListener("click", e => { e.preventDefault(); hideLogoutBtn(); hideCharts(); expandGoalsContainer(); toggleContent('Locations/monthly.html'); });
    if (yearlyLink) yearlyLink.addEventListener("click", e => { e.preventDefault(); hideLogoutBtn(); hideCharts(); expandGoalsContainer(); toggleContent('Locations/yearly.html'); });

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

    // Advanced goal creation: includes progress and timestamp
    function createGoalElement(text, completed = false, isDefault = false, progress = 0) {
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
        li.appendChild(span);

        // Add progress bar
        const progressBarContainer = document.createElement("div");
        progressBarContainer.classList.add("progress-bar-container");
        const progressBar = document.createElement("div");
        progressBar.classList.add("progress-bar");
        progressBar.style.width = `${progress}%`;
        progressBarContainer.appendChild(progressBar);
        li.appendChild(progressBarContainer);

        if (completed) li.classList.add("completed");

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

    // Load saved goals with enhanced properties (progress, timestamps)
    function loadSavedGoals() {
        const goalLists = document.querySelectorAll(".goal-category ul");
        if (!goalLists.length) return;

        goalLists.forEach(goalList => {
            const category = goalList.closest('.goal-category').classList[1].replace('-goals', '');
            const savedGoals = JSON.parse(localStorage.getItem(category) || '[]');

            goalList.innerHTML = '';

            savedGoals.forEach(goal => {
                const li = createGoalElement(goal.text, goal.completed, false, goal.progress || 0);
                goalList.appendChild(li);
            });
        });

        initializeDragAndDrop();
    }

    // Save goal progress in localStorage
    function saveGoals() {
        const goalLists = document.querySelectorAll(".goal-category ul");

        goalLists.forEach(goalList => {
            const category = goalList.closest('.goal-category').classList[1].replace('-goals', '');
            const goals = Array.from(goalList.children)
                .filter(li => !li.classList.contains('default-goal'))
                .map(li => ({
                    text: li.querySelector("span").textContent,
                    completed: li.querySelector("input")?.checked || false,
                    progress: li.querySelector(".progress-bar")?.style.width.replace("%", "") || 0
                }));

            localStorage.setItem(category, JSON.stringify(goals));
        });
    }

    // Logout functionality
    document.addEventListener('DOMContentLoaded', () => {
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function () {
                localStorage.clear();  // Clear all stored goals
                location.href = '/login';  // Redirect to login page
            });
        }
    });

    renderCategoryCharts(); // Initial chart rendering
    if (chartsDiv) chartsDiv.style.display = "flex";
    if (logoutBtn) logoutBtn.style.display = "block";
    if (goalsContainer) goalsContainer.classList.remove("full-width-goals");
    initializeDragAndDrop();
});
