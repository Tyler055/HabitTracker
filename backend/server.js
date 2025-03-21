const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const connectMongoDB = require("./config/mongoDB"); // MongoDB connection
const connectMySQL = require("./config/mysql"); // MySQL connection
const habitRoutes = require("./routes/habitRoutes");
const userRoutes = require("./routes/userRoutes");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Database Connections
if (process.env.DB_TYPE === "mongodb") {
  connectMongoDB(); // MongoDB
} else {
  const db = connectMySQL(); // MySQL
  // Example MySQL routes (optional)
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
        res.json({ message: "✅ Habit added successfully!", id: results.insertId });
      }
    );
  });

  app.delete("/habits/:id", (req, res) => {
    const { id } = req.params;
    db.query("DELETE FROM habits WHERE id = ?", [id], (err, results) => {
      if (err) return res.status(500).send(err);
      res.json({ message: "✅ Habit deleted successfully!" });
    });
  });
}

// Custom API Routes (for Mongo or shared logic)
app.use("/api/habits", habitRoutes);
app.use("/api/users", userRoutes);

// Default route
app.get("/", (req, res) => {
  res.send("Welcome to the Habit Tracker API");
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
