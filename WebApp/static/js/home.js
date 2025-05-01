import { fetchContent, resetGoalsData } from './saveData.js';

let charts = {};
let chartPercentages = {};

// Register the center text plugin once
Chart.register({
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { left, right, top, bottom, width, height } } = chart;
    const canvasId = chart.canvas.id;
    const percentage = chartPercentages[canvasId] || 0;
    
    // Calculate the center of the chart area
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

document.addEventListener('DOMContentLoaded', () => {
  console.log('Home.js loaded ');
  setupButtons();
  updateAllCharts();
});

function setupButtons() {
  const resetBtn = document.getElementById('reset-btn');
  const logoutBtn = document.getElementById('logout-btn');

  if (resetBtn) {
    resetBtn.addEventListener('click', async () => {
      if (confirm('Are you sure you want to reset all your goals? This cannot be undone.')) {
        try {
          await resetGoalsData();
          await updateAllCharts();
          alert('All goals have been reset.');
        } catch (error) {
          console.error('Reset failed:', error);
        }
      }
    });
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      window.location.href = '/logout';
    });
  }
}

async function updateAllCharts() {
  try {
    const daily = await fetchContent('daily');
    const weekly = await fetchContent('weekly');
    const monthly = await fetchContent('monthly');
    const yearly = await fetchContent('yearly');

    const allGoals = [...daily, ...weekly, ...monthly, ...yearly];

    updateChart('allGoalsChart', countCompleted(allGoals), allGoals.length, '#673ab7');
    updateChart('dailyChart', countCompleted(daily), daily.length, '#28a745');
    updateChart('weeklyChart', countCompleted(weekly), weekly.length, '#17a2b8');
    updateChart('monthlyChart', countCompleted(monthly), monthly.length, '#ffc107');
    updateChart('yearlyChart', countCompleted(yearly), yearly.length, '#dc3545');
    
  } catch (error) {
    console.error('Error updating charts:', error);
  }
}

function countCompleted(goals) {
  return goals.filter(g => g.completed).length;
}

function updateChart(canvasId, completed, total, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
  
  // Store the percentage for this chart
  chartPercentages[canvasId] = percentage;

  if (charts[canvasId]) {
    charts[canvasId].destroy();
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
  });
}
