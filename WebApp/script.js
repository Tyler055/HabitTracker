document.addEventListener("DOMContentLoaded", function () {
    const homeLink = document.getElementById("home-link");
    const goalsLink = document.getElementById("load-goals");
    const dailyLink = document.getElementById("load-daily-goals");
    const weeklyLink = document.getElementById("load-weekly-goals");
    const monthlyLink = document.getElementById("load-monthly-goals");
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

    // Home link event listener
    homeLink.addEventListener("click", function (e) {
        e.preventDefault();
        // Hide the goals container
        goalsContainer.style.display = "none";
        currentContent = "";
        // Show the background
        document.body.style.backgroundImage = "url('https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')";
        document.body.style.backgroundSize = "cover";
        document.body.style.backgroundPosition = "center";
        document.body.style.backgroundAttachment = "fixed";
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

    monthlyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('Locations/monthly.html');
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

    // Function to get current category
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

    // Function to load saved goals from localStorage
    function loadSavedGoals() {
        const goalLists = document.querySelectorAll(".goal-category ul");
        if (!goalLists.length) return;

        // allgoals.html 페이지인 경우
        if (goalLists.length > 1) {
            goalLists.forEach(goalList => {
                const category = goalList.closest('.goal-category').classList[1].replace('-goals', '');
                const savedGoals = JSON.parse(localStorage.getItem(category) || '[]');
                
                // Convert existing goals to array and mark them as default
                const defaultGoals = Array.from(goalList.children).map(li => ({
                    text: li.textContent,
                    completed: false,
                    isDefault: true
                }));

                // Clear the list
                goalList.innerHTML = '';

                // Add default goals first
                defaultGoals.forEach(goal => {
                    const li = createGoalElement(goal.text, goal.completed, true);
                    goalList.appendChild(li);
                });

                // Add saved goals that are not defaults
                savedGoals.forEach(goal => {
                    if (!defaultGoals.some(defaultGoal => defaultGoal.text === goal.text)) {
                        const li = createGoalElement(goal.text, goal.completed, false);
                        goalList.appendChild(li);
                    }
                });
            });
        } 
        // 개별 페이지인 경우
        else {
            const goalList = goalLists[0];
            const category = getCurrentCategory();
            const savedGoals = JSON.parse(localStorage.getItem(category) || '[]');
            
            // Convert existing goals to array and mark them as default
            const defaultGoals = Array.from(goalList.children).map(li => ({
                text: li.textContent,
                completed: false,
                isDefault: true
            }));

            // Clear the list
            goalList.innerHTML = '';

            // Add default goals first
            defaultGoals.forEach(goal => {
                const li = createGoalElement(goal.text, goal.completed, true);
                goalList.appendChild(li);
            });

            // Add saved goals that are not defaults
            savedGoals.forEach(goal => {
                if (!defaultGoals.some(defaultGoal => defaultGoal.text === goal.text)) {
                    const li = createGoalElement(goal.text, goal.completed, false);
                    goalList.appendChild(li);
                }
            });
        }
    }

    // Function to create a goal element
    function createGoalElement(text, completed = false, isDefault = false) {
        const li = document.createElement("li");
        
        if (!isDefault) {
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = completed;
            checkbox.addEventListener("change", function() {
                li.classList.toggle("completed");
                saveGoals();
            });
            li.appendChild(checkbox);
        }

        const span = document.createElement("span");
        span.textContent = text;
        if (completed) {
            li.classList.add("completed");
        }
        li.appendChild(span);

        if (!isDefault) {
            const deleteBtn = document.createElement("span");
            deleteBtn.textContent = "×";
            deleteBtn.className = "delete-btn";
            deleteBtn.addEventListener("click", function() {
                li.remove();
                saveGoals();
            });
            li.appendChild(deleteBtn);
        }

        return li;
    }

    // Function to save goals to localStorage
    function saveGoals() {
        // allgoals.html 페이지인 경우
        const goalLists = document.querySelectorAll(".goal-category ul");
        if (goalLists.length > 1) {
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
        // 개별 페이지인 경우
        else {
            const goalList = goalLists[0];
            const category = getCurrentCategory();
            const goals = Array.from(goalList.children)
                .filter(li => !li.classList.contains('default-goal'))
                .map(li => ({
                    text: li.querySelector("span").textContent,
                    completed: li.querySelector("input")?.checked || false
                }));

            localStorage.setItem(category, JSON.stringify(goals));
        }
    }

    // Function to bind the form for adding new goals
    function bindGoalForm() {
        const goalForm = document.getElementById("goal-form");
        const goalInput = document.getElementById("goal-input");
        const goalCategory = document.getElementById("goal-category");

        if (goalForm) {
            goalForm.addEventListener("submit", function (e) {
                e.preventDefault();
                const goalText = goalInput.value.trim();
                
                if (goalText) {
                    // allgoals.html 페이지인 경우
                    if (goalCategory) {
                        const category = goalCategory.value;
                        const goalList = document.querySelector(`.${category}-goals ul`);
                        if (goalList) {
                            const li = createGoalElement(goalText);
                            goalList.appendChild(li);
                            goalInput.value = "";
                            saveGoals();
                        }
                    } 
                    // daily, weekly, yearly 페이지인 경우
                    else {
                        const goalList = document.querySelector(".goal-category ul");
                        if (goalList) {
                            const li = createGoalElement(goalText);
                            goalList.appendChild(li);
                            goalInput.value = "";
                            saveGoals();
                        }
                    }
                }
            });
        }
    }
});
