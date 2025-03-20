const Habit = require("../models/Habit");

// Get all habits for a user
exports.getHabits = async (req, res) => {
  try {
    const habits = await Habit.find({ user: req.user.id });
    res.json(habits);
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Create a new habit
exports.createHabit = async (req, res) => {
  try {
    const { name, description } = req.body;
    const newHabit = new Habit({ name, description, user: req.user.id });
    await newHabit.save();
    res.status(201).json(newHabit);
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Mark habit as completed
exports.completeHabit = async (req, res) => {
  try {
    const habit = await Habit.findById(req.params.id);
    if (!habit) return res.status(404).json({ message: "Habit not found" });

    habit.lastCompleted = new Date();
    habit.streak += 1;
    await habit.save();

    res.json(habit);
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};
