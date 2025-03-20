const mongoose = require("mongoose");

const HabitSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String },
  createdAt: { type: Date, default: Date.now },
  lastCompleted: { type: Date, default: null },
  streak: { type: Number, default: 0 },
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
});

module.exports = mongoose.model("Habit", HabitSchema);
