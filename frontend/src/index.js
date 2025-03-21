import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";  // Your main component
import "./index.css"; // Your global styles
import reportWebVitals from "./reportWebVitals";

// Render the app in the 'root' div
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Measure performance (optional)
reportWebVitals();
