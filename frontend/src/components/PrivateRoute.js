import React from 'react';
import { Navigate } from 'react-router-dom';

// Utility to check if a JWT token is expired
const isTokenExpired = (token) => {
  if (!token) return true;
  
  const payload = JSON.parse(atob(token.split('.')[1])); // Decode JWT token
  const expiration = payload.exp * 1000; // Convert expiration to milliseconds
  return Date.now() > expiration; // Check if the token is expired
};

const PrivateRoute = ({ element, redirectTo = "/login" }) => {
  const token = localStorage.getItem('token');  // Get token from localStorage

  // If token is missing or expired, redirect to login
  if (!token || isTokenExpired(token)) {
    return <Navigate to={redirectTo} replace />;
  }

  // If token exists and is not expired, render the protected component
  return element;
};

export default PrivateRoute;
