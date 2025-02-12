function startStream() {1
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
                document.getElementById("audio-player").play();
            } else {
                document.getElementById("audio-player").pause();
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", checkStatus);