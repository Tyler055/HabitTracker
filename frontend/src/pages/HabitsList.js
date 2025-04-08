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
  const habitsToDisplay = habits.length > 0 ? habits : [];

  return (
    <div>
      {habitsToDisplay.length === 0 && (
        <p className="text-center text-gray-500">No habits available</p>
      )}
      <ul className="space-y-2">
        {habitsToDisplay.map((habit) => (
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

              <input
                type="checkbox"
                checked={habit.completed_today}
                onChange={() => handleCompleteHabit(habit.id)}
                className="form-checkbox h-4 w-4 text-green-500"
              />

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
    </div>
  );
};

export default HabitList;
