// saveData.js — all network calls here

// Fetch content for a specific goal category (e.g., daily, weekly)
export function fetchContent(category) {
  return fetch(`/api/goals?category=${encodeURIComponent(category)}`)
    .then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    });
}

// Save the list of goals for a specific category
export function saveGoalsData(category, goalsList) {
  return fetch(`/api/goals?category=${encodeURIComponent(category)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ goals: goalsList })
  }).then(res => {
    if (!res.ok) throw new Error(res.statusText);
    return res;
  });
}

// Reset all goals data
export function resetGoalsData() {
  return fetch('/api/reset', { method: 'POST' })
    .then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res;
    });
}
