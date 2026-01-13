
const downloadButton = document.getElementById("download_tokens");

downloadButton.addEventListener('click', function () {
    console.log("button was clicked")
    fetch('/download-token-list/')
        .then(response => response.json())
        .then(data => {
            console.log('Data received:', data);
            alert(`Message: ${data.message}, Status: ${data.status}`);
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('Something went wrong while fetching the data.');
        });
});
 

    