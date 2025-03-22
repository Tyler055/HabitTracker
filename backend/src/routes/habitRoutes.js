const express = require("express");
const { getHabits, createHabit } = require("../controllers/habitController");
const authMiddleware = require("../middleware/authMiddleware");

const router = express.Router();

// Route to get all habits
router.get("/", authMiddleware, async (req, res, next) => {
  try {
    await getHabits(req, res);
  } catch (err) {
    next(err);  // In case of any unhandled error, pass it to the error handler
  }
});

// Route to create a new habit
router.post("/", authMiddleware, async (req, res, next) => {
  try {
    await createHabit(req, res);
  } catch (err) {
    next(err);  // Handle errors if the habit creation fails
  }
});

module.exports = router;
