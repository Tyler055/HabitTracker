require("dotenv").config();
const mongoose = require("mongoose");
const Habit = require("./models/Habit"); // Adjust path if needed

const defaultHabits = [
  {
    name: "Drink Water",
    description: "Stay hydrated by drinking enough water.",
  },
  { name: "Exercise", description: "Get active and move your body." },
  { name: "Read", description: "Read something new every day." },
  { name: "Sleep Well", description: "Get at least 7-8 hours of sleep." },
];

async function insertDefaultHabits() {
  try {
    console.log("⏳ Connecting to MongoDB...");
    await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("✅ MongoDB connected");

    const count = await Habit.countDocuments();
    if (count === 0) {
      console.log("🌱 Inserting default habits...");
      await Habit.insertMany(defaultHabits);
      console.log("🌱 Default habits inserted successfully");
    } else {
      console.log("ℹ️ Habits already exist, skipping insert");
    }
    
    mongoose.connection.close();
    console.log("🛑 MongoDB connection closed");

  } catch (error) {
    console.error("❌ Error inserting default habits:", error.message);
    mongoose.connection.close();
    console.log("🛑 MongoDB connection closed due to error");
  }
}

insertDefaultHabits();
