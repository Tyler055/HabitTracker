// saveData.js

// Generic function to handle API requests
export function request(url, options = {}) {
  return fetch(url, options)
    .then(res => {
      if (!res.ok) {
        throw new Error(`Request failed: ${res.statusText}`);
      }
      return res.json(); // Automatically parse JSON response
    })
    .catch(error => {
      console.error(error);
      throw error;
    });
}

// Fetch content for a specific goal category (e.g., daily, weekly)
export function fetchContent(category) {
  const url = `/api/goals?category=${encodeURIComponent(category)}`;
  return request(url);
}

// Save the list of goals for a specific category
export function saveGoalsData(category, goalsList) {
  const url = `/api/goals?category=${encodeURIComponent(category)}`;
  return request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ goals: goalsList })
  }).then(() => {
    console.log('Goals saved successfully');
  });
}

// Reset all goals data
export function resetGoalsData() {
  return request('/api/reset', { method: 'POST' })
    .then(() => {
      console.log('Goals reset successfully');
    });
}

// Load HTML content from a URL (optional)
export function loadHTML(url) {
  return request(url)
    .then(res => res);  // Just return the HTML content
}
