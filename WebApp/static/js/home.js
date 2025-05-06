import { fetchContent, resetGoalsData } from './saveData.js';

let charts = {};
let chartPercentages = {};

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
    resetBtn.addEventListener('click', handleResetClick);
  }

  // Logout button event listener
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogoutClick);
  }
}

async function handleResetClick() {
  if (confirm('Are you sure you want to reset all your goals? This cannot be undone.')) {
    try {
      // Optimistically clear the charts
      updateAllCharts();

      await resetGoalsData();
      alert('All goals have been reset.');
    } catch (error) {
      console.error('Reset failed:', error);
      alert('Failed to reset goals. Please try again.');
    }
  }
}

function handleLogoutClick() {
  window.location.href = '/logout';
}

// Function to fetch and update all charts
async function updateAllCharts() {
  try {
    const [daily, weekly, monthly, yearly] = await Promise.all([
      fetchContent('daily'),
      fetchContent('weekly'),
      fetchContent('monthly'),
      fetchContent('yearly')
    ]);

    const allGoals = [...daily, ...weekly, ...monthly, ...yearly];
    const goalsData = {
      allGoals: { data: allGoals, color: '#673ab7' },
      daily: { data: daily, color: '#28a745' },
      weekly: { data: weekly, color: '#17a2b8' },
      monthly: { data: monthly, color: '#ffc107' },
      yearly: { data: yearly, color: '#dc3545' }
    };

    Object.keys(goalsData).forEach(key => {
      const { data, color } = goalsData[key];
      updateChartData(`${key}Chart`, countCompleted(data), data.length, color);
    });
    
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
function updateChartData(canvasId, completed, total, color) {
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return;

  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
  chartPercentages[canvasId] = percentage;

  if (charts[canvasId]) {
    charts[canvasId].destroy();
  }

  charts[canvasId] = new Chart(ctx, createChartOptions(completed, total, color));
}

function createChartOptions(completed, total, color) {
  return {
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
            label: context => `${context.label}: ${context.parsed}`
          }
        },
        centerText: true
      },
      layout: {
        padding: {
          top: 20,
          bottom: 20
        }
      }
    }
  };
}

// Register center text plugin for charts
Chart.register({
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { left, right, top, bottom } } = chart;
    const canvasId = chart.canvas.id;
    const percentage = chartPercentages[canvasId] || 0;

    const centerX = (left + right) / 2;
    const centerY = (top + bottom) / 2;

    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = 'bold 24px Arial';
    ctx.fillStyle = '#333';
    ctx.fillText(`${percentage}%`, centerX, centerY);
    ctx.restore();
  }
});
