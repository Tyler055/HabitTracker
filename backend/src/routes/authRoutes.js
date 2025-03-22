// routes/authRoutes.js
const express = require("express");
const { check } = require("express-validator");
const {
  register,
  login,
  refreshToken,
  logout,
} = require("../controllers/authController");

const router = express.Router();

router.post(
  "/register",
  [
    check("email", "Please include a valid email").isEmail(),
    check("password", "Password must be 6 or more characters").isLength({
      min: 6,
    }),
  ],
  register
);

router.post(
  "/login",
  [
    check("email", "Please include a valid email").isEmail(),
    check("password", "Password is required").exists(),
  ],
  login
);

router.post("/refresh", refreshToken);
router.post("/logout", logout);

module.exports = router;
