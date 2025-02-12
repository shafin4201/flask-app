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
            let audioPlayer = document.getElementById("audioPlayer");

            if (data.status === "running") {
                audioPlayer.load();
                audioPlayer.play();
            } else {
                audioPlayer.pause();
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", checkStatus);