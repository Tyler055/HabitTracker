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
window.addEventListener('DOMContentLoaded', () => {
  try {
    // Load theme from localStorage and apply it
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme && themeSelector) {
      themeSelector.value = savedTheme;
      document.body.setAttribute('data-theme', savedTheme);
    }

    // Apply saved notification preferences
    const emailPref = localStorage.getItem('emailNotifications');
    const pushPref = localStorage.getItem('pushNotifications');

    if (emailToggle && emailPref !== null) emailToggle.checked = JSON.parse(emailPref);
    if (pushToggle && pushPref !== null) pushToggle.checked = JSON.parse(pushPref);

    // Load saved notifications from localStorage and display them
    const savedNotifications = JSON.parse(localStorage.getItem('notifications')) || [];
    savedNotifications.forEach((notification) => {
      addNotificationToDOM(notification.message, notification.time);
    });

    // Load scheduled notifications
    const scheduledNotifications = JSON.parse(localStorage.getItem('scheduledNotifications')) || [];
    scheduledNotifications.forEach(schedule => {
      scheduleNotification(schedule.message, schedule.time);
    });

  } catch (err) {
    console.error('Error loading settings from localStorage:', err);
  }
});

// Save theme preference
if (themeSelector) {
  themeSelector.addEventListener('change', (event) => {
    const selectedTheme = event.target.value;
    localStorage.setItem('theme', selectedTheme);
    document.body.setAttribute('data-theme', selectedTheme);
  });
}

// Save notification preferences (email and push)
if (saveNotificationsBtn) {
  saveNotificationsBtn.addEventListener('click', () => {
    try {
      localStorage.setItem('emailNotifications', emailToggle.checked);
      localStorage.setItem('pushNotifications', pushToggle.checked);
      alert('Notification preferences saved!');
    } catch (err) {
      console.error('Error saving notification preferences:', err);
      alert('❌ Failed to save your notification preferences.');
    }
  });
}

// Clear notifications
if (clearNotificationsBtn) {
  clearNotificationsBtn.addEventListener('click', () => {
    localStorage.removeItem('notifications');
    notificationList.innerHTML = '';
    alert('All notifications cleared.');
  });
}

// Handle notification creation form
if (createNotificationForm) {
  createNotificationForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();
    const time = notificationTimeInput.value;

    if (message && time) {
      const notificationTime = new Date(time).toLocaleTimeString();

      // Add notification to DOM
      addNotificationToDOM(message, notificationTime);

      // Save notification to localStorage
      const notifications = JSON.parse(localStorage.getItem('notifications')) || [];
      notifications.push({ message, time: notificationTime });
      localStorage.setItem('notifications', JSON.stringify(notifications));

      // Schedule the notification
      scheduleNotification(message, time);

      // Clear input after adding notification
      messageInput.value = '';
      notificationTimeInput.value = '';
      alert('New notification added!');
    } else {
      alert('❌ Please enter a valid message and time.');
    }
  });
}

// Function to add notification to the DOM
function addNotificationToDOM(message, time) {
  const newNotification = document.createElement('div');
  newNotification.classList.add('notification-item');
  newNotification.innerHTML = `
    <p><strong>${message}</strong></p>
    <span class="notification-time">${time}</span>
  `;
  notificationList.appendChild(newNotification);
}

// Function to schedule a notification
function scheduleNotification(message, time) {
  const notificationTime = new Date(time).getTime();
  const now = Date.now();
  const delay = notificationTime - now;

  if (delay > 0) {
    setTimeout(() => {
      alert(`🔔 Notification: ${message}`);
      addNotificationToDOM(message, new Date().toLocaleTimeString());
    }, delay);
  }
}
