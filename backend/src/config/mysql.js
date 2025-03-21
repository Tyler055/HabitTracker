const mysql = require("mysql");

const connectMySQL = () => {
  const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD || "password",
    database: process.env.DB_NAME || "habit_tracker",
  });

  db.connect((err) => {
    if (err) {
      console.error("❌ MySQL connection failed:", err);
    } else {
      console.log("✅ Connected to MySQL Database");
    }
  });

  return db;
};

module.exports = connectMySQL;
