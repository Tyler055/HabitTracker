// home.js

import { fetchContent, resetGoalsData } from './saveData.js';

let charts = {};

document.addEventListener('DOMContentLoaded', () => {
  console.log('Home.js loaded');
  setupButtons();
  updateAllCharts();
});

// Setup the reset and logout buttons
function setupButtons() {
  const actions = [
    { 
      id: 'reset-btn', 
      handler: async () => {
        if (confirm('Reset all goals? This cannot be undone.')) {
          try {
            await resetGoalsData();
            await updateAllCharts(); // Refresh charts after reset
            alert('All goals have been reset.');
          } catch (err) {
            console.error('Reset failed:', err);
            alert('Error resetting goals. Please try again.');
          }
        }
      }
    },
    { 
      id: 'logout-btn', 
      handler: () => window.location.href = '/logout'
    }
  ];

  // Attach event listeners to the buttons
  actions.forEach(({ id, handler }) => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', handler);
  });
}

// Update all charts with the latest goal data
async function updateAllCharts() {
  try {
    const categories = [
      { name: 'daily', color: '#28a745' },
      { name: 'weekly', color: '#17a2b8' },
      { name: 'monthly', color: '#ffc107' },
      { name: 'yearly', color: '#dc3545' }
    ];

    let allGoals = [];

    // Fetch goals for each category and update respective charts
    for (const { name, color } of categories) {
      const goals = await fetchContent(name);
      allGoals = [...allGoals, ...goals];
      updateChart(`${name}Chart`, goals, color);
    }

    // Create a combined chart for all goals
    updateChart('allGoalsChart', allGoals, '#673ab7');

  } catch (err) {
    console.error('Error updating charts:', err);
    alert('Failed to update charts. Please try again.');
  }
}

// Count the number of completed goals
function countCompleted(goals) {
  return goals.filter(g => g.completed).length;
}

// Update the chart with goal data for a given category
function updateChart(canvasId, goals, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const completed = countCompleted(goals);
  const total = goals.length;
  const percent = total ? Math.round((completed / total) * 100) : 0;

  // Destroy the old chart before creating a new one
  try {
    if (charts[canvasId]) charts[canvasId].destroy();
  } catch (err) {
    console.error('Error destroying chart:', err);
  }

  // Create a new doughnut chart
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
      animation: { animateRotate: true, animateScale: true },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ({ label, parsed }) => {
              const percentLabel = total ? Math.round((parsed / total) * 100) : 0;
              return `${label}: ${parsed} (${percentLabel}%)`;
            }
          }
        },
        doughnutLabel: {
          labels: [{ 
            text: percent + '%', 
            font: { size: '28', weight: 'bold' }, 
            color 
          }]
        }
      }
    },
    plugins: [doughnutCenterText]
  });
}

// Custom plugin to draw center text on doughnut charts
const doughnutCenterText = {
  id: 'doughnutCenterText',
  beforeDraw(chart) {
    const { width, height } = chart;
    const ctx = chart.ctx;
    const text = chart.config.options.plugins.doughnutLabel.labels[0].text;

    ctx.save();
    ctx.font = `${(height / 8).toFixed(0)}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = chart.config.options.plugins.doughnutLabel.labels[0].color;

    // Draw the percentage text in the center of the doughnut
    ctx.fillText(text, width / 2, height / 2);
    ctx.restore();
  }
};
