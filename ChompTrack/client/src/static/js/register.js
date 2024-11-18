function validatePassword(password) {
    const passwordPattern = /^(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$/;
    return passwordPattern.test(password);
}

function validateEmail(email) {
    // Simple regex for email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

async function register() {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('cfmpassword').value;


    if (username === "" || !username || !email || !password || !confirmPassword) {
        alert('Please fill in the blank fields.');
        return;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }
    
    // Validate password strength
    if (!validatePassword(password)) {
        alert('Your password must contain at least 8 characters, at least 1 uppercase character, and at least 1 special character.');
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // window.location.href = './profileCreation';

    // Prepare data for submission
    const registrationData = {
        username: username,
        email: email,
        password: password
    };


    // Send data to the server
    registerDataInServer(registrationData);

}

async function registerDataInServer(data) {
    fetch('http://127.0.0.1:5000/register', { // Replace with your actual API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Check if the response is not OK
        if (!response.ok) {
            return response.json().then(errData => {
                // Here we check if the error message is present and return it
                throw new Error(errData.error || response.statusText);
            });
        }
        return response.json(); // Process successful response
    })
    .then(data => {
        console.log(data)

        // Handle successful Registration (e.g., redirect to the next page)
        alert('Registration successful.');

        // Save the userID to session storage
        sessionStorage.setItem('userID', data.userID);
        window.location.href = 'profile-creation'; // Redirect to the next page
    })
    .catch(error => {
        // Handle error (e.g., show error message)
        // Specifically print the error message from the server
        alert(error.message === "Registration failed. Username or email already exists." 
            ? "Registration failed. Username or email already exists." 
            : "An error occurred. Please try again.");
    });
}