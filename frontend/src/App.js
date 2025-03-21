import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';

// HomePage Component (added from the initial code snippet)
import HomePage from './pages/HomePage';

const App = () => {
  const isAuthenticated = localStorage.getItem('token'); // Check if user is authenticated

  return (
    <Router>
      <Switch>
        {/* Public routes */}
        <Route exact path="/" component={HomePage} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />

        {/* Protected route */}
        <Route
          path="/dashboard"
          render={() => (isAuthenticated ? <Dashboard /> : <Redirect to="/login" />)}
        />
      </Switch>
    </Router>
  );
};

export default App;
