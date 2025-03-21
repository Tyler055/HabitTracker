const mongoose = require('mongoose');

// Schema definition
const habitSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  description: {
    type: String,
  },
  createdAt: {
    type: Date,
    default: Date.now, // Default to the current date when the habit is created
  },
  lastCompleted: {
    type: Date, // Tracks the last completion date
    default: null,
  },
  progress: [
    {
      date: { type: Date, default: Date.now }, // Date of habit completion
      completed: { type: Boolean, default: false }, // Whether the habit was completed that day
    },
  ],
  streak: {
    type: Number,
    default: 0, // Tracks consecutive habit completions
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User", // Links the habit to a specific user
  },
});

const Habit = mongoose.model("Habit", habitSchema);

module.exports = Habit;
