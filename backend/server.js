// server.js or app.js
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const cookieParser = require('cookie-parser');

const habitRoutes = require('./src/routes/habitRoutes');
const userRoutes = require('./src/routes/userRoutes');
const authRoutes = require('./routes/authRoutes');

const connectMongoDB = require('./src/config/mongoDB');
const connectMySQL = require('./src/config/mysqlDB');

// Load .env variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// === Middlewares ===
app.use(cors({ credentials: true, origin: process.env.CLIENT_URL || 'http://localhost:3000' }));
app.use(express.json());
app.use(cookieParser());

// === Auth Routes (Login/Register/Refresh/Logout) ===
app.use('/auth', authRoutes);

// === Connect Database ===
if (process.env.DB_TYPE === 'mongodb') {
  connectMongoDB(); // MongoDB connection
} else if (process.env.DB_TYPE === 'mysql') {
  const db = connectMySQL(); // MySQL connection

  // Example MySQL-based habit routes (if needed separately)
  app.get('/habits', (req, res) => {
    db.query('SELECT * FROM habits', (err, results) => {
      if (err) return res.status(500).send(err);
      res.json(results);
    });
  });

  app.post('/habits', (req, res) => {
    const { name, description } = req.body;
    db.query('INSERT INTO habits (name, description) VALUES (?, ?)', [name, description], (err, results) => {
      if (err) return res.status(500).send(err);
      res.json({ message: '✅ Habit added successfully!', id: results.insertId });
    });
  });

  app.delete('/habits/:id', (req, res) => {
    const { id } = req.params;
    db.query('DELETE FROM habits WHERE id = ?', [id], (err) => {
      if (err) return res.status(500).send(err);
      res.json({ message: '✅ Habit deleted successfully!' });
    });
  });
}

// === API Routes (MongoDB or shared logic) ===
app.use('/api/habits', habitRoutes);
app.use('/api/users', userRoutes);

// === Health Check ===
app.get('/', (req, res) => {
  res.send('✅ Welcome to the Habit Tracker API');
});

// === Start Server ===
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});

module.exports = app;
