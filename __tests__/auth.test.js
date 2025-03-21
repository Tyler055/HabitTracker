// __tests__/auth.test.js
const request = require("supertest");
const app = require("../server"); // Assuming your app is exported from a 'server.js' file
const User = require("../models/User");
const mongoose = require("mongoose");

// Set up a test user for login testing
beforeAll(async () => {
  await mongoose.connect("mongodb://localhost:27017/test_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
});

afterAll(async () => {
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
    token = response.body.token;
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
});
