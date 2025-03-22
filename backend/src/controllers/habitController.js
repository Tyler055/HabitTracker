const Habit = require("../models/Habit");
const db = require("../config/env");  // MySQL DB connection

// Validate input data
const validateHabitInput = (name, description) => {
  if (!name || !description) {
    return { valid: false, message: "Name and description are required" };
  }
  return { valid: true };
};

// Get all habits
exports.getHabits = async (req, res) => {
  try {
    let habits;
    if (process.env.DB_TYPE === "mongodb") {
      // MongoDB logic
      habits = await Habit.find({ user: req.user.id });
    } else {
      // MySQL logic
      const [results] = await db.query("SELECT * FROM habits WHERE user_id = ?", [req.user.id]);
      habits = results;
    }

    if (!habits || habits.length === 0) {
      return res.status(404).json({ success: false, message: "No habits found" });
    }

    res.json({ success: true, data: habits });
  } catch (error) {
    console.error("❌ Error fetching habits:", error);
    res.status(500).json({ success: false, message: "Server Error" });
  }
};

// Add a habit
exports.createHabit = async (req, res) => {
  const { name, description } = req.body;

  // Validate input data
  const { valid, message } = validateHabitInput(name, description);
  if (!valid) {
    return res.status(400).json({ success: false, message });
  }

  try {
    let newHabit;
    if (process.env.DB_TYPE === "mongodb") {
      // MongoDB logic
      newHabit = new Habit({ name, description, user: req.user.id });
      await newHabit.save();
    } else {
      // MySQL logic
      const [results] = await db.query("INSERT INTO habits (name, description, user_id) VALUES (?, ?, ?)", 
        [name, description, req.user.id]);
      newHabit = { id: results.insertId, name, description, user_id: req.user.id };
    }

    res.status(201).json({
      success: true,
      message: "✅ Habit added successfully!",
      data: newHabit,
    });
  } catch (error) {
    console.error("❌ Error creating habit:", error);
    res.status(500).json({ success: false, message: "Server Error" });
  }
};
