const Habit = require("../models/Habit");
const db = require("../config/env");  // MySQL DB connection

// Get all habits
exports.getHabits = async (req, res) => {
  if (process.env.DB_TYPE === "mongodb") {
    try {
      // MongoDB query to get habits for the logged-in user
      const habits = await Habit.find({ user: req.user.id });
      res.json(habits);
    } catch (error) {
      console.error("❌ Error fetching habits from MongoDB:", error);
      res.status(500).json({ message: "Server Error" });
    }
  } else {
    // MySQL query to fetch all habits
    db.query("SELECT * FROM habits", (err, results) => {
      if (err) {
        console.error("❌ Error fetching habits from MySQL:", err);
        return res.status(500).json({ message: "Server Error" });
      }
      res.json(results);  // Send the results as a JSON response
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
      res.status(201).json(newHabit); // Return the newly created habit
    } catch (error) {
      console.error("❌ Error creating habit in MongoDB:", error);
      res.status(500).json({ message: "Server Error" });
    }
  } else {
    db.query(
      "INSERT INTO habits (name, description) VALUES (?, ?)",
      [name, description],
      (err, results) => {
        if (err) {
          console.error("❌ Error creating habit in MySQL:", err);
          return res.status(500).send(err);
        }
        res.json({
          message: "✅ Habit added successfully!",
          id: results.insertId,
        });
      }
    );
  }
};
