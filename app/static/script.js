document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });

  // User registration
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Add registration logic here
      alert('User registered successfully!');
    });
  }

  // User login
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Add login logic here
      alert('User logged in successfully!');
    });
  }

  // Show/Hide password functionality
  const togglePasswordButton = document.getElementById('togglePassword');
  if (togglePasswordButton) {
    togglePasswordButton.addEventListener('click', () => {
      const passwordField = document.getElementById('password');
      const type =
        passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordField.setAttribute('type', type);
      togglePasswordButton.textContent = type === 'password' ? 'Show' : 'Hide';
    });
  }

  // Recycling tracker
  const recyclingForm = document.getElementById('recycling-form');
  if (recyclingForm) {
    recyclingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Add recycling tracking logic here
      alert('Recycling entry added successfully!');
    });
  }

  // Admin dashboard functionality
  const userManagementForm = document.getElementById('user-management-form');
  if (userManagementForm) {
    userManagementForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Add user management logic here
      alert('User management action completed successfully!');
    });
  }

  const routeManagementForm = document.getElementById('route-management-form');
  if (routeManagementForm) {
    routeManagementForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Add route management logic here
      alert('Route management action completed successfully!');
    });
  }
});
