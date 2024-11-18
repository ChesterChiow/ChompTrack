document.addEventListener('DOMContentLoaded', function() {
    const mealGrid = document.getElementById('meal-grid');
    const loadMoreBtn = document.getElementById('load-more');
    const categoryBtns = document.querySelectorAll('.category-btn');

    let recipesShown = [];  // Use an object to store all recipes
    let filteredMeals = []; // Array to store filtered meals
    let allRecipeIDs = [];
    let criterias ={'mealType': [], 'cuisine':[], 'time':[0,120], 'cost':[0,100]};

    // Initial fetch of meals on page load
    loadMoreBtn.style.display = 'none';
    loadDiscover(); // Pass true to indicate initial fetch

    async function loadDiscover() {
    
        document.getElementById('loading-spinner').style.display = 'flex';

        fetch('http://127.0.0.1:5000/loadRecipes', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                allRecipeIDs
            })  // Sending back all the IDs of recipes fetched
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

            let recipeIDs = Object.values(data).map(recipe => recipe.recipeID);
            allRecipeIDs = allRecipeIDs.concat(recipeIDs);

            Object.values(data).forEach((recipe, index) => {
            recipesShown.push(recipe);  // Use currentRecipeCount + index + 1 for unique keys
            });

            filteredMeals = recipesShown; // Initialize filtered meals
        
            updateMealGrid();  // Update the grid with the fetched meals
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
            
    }

    function getMealCategory(meal) {
        if (meal.Breakfast) return 'Breakfast';
        if (meal.Lunch) return 'Lunch, Dinner';
        if (meal.Dinner) return 'Dinner';
        if (meal.Snack) return 'Snack';
        return 'Other';
    }

    function getMealImage(meal){
        return meal.image ? meal.image : 'https://t3.ftcdn.net/jpg/04/62/93/66/360_F_462936689_BpEEcxfgMuYPfTaIAOC1tCDurmsno7Sp.jpg';
    }

    function getMealCuisine(meal){
        return meal.cuisine ? meal.cuisine : 'Other';
    }

    function createMealCard(meal) {
        const card = document.createElement('div');
        card.className = 'meal-card';
        card.innerHTML = `
            <img src="${getMealImage(meal)}" alt="${meal.name}">
            <div class="meal-info">
                <h3>${meal.name}</h3>
                <p>Cuisine: ${getMealCuisine(meal)}</p>
                <p>Meal Category: ${getMealCategory(meal)}</p>
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
        if (filteredMeals.length==0){
            return;
        }
        else {
                filteredMeals.forEach(meal => {
                const card = createMealCard(meal);
                mealGrid.appendChild(card);
                console.log('appended');
            });
        }
        // Hide the loading spinner after fetch is complete
        document.getElementById('loading-spinner').style.display = 'none';
        loadMoreBtn.style.display = filteredMeals.length > 0 ? 'block' : 'none';
    }

    async function filterRecipes() {

        fetch('http://127.0.0.1:5000/filterRecipes', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipesShown, criterias
            })  // Sending back all recipe list
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data);  // For debugging purposes
            filteredMeals=data.filteredRecipeList;     
            console.log("woenwoeo")
            console.log(filteredMeals) 
            updateMealGrid();  // Update the grid with the filtered recipes
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
            
    }

    // Cost filter inputs event listeners
    const costFilterInputs = document.querySelectorAll('.cost input[type="number"]');
    costFilterInputs.forEach(input => {
        input.addEventListener('input', () => {
            criterias.cost[0]=(parseFloat(document.getElementById('costMin').value));
            criterias.cost[1]=(parseFloat(document.getElementById('costMax').value));
            filterRecipes();
        });
    });

        // Time filter inputs event listeners
    const timeFilterInputs = document.querySelectorAll('.time input[type="number"]');
    timeFilterInputs.forEach(input => {
        input.addEventListener('input', () => {
            criterias.time[0]=(parseInt(document.getElementById('timeMin').value));
            criterias.time[1]=(parseInt(document.getElementById('timeMax').value));
            filterRecipes();
        });
    });

    // Meal category buttons event listeners
    categoryBtns.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            const selectedCategories = Array.from(document.querySelectorAll('.category-btn.active'))
                .map(btn => btn.dataset.category);
            criterias.mealType = selectedCategories;
            filterRecipes();
        });
    });

    // Cuisine checkboxes event listeners
    document.querySelectorAll('input[name="cuisine"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const selectedCuisines = Array.from(document.querySelectorAll('input[name="cuisine"]:checked'))
                .map(input => input.value);
            criterias.cuisine = selectedCuisines;
            filterRecipes()
        });
    });

    // Clear filters function
    function clearFilters() {
        // Clear the active class from all category buttons
        categoryBtns.forEach(button => {
            button.classList.remove('active');
        });

        // Clear all checkboxes
        document.querySelectorAll('input[name="cuisine"]').forEach(checkbox => {
            checkbox.checked = false;
        });

        // Reset filter inputs
        document.getElementById('costMin').value = '0';
        document.getElementById('costMax').value = '100';
        document.getElementById('timeMin').value = '0';
        document.getElementById('timeMax').value = '120';

        // Reset filteredMeals to all recipes
        filteredMeals = recipesShown;
        updateMealGrid(); // Update the grid after clearing
    }

    // Load more button functionality
    loadMoreBtn.addEventListener('click', function() {
        clearFilters();
        loadDiscover();
    });

});
