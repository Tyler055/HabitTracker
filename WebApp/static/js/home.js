import { fetchContent, resetGoalsData } from './saveData.js';

let charts = {};

document.addEventListener('DOMContentLoaded', () => {
  console.log('Home.js loaded');
  setupButtons();
  updateAllCharts();
});

function setupButtons() {
  const resetBtn = document.getElementById('reset-btn');
  const logoutBtn = document.getElementById('logout-btn');

  // Reset button event listener
  if (resetBtn) {
    resetBtn.addEventListener('click', async () => {
      if (confirm('Are you sure you want to reset all your goals? This cannot be undone.')) {
        try {
          await resetGoalsData();
          await updateAllCharts();
          alert('All goals have been reset.');
        } catch (error) {
          console.error('Reset failed:', error);
          alert('Failed to reset goals. Please try again.');
        }
      }
    });
  }

  // Logout button event listener
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      window.location.href = '/logout';
    });
  }
}

// Function to fetch and update all charts
async function updateAllCharts() {
  try {
    const [daily, weekly, monthly, yearly,advanced] = await Promise.all([
      fetchContent('daily'),
      fetchContent('weekly'),
      fetchContent('monthly'),
      fetchContent('yearly'),
      fetchContent('advanced')
    ]);

    const allGoals = [...daily, ...weekly, ...monthly, ...yearly];

    updateChart('allGoalsChart', countCompleted(allGoals), allGoals.length, '#673ab7');
    updateChart('dailyChart', countCompleted(daily), daily.length, '#28a745');
    updateChart('weeklyChart', countCompleted(weekly), weekly.length, '#17a2b8');
    updateChart('monthlyChart', countCompleted(monthly), monthly.length, '#ffc107');
    updateChart('yearlyChart', countCompleted(yearly), yearly.length, '#dc3545');
    
  } catch (error) {
    console.error('Error updating charts:', error);
    alert('Failed to load or update charts. Please try again later.');
  }
}

// Function to count completed goals
function countCompleted(goals) {
  return goals.filter(g => g.completed).length;
}

// Function to update chart
function updateChart(canvasId, completed, total, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');

  if (charts[canvasId]) {
    charts[canvasId].destroy(); // Destroy previous chart instance if it exists
  }

  charts[canvasId] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'Incomplete'],
      datasets: [{
        data: [completed, total - completed],
        backgroundColor: [color, '#e0e0e0'],
        borderWidth: 2
      }]
    },
    options: {
      cutout: '70%',
      animation: {
        animateRotate: true,
        animateScale: true
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.parsed}`;
            }
          }
        }
      }
    }
  });
}
