const React = require("react");
const { BrowserRouter: Router, Routes, Route } = require("react-router-dom");

const Login = require("./components/Login.js").default;
const Register = require("./components/Register.js").default;
const Dashboard = require("./components/Dashboard.js").default;
const HabitTracker = require("./components/HabitTracker.js").default;
const Layout = require("./components/Layout.js").default;
const ProtectedRoute = require("./components/ProtectedRoute.js").default;
const HomePage = require("./pages/HomePage.js").default;

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected route with layout */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Habit Tracker route */}
        <Route path="/habit-tracker" element={<HabitTracker />} />
      </Routes>
    </Router>
  );
};

module.exports = App;
