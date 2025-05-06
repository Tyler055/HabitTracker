// saveData.js — all network calls here

// Utility function for handling fetch errors
async function handleFetchError(response) {
  if (!response.ok) {
    const errorMessage = await response.text();
    throw new Error(errorMessage || response.statusText);
  }
  return response.json();
}

// Fetch content for a specific goal category (e.g., daily, weekly)
export async function fetchContent(category) {
  try {
    const response = await fetch(`/api/goals?category=${encodeURIComponent(category)}`);
    return await handleFetchError(response);
  } catch (error) {
    console.error(`Error fetching goals for ${category}:`, error.message);
    throw error;
  }
}

// Save the list of goals for a specific category
export async function saveGoalsData(category, goalsList) {
  try {
    const response = await fetch(`/api/goals?category=${encodeURIComponent(category)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goals: goalsList })
    });
    await handleFetchError(response);
  } catch (error) {
    console.error(`Error saving goals for ${category}:`, error.message);
    throw error;
  }
}

// Reset all goals data
export async function resetGoalsData() {
  try {
    const response = await fetch('/api/reset', { method: 'POST' });
    await handleFetchError(response);
  } catch (error) {
    console.error('Error resetting goals data:', error.message);
    throw error;
  }
}
