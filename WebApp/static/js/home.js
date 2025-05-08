// home.js

import { fetchContent, resetGoalsData } from './saveData.js';

let charts = {};

document.addEventListener('DOMContentLoaded', () => {
  console.log('Home.js loaded');
  setupButtons();
  updateAllCharts();
});

function setupButtons() {
  const actions = [
    { id: 'reset-btn', handler: async () => {
      if (confirm('Reset all goals? This cannot be undone.')) {
        try {
          await resetGoalsData();
          await updateAllCharts();
          alert('All goals have been reset.');
        } catch (err) {
          console.error('Reset failed:', err);
        }
      }
    }},
    { id: 'logout-btn', handler: () => window.location.href = '/logout' }
  ];

  actions.forEach(({ id, handler }) => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', handler);
  });
}

async function updateAllCharts() {
  try {
    const categories = [
      { name: 'daily', color: '#28a745' },
      { name: 'weekly', color: '#17a2b8' },
      { name: 'monthly', color: '#ffc107' },
      { name: 'yearly', color: '#dc3545' }
    ];

    let allGoals = [];

    for (const { name, color } of categories) {
      const goals = await fetchContent(name);
      allGoals = [...allGoals, ...goals];
      updateChart(`${name}Chart`, goals, color);
    }

    updateChart('allGoalsChart', allGoals, '#673ab7');

  } catch (err) {
    console.error('Error updating charts:', err);
  }
}

function countCompleted(goals) {
  return goals.filter(g => g.completed).length;
}

function updateChart(canvasId, goals, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const completed = countCompleted(goals);
  const total = goals.length;
  const percent = total ? Math.round((completed / total) * 100) : 0;

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
            label: ({ label, parsed }) => {
              const percentLabel = total ? Math.round((parsed / total) * 100) : 0;
              return `${label}: ${parsed} (${percentLabel}%)`;
            }
          }
        },
        doughnutLabel: {
          labels: [{ text: percent + '%', font: { size: '28', weight: 'bold' }, color }]
        }
      }
    },
    plugins: [doughnutCenterText]
  });
}

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

    ctx.fillText(text, width / 2, height / 2);

    ctx.restore();
  }
};
