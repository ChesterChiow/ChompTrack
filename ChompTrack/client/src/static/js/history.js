document.addEventListener('DOMContentLoaded', function() {
    const mealGrid = document.getElementById('meal-grid');
    const searchInput = document.getElementById('search-Input'); // Define this if you have a search input
    const dateInput = document.getElementById('date-Input'); // Define the date input
    let currentRecipeCount = 0;  // Initialize current recipe count
    let recipesShown = [];  // Use an object to store all recipes
    let filteredMeals = []; // Array to store filtered meals

    async function loadHistory() {
    
        fetch('http://127.0.0.1:5000/loadHistory', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                number_of_recipes : 10
            })  // Sending number_of_recipes in the request body
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data);  // For debugging purposes
            // Populate recipesShown with the fetched data

            Object.values(data).forEach((recipe, index) => {
            recipesShown[currentRecipeCount + index + 1] = recipe;  // Use currentRecipeCount + index + 1 for unique keys
            });

            currentRecipeCount += Object.values(data).length;  // Update current recipe count
            filteredMeals = recipesShown; // Initialize filtered meals
        
            console.log(currentRecipeCount);
            updateMealGrid();  // Update the grid with the fetched meals
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert("There are no past recipes used.")
        });
        
    }

    function getMealCuisine(meal){
        return meal.cuisine ? meal.cuisine : 'Other';
    }

    function formatDateToLong(dateString) {
        const date = new Date(dateString);
        const day = date.getDate();
        const month = date.toLocaleString('default', { month: 'long' });
        const year = date.getFullYear();
        return `${day} ${month} ${year}`;
    }

    function createMealCard(meal) {
        const card = document.createElement('div');
        card.className = 'meal-card';
        card.innerHTML = `
            <img src="${meal.image}" alt="${meal.name}">
            <div class="meal-info">
                <h3>${meal.name}</h3>
                <p>Recipe used on: ${formatDateToLong(meal.dateUsed)}<p>
                <p>Cuisine: ${getMealCuisine(meal)}</p>
                <p>Meal Category: ${meal.mealCategory}</p>
                <p class="prep-time">Estimated Prep. Time: ${meal.prepTime} Min</p>
                <p>Cost: $${(meal.cost/100).toFixed(2)}</p>
            </div>
        `;

        // Add a click event to navigate to the recipe page
        card.addEventListener('click', function() {
            window.location.href = `/recipe?id=${meal.recipeID}`;
        });

        return card;
    }

    function updateMealGrid() {
        mealGrid.innerHTML = '';

        if (filteredMeals.length === 0) {
            console.log(empty);
            noRecipesMessage.style.display = 'block';
        } else {
            noRecipesMessage.style.display = 'none';
            filteredMeals.forEach(meal => {
                const card = createMealCard(meal);
                mealGrid.appendChild(card);
                console.log('appended');
            });
        }
    }

    // Search functionality triggered by typing in search input
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        if (searchTerm) {
            filteredMeals = Object.values(recipesShown).filter(meal =>
                meal.name.toLowerCase().includes(searchTerm)
            );
        } else {
            // Show all meals if search is cleared
            filteredMeals = Object.values(recipesShown);
        }
        updateMealGrid();
    });

    function formatDateForInput(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');  // Months are 0-based, so add 1
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // Date filtering functionality
    dateInput.addEventListener('input', function() {
        const selectedDate = dateInput.value; 
        if (selectedDate) {
            filteredMeals = Object.values(recipesShown).filter(meal =>
                formatDateForInput(meal.dateUsed) === selectedDate 
            );
        } else {
            filteredMeals = Object.values(recipesShown);
        }
        updateMealGrid(); 
    });

    // No recipes message element
    const noRecipesMessage = document.createElement('p');
    noRecipesMessage.className = 'no-recipes-message';
    noRecipesMessage.textContent = 'There are no past recipes used.';
    noRecipesMessage.style.display = 'none'; // Hide initially
    mealGrid.appendChild(noRecipesMessage);

    // Fetch initial data
    loadHistory();

});