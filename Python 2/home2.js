

const music = document.getElementById('music');
const musicToggle = document.getElementById('musicToggle');
const statusDisplay = document.getElementById('status');

musicToggle.addEventListener('change', function() {
    if (this.checked) {
        music.play()
            .then(() => {
                statusDisplay.textContent = 'ON';
            })
            .catch(error => {

                console.error("Music playback failed:", error);

                this.checked = false;
                statusDisplay.textContent = 'OFF (Blocked)';
                alert("The browser blocked the music. Please click the main 'play' button first.");
            });

    } else {
        music.pause();
        music.currentTime = 0;
        statusDisplay.textContent = 'OFF';
    }
});