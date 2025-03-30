import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = ({ autoColorAdjustment }) => {
  const navigate = useNavigate();

  // Redirect to Habit Tracker page on load if auto-color adjustment is disabled
  useEffect(() => {
    if (!autoColorAdjustment) {
      navigate('/habit-tracker');
    }
  }, [autoColorAdjustment, navigate]);

  return (
    <div>
      <h1>Welcome to Your Habit Tracker</h1>
      <p>Customize your page colors here!</p>
    </div>
  );
};

export default Home;
