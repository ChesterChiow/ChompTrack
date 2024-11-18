let recipeID;

document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    recipeID = urlParams.get('id');

    // Call the function to fetch and display data
    getRecipeData(recipeID)
});

function formatDateToYYYYMMDD(date) {
    const year = date.getFullYear(); // Get the full year (YYYY)
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Get month (0-11) and pad to 2 digits
    const day = String(date.getDate()).padStart(2, '0'); // Get day (1-31) and pad to 2 digits
    return `${year}-${month}-${day}`; // Construct the YYYY-MM-DD format
}

// Datepicker
$(document).ready(function() {
    // Initialize the datepicker
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd', // Choose your date format
        autoclose: true,
        todayHighlight: true
    });

    // Get the modal and elements
    const mealPlanModal = document.getElementById("mealPlanModal");
    const addToMealPlanBtn = document.getElementById("addToMealPlanBtn");
    const closeModalBtn = document.querySelector(".close");
    const confirmMealPlanBtn = document.getElementById("confirmMealPlanBtn");

    // Show the modal when "Add to Meal Plan" button is clicked
    addToMealPlanBtn.addEventListener("click", function () {
        mealPlanModal.style.display = "block";
    });

    // Hide the modal when the close button is clicked
    closeModalBtn.addEventListener("click", function () {
        mealPlanModal.style.display = "none";
    });

    // Hide the modal when clicking outside the modal content
    window.addEventListener("click", function (event) {
        if (event.target == mealPlanModal) {
            mealPlanModal.style.display = "none";
        }
    });

    // Confirm button to process the selected date
    confirmMealPlanBtn.addEventListener("click", function () {
        const selectedDate = new Date(document.getElementById('mealPlanDate').value);  // Get the datepicker value
        const selectedMealType = document.getElementById('mealType').value; // Get the meal type value

            addMealPlanToDataBase(selectedDate, selectedMealType);  // Pass both values

            // Hide the modal
            mealPlanModal.style.display = "none";
    });
});

async function getRecipeData(recipeID) {
    try {
        // Make sure to use the GET method since the route expects it
        const response = await fetch(`/getRecipe/${recipeID}`, {
            method: 'GET',  // Change to GET request
            headers: {
                'Content-Type': 'application/json'  // Optional for GET, but keeping for consistency
            }
        });

        // Check if the response was successful
        if (!response.ok) throw new Error(`Failed to fetch data: ${response.status}`);

        // Parse the response JSON
        const data = await response.json();
        console.log(data);  // For debugging

        // Populate HTML with the fetched data
        displayRecipeData(data);
    } catch (error) {
        console.error('Error fetching recipe data:', error);
    }
}


    async function addMealPlanToDataBase(selectedMealPlanDate, selectedMealType) {
        try {

            if (isNaN(selectedMealPlanDate.getTime())){
                alert("Please select a date.")
                return;
            }

            if(selectedMealType.length===0){
                alert("Please select a course.")
                return;
            }

            // Prepare the data to be sent
            const mealPlanData = {
                recipeID: recipeID,
                selectedMealPlanDate: formatDateToYYYYMMDD(selectedMealPlanDate),
                mealType: selectedMealType
            };

            // Send a POST request with the recipeID and date
            const response = await fetch('/addMealPlans', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(mealPlanData)
            });

            const data = await response.json();
            if (!response.ok) {
                // Handle error based on the status code or message
                alert(data.error || 'An unexpected error occurred.');
                return;
            }
    
            window.location.href = "/";
        } catch (error) {
            console.error('Error sending meal plan data:', error);
        }
    }


    function displayRecipeData(recipe) {

        // Basic recipe info
        document.getElementById('recipeName').innerText = recipe.title;
        document.getElementById('recipeCost').innerHTML = `<strong>Cost:</strong> $${(recipe.pricePerServing / 100).toFixed(2)}`;

        const cuisines = recipe.cuisine
        var cuisineStr = ""
        if (Array.isArray(cuisines) && cuisines.length > 0) {
            cuisines.forEach((cuisine, idx) => {
                cuisineStr += cuisine

                if (idx < cuisines.length - 1) {
                    cuisineStr += ", ";
                }
            });
        } else {
            cuisineStr = "Other";
        }
        document.getElementById('recipeCuisine').innerHTML = `<strong>Cuisine:</strong> ${cuisineStr}`;


        document.getElementById('prepTime').innerHTML = `<strong>Estimated Preparation time:</strong> ${recipe.readyInMinutes}min`;

        // Recipe image
        document.getElementById('recipeImage').src = recipe.image || 'https://t3.ftcdn.net/jpg/04/62/93/66/360_F_462936689_BpEEcxfgMuYPfTaIAOC1tCDurmsno7Sp.jpg';

        // Ingredients list
        const ingredientsList = document.getElementById('ingredientsList');
        ingredientsList.innerHTML = '';  // Clear existing content
        console.log("ingredient");
        recipe.extendedIngredients.forEach(ingredient => {
            const li = document.createElement('li');
            li.textContent = ingredient.original;    // Edit accordingly
            ingredientsList.appendChild(li);
        });

        // Nutrition information
        document.getElementById('calories').innerText = `${recipe.nutrition.nutrients[0].name}: ${Math.round(Number(recipe.nutrition.nutrients[0].amount))}${recipe.nutrition.nutrients[0].unit}`;
        document.getElementById('carbohydrates').innerText = `${recipe.nutrition.nutrients[3].name}: ${Math.round(Number(recipe.nutrition.nutrients[3].amount))}${recipe.nutrition.nutrients[3].unit}`;
        document.getElementById('protein').innerText = `${recipe.nutrition.nutrients[10].name}: ${Math.round(Number(recipe.nutrition.nutrients[10].amount))}${recipe.nutrition.nutrients[10].unit}`;
        document.getElementById('fats').innerText = `${recipe.nutrition.nutrients[1].name}: ${Math.round(Number(recipe.nutrition.nutrients[1].amount))}${recipe.nutrition.nutrients[1].unit}`;

        // Full recipe link
        const fullRecipeLink = document.getElementById('fullRecipeLink');

        if ("spoonacularSourceUrl" in recipe) {
            fullRecipeLink.href = recipe.spoonacularSourceUrl;
        } else if ("sourceUrl" in recipe) {
            fullRecipeLink.href = recipe.sourceUrl;
        } else {
            fullRecipeLink.href = "https://www.google.com/";
        }
        fullRecipeLink.href = recipe.sourceUrl;

        fullRecipeLink.innerHTML = '<strong>View recipe instructions</strong>';
    }
