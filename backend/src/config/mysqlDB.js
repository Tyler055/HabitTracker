const mysql = require("mysql");

const connectMySQL = () => {
  const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",  // Use DB_HOST if set in .env, default to localhost
    user: process.env.DB_USER || "root",      // Use DB_USER if set, default to root
    password: process.env.DB_PASSWORD || "",  // Use DB_PASSWORD if set, default to empty string
    database: process.env.DB_NAME || "habit-tracker",  // Use DB_NAME if set, default to habit-tracker
    port: process.env.DB_PORT || 3306         // Ensure port is correctly set (default MySQL port)
  });

  db.connect((err) => {
    if (err) {
      console.error("❌ MySQL Connection Failed:", err);
      process.exit(1);  // Exit the process on connection failure
    } else {
      console.log("✅ MySQL Connected");
    }
  });

  return db;
};

module.exports = connectMySQL;
