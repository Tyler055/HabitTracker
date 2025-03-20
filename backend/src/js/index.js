// index.js

import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './app';
import { HabitProvider } from './context/HabitContext';
import { initializeTheme } from './utils/theme';

document.addEventListener('DOMContentLoaded', () => {
  // Initialize theme when the document is loaded
  initializeTheme();

  ReactDOM.render(
    <HabitProvider>
      <App />
    </HabitProvider>,
    document.getElementById('root')
  );
});
