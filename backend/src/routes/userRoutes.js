const express = require("express");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs"); // For password hashing
const User = require("../models/User");

const router = express.Router();

// Register route
router.post("/register", async (req, res) => {
  const { username, email, password } = req.body;

  try {
    // Input validation
    if (!username || !email || !password) {
      return res
        .status(400)
        .json({ message: "Please provide all required fields" });
    }

    // Check if user already exists
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ message: "User already exists" });
    }

    // Hash the password before saving it
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create and save new user
    const user = new User({ username, email, password: hashedPassword });
    await user.save();

    // Create JWT token
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
      expiresIn: "1h", // Consider longer expiration times or refresh tokens
    });

    res.status(201).json({ token });
  } catch (error) {
    console.error("❌ Error during registration:", error);
    res.status(500).json({ message: "Server Error" });
  }
});

// Login route
router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  try {
    // Input validation
    if (!email || !password) {
      return res
        .status(400)
        .json({ message: "Please provide both email and password" });
    }

    // Find the user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    // Check if password matches the stored hashed password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    // Create JWT token
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
      expiresIn: "1h", // Consider longer expiration times or refresh tokens
    });

    res.status(200).json({ token });
  } catch (error) {
    console.error("❌ Error during login:", error);
    res.status(500).json({ message: "Server Error" });
  }
});

module.exports = router;
