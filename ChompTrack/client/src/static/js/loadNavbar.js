// loadNavbar.js
document.addEventListener('DOMContentLoaded', function() {

    fetch('/navbar')  // Path to your navbar.html file
    .then(response => response.text())  // Get the HTML content
    .then(data => {
        document.getElementById('navbar-container').innerHTML = data;  // Insert navbar into the placeholder
        
        // Add event listener for menu toggle button
        document.querySelector('.menu-toggle').addEventListener('click', function() {
            document.querySelector('.nav-links').classList.toggle('active');
        });

        // Add event listener for logout button
        document.getElementById('logoutBtn').addEventListener('click', function() {
            if (confirm('Are you sure you want to log out?')) {
                // Perform logout action here
                alert('You have been logged out.');
                // Redirect to login page or perform other logout actions
                window.location.href = "/logout";
            }
        });
    })
    .catch(error => console.error('Error loading navbar:', error));  // Log any errors
});