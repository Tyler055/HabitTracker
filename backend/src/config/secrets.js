const jwt = require("jsonwebtoken");

// Utility function to fetch environment variables as strings
const getEnv = (key, defaultValue = null, required = true) => {
  const value = process.env[key] || defaultValue;
  if (!value && required) {
    console.error(`❌ Missing required environment variable: ${key}`);
    process.exit(1);
  }
  return value;
};

// Utility function to fetch environment variables as booleans
const getBoolean = (key, defaultValue = false) => {
  const val = process.env[key];
  return val !== undefined ? val.toLowerCase() === "true" : defaultValue;
};

// Utility function to fetch environment variables as numbers
const getNumber = (key, defaultValue = null, required = false) => {
  const raw = process.env[key] || defaultValue;

  if (raw === undefined && required) {
    console.error(`❌ Missing required number environment variable: ${key}`);
    process.exit(1);
  }

  return raw; // Return as string, will convert when needed
};

// Fetch and return secret keys as needed
const getSecrets = () => {
  const secrets = {
    // JWT Secrets
    jwtSecret: getEnv("JWT_SECRET"),
    refreshSecret: getEnv("JWT_REFRESH_SECRET", "defaultRefreshSecret", false),

    // Database credentials
    dbHost: getEnv("DB_HOST_MYSQL"),
    dbPort: getNumber("DB_PORT_MYSQL", "3307"),
    dbUser: getEnv("DB_USER"),
    dbPassword: getEnv("DB_PASSWORD"),
    dbName: getEnv("DB_NAME"),

    // Mail credentials
    mailServer: getEnv("MAIL_SERVER", "smtp.gmail.com"),
    mailPort: getNumber("MAIL_PORT", "587"),
    mailUsername: getEnv("MAIL_USERNAME"),
    mailPassword: getEnv("MAIL_PASSWORD"),

    // Cache-related secrets
    cacheUrl: getEnv("CACHE_URL", "redis://localhost:6379/0"),
    cacheTimeout: getNumber("CACHE_DEFAULT_TIMEOUT", "300"),
  };

  return secrets;
};

// Function to generate JWT tokens (using secrets)
const generateToken = (payload) => {
  const secrets = getSecrets();
  const options = { expiresIn: "1h" };
  return jwt.sign(payload, secrets.jwtSecret, options);
};

// Function to connect to MySQL (uses DB secrets)
const connectToDatabase = () => {
  const secrets = getSecrets();
  console.log(`Connecting to MySQL at ${secrets.dbHost}:${secrets.dbPort}`);
  // Actual connection logic to DB goes here (using secrets.dbHost, secrets.dbUser, etc.)
};

// Example of accessing other secrets
const sendEmail = (emailData) => {
  const secrets = getSecrets();
  console.log(
    `Sending email via ${secrets.mailServer} at port ${secrets.mailPort}`
  );
  // Actual email sending logic goes here (using secrets.mailUsername, secrets.mailPassword)
};

// Expose only the necessary functions for the app to request secrets
module.exports = {
  getSecrets, // To fetch all secrets as needed
  generateToken, // To generate JWT tokens (using secrets)
  connectToDatabase, // To connect to the database
  sendEmail, // To send emails
};
