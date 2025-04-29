// saveData.js — all network calls here
export function loadHTML(url) {
  return fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res.text();
    });
}

export function fetchContent(category) {
  return fetch(`/api/goals?category=${encodeURIComponent(category)}`)
    .then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    });
}

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

export function resetGoalsData() {
  return fetch('/api/reset', { method: 'POST' })
    .then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res;
    });
}