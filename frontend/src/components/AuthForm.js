import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function AuthForm({ setUser, isLoginModeProp }) {
  const [identifier, setIdentifier] = useState(""); // Username or Email for login
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState(""); // Always required for signup
  const [email, setEmail] = useState(""); // Always required for signup
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [isLoginMode, setIsLoginMode] = useState(isLoginModeProp);

  const navigate = useNavigate();

  const validateForm = () => {
    if (isLoginMode) {
      if (!identifier || !password) {
        setErrorMsg("Username/Email and Password are required.");
        return false;
      }
    } else {
      if (!username || !email || !password || !confirmPassword) {
        setErrorMsg("All fields are required for sign-up.");
        return false;
      }
      if (password !== confirmPassword) {
        setErrorMsg("Passwords do not match.");
        return false;
      }
      if (password.length < 6) {
        setErrorMsg("Password must be at least 6 characters.");
        return false;
      }
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    if (!validateForm()) {
      setLoading(false);
      return;
    }

    const endpoint = isLoginMode
      ? "http://127.0.0.1:5000/auth/login"
      : "http://127.0.0.1:5000/auth/signup";

    const requestData = isLoginMode
      ? { identifier, password }
      : { username, email, password, confirmPassword };

    try {
      const response = await axios.post(endpoint, requestData, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        setUser(response.data.username || identifier);
        navigate("/habit-tracker");
      } else {
        setErrorMsg("Unexpected response. Please try again.");
        setShowErrorModal(true);
      }
    } catch (err) {
      console.error("Login/Signup error:", err.response?.data);
      setErrorMsg(err.response?.data?.message || "An error occurred. Please try again.");
      setShowErrorModal(true);
    } finally {
      setLoading(false);
    }
  };

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
        {isLoginMode ? (
          <input
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="Email or Username"
            required
            disabled={loading}
            autoComplete="username"
            className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
          />
        ) : (
          <>
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
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
              disabled={loading}
              autoComplete="email"
              className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600"
            />
          </>
        )}

        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            disabled={loading}
            autoComplete={isLoginMode ? "current-password" : "new-password"}
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

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
        >
          {loading ? "Please wait..." : isLoginMode ? "Log In" : "Sign Up"}
        </button>
      </form>

      <p
        onClick={() => setIsLoginMode((prev) => !prev)}
        className="text-center text-blue-500 cursor-pointer mt-4"
      >
        {isLoginMode
          ? "Don't have an account? Sign up here."
          : "Already have an account? Log in."}
      </p>

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
