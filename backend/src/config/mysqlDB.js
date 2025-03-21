const mysql = require("mysql");
require("dotenv").config();

const db = mysql.createConnection({
  host: process.env.DB_HOST || "localhost",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "password",
  database: process.env.DB_NAME || "habit_tracker",
});

db.connect((err) => {
  if (err) {
    console.error("❌ MySQL Connection Failed: ", err);
    return;
  }
  console.log("✅ Connected to MySQL Database");
});

module.exports = db;
