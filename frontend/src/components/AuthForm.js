import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Use React Router's navigation

export default function AuthForm({ setUser, isLoginModeProp }) {
  const [identifier, setIdentifier] = useState(""); // Email or Username
  const [password, setPassword] = useState(""); // Password
  const [username, setUsername] = useState(""); // Username (only for sign-up)
  const [confirmPassword, setConfirmPassword] = useState(""); // Confirm password (only for sign-up)
  const [showPassword, setShowPassword] = useState(false); // Show password toggle
  const [loading, setLoading] = useState(false); // Loading state
  const [errorMsg, setErrorMsg] = useState(""); // Error message
  const [showErrorModal, setShowErrorModal] = useState(false); // Error modal visibility
  const [isLoginMode, setIsLoginMode] = useState(isLoginModeProp); // Login or signup mode
  const navigate = useNavigate(); // For redirection

  // Validate password length and confirmation
  const validateForm = () => {
    if (!identifier || !password) {
      setErrorMsg("Email/Username and Password are required.");
      return false;
    }
    if (!isLoginMode && password !== confirmPassword) {
      setErrorMsg("Passwords do not match.");
      return false;
    }
    if (!isLoginMode && password.length < 6) {
      setErrorMsg("Password must be at least 6 characters long.");
      return false;
    }
    return true;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");
    
    if (!validateForm()) {
      setLoading(false);
      return;
    }

    const endpoint = isLoginMode
      ? `http://127.0.0.1:5000/auth/login`
      : `http://127.0.0.1:5000/auth/signup`;

    // Prepare request data
    const requestData = {
      email: identifier,
      username: !isLoginMode ? username : undefined,
      password,
      confirmPassword: !isLoginMode ? confirmPassword : undefined,
    };

    try {
      const response = await axios.post(endpoint, requestData, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        setUser(response.data.username || identifier);
        if (isLoginMode) {
          navigate("/habit-tracker"); // Redirect to habit tracker after login
        }
      } else {
        setErrorMsg("Unexpected response. Please try again.");
      }
    } catch (err) {
      console.error("Error response:", err.response?.data); // Log the error response for debugging
      setErrorMsg(err.response?.data?.message || "An error occurred. Please try again.");
      setShowErrorModal(true);
    } finally {
      setLoading(false);
    }
  };

  // Close error modal
  const closeModal = () => {
    setShowErrorModal(false);
    setErrorMsg("");
  };

  return (
    <div className="auth-form w-full max-w-sm mx-auto p-6 border rounded-lg shadow-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white">
      <h2 className="text-2xl font-semibold text-center mb-4">
        {isLoginMode ? "Log In" : "Sign Up"}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email or Username Field */}
        <input
          type="email"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="Email"
          required
          disabled={loading}
          autoComplete="email"
          className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
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
            className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
          />
        )}

        {/* Password Field */}
        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            disabled={loading}
            autoComplete="current-password"
            className="w-full p-2 pr-10 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
          />
          <button
            type="button"
            className="absolute right-2 top-2 text-sm text-blue-500 dark:text-blue-300"
            onClick={() => setShowPassword(!showPassword)}
            disabled={loading}
          >
            {showPassword ? "Hide" : "Show"}
          </button>
        </div>

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
            className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
          />
        )}

        {/* Submit Button */}
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

      {/* Toggle between login/signup */}
      <p
        onClick={() => setIsLoginMode((prev) => !prev)}
        className="text-center text-blue-500 cursor-pointer mt-4"
      >
        {isLoginMode
          ? "Don't have an account? Sign up here."
          : "Already have an account? Log in."}
      </p>

      {/* Social login placeholders */}
      <div className="mt-6 space-y-2">
        <button className="w-full p-2 border rounded-md bg-white text-black dark:bg-gray-700 dark:text-white">
          Continue with Google
        </button>
        <button className="w-full p-2 border rounded-md bg-white text-black dark:bg-gray-700 dark:text-white">
          Continue with Facebook
        </button>
      </div>

      {/* Error Modal */}
      {showErrorModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md w-11/12 max-w-sm text-center">
            <h3 className="text-lg font-semibold text-red-600 dark:text-red-400 mb-2">Error</h3>
            <p className="text-gray-800 dark:text-white mb-4">{errorMsg}</p>
            <button
              onClick={closeModal}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
