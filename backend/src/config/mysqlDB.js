const mysql = require("mysql");

const connectMySQL = () => {
  const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD || "",
    database: process.env.DB_NAME || "habit_tracker",
  });

  db.connect((err) => {
    if (err) {
      console.error("❌ MySQL Connection Failed:", err);
      process.exit(1);
    } else {
      console.log("✅ MySQL Connected");
    }
  });

  return db;
};

module.exports = connectMySQL;
