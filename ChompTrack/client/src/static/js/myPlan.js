document.addEventListener("DOMContentLoaded", function () {

    async function getNutritions() {
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
        document.getElementById('Calories').innerHTML = '<b>Calories:</b> ' + nutritions.calories.toFixed(0) + ' kcal';
        document.getElementById('Carbohydrates').innerHTML = '<b>Carbohydrates:</b> ' + nutritions.carbohydrates + ' g';
        document.getElementById('Protein').innerHTML = '<b>Protein:</b> ' + nutritions.protein + ' g';
        document.getElementById('Fats').innerHTML = '<b>Fats:</b> ' + nutritions.fats + ' g';
    }

    async function getUsername() {
        const userID = sessionStorage.getItem('userID');
        console.log(userID)

        fetch('http://127.0.0.1:5000/getCurrentUser', {  // Your API URL here
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
            document.getElementById('username').innerText = data.username;                  // Call the function to display the data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }

    function getDailyProgress(date) {
        const userID = sessionStorage.getItem('userID');
        console.log(userID)
        console.log(date)
        fetch('http://127.0.0.1:5000/getDailyProgress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userID, date})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch daily progress data: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            updateProgressCircles(data);
        })
        .catch(error => {
            console.error('Error fetching daily progress data:', error);
        });
    }

    // Function to update progress circles based on fetched data
    function updateProgressCircles(data) {
        document.getElementById('calories-circle').style.setProperty('--progress', `${data.calories}%`);
        document.getElementById('calories-circle').textContent = `${data.calories}%`;

        console.log("fats2:",data.fats);
        document.getElementById('fats-circle').style.setProperty('--progress', `${data.fats}%`);
        document.getElementById('fats-circle').textContent = `${data.fats}%`;

        document.getElementById('protein-circle').style.setProperty('--progress', `${data.protein}%`);
        document.getElementById('protein-circle').textContent = `${data.protein}%`;

        document.getElementById('carbohydrates-circle').style.setProperty('--progress', `${data.carbohydrates}%`);
        document.getElementById('carbohydrates-circle').textContent = `${data.carbohydrates}%`;
    }


    async function getMealPlans(date) {
        const userID = sessionStorage.getItem('userID');
        console.log(userID)
        console.log(date)

        fetch('http://127.0.0.1:5000/getMealPlans', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userID, date})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data);  // For debugging purposes
            allMealPlans=data;   
            updateMealGrid(date);  // Update the grid with the fetched meals
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        })
    }

    async function removeMealPlan(date, mealType) {
        const userID = sessionStorage.getItem('userID');
        console.log('Removing meal plan with userID:', userID, 'date:', date, 'mealType:', mealType);

        fetch('http://127.0.0.1:5000/removeMealPlan', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userID, date, mealType})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data)
            // Optionally show a message to the user
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        })
    }

    async function completeMealPlan(date, mealType, completed) {
        const userID = sessionStorage.getItem('userID');
        console.log('completing meal plan with userID:', userID, 'date:', date, 'mealType:', mealType, 'completed:', completed);

        fetch('http://127.0.0.1:5000/completeMealPlan', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userID, date, mealType, completed})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data)
            // Optionally show a message to the user
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        })
    }

    function getMealCuisine(meal){
        return meal.cuisine ? meal.cuisine : 'Other';
    }

    const mealGrid = document.getElementById('meal-grid');

    // function to create meal card
    function createMealCard(date, key, meal) {
        const card = document.createElement('div');
        card.className = 'meal-card';

        if (Object.keys(meal).length === 0){
            card.innerHTML = `
            <div class="empty-card">
                <h3 class ="no-meal-planned" >No meal planned</h3>
                <button class="add-recipe">Add Recipe</button>
            </div>
        `; 
        // Event listener for "Add Recipe" button to restore the original content
        card.querySelector('.add-recipe').addEventListener('click', function() {
            window.location.href = '/discover';
        });
        }
        else{
            card.innerHTML = `
                <img src="${meal.image}" alt="${meal.name}">
                <div class="meal-info">
                    <h3>${capitalizeFirstLetter(key)}</h3>
                    <p>Name: ${meal.name}</p>
                    <p>Cuisine: ${getMealCuisine(meal)}</p>
                    <p class="prep-time">Estimated Prep. Time: ${meal.prepTime} Min</p>
                    <p>Cost: $${(meal.cost/100).toFixed(2)}</p>
                </div>
                <div class="meal-actions">
                    <button class="action-button tick-btn">✔️</button>
                    <button class="action-button cross-btn">✖</button>
                </div>
            `;
            if (meal.completed){
                console.log("added completed class")
                card.classList.add('completed');
            }
            // Add event listener for the tick button (meal completed)
            card.querySelector('.tick-btn').addEventListener('click', async function() {
                    // Toggle visual completion state
                card.classList.toggle('completed');
                
                // Toggle the completed state and send it to the backend
                meal.completed = !meal.completed;  // Toggle completed status
                await completeMealPlan(date, key, meal.completed);

                // Fetch and update the progress data to reflect changes
                getDailyProgress(formatDateToYYYYMMDD(selectedDate)); 
            });
            // Event listener for cross button (replace card with "Add Recipe" button)
            card.querySelector('.cross-btn').addEventListener('click', function() {
                // Save the current content of the card to restore it later
                const originalContent = card.innerHTML;
                card.classList.remove('completed');
                // Replace card content with "Add Recipe" button
                card.innerHTML = `
                    <div class="empty-card">
                        <h3 class ="no-meal-planned" >No meal planned</h3>
                        <button class="add-recipe">Add Recipe</button>
                    </div>
                `;
                removeMealPlan(date, key);
                getDailyProgress(formatDateToYYYYMMDD(selectedDate));
                // Event listener for "Add Recipe" button to restore the original content
                card.querySelector('.add-recipe').addEventListener('click', function() {
                    window.location.href = '/discover';
                });
            });
        }
        return card;
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // function to dynamically add meal card
    function updateMealGrid(date) {
        
        mealGrid.innerHTML = '';
        // Define the desired order for meal types
        const mealOrder = ["breakfast", "lunch", "dinner", "snack"];

        // Sort allMealPlans based on the defined order
        const sortedMealPlans = Object.entries(allMealPlans).sort((a, b) => {
            return mealOrder.indexOf(a[0]) - mealOrder.indexOf(b[0]);
        });

        sortedMealPlans.forEach(([key, meal]) => {  // Loop through key-value pairs in allMealPlans
            const card = createMealCard(date, key, meal);  // Pass key and meal object
            mealGrid.appendChild(card);
            console.log('appended');
        });
    }

    let startDate = getMonday(new Date());
    const today = new Date();
    let currentDate = new Date(today);
    const dateButtonsContainer = document.getElementById('date-buttons');
    document.getElementById('date').innerText=`Date: ${currentDate.toLocaleString('en-US', {weekday:'long', day: 'numeric', month:'long' ,year: 'numeric'})}`
    let selectedDate =new Date();

    // get first date of the week
    function getMonday(date) {
        const dayOfWeek = date.getDay(); // 0 (Sun) to 6 (Sat)
        const daysUntilMonday = (dayOfWeek === 0) ? -6 : 1 - dayOfWeek; // If Sunday (0), go back 6 days, else go back to last Monday
        date.setDate(date.getDate() + daysUntilMonday); // Set to the correct Monday
        return date;
    }

    // Event listeners for week navigation buttons
    document.getElementById('prev-week').addEventListener('click', function () {
        startDate.setDate(startDate.getDate() - 7);  // Go back a week
        createDateButtons();
    });

    document.getElementById('next-week').addEventListener('click', function () {
        startDate.setDate(startDate.getDate() + 7);  // Go forward a week
        createDateButtons();
    });

    // Function to create date buttons for the week
    function createDateButtons() {
        dateButtonsContainer.innerHTML = '';  // Clear existing buttons
        for (let i = 0; i < 7; i++) {
            const buttonDate = new Date(startDate);
            buttonDate.setDate(startDate.getDate() + i);  // Set date for the button
            const button = document.createElement('button');
            button.className = 'date-button';
            button.innerHTML = `<span>${buttonDate.toLocaleString('en-US', {day:'numeric', weekday: 'short' })}</span>`;
            button.addEventListener('click', function() {
                document.querySelectorAll('.date-button').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                document.getElementById('date').innerText=`Date: ${buttonDate.toLocaleString('en-US', {weekday:'long', day: 'numeric', month:'long' ,year: 'numeric'})}`
                getMealPlans(formatDateToYYYYMMDD(buttonDate)); // Fetch meal plans for selected date
                getDailyProgress(formatDateToYYYYMMDD(buttonDate));
                selectedDate=buttonDate;
            });
            dateButtonsContainer.appendChild(button);
        }
    }

    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear(); // Get the full year (YYYY)
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Get month (0-11) and pad to 2 digits
        const day = String(date.getDate()).padStart(2, '0'); // Get day (1-31) and pad to 2 digits
        return `${year}-${month}-${day}`; // Construct the YYYY-MM-DD format
    }

    // Initialize the week view
    createDateButtons();

     // Call the function to fetch and display data
     getNutritions();
     getUsername();
     getDailyProgress(formatDateToYYYYMMDD(currentDate));
     getMealPlans(formatDateToYYYYMMDD(currentDate));
 
});