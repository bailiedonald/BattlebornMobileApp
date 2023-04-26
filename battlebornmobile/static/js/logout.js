// Set the inactivity timeout to 30 minutes (in milliseconds)
const INACTIVITY_TIMEOUT = 30 * 60 * 1000;

// Set the logout URL
const LOGOUT_URL = '/logout';

// Define a variable to store the ID of the inactivity timeout
let inactivityTimeoutId;

// Start the inactivity timeout when the user interacts with the page
document.addEventListener('mousemove', resetInactivityTimeout);
document.addEventListener('keydown', resetInactivityTimeout);
document.addEventListener('scroll', resetInactivityTimeout);

function resetInactivityTimeout() {
  // Clear the existing inactivity timeout
  clearTimeout(inactivityTimeoutId);

  // Start a new inactivity timeout
  inactivityTimeoutId = setTimeout(logout, INACTIVITY_TIMEOUT);
}

function logout() {
  // Redirect the user to the logout URL
  window.location.href = LOGOUT_URL;
}
