// Theme Selector
const themeSelector = document.getElementById('theme-selector');
const saveThemeBtn = document.getElementById('save-theme');
const emailToggle = document.getElementById('email-notifications');
const pushToggle = document.getElementById('push-notifications');
const saveNotificationsBtn = document.getElementById('save-notifications');
const clearNotificationsBtn = document.getElementById('clear-notifications');
const notificationList = document.getElementById('notification-list');

// Load settings from localStorage on page load
window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  const emailPref = localStorage.getItem('emailNotifications');
  const pushPref = localStorage.getItem('pushNotifications');

  if (savedTheme) {
    themeSelector.value = savedTheme;
    document.body.setAttribute('data-theme', savedTheme);
  }

  if (emailPref !== null) emailToggle.checked = JSON.parse(emailPref);
  if (pushPref !== null) pushToggle.checked = JSON.parse(pushPref);
});

// Save theme
saveThemeBtn.addEventListener('click', () => {
  const selectedTheme = themeSelector.value;
  localStorage.setItem('theme', selectedTheme);
  document.body.setAttribute('data-theme', selectedTheme);
  alert('Theme saved!');
});

// Save notification preferences
saveNotificationsBtn.addEventListener('click', () => {
  localStorage.setItem('emailNotifications', emailToggle.checked);
  localStorage.setItem('pushNotifications', pushToggle.checked);
  alert('Notification preferences saved!');
});

// Clear notifications
clearNotificationsBtn.addEventListener('click', () => {
  const items = document.querySelectorAll('.notification-item');
  if (items.length === 0) {
    alert('No notifications to clear.');
    return;
  }

  items.forEach(item => item.remove());
  alert('All notifications cleared.');
});
