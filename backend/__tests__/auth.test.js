const request = require("supertest");
const app = require("../server"); // Assuming your app is exported from a 'server.js' file
const mongoose = require("mongoose");
const User = require("../src/models/User");

// Set up a test user for login testing
beforeAll(async () => {
  // Connect to the MongoDB test database
  await mongoose.connect("mongodb://localhost:27017/test_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  // Optional: Clear any pre-existing data before running tests
  await User.deleteMany({});
});

afterAll(async () => {
  // Close MongoDB connection after tests
  await mongoose.disconnect();
});

describe("Auth Routes", () => {
  let token;

  it("should register a new user", async () => {
    const response = await request(app).post("/api/auth/register").send({
      username: "testuser",
      email: "testuser@example.com",
      password: "password123",
    });
    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
    token = response.body.token; // Save the token for further use
  });

  it("should login the user", async () => {
    const response = await request(app).post("/api/auth/login").send({
      email: "testuser@example.com",
      password: "password123",
    });
    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
  });

  it("should return unauthorized for invalid login", async () => {
    const response = await request(app).post("/api/auth/login").send({
      email: "wrongemail@example.com",
      password: "wrongpassword",
    });
    expect(response.status).toBe(400);
  });

  // Example of testing a protected route with a valid token
  it("should access a protected route with valid token", async () => {
    const response = await request(app)
      .get("/api/protected-route") // Replace with your protected route
      .set("Authorization", `Bearer ${token}`);
    
    expect(response.status).toBe(200);
    expect(response.body.message).toBe("You are authorized!");
  });

  // Example of testing a protected route without a token
  it("should return unauthorized for protected route without token", async () => {
    const response = await request(app).get("/api/protected-route"); // Replace with your protected route
    
    expect(response.status).toBe(401);
    expect(response.body.message).toBe("No token, authorization denied");
  });
});
