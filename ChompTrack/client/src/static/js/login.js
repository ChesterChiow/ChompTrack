async function login(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Make the fetch call and store the response
    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    });

    const result = await response.json();  // Parse the JSON from the response

    if (response.ok) {
        // Check if a redirection URL is provided in the response
        if (response.status === 201) {
            // Redirect to the URL specified in the response
            window.location.href = '../profile-creation';
        } else {
            alert('Login successful.')
            // Handle cases where no redirection URL is specified
            window.location.href = '../my-plan';
        }
    } else if (response.status === 401) {
        // Login failed, show error message
        alert('Login failed: ' + result.error);
    } else {
        // Handle other errors
        alert('An error occurred: ' + result.error);
    }
}