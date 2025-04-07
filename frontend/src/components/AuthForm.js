import React, { useState } from "react";
import axios from "axios";

export default function AuthForm({ setUser, isLoginModeProp }) {
  const [identifier, setIdentifier] = useState(""); // Email or Username
  const [password, setPassword] = useState(""); // Password
  const [username, setUsername] = useState(""); // Username (only for sign-up)
  const [confirmPassword, setConfirmPassword] = useState(""); // Confirm password (only for sign-up)
  const [loading, setLoading] = useState(false); // Loading state
  const [errorMsg, setErrorMsg] = useState(""); // Error message
  const [isLoginMode, setIsLoginMode] = useState(isLoginModeProp); // Determine login or sign-up mode

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    const endpoint = `${process.env.REACT_APP_API_URL}/api/${isLoginMode ? "login" : "signup"}`;

    // Prepare request data
    const requestData = {
      email: identifier, // Always use email or username
      username: !isLoginMode ? username : undefined, // Only include username for sign-up
      password,
      confirmPassword: !isLoginMode ? confirmPassword : undefined, // Only include confirmPassword for sign-up
    };

    try {
      const response = await axios.post(endpoint, requestData);

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        setUser(response.data.username || identifier); // Store user info
        if (isLoginMode) {
          window.location.href = "/habit-tracker"; // Redirect to habit tracker after login
        }
      } else {
        setErrorMsg("Unexpected response. Please try again.");
      }
    } catch (err) {
      setErrorMsg(err.response?.data?.message || "An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form w-full max-w-sm mx-auto p-6 border rounded-lg shadow-lg bg-white">
      <h2 className="text-2xl font-semibold text-center mb-4">
        {isLoginMode ? "Log In" : "Sign Up"}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email Field */}
        <input
          type="email"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="Email"
          required
          disabled={loading}
          autoComplete="email"
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Username Field (only for sign-up) */}
        {!isLoginMode && (
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

        {/* Confirm Password Field (only for sign-up) */}
        {!isLoginMode && (
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm Password"
            required
            disabled={loading}
            autoComplete="new-password"
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}

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
          ) : isLoginMode ? "Log In" : "Sign Up"}
        </button>
      </form>

      {errorMsg && (
        <p className="text-red-500 text-center mt-2" aria-live="assertive">
          {errorMsg}
        </p>
      )}

      <p
        onClick={() => setIsLoginMode((prev) => !prev)}
        className="text-center text-blue-500 cursor-pointer mt-4"
      >
        {isLoginMode
          ? "Don't have an account? Sign up here."
          : "Already have an account? Log in."}
      </p>
    </div>
  );
}
