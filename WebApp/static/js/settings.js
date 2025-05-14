// Theme Selector Element
const themeSelector = document.getElementById('theme-selector');

// Notification Preferences Elements
const emailToggle = document.getElementById('email-notifications');
const pushToggle = document.getElementById('push-notifications');
const saveNotificationsBtn = document.getElementById('save-notifications');
const clearNotificationsBtn = document.getElementById('clear-notifications');
const notificationList = document.getElementById('notification-list');

// Notification Creation Form
const createNotificationForm = document.getElementById('create-notification-form');
const messageInput = document.getElementById('message');
const notificationTimeInput = document.getElementById('notification-time');

// Load settings from localStorage on page load
window.addEventListener('DOMContentLoaded', loadSettings);

// Event listeners
if (themeSelector) themeSelector.addEventListener('change', saveThemePreference);
if (saveNotificationsBtn) saveNotificationsBtn.addEventListener('click', saveNotificationPreferences);
if (clearNotificationsBtn) clearNotificationsBtn.addEventListener('click', clearNotifications);
if (createNotificationForm) createNotificationForm.addEventListener('submit', handleNotificationFormSubmit);

// Load settings from localStorage
function loadSettings() {
  try {
    loadTheme();
    loadNotificationPreferences();
    loadNotifications();
    loadScheduledNotifications();
  } catch (err) {
    console.error('Error loading settings from localStorage:', err);
  }
}

function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme && themeSelector) {
    themeSelector.value = savedTheme;
    document.body.setAttribute('data-theme', savedTheme);
  }
}

function loadNotificationPreferences() {
  const emailPref = localStorage.getItem('emailNotifications');
  const pushPref = localStorage.getItem('pushNotifications');
  
  if (emailToggle && emailPref !== null) emailToggle.checked = JSON.parse(emailPref);
  if (pushToggle && pushPref !== null) pushToggle.checked = JSON.parse(pushPref);
}

function loadNotifications() {
  const savedNotifications = JSON.parse(localStorage.getItem('notifications')) || [];
  savedNotifications.forEach(notification => addNotificationToDOM(notification.message, notification.time));
}

function loadScheduledNotifications() {
  const scheduledNotifications = JSON.parse(localStorage.getItem('scheduledNotifications')) || [];
  scheduledNotifications.forEach(schedule => scheduleNotification(schedule.message, schedule.time));
}

// Save theme preference
function saveThemePreference(event) {
  const selectedTheme = event.target.value;
  localStorage.setItem('theme', selectedTheme);
  document.body.setAttribute('data-theme', selectedTheme);
}

// Save notification preferences (email and push)
function saveNotificationPreferences() {
  try {
    localStorage.setItem('emailNotifications', emailToggle.checked);
    localStorage.setItem('pushNotifications', pushToggle.checked);
    alert('Notification preferences saved!');
  } catch (err) {
    console.error('Error saving notification preferences:', err);
    alert('Failed to save your notification preferences.');
  }
}

// Clear notifications
function clearNotifications() {
  localStorage.removeItem('notifications');
  notificationList.innerHTML = '';
  alert('All notifications cleared.');
}

// Handle notification creation form
function handleNotificationFormSubmit(event) {
  event.preventDefault();

  const message = messageInput.value.trim();
  const time = notificationTimeInput.value;

  if (message && time) {
    const notificationTime = new Date(time).toLocaleTimeString();

    // Add notification to DOM and save it
    addNotificationToDOM(message, notificationTime);
    saveNotificationToLocalStorage(message, notificationTime);
    scheduleNotification(message, time);

    // Clear input after adding notification
    messageInput.value = '';
    notificationTimeInput.value = '';
    alert('New notification added!');
  } else {
    alert('Please enter a valid message and time.');
  }
}

// Save notification to localStorage
function saveNotificationToLocalStorage(message, time) {
  const notifications = JSON.parse(localStorage.getItem('notifications')) || [];
  notifications.push({ message, time });
  localStorage.setItem('notifications', JSON.stringify(notifications));
}

// Secure Function to Add Notification to the DOM
function addNotificationToDOM(message, time) {
  const newNotification = document.createElement('div');
  newNotification.classList.add('notification-item');

  const messagePara = document.createElement('p');
  const strongText = document.createElement('strong');
  strongText.textContent = message; // Securely set text content
  messagePara.appendChild(strongText);

  const timeSpan = document.createElement('span');
  timeSpan.classList.add('notification-time');
  timeSpan.textContent = time; // Securely set text content

  newNotification.appendChild(messagePara);
  newNotification.appendChild(timeSpan);

  notificationList.appendChild(newNotification);
}

// Function to schedule a notification
function scheduleNotification(message, time) {
  const notificationTime = new Date(time).getTime();
  const now = Date.now();
  const delay = notificationTime - now;

  if (delay > 0) {
    setTimeout(() => {
      alert(`Notification: ${message}`);
      addNotificationToDOM(message, new Date().toLocaleTimeString());
    }, delay);
  }
}
