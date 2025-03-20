// habitService.js

export const fetchHabits = async () => {
  try {
    const response = await fetch('/api/habits');
    if (!response.ok) throw new Error('Failed to fetch habits');
    return await response.json();
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const addHabit = async (habit) => {
  try {
    const response = await fetch('/api/habits', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(habit),
    });
    if (!response.ok) throw new Error('Failed to add habit');
    return await response.json();
  } catch (error) {
    console.error(error);
  }
};

export const deleteHabit = async (habitId) => {
  try {
    const response = await fetch(`/api/habits/${habitId}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete habit');
  } catch (error) {
    console.error(error);
  }
};

export const updateStreak = async (habitId, streak) => {
  try {
    const response = await fetch(`/api/habits/${habitId}/streak`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ streak }),
    });
    if (!response.ok) throw new Error('Failed to update streak');
  } catch (error) {
    console.error(error);
  }
};
