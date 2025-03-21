const express = require("express");
const { getHabits, createHabit } = require("../controllers/habitController");
const authMiddleware = require("../middleware/authMiddleware");

const router = express.Router();

router.get("/", authMiddleware, getHabits);
router.post("/", authMiddleware, createHabit);

module.exports = router;
