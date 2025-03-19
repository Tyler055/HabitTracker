const express = require("express");
const { getHabits, createHabit, completeHabit } = require("../controllers/habitController");
const authMiddleware = require("../middleware/authMiddleware");

const router = express.Router();

router.get("/", authMiddleware, getHabits);
router.post("/", authMiddleware, createHabit);
router.put("/:id/complete", authMiddleware, completeHabit);

module.exports = router;
