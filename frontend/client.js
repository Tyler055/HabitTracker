// client.js

const API_URL = 'http://localhost:5173/api';  // Backend API URL

const getCsrfToken = () => {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

const handleError = (error) => {
  console.error('API Error:', error);
  alert("An error occurred, please try again later.");
};

const login = async (username, password) => {
  try {
    const csrfToken = getCsrfToken();
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken,
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to login');
    
    document.cookie = `token=${data.token}; path=/; secure; HttpOnly; SameSite=Strict`;
    alert('Login successful!');
    return data;
  } catch (error) {
    handleError(error);
  }
};

const getHabitData = async () => {
  try {
    const token = getCookie('token');
    if (!token) throw new Error('You are not authenticated.');

    const csrfToken = getCsrfToken();
    const response = await fetch(`${API_URL}/habits`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-CSRF-Token': csrfToken,
      },
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch habit data');
    
    return data;
  } catch (error) {
    handleError(error);
  }
};

const logout = async () => {
  try {
    const token = getCookie('token');
    if (!token) throw new Error('You are not logged in.');

    const csrfToken = getCsrfToken();
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-CSRF-Token': csrfToken,
      },
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Logout failed');

    document.cookie = 'token=; path=/; max-age=-1; secure; HttpOnly; SameSite=Strict';
    alert('You have logged out!');
  } catch (error) {
    handleError(error);
  }
};

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
};

// Handling form submission for login
document.querySelector('#loginForm').addEventListener('submit', (event) => {
  event.preventDefault();
  const username = event.target.username.value;
  const password = event.target.password.value;
  
  login(username, password);
});

// Fetch habit data after login
document.querySelector('#getHabitsBtn').addEventListener('click', () => {
  getHabitData().then(data => {
    console.log('Fetched habit data:', data);
  });
});

// Logout functionality
document.querySelector('#logoutBtn').addEventListener('click', logout);
