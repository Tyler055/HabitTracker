// saveData.js — All network/API calls are managed here

/**
 * Handle errors from fetch responses.
 * @param {Response} response - The fetch response object
 * @returns {Promise<any>} - Parsed JSON if successful, otherwise throws an error
 */
async function handleFetchError(response) {
  if (!response.ok) {
    const errorMessage = await response.text();
    throw new Error(errorMessage || response.statusText);
  }
  return response.json();
}

/**
 * Fetch goals from the server for a specific category.
 * @param {string} category - One of: 'daily', 'weekly', 'monthly', 'yearly'
 * @returns {Promise<Array>} - Array of goal objects
 */
export async function fetchContent(category) {
  try {
    const response = await fetch(`/api/goals?category=${encodeURIComponent(category)}`);
    return await handleFetchError(response);
  } catch (error) {
    console.error(`Error fetching goals for ${category}:`, error.message);
    throw error;
  }
}

/**
 * Save an array of goals to the server for a given category.
 * @param {string} category - The goal category (e.g., 'daily')
 * @param {Array<Object>} goalsList - List of goal objects
 * @returns {Promise<void>}
 */
export async function saveGoalsData(category, goalsList) {
  try {
    const response = await fetch(`/api/goals?category=${encodeURIComponent(category)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ goals: goalsList })
    });
    await handleFetchError(response);
  } catch (error) {
    console.error(`Error saving goals for ${category}:`, error.message);
    throw error;
  }
}

/**
 * Reset all goals for the current user across all categories.
 * @returns {Promise<void>}
 */
export async function resetGoalsData() {
  try {
    const response = await fetch('/api/reset', {
      method: 'POST'
    });
    await handleFetchError(response);
  } catch (error) {
    console.error('Error resetting goals data:', error.message);
    throw error;
  }
}
