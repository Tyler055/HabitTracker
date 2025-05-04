// Password strength checker for signup form only
const signupPasswordInput = document.getElementById('signup-password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorDiv = document.getElementById('form-error');

if (signupPasswordInput && confirmPasswordInput) {
  signupPasswordInput.addEventListener('input', checkStrength);
  confirmPasswordInput.addEventListener('input', checkMatch);

  function checkStrength(e) {
    const password = e.target.value;
    const strengthDiv = document.getElementById('password-strength');
    let strength = 0;

    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[!@#$%^&*]/.test(password)) strength++;

    const strengthText = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
    const strengthColor = ['#ff4d4d', '#ffa64d', '#ffff4d', '#4dff4d', '#4d4dff'];

    if (password.length > 0 && strength > 0) {
      strengthDiv.textContent = `Password Strength: ${strengthText[strength - 1]}`;
      strengthDiv.style.color = strengthColor[strength - 1];
    } else {
      strengthDiv.textContent = '';
    }
  }

  function checkMatch() {
    const password = signupPasswordInput.value;
    const confirm = confirmPasswordInput.value;
    if (confirm && password !== confirm) {
      errorDiv.textContent = 'Passwords do not match.';
      errorDiv.style.color = '#ff4d4d';
    } else {
      errorDiv.textContent = '';
    }
  }
}
