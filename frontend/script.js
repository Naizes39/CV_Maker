const fetchMessage = () => {
    const messageElement = document.getElementById('message');
    messageElement.textContent = 'Fetching data...';

    fetch('/api/message')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            messageElement.textContent = data.message;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            messageElement.textContent = 'Failed to load message from backend.';
        });
};

document.addEventListener('DOMContentLoaded', fetchMessage);

document.getElementById('fetchButton').addEventListener('click', fetchMessage);
