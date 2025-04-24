document.addEventListener("DOMContentLoaded", function() {
    const categorySelect = document.querySelector('#category');
    const goalForm = document.querySelector('#goal-form');
    const goalInput = document.querySelector('#goal-input');
    const goalsContainer = document.querySelector('#goals-container');
    const summary = document.querySelector('#summary');
    
    // Initialize goal categories
    let goals = {
      daily: [],
      weekly: [],
      monthly: [],
      yearly: []
    };
  
    // Fetch habits from localStorage or from the server
    function fetchHabits(category) {
      let cachedHabits = localStorage.getItem(category);
      if (cachedHabits) {
        goals[category] = JSON.parse(cachedHabits);
        renderHabits(category);
      } else {
        fetch(`/api/habits/${category}`)
          .then(response => response.json())
          .then(data => {
            goals[category] = data;
            localStorage.setItem(category, JSON.stringify(data));
            renderHabits(category);
          });
      }
    }
  
    // Render habits for a given category
    function renderHabits(category) {
      const categoryContainer = document.createElement('div');
      categoryContainer.classList.add('goal-category');
      categoryContainer.classList.add(`${category}-goals`);
  
      const categoryTitle = document.createElement('h2');
      categoryTitle.textContent = `${category.charAt(0).toUpperCase() + category.slice(1)} Goals`;
      categoryContainer.appendChild(categoryTitle);
  
      const goalList = document.createElement('ul');
      goals[category].forEach(goal => {
        const goalItem = document.createElement('li');
        const goalCheckbox = document.createElement('input');
        goalCheckbox.type = 'checkbox';
        goalCheckbox.checked = goal.completed;
        goalCheckbox.addEventListener('change', () => toggleGoalCompletion(category, goal));
  
        const goalText = document.createElement('span');
        goalText.textContent = goal.name;
  
        const deleteBtn = document.createElement('button');
        deleteBtn.classList.add('delete-btn');
        deleteBtn.textContent = '×';
        deleteBtn.addEventListener('click', () => deleteGoal(category, goal));
  
        goalItem.appendChild(goalCheckbox);
        goalItem.appendChild(goalText);
        goalItem.appendChild(deleteBtn);
        goalList.appendChild(goalItem);
      });
  
      categoryContainer.appendChild(goalList);
      goalsContainer.appendChild(categoryContainer);
    }
  
    // Toggle completion of a goal
    function toggleGoalCompletion(category, goal) {
      goal.completed = !goal.completed;
      localStorage.setItem(category, JSON.stringify(goals[category]));
    }
  
    // Delete a goal
    function deleteGoal(category, goal) {
      const goalIndex = goals[category].indexOf(goal);
      if (goalIndex > -1) {
        goals[category].splice(goalIndex, 1);
        localStorage.setItem(category, JSON.stringify(goals[category]));
        renderHabits(category);
      }
    }
  
    // Handle goal form submission
    goalForm.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const newGoal = {
        name: goalInput.value,
        completed: false
      };
  
      const category = categorySelect.value;
      goals[category].push(newGoal);
      localStorage.setItem(category, JSON.stringify(goals[category]));
      renderHabits(category);
  
      goalInput.value = '';
    });
  
    // Fetch the habits when the page loads
    Object.keys(goals).forEach(fetchHabits);
  });
  