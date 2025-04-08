const express = require("express");
const secrets = require("./secrets"); // Import secrets.js

const { generateToken, connectToDatabase, sendEmail } = secrets;

// Example: Generate JWT token using secrets
const token = generateToken({ userId: 123 });
console.log(`Generated JWT Token: ${token}`);

// Example: Connect to MySQL database using secrets
connectToDatabase();

// Example: Send email using mail credentials
const emailData = {
  to: "user@example.com",
  subject: "Hello",
  message: "Welcome!",
};
sendEmail(emailData);

// Start the server
const app = express();
const port = 5000;

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
