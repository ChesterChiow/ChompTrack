document.addEventListener('DOMContentLoaded', function() {
    let startDate = getMonday(new Date());
    let endDate = new Date(startDate);  // End date starts as the same as startDate
    endDate.setDate(endDate.getDate() + 6);
    let groceryLists ={};

    console.log('Start', formatDateToYYYYMMDD(startDate))

    async function getGroceryList() {
        console.log(formatDateToYYYYMMDD(startDate))
        console.log(formatDateToYYYYMMDD(endDate))
        fetch('http://127.0.0.1:5000/getGroceryList', {  // Your API URL here
            method: 'POST',  // Use POST to avoid showing parameters in URL
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // send back in YYYY-MM-DD format the first date of the week and last date of the week
                startDate : formatDateToYYYYMMDD(startDate),
                endDate: formatDateToYYYYMMDD(endDate)
            })  
            
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.status);
            }
            return response.json();  // Parse JSON data
        })
        .then(data => {
            console.log(data);  // For debugging purposes
            groceryLists = data;
            renderGroceryList();
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            groceryLists={};
            renderGroceryList();
        });
        
    }

    function getMonday(date) {
        const dayOfWeek = date.getDay(); // 0 (Sun) to 6 (Sat)
        const daysUntilMonday = (dayOfWeek === 0) ? -6 : 1 - dayOfWeek; // If Sunday (0), go back 6 days, else go back to last Monday
        date.setDate(date.getDate() + daysUntilMonday); // Set to the correct Monday
        return date;
    }

    function formatDateRange(date) {
        const start = new Date(date);
        const end = new Date(start);
        end.setDate(end.getDate() + 6);
        return `${start.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} - ${end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
    }

    function updateDateRange() {
        document.getElementById('dateRange').textContent = formatDateRange(startDate);
    }

    document.getElementById('previousWeek').addEventListener('click', () => {
        startDate.setDate(startDate.getDate()-7);
        endDate.setDate(endDate.getDate() - 7);
        updateDateRange();
        getGroceryList();
    });

    document.getElementById('nextWeek').addEventListener('click', () => {
        startDate.setDate(startDate.getDate()+7);
        endDate.setDate(endDate.getDate() + 7);
        updateDateRange();
        getGroceryList();
    });

    // Function to render grocery list and calculate total cost
    function renderGroceryList() {
        const tableBody = document.querySelector('#groceryTable tbody');
        tableBody.innerHTML = ''; // Clear existing items
        let totalCost = 0;

        let groceryItems = Object.values(groceryLists) || []; // Get items for the current week

        // If the grocery list is empty, do not display anything
        if (groceryItems.length === 0) {
            document.getElementById('totalCost').innerText = totalCost.toFixed(2);
            return;
        }

        groceryItems.forEach(item => {
            // Create table row
            const row = document.createElement('tr');
            if (item.amount == 0){
                row.innerHTML = `
                <td class="item-name">${item.name}</td>
                <td>${item.quantity}</td>
                <td class="item-price">$${item.price.toFixed(2)}</td>
            `;
            }
            else{
                row.innerHTML = `
                <td class="item-name">${item.name} (${item.amount}${item.measurement})</td>
                <td>${item.quantity}</td>
                <td class="item-price">$${item.price.toFixed(2)}</td>
            `;
            }

            // Add click event to toggle strike-through for the entire row
            row.addEventListener('click', function() {
                row.classList.toggle('strike-through');
                
                // Adjust total cost based on strike-through status
                if (row.classList.contains('strike-through')) {
                    totalCost -= item.price;
                } else {
                    totalCost += item.price;
                }

                // Update the total cost display
                document.getElementById('totalCost').innerText = totalCost.toFixed(2);
            });

            // Append the row to the table body
            tableBody.appendChild(row);

            // Calculate initial total cost
            totalCost += item.price;
        });

        // Display total cost
        document.getElementById('totalCost').innerText = totalCost.toFixed(2);
    }

    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear(); // Get the full year (YYYY)
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Get month (0-11) and pad to 2 digits
        const day = String(date.getDate()).padStart(2, '0'); // Get day (1-31) and pad to 2 digits
        return `${year}-${month}-${day}`; // Construct the YYYY-MM-DD format
    }

    // Call the function to render the grocery list
    getGroceryList();
    renderGroceryList();
    updateDateRange();

});