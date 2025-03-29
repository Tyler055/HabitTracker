import React, { useEffect, useState } from 'react';

const HabitTracker = () => {
  const [habit, setHabit] = useState('');
  const [habits, setHabits] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  const fetchHabits = () => {
    fetch('/')
      .then(res => res.json())
      .then(data => setHabits(data))
      .catch(() => setErrorMessage('Failed to fetch habits.'));
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!habit.trim()) return;

    fetch('/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ habit_name: habit }),
    })
      .then(res => res.ok ? fetchHabits() : alert('Error adding habit'))
      .catch(() => setErrorMessage('Failed to add habit.'));

    setHabit('');
  };

  const deleteHabit = (id) => {
    fetch(`/delete/${id}`, { method: 'GET' })
      .then(res => res.ok ? fetchHabits() : alert('Error deleting habit'))
      .catch(() => setErrorMessage('Failed to delete habit.'));
  };

  const resetHabits = () => {
    setErrorMessage('');
    fetch('/reset_habits', { method: 'POST' })
      .then(res => {
        if (!res.ok) throw new Error();
        fetchHabits();
      })
      .catch(() => setErrorMessage('Failed to reset habits.'));
  };

  return (
    <div>
      <h2>Track Your Habits</h2>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="input-box"
          placeholder="Add new habit"
          value={habit}
          onChange={(e) => setHabit(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>

      <div className="habit-list">
        {habits.length > 0 ? (
          habits.map((h) => (
            <div key={h.id} className="habit-item">
              <span>{h.name}</span>
              <button className="delete-btn" onClick={() => deleteHabit(h.id)}>Delete</button>
            </div>
          ))
        ) : (
          <p>No habits found.</p>
        )}
      </div>

      <button onClick={resetHabits}>Reset Habits</button>
    </div>
  );
};

export default HabitTracker;
