import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [identifier, setIdentifier] = useState(""); // email or username
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/habit-tracker");
    }
  }, [navigate]);

  const toggleMode = () => {
    setIsLoginMode((prev) => !prev);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const endpoint = isLoginMode
      ? "http://127.0.0.1:5000/auth/login"
      : "http://127.0.0.1:5000/auth/signup";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: identifier, password }), // same key used for email/username
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Something went wrong");
      }

      if (data.token) {
        localStorage.setItem("token", data.token);
        navigate("/habit-tracker");
      } else {
        throw new Error("Token not received");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h1>{isLoginMode ? "Log In" : "Sign Up"}</h1>
      <p>Welcome to your Habit Tracker!</p>

      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="text"
          placeholder="Email or Username"
          autoComplete="username"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "Please wait..." : isLoginMode ? "Log In" : "Sign Up"}
        </button>
      </form>

      <button onClick={toggleMode} className="link-btn">
        {isLoginMode
          ? "Don't have an account? Sign up here."
          : "Already have an account? Log in."}
      </button>

      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Home;
