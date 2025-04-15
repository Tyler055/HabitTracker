document.addEventListener("DOMContentLoaded", function () {
    const goalsLink = document.getElementById("load-goals");
    const goalsContainer = document.getElementById("goals-container");
    const navbar = document.getElementById("navbar");

    // Initially hide the container
    goalsContainer.style.display = "none";

    // Toggle a class on the body based on navbar hover events
    navbar.addEventListener("mouseenter", function() {
      document.body.classList.add("nav-expanded");
    });
    navbar.addEventListener("mouseleave", function() {
      document.body.classList.remove("nav-expanded");
    });

    // Load "All Goals" content when its link is clicked
    goalsLink.addEventListener("click", function (e) {
        e.preventDefault();

        if (goalsContainer.innerHTML === "") {
            fetch('/Locations/allgoals.html')
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.text();
                })
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, "text/html");

                    const content = doc.querySelector("#content");
                    const input = doc.querySelector("#input");

                    goalsContainer.innerHTML = "";
                    if (content) goalsContainer.appendChild(content);
                    if (input) goalsContainer.appendChild(input);

                    bindGoalForm();
                    goalsContainer.style.display = "block";
                })
                .catch(error => {
                    console.error("Failed to load All Goals:", error.message);
                });
        } else {
            // Toggle visibility if content is already loaded
            goalsContainer.style.display =
              goalsContainer.style.display === "none" ? "block" : "none";
        }
    });

    function bindGoalForm() {
        const goalForm = document.getElementById("goal-form");
        const goalInput = document.getElementById("goal-input");
        const goalCategory = document.getElementById("goal-category");

        const goalLists = {
            daily: document.querySelectorAll(".goal-category h2 + ul")[0],
            weekly: document.querySelectorAll(".goal-category h2 + ul")[1],
            monthly: document.querySelectorAll(".goal-category h2 + ul")[2],
            yearly: document.querySelectorAll(".goal-category h2 + ul")[3]
        };

        if (goalForm) {
            goalForm.addEventListener("submit", function (e) {
                e.preventDefault();

                const goalText = goalInput.value.trim();
                const category = goalCategory.value;

                if (goalText && goalLists[category]) {
                    const li = document.createElement("li");
                    li.textContent = goalText;
                    goalLists[category].appendChild(li);
                    goalInput.value = "";
                }
            });
        }
    }
});

// Function to load goals
function loadGoals() {
    const goalsContainer = document.getElementById('goals-container');
    goalsContainer.innerHTML = '<h2>Your Goals</h2><p>Goals will be loaded here.</p>';
}
