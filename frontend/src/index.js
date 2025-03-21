import React from "react";
import ReactDOM from "react-dom/client";
import App from "./components/App";
import "./index.css"; // Your global styles
import reportWebVitals from "../reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Measure performance
reportWebVitals();
