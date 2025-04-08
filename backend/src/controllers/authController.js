const jwt = require("jsonwebtoken");

const register = async (req, res) => {
  const { email, password } = req.body;

  // TODO: Save user to database after hashing the password
  const user = { id: 1, email, role: "user" };

  const accessToken = jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: "15m" }
  );
  const refreshToken = jwt.sign(
    { id: user.id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: "7d" }
  );

  res.cookie("token", accessToken, {
    httpOnly: true,
    sameSite: "Strict",
    secure: process.env.NODE_ENV === "production",
    maxAge: 15 * 60 * 1000,
  });

  res.cookie("refreshToken", refreshToken, {
    httpOnly: true,
    sameSite: "Strict",
    secure: process.env.NODE_ENV === "production",
    maxAge: 7 * 24 * 60 * 60 * 1000,
  });

  res.json({ message: "User registered successfully" });
};

const login = async (req, res) => {
  const { email, password } = req.body;

  // Example user
  const user = { id: 1, email, role: "admin" };

  // TODO: Verify password, etc.
  const accessToken = jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: "15m" }
  );
  const refreshToken = jwt.sign(
    { id: user.id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: "7d" }
  );

  res.cookie("token", accessToken, {
    httpOnly: true,
    sameSite: "Strict",
    secure: process.env.NODE_ENV === "production",
    maxAge: 15 * 60 * 1000,
  });

  res.cookie("refreshToken", refreshToken, {
    httpOnly: true,
    sameSite: "Strict",
    secure: process.env.NODE_ENV === "production",
    maxAge: 7 * 24 * 60 * 60 * 1000,
  });

  res.json({ message: "Login successful" });
};

const refreshToken = (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  if (!refreshToken)
    return res.status(401).json({ message: "No refresh token provided" });

  try {
    const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);
    const newAccessToken = jwt.sign(
      { id: payload.id, role: payload.role },
      process.env.JWT_SECRET,
      { expiresIn: "15m" }
    );

    res.cookie("token", newAccessToken, {
      httpOnly: true,
      sameSite: "Strict",
      secure: process.env.NODE_ENV === "production",
      maxAge: 15 * 60 * 1000,
    });

    res.json({ message: "Access token refreshed" });
  } catch (err) {
    res.status(403).json({ message: "Invalid refresh token" });
  }
};

const logout = (req, res) => {
  res.clearCookie("token");
  res.clearCookie("refreshToken");
  res.json({ message: "Logged out successfully" });
};

module.exports = { register, login, refreshToken, logout };
