const React = require('react');
const ReactDOM = require('react-dom/client');
const App = require('./App.js');  // Add the .js extension
const reportWebVitals = require('./reportWebVitals.js');  // Add the .js extension

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  React.createElement(React.StrictMode, null, React.createElement(App))
);

reportWebVitals();
