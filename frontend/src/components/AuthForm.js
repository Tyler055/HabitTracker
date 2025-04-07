import React, { useState } from "react";
import axios from "axios";

export default function AuthForm({ setUser }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState(""); // Email input field
  const [username, setUsername] = useState(""); // Username input field (for signup)
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    const endpoint = isLogin
      ? "http://127.0.0.1:5000/auth/login"
      : "http://127.0.0.1:5000/auth/signup";

    try {
      const response = await axios.post(endpoint, {
        email, // use email for both login and signup
        username: isLogin ? undefined : username, // Include username only during signup
        password,
      });

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        setUser(response.data.username || email); // fallback to entered email if no username
      } else {
        setErrorMsg("Unexpected response. Please try again.");
      }
    } catch (err) {
      const message =
        err.response?.data?.message ||
        "An error occurred. Please try again.";
      setErrorMsg(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form w-full max-w-sm mx-auto p-6 border rounded-lg shadow-lg bg-white">
      <h2 className="text-2xl font-semibold text-center mb-4">
        {isLogin ? "Log In" : "Sign Up"}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email Field */}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          disabled={loading}
          autoComplete="email"
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Username Field (only for sign-up) */}
        {!isLogin && (
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
            disabled={loading}
            autoComplete="username"
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}

        {/* Password Field */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          disabled={loading}
          autoComplete="current-password"
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
        >
          {loading ? (
            <span className="flex justify-center items-center">
              <svg
                className="animate-spin h-5 w-5 mr-3 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                ></path>
              </svg>
              Please wait...
            </span>
          ) : isLogin ? "Log In" : "Sign Up"}
        </button>
      </form>

      {errorMsg && (
        <p className="text-red-500 text-center mt-2" aria-live="assertive">
          {errorMsg}
        </p>
      )}

      <p
        onClick={() => setIsLogin(!isLogin)}
        className="text-center text-blue-500 cursor-pointer mt-4"
      >
        {isLogin ? "Don't have an account?" : "Already have an account?"} Click here
      </p>
    </div>
  );
}
