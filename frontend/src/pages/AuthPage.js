import React, { useState } from "react";
import AuthForm from "../components/AuthForm"; // Import AuthForm component

const AuthPage = ({ setUser }) => {
  const [isLoginMode, setIsLoginMode] = useState(true); // Default mode is login

  return (
    <div className="auth-container">
      <h1 className="text-2xl text-center mb-4">{isLoginMode ? "Login" : "Sign Up"}</h1>
      <AuthForm setUser={setUser} isLoginMode={isLoginMode} />

      <button onClick={() => setIsLoginMode((prev) => !prev)} className="toggle-mode-btn">
        {isLoginMode
          ? "Don't have an account? Sign up here."
          : "Already have an account? Log in."}
      </button>
    </div>
  );
};

export default AuthPage;
