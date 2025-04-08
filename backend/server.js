const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const cookieParser = require("cookie-parser");
const path = require("path");
const morgan = require("morgan");
const jwt = require("jsonwebtoken");
const rateLimit = require("express-rate-limit");
const helmet = require("helmet");
const mongoSanitize = require("express-mongo-sanitize");
const xss = require("xss-clean");
const secrets = require("./src/config/secrets"); // Use secrets for better management
const habitRoutes = require("./src/routes/habitRoutes");
const userRoutes = require("./src/routes/userRoutes");
const authRoutes = require("./src/routes/authRoutes");

dotenv.config();
const app = express();
const PORT = process.env.PORT || 5000;

// === JWT Configuration ===
const JWT_SECRET = secrets.JWT_SECRET; // Use secrets for JWT secret management
const JWT_REFRESH_SECRET = secrets.JWT_REFRESH_SECRET; // Use secrets for refresh secret management

// === Security Middleware ===
app.use(helmet());
app.use(
  cors({
    credentials: true,
    origin: process.env.CLIENT_URL || "http://localhost:3000",
  })
);
app.use(express.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use(mongoSanitize());
app.use(xss());

// === Logging Middleware ===
app.use(morgan(process.env.NODE_ENV === "development" ? "dev" : "tiny"));

// === Rate Limiting ===
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { message: "Too many login attempts. Try again later." },
});
app.use("/auth/login", loginLimiter);

// === Authentication Middleware ===
const authenticateUser = (req, res, next) => {
  const token = req.cookies.token || req.headers.authorization?.split(" ")[1];
  if (!token)
    return res.status(401).json({ message: "Unauthorized. Token required." });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err)
      return res.status(403).json({ message: "Forbidden. Invalid token." });
    req.user = user;
    next();
  });
};

// === Role-Based Access Control ===
const authorizeRole = (roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res
      .status(403)
      .json({ message: "Forbidden. Insufficient privileges." });
  }
  next();
};

// === Token Refresh System ===
app.post("/auth/refresh", async (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken)
    return res.status(400).json({ message: "No refresh token provided." });

  try {
    const results = await db.query(
      "SELECT * FROM refresh_tokens WHERE token = ?",
      [refreshToken]
    );
    if (results.length === 0)
      return res.status(403).json({ message: "Invalid refresh token." });

    jwt.verify(refreshToken, JWT_REFRESH_SECRET, (err, user) => {
      if (err)
        return res.status(403).json({ message: "Token expired or invalid." });

      const newAccessToken = jwt.sign(
        { id: user.id, role: user.role },
        JWT_SECRET,
        { expiresIn: "14m" }
      );
      res.json({ accessToken: newAccessToken });
    });
  } catch (err) {
    res.status(500).json({ message: "Database error during token refresh." });
  }
});

// === Logout Route ===
app.post("/auth/logout", authenticateUser, async (req, res) => {
  const { refreshToken } = req.body;
  try {
    await db.query("DELETE FROM refresh_tokens WHERE token = ?", [
      refreshToken,
    ]);
    res.clearCookie("token", {
      httpOnly: true,
      secure: true,
      sameSite: "Strict",
    });
    res.json({ message: "Successfully logged out." });
  } catch (err) {
    res.status(500).json({ message: "Error during logout." });
  }
});

// === Database Connection with Retry Logic ===
const connectToDatabase = async () => {
  try {
    if (process.env.DB_TYPE === "mongodb") {
      await connectMongoDB();
    } else if (process.env.DB_TYPE === "mysql") {
      db.connect((err) => {
        if (err) {
          console.error("❌ MySQL Connection Error:", err);
          setTimeout(connectToDatabase, 5000); // Retry after 5 seconds
        } else {
          console.log("✅ MySQL Connected");
        }
      });
    }
  } catch (err) {
    console.error("❌ Database connection error:", err);
    setTimeout(connectToDatabase, 5000); // Retry after 5 seconds
  }
};
app.get("/", (req, res) => {
  res.send(
    `hello world. welcome to the home page ${new Date().toLocaleTimeString()}`
  );
});

// === API Routes ===
app.use("/auth", authRoutes);
app.use("/api/habits", authenticateUser, habitRoutes);
app.use("/api/users", authenticateUser, authorizeRole(["admin"]), userRoutes);

// === Centralized Error Handling ===
app.use((err, req, res, next) => {
  console.error("❌ Error:", err.message);
  res
    .status(err.status || 500)
    .json({ message: err.message || "Internal Server Error" });
});

// === Health Check ===
app.get("/health", (req, res) => {
  res.send("✅ API is running smoothly");
});

// === Graceful Shutdown ===
process.on("SIGINT", () => {
  console.log("\nGracefully shutting down...");
  db.close(); // Close MySQL pool
  connectMongoDB.disconnect(); // Close MongoDB connection if needed
  process.exit();
});

// === Start Server ===
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});

module.exports = app;
