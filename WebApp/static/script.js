document.addEventListener("DOMContentLoaded", function () {
    const goalsLink      = document.getElementById("load-goals");
    const dailyLink      = document.getElementById("load-daily-goals");
    const weeklyLink     = document.getElementById("load-weekly-goals");
    const monthlyLink    = document.getElementById("load-monthly-goals")
    const yearlyLink     = document.getElementById("load-yearly-goals");
    const advancedLink    = document.getElementById("load-advanced-goals")
    const goalsContainer = document.getElementById("goals-container");
    const navbar         = document.getElementById("navbar");

    goalsContainer.style.display = "none";
    let currentContent = "";

    navbar.addEventListener("mouseenter", () => document.body.classList.add("nav-expanded"));
    navbar.addEventListener("mouseleave", () => document.body.classList.remove("nav-expanded"));

    goalsLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/allgoals.html');
    });
    dailyLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/daily.html');
    });
    weeklyLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/weekly.html');
    });
    monthlyLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/monthly.html');
    });
    yearlyLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/yearly.html');
    });
    advancedLink.addEventListener("click", e => {
        e.preventDefault();
        toggleContent('/static/Locations/advanced.html');
    });

    function toggleContent(url) {
        if (currentContent === url) {
            goalsContainer.style.display = "none";
            currentContent = "";
        } else {
            loadContent(url);
        }
    }

    function loadContent(url) {
        goalsContainer.innerHTML = "";
        fetch(url)
        .then(res => {
            if (!res.ok) throw new Error("Network error");
            return res.text();
        })
        .then(html => {
            const doc     = new DOMParser().parseFromString(html, "text/html");
            const content = doc.querySelector("#content");
            const input   = doc.querySelector("#input");

            if (content) goalsContainer.appendChild(content);
            if (input)   goalsContainer.appendChild(input);

            bindGoalForm();
            goalsContainer.style.display = "block";
            currentContent = url;
        })
        .catch(err => console.error("Failed to load:", err));
    }

    function bindGoalForm() {
        const form = document.getElementById("goal-form");
        const input = document.getElementById("goal-input");
        const list  = document.querySelector(".goal-category ul");
        if (!form || !list) return;

        form.onsubmit = e => {
            e.preventDefault();
            const text = input.value.trim();
            if (!text) return;
            const li = document.createElement("li");
            li.textContent = text;
            list.appendChild(li);
            input.value = "";
        };
    }
});
