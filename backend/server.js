// Import dependencies
const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const connectMongoDB = require("./src/config/mongoDB"); // Adjust if needed
const connectMySQL = require("./src/config/mysqlDB"); // MySQL connection
const habitRoutes = require("./src/routes/habitRoutes");
const userRoutes = require("./src/routes/userRoutes");

// Load .env variables
dotenv.config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Database Connections
if (process.env.DB_TYPE === "mongodb") {
  connectMongoDB();
} else if (process.env.DB_TYPE === "mysql") {
  const db = connectMySQL();

  // Example MySQL-based habit routes
  app.get("/habits", (req, res) => {
    db.query("SELECT * FROM habits", (err, results) => {
      if (err) return res.status(500).send(err);
      res.json(results);
    });
  });

  app.post("/habits", (req, res) => {
    const { name, description } = req.body;
    db.query(
      "INSERT INTO habits (name, description) VALUES (?, ?)",
      [name, description],
      (err, results) => {
        if (err) return res.status(500).send(err);
        res.json({
          message: "✅ Habit added successfully!",
          id: results.insertId,
        });
      }
    );
  });

  app.delete("/habits/:id", (req, res) => {
    const { id } = req.params;
    db.query("DELETE FROM habits WHERE id = ?", [id], (err) => {
      if (err) return res.status(500).send(err);
      res.json({ message: "✅ Habit deleted successfully!" });
    });
  });
}

// Custom API Routes (Mongo or shared logic)
app.use("/api/habits", habitRoutes);
app.use("/api/users", userRoutes);

// Health check route
app.get("/", (req, res) => {
  res.send("✅ Welcome to the Habit Tracker API");
});

// Start the server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
