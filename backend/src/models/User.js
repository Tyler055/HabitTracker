const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");

// Define the User Schema
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
});

// Hash password before saving user
userSchema.pre("save", async function (next) {
  // Only hash the password if it's modified or newly created
  if (!this.isModified("password")) return next();

  // Generate salt and hash the password
  const salt = await bcrypt.genSalt(10); // Generate salt
  this.password = await bcrypt.hash(this.password, salt); // Hash password with salt
  next(); // Continue with saving the user
});

// Add a method to compare passwords (for login validation)
userSchema.methods.comparePassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password); // Compare entered password with the stored hash
};

// Create the User model from the schema
const User = mongoose.model("User", userSchema);

module.exports = User; // Export the model for use in other parts of the app
