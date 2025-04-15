document.addEventListener("DOMContentLoaded", function () {
    const goalsLink = document.getElementById("load-goals");
    const dailyLink = document.getElementById("load-daily-goals");
    const weeklyLink = document.getElementById("load-weekly-goals");
    const yearlyLink = document.getElementById("load-yearly-goals");
    const goalsContainer = document.getElementById("goals-container");
    const navbar = document.getElementById("navbar");

    // Initially hide the container
    goalsContainer.style.display = "none";

    // Track the current content loaded
    let currentContent = "";

    // Toggle class on body on navbar hover for content shifting
    navbar.addEventListener("mouseenter", function() {
        document.body.classList.add("nav-expanded");
    });
    navbar.addEventListener("mouseleave", function() {
        document.body.classList.remove("nav-expanded");
    });

    // Event listeners for each link
    goalsLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('Locations/allgoals.html');
    });

    dailyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('Locations/daily.html');
    });

    weeklyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('Locations/weekly.html');
    });

    yearlyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('Locations/yearly.html');
    });

    // Function to toggle visibility and load content dynamically from URL
    function toggleContent(url) {
        if (currentContent === url) {
            // If the same content is clicked, hide it
            goalsContainer.style.display = "none";
            currentContent = "";  // Reset the current content
        } else {
            // If it's a new content, load it
            loadContent(url);
        }
    }

    // Function to load content dynamically from URL
    function loadContent(url) {
        // Always clear the container to fetch fresh content every time
        goalsContainer.innerHTML = "";

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load ${url}: ${response.status} ${response.statusText}`);
                }
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");

                // Get the content and input sections from the fetched document
                const content = doc.querySelector("#content");
                const input = doc.querySelector("#input");

                if (!content) {
                    throw new Error(`No content found in ${url}`);
                }

                if (content) goalsContainer.appendChild(content);
                if (input) goalsContainer.appendChild(input);

                // Load saved goals from localStorage
                loadSavedGoals();
                
                // Bind goal form functionality from the loaded content
                bindGoalForm();
                
                // Show the container
                goalsContainer.style.display = "block";
                currentContent = url;  // Track the current content
            })
            .catch(error => {
                console.error("Failed to load content:", error.message);
                goalsContainer.innerHTML = `<div class="error-message">Failed to load content: ${error.message}</div>`;
                goalsContainer.style.display = "block";
            });
    }

    // Function to load saved goals from localStorage
    function loadSavedGoals() {
        const goalList = document.querySelector(".goal-category ul");
        if (!goalList) return;

        const category = getCurrentCategory();
        const savedGoals = JSON.parse(localStorage.getItem(category) || '[]');
        
        goalList.innerHTML = '';
        savedGoals.forEach(goal => {
            const li = createGoalElement(goal.text, goal.completed);
            goalList.appendChild(li);
        });
    }

    // Function to get current category
    function getCurrentCategory() {
        const heading = document.querySelector("#content h1");
        if (heading) {
            const text = heading.textContent.toLowerCase();
            if (text.includes("daily")) return "daily";
            if (text.includes("weekly")) return "weekly";
            if (text.includes("yearly")) return "yearly";
        }
        return "all";
    }

    // Function to create a goal element
    function createGoalElement(text, completed = false) {
        const li = document.createElement("li");
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = completed;
        checkbox.addEventListener("change", function() {
            li.classList.toggle("completed");
            saveGoals();
        });

        const span = document.createElement("span");
        span.textContent = text;
        if (completed) {
            li.classList.add("completed");
        }

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "×";
        deleteBtn.className = "delete-btn";
        deleteBtn.addEventListener("click", function() {
            li.remove();
            saveGoals();
        });

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(deleteBtn);
        return li;
    }

    // Function to save goals to localStorage
    function saveGoals() {
        const goalList = document.querySelector(".goal-category ul");
        if (!goalList) return;

        const category = getCurrentCategory();
        const goals = Array.from(goalList.children).map(li => ({
            text: li.querySelector("span").textContent,
            completed: li.querySelector("input").checked
        }));

        localStorage.setItem(category, JSON.stringify(goals));
    }

    // Function to bind the form for adding new goals
    function bindGoalForm() {
        const goalForm = document.getElementById("goal-form");
        const goalInput = document.getElementById("goal-input");
        const goalList = document.querySelector(".goal-category ul");

        if (goalForm && goalList) {
            goalForm.addEventListener("submit", function (e) {
                e.preventDefault();
                const goalText = goalInput.value.trim();
                if (goalText) {
                    const li = createGoalElement(goalText);
                    goalList.appendChild(li);
                    goalInput.value = "";
                    saveGoals();
                }
            });
        }
    }
});
