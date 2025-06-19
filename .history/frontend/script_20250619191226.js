// frontend/script.js

// This function will be called to fetch data from our backend API.
const fetchMessage = () => {
    const messageElement = document.getElementById('message');
    messageElement.textContent = 'Fetching data...';

    // The fetch request goes to '/api/message'.
    // Nginx will see this path and proxy the request to our Python backend.
    fetch('/api/message')
        .then(response => {
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON from the response
        })
        .then(data => {
            // Update the HTML with the message from the backend.
            messageElement.textContent = data.message;
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch.
            console.error('Error fetching data:', error);
            messageElement.textContent = 'Failed to load message from backend.';
        });
};

// Add an event listener to run our fetch function when the page loads.
document.addEventListener('DOMContentLoaded', fetchMessage);

// Add an event listener to the button to fetch the message again.
document.getElementById('fetchButton').addEventListener('click', fetchMessage);
