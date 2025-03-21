// backend/src/config/mongoDB.js
const mongoose = require('mongoose');

const connectMongoDB = async () => {
  try {
    // Attempt to connect to MongoDB
    await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("✅ MongoDB Connected");
  } catch (error) {
    // If the connection fails, log the error and exit the process
    console.error("❌ MongoDB Connection Failed:", error);
    process.exit(1);  // Exits the process if the connection fails
  }
};

module.exports = connectMongoDB;
