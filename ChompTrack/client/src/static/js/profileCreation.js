$('.ui.dropdown').dropdown();

        function validateProfileForm(event) {
            event.preventDefault(); // Prevent the default form submission

            const name = document.getElementById('name').value.trim();
            const age = parseInt(document.getElementById('age').value);
            const height = parseInt(document.getElementById('height').value);
            const weight = parseInt(document.getElementById('weight').value);
            const gender = document.getElementById('gender').value;
            const activityLevel = document.getElementById('activity-level').value;

            // Get multiple selected values from diet-type and allergy
            var dietType = Array.from(document.getElementById('diet-type').selectedOptions).map(option => option.value);
            var allergy = Array.from(document.getElementById('allergy').selectedOptions).map(option => option.value);

            if (name === "" || !name || !age || !gender || !height || !weight || !activityLevel) {
                alert('Please fill in the blank fields.');
                return; // Prevent further execution
            }

            if (dietType.length == 0) {
                dietType = ['Anything']
            }

            if (allergy.length == 0) {
                allergy = ['None']
            }

            const userID = sessionStorage.getItem('userID');
            console.log(userID)

            // Prepare data for submission
            const profileData = {
                userID: userID,
                name: name,
                age: age,
                gender: gender,
                height: height,
                weight: weight,
                activityLevel: activityLevel,
                dietType: dietType,
                allergy: allergy
            };

            // Send data to the server
            updateProfile(profileData);
        }

        function updateProfile(data) {
            fetch('http://127.0.0.1:5000/updateProfile', { // Replace with your actual API endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle successful profile update (e.g., redirect to the next page)
                alert('Profile updated successfully!');
                window.location.href = 'suggested-intake'; // Redirect to the next page
            })
            .catch(error => {
                // Handle error (e.g., show error message)
                alert('Profile update failed: ' + error.message);
            });
        }