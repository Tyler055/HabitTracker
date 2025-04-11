

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
        toggleContent('../Locations/allgoals.html');
    });

    dailyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('../Locations/daily.html');
    });

    weeklyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('../Locations/weekly.html');
    });

    yearlyLink.addEventListener("click", function (e) {
        e.preventDefault();
        toggleContent('../Locations/yearly.html');
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
                    throw new Error("Network response was not ok");
                }
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");

                // Get the content and input sections from the fetched document
                const content = doc.querySelector("#content");
                const input = doc.querySelector("#input");

                if (content) goalsContainer.appendChild(content);
                if (input) goalsContainer.appendChild(input);

                // Bind goal form functionality from the loaded content
                bindGoalForm();
                
                // Show the container
                goalsContainer.style.display = "block";
                currentContent = url;  // Track the current content
            })
            .catch(error => {
                console.error("Failed to load content:", error.message);
            });
    }

    // Function to bind the form for adding new goals
    function bindGoalForm() {
        const goalForm = document.getElementById("goal-form");
        const goalInput = document.getElementById("goal-input");
      
        const goalCategory = document.getElementById("goal-category");

        // Determine the default category based on the loaded page
        let categoryKey = "";
        if (goalCategory) {
            categoryKey = goalCategory.value;
        } else {
            // Derive from h1 text in #content
            const heading = document.querySelector("#content h1");
            if (heading) {
                const text = heading.textContent.toLowerCase();
                if (text.includes("daily")) {
                    categoryKey = "daily";
                } else if (text.includes("weekly")) {
                    categoryKey = "weekly";
                } else if (text.includes("yearly")) {
                    categoryKey = "yearly";
                } else {
                    categoryKey = "all";
                }
            } else {
                categoryKey = "all";
            }
        }
      
        // For simplicity, we assume that on pages without a dropdown, there's one ul inside .goal-category.
        const goalList = document.querySelector(".goal-category ul");

        if (goalForm && goalList) {
            goalForm.addEventListener("submit", function (e) {
                e.preventDefault();
                const goalText = goalInput.value.trim();
                if (goalText) {
                    const li = document.createElement("li");
                    li.textContent = goalText;
                    goalList.appendChild(li);
                    goalInput.value = "";
                }
            });
        }
    }
});
