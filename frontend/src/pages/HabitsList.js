// HabitList.jsx
import React from "react";

const HabitList = ({
  habits,
  editingHabitId,
  editedHabitName,
  setEditingHabitId,
  setEditedHabitName,
  handleEditHabit,
  handleDeleteHabit,
  handleCompleteHabit,
}) => {
  return (
    <ul className="space-y-2">
      {habits.map((habit) => (
        <li
          key={habit.id}
          className="flex items-center justify-between bg-white p-3 rounded shadow"
        >
          {editingHabitId === habit.id ? (
            <input
              value={editedHabitName}
              onChange={(e) => setEditedHabitName(e.target.value)}
              onBlur={() => handleEditHabit(habit.id)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleEditHabit(habit.id);
              }}
              autoFocus
              className="border rounded px-2 py-1 w-full"
            />
          ) : (
            <span
              onClick={() => {
                setEditingHabitId(habit.id);
                setEditedHabitName(habit.name);
              }}
              className="cursor-pointer w-full"
            >
              {habit.name}
            </span>
          )}

          <div className="flex items-center space-x-2 ml-4">
            {habit.completed_today && (
              <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
                Completed Today
              </span>
            )}
            <button
              onClick={() => handleCompleteHabit(habit.id)}
              className="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-sm"
            >
              Complete
            </button>
            <button
              onClick={() => handleDeleteHabit(habit.id)}
              className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm"
            >
              Delete
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
};

export default HabitList;
