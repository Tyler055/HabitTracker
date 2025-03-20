const User = require("../models/User");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const config = require("../config/env");

// Register a new user
exports.registerUser = async (req, res) => {
  try {
    const { username, email, password } = req.body;
    let user = await User.findOne({ email });
    if (user) return res.status(400).json({ message: "User already exists" });

    user = new User({ username, email, password });
    await user.save();

    const token = jwt.sign({ id: user.id }, config.JWT_SECRET, { expiresIn: "7d" });

    res.status(201).json({ token, user: { id: user.id, username, email } });
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Login a user
exports.loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(400).json({ message: "Invalid credentials" });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ message: "Invalid credentials" });

    const token = jwt.sign({ id: user.id }, config.JWT_SECRET, { expiresIn: "7d" });

    res.json({ token, user: { id: user.id, username: user.username, email } });
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};
