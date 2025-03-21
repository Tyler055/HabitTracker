const Habit = require("../models/Habit");
const db = require("../config/mysqlDB");

// Get all habits
exports.getHabits = async (req, res) => {
  if (process.env.DB_TYPE === "mongodb") {
    try {
      const habits = await Habit.find({ user: req.user.id });
      res.json(habits);
    } catch (error) {
      res.status(500).json({ message: "Server Error" });
    }
  } else {
    db.query("SELECT * FROM habits", (err, results) => {
      if (err) return res.status(500).send(err);
      res.json(results);
    });
  }
};

// Add a habit
exports.createHabit = async (req, res) => {
  const { name, description } = req.body;
  
  if (process.env.DB_TYPE === "mongodb") {
    try {
      const newHabit = new Habit({ name, description, user: req.user.id });
      await newHabit.save();
      res.status(201).json(newHabit);
    } catch (error) {
      res.status(500).json({ message: "Server Error" });
    }
  } else {
    db.query(
      "INSERT INTO habits (name, description) VALUES (?, ?)",
      [name, description],
      (err, results) => {
        if (err) return res.status(500).send(err);
        res.json({ message: "✅ Habit added successfully!", id: results.insertId });
      }
    );
  }
};
