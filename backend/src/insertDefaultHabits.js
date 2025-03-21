const mongoose = require("mongoose");
const Habit = require("./models/Habit"); // Adjust the path to where the Habit model is located
const dotenv = require("dotenv");

// Load environment variables from the .env file
dotenv.config();

// Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(async () => {
    console.log("✅ MongoDB connected");

    // Default habits to insert
    const defaultHabits = ["Drink Water", "Exercise", "Read", "Sleep Well"];

    // Loop through each habit and insert it into the database
    for (const habitName of defaultHabits) {
      const habit = new Habit({
        name: habitName,
        description: `${habitName} habit description`, // Optional description for each habit
        // Add a user reference if needed (e.g., user: someUserId)
      });

      // Save the habit to the database
      await habit.save();
      console.log(`✅ Habit "${habitName}" inserted into MongoDB.`);
    }

    // Close the MongoDB connection
    mongoose.connection.close();
  })
  .catch((err) => {
    console.error("❌ Error connecting to MongoDB:", err);
  });
