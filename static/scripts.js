let pc = new RTCPeerConnection();

async function startStream() {
    let offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    let response = await fetch("/offer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ offer: pc.localDescription })
    });

    let { answer } = await response.json();
    await pc.setRemoteDescription(answer);

    pc.ontrack = (event) => {
        let audio = document.getElementById("audio-player");
        audio.srcObject = event.streams[0];
        audio.play();
    };
}

document.addEventListener("DOMContentLoaded", startStream);