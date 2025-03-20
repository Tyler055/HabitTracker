// HabitContext.js

import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { fetchHabits, addHabit, deleteHabit, updateStreak } from '../services/habitService';

const HabitContext = createContext();

export const useHabits = () => useContext(HabitContext);

export const HabitProvider = ({ children }) => {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(false);

  const getHabits = useCallback(async () => {
    setLoading(true);
    try {
      const fetchedHabits = await fetchHabits();
      setHabits(fetchedHabits);
    } catch (error) {
      console.error('Error fetching habits:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    getHabits();
  }, [getHabits]);

  const handleAddHabit = async (habit) => {
    const newHabit = await addHabit(habit);
    setHabits((prevHabits) => [...prevHabits, newHabit]);
  };

  const handleDeleteHabit = async (habitId) => {
    await deleteHabit(habitId);
    setHabits((prevHabits) => prevHabits.filter((habit) => habit.id !== habitId));
  };

  const handleUpdateStreak = async (habitId, streak) => {
    await updateStreak(habitId, streak);
    setHabits((prevHabits) =>
      prevHabits.map((habit) =>
        habit.id === habitId ? { ...habit, streak } : habit
      )
    );
  };

  return (
    <HabitContext.Provider value={{ habits, loading, handleAddHabit, handleDeleteHabit, handleUpdateStreak }}>
      {children}
    </HabitContext.Provider>
  );
};
