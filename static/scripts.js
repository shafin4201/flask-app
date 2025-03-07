let audioPlayer = document.getElementById("audio-player");
let audioStream = null;

// লাইভ অডিও স্ট্রিম শুরু করা
function startStream() {
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            checkStatus();

            // WebSocket কানেকশন তৈরি করা
            if (!audioStream) {
                audioStream = new WebSocket("wss://" + window.location.host + "/audio");

                audioStream.onmessage = function(event) {
                    let audioBlob = new Blob([event.data], { type: "audio/wav" });
                    let objectURL = URL.createObjectURL(audioBlob);
                    audioPlayer.src = objectURL;
                    audioPlayer.play();
                };

                audioStream.onerror = function(error) {
                    console.error("WebSocket Error:", error);
                };
            }
        })
        .catch(error => console.error('Error:', error));
}

// স্ট্রিম বন্ধ করা
function stopStream() {
    fetch('/stop')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            checkStatus();

            // WebSocket কানেকশন বন্ধ করা
            if (audioStream) {
                audioStream.close();
                audioStream = null;
            }

            audioPlayer.pause();
            audioPlayer.src = "";
        })
        .catch(error => console.error('Error:', error));
}

// সার্ভারের স্ট্যাটাস চেক করা
function checkStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = `Status: ${data.message}`;
            if (data.status === "running" && !audioStream) {
                startStream();
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", checkStatus);