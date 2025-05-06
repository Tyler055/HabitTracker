import { fetchContent, resetGoalsData } from './saveData.js';

// Chart storage
let charts = {};
let chartPercentages = {};

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('Home.js loaded');
  loadGoals();
  bindGoalForm();
  setupDragAndDrop();
  setupKeyboardDragAndDrop();
  setupButtons();
  updateAllCharts();
});

// Setup buttons
function setupButtons() {
  const resetBtn = document.getElementById('reset-btn');
  const logoutBtn = document.getElementById('logout-btn');

  if (resetBtn) resetBtn.addEventListener('click', handleResetClick);
  if (logoutBtn) logoutBtn.addEventListener('click', () => window.location.href = '/logout');
}

// Handle goal reset
async function handleResetClick() {
  if (confirm('Are you sure you want to reset all your goals? This cannot be undone.')) {
    try {
      updateAllCharts();
      await resetGoalsData();
      alert('All goals have been reset.');
    } catch (error) {
      console.error('Reset failed:', error);
      alert('Failed to reset goals. Please try again.');
    }
  }
}

// Fetch and update all charts
async function updateAllCharts() {
  try {
    const [daily, weekly, monthly, yearly] = await Promise.all([
      fetchContent('daily'),
      fetchContent('weekly'),
      fetchContent('monthly'),
      fetchContent('yearly')
    ]);

    const allGoals = [...daily, ...weekly, ...monthly, ...yearly];
    const datasets = {
      allGoals: { data: allGoals, color: '#673ab7' },
      daily: { data: daily, color: '#28a745' },
      weekly: { data: weekly, color: '#17a2b8' },
      monthly: { data: monthly, color: '#ffc107' },
      yearly: { data: yearly, color: '#dc3545' }
    };

    Object.keys(datasets).forEach(key => {
      const { data, color } = datasets[key];
      updateChartData(`${key}Chart`, countCompleted(data), data.length, color);
    });

  } catch (error) {
    console.error('Chart update error:', error);
    alert('Failed to load charts. Try again later.');
  }
}

function countCompleted(goals) {
  return goals.filter(g => g.completed).length;
}

function updateChartData(canvasId, completed, total, color) {
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return;

  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
  chartPercentages[canvasId] = percentage;

  if (charts[canvasId]) charts[canvasId].destroy();

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
            label: context => `${context.label}: ${context.parsed}`
          }
        },
        centerText: true
      },
      layout: { padding: { top: 20, bottom: 20 } }
    }
  });
}

// Chart.js center text plugin
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

// Placeholder: load goals from backend
function loadGoals() {
  // implement fetching and displaying goals in the DOM
  console.log('Loading goals...');
}

// Placeholder: bind the goal form logic
function bindGoalForm() {
  // implement form submission logic
  console.log('Binding goal form...');
}

// Drag and Drop Logic (Mouse)
function setupDragAndDrop() {
  let dragged;

  document.querySelectorAll('.goal').forEach(goal => {
    goal.setAttribute('draggable', true);

    goal.addEventListener('dragstart', e => {
      dragged = e.target;
      e.target.classList.add('dragging');
    });

    goal.addEventListener('dragend', e => {
      e.target.classList.remove('dragging');
    });
  });

  document.querySelectorAll('.goal-column').forEach(col => {
    col.addEventListener('dragover', e => {
      e.preventDefault();
      const dragging = document.querySelector('.dragging');
      col.appendChild(dragging);
    });
  });
}

// Drag and Drop Logic (Keyboard)
function setupKeyboardDragAndDrop() {
  let selected = null;

  document.querySelectorAll('.goal').forEach(goal => {
    goal.setAttribute('tabindex', 0);

    goal.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        if (!selected) {
          selected = e.target;
          selected.classList.add('dragging');
        } else if (selected === e.target) {
          selected.classList.remove('dragging');
          selected = null;
        }
      } else if (selected && ['ArrowRight', 'ArrowLeft'].includes(e.key)) {
        const currentCol = selected.closest('.goal-column');
        const columns = Array.from(document.querySelectorAll('.goal-column'));
        const currentIndex = columns.indexOf(currentCol);
        const newIndex = e.key === 'ArrowRight' ? currentIndex + 1 : currentIndex - 1;

        if (columns[newIndex]) {
          columns[newIndex].appendChild(selected);
          selected.classList.remove('dragging');
          selected = null;
        }
      }
    });
  });
}
