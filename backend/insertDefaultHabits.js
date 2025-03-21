require("dotenv").config();
const mongoose = require("mongoose");
const dbUri = process.env.MONGO_URI;
const Habit = require("./src/models/Habit"); // Adjust path if needed

const defaultHabits = [
  { name: "Drink Water", description: "Stay hydrated by drinking enough water." },
  { name: "Exercise", description: "Get active and move your body." },
  { name: "Read", description: "Read something new every day." },
  { name: "Sleep Well", description: "Get at least 7-8 hours of sleep." }
];

async function insertDefaultHabits() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("✅ MongoDB connected");

    const count = await Habit.countDocuments();
    if (count === 0) {
      await Habit.insertMany(defaultHabits);
      console.log("🌱 Default habits inserted successfully");
    } else {
      console.log("ℹ️ Habits already exist, skipping insert");
    }

    mongoose.connection.close();
  } catch (error) {
    console.error("❌ Error inserting default habits:", error);
    mongoose.connection.close();
  }
}

insertDefaultHabits();
