// theme.js

export const initializeTheme = () => {
  let currentTheme = localStorage.getItem('theme') || 'dark';
  document.body.classList.add(`${currentTheme}-theme`);
  updateButtonText(currentTheme);
};

export const toggleTheme = () => {
  let currentTheme = localStorage.getItem('theme') || 'dark';
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.body.classList.remove('dark-theme', 'light-theme');
  document.body.classList.add(`${currentTheme}-theme`);
  localStorage.setItem('theme', currentTheme);
  updateButtonText(currentTheme);
};

const updateButtonText = (theme) => {
  const themeButton = document.getElementById('theme-toggle');
  if (themeButton) {
    themeButton.textContent = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  }
};
