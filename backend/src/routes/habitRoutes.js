const express = require("express");
const { getHabits, createHabit } = require("../controllers/habitController");
const authMiddleware = require("../middleware/authMiddleware");

const router = express.Router();

// Route to get all habits
router.get("/", authMiddleware, getHabits);

// Route to create a new habit
router.post("/", authMiddleware, createHabit);

module.exports = router;
