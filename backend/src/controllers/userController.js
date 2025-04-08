const User = require("../models/User");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const config = require("../config/env");

exports.registerUser = async (req, res) => {
  try {
    const { username, email, password } = req.body;
    let user = await User.findOne({ email });
    if (user) return res.status(400).json({ message: "User already exists" });

    const hashedPassword = await bcrypt.hash(password, 10);
    user = new User({ username, email, password: hashedPassword });
    await user.save();

    const token = jwt.sign({ id: user.id }, config.JWT_SECRET, {
      expiresIn: "7d",
    });

    res.status(201).json({ token, user: { id: user.id, username, email } });
  } catch (error) {
    res.status(500).json({ message: "Server Error" });
  }
};
