document.addEventListener("DOMContentLoaded", function () {
    // Call the function to fetch and display data
    getNutrients();
});

async function getNutrients() {
    const userID = sessionStorage.getItem('userID');
    console.log(userID)

    fetch('http://127.0.0.1:5000/getNutritions', {  // Your API URL here
        method: 'POST',  // Use POST to avoid showing parameters in URL
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID })  // Sending userID in the request body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch data: ' + response.status);
        }
        return response.json();  // Parse JSON data
    })
    .then(data => {
        console.log(data);  // For debugging purposes
        displayData(data);  // Call the function to display the data
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// Function to display data in the HTML
function displayData(nutritions) {
    document.getElementById('Calories').innerText = Math.round(Number(nutritions.calories)) + 'kcal';
    document.getElementById('Carbohydrates').innerText = Math.round(Number(nutritions.carbohydrates)) + 'g';
    document.getElementById('Protein').innerText = Math.round(Number(nutritions.protein)) + 'g';
    document.getElementById('Fats').innerText = Math.round(Number(nutritions.fats)) + 'g';
}
