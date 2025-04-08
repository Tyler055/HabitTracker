const express = require("express");
const connectDB = require("./config/db");
const cors = require("cors");
const habitRoutes = require("./routes/habitRoutes");
const userRoutes = require("./routes/userRoutes");

require("dotenv").config();

const app = express();
app.use(express.json());
app.use(cors());

connectDB();

// Routes
app.use("/api/habits", habitRoutes);
app.use("/api/users", userRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
