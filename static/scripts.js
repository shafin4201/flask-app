document.addEventListener("DOMContentLoaded", checkStatus);

function startStream() {
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            checkStatus();
        })
        .catch(error => console.error('Error:', error));
}

function stopStream() {
    fetch('/stop')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            checkStatus();
        })
        .catch(error => console.error('Error:', error));
}

function checkStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = `Status: ${data.message}`;
            if (data.status === "running") {
                document.getElementById("audioPlayer").play();
            } else {
                document.getElementById("audioPlayer").pause();
            }
        })
        .catch(error => console.error('Error:', error));
}
