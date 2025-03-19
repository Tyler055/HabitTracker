const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json()); // To parse JSON bodies

// MySQL Connection (Using Environment Variables)
const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",   
    user: process.env.DB_USER || "root",        
    password: process.env.DB_PASSWORD || "password", 
    database: process.env.DB_NAME || "habit_tracker"
});

db.connect((err) => {
    if (err) {
        console.error("❌ Database connection failed: ", err);
        return;
    }
    console.log("✅ Connected to MySQL Database");
});

// Routes
app.get("/", (req, res) => {
    res.send("Welcome to the Habit Tracker API");
});

// Get all habits
app.get("/habits", (req, res) => {
    db.query("SELECT * FROM habits", (err, results) => {
        if (err) return res.status(500).send(err);
        res.json(results);
    });
});

// Add a new habit
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

// Delete a habit
app.delete("/habits/:id", (req, res) => {
    const { id } = req.params;
    db.query("DELETE FROM habits WHERE id = ?", [id], (err, results) => {
        if (err) return res.status(500).send(err);
        res.json({ message: "✅ Habit deleted successfully!" });
    });
});

// Start Server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
